#!/usr/bin/env python3
"""Validate and register a WP7 exercise submission.

Usage::

    pixi run submit ex1
    pixi run submit ex5-dimred-1
    pixi run submit 7

What it does:

1. Resolves the exercise (directory under ``exercises/``).
2. Looks for ``exN_<your-slug>.ipynb`` — or ``.py`` for Ex3 — in that directory.
3. Validates the notebook:
   * No ``raise NotImplementedError`` left.
   * At least one code cell has output (was it executed?).
   * Executes the notebook end-to-end (default; pass ``--skip-run`` for the
     fast static-only check).
4. Records the submission in a sidecar file ``exN_<slug>.submission.json``
   next to the notebook. The TA's grading script picks these up.
5. Emails a confirmation to the address in ``~/.wp7/config.toml``. Opt out
   with ``--no-email`` or ``WP7_NO_EMAIL=1``.

Prints a clear PASS/FAIL at the end.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from _wp7_config import load

# Base URL where submission HTML is published. Keep in sync with
# mkdocs.yml ``site_url``.
SITE_URL = "https://sirotalab.pages.gitlab.lrz.de/wp7-course"

# ANSI colours
def _c(code, s): return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else s
def g(s): return _c("32", s)
def r(s): return _c("31", s)
def y(s): return _c("33", s)
def b(s): return _c("1;34", s)


def repo_root() -> Path:
    """Find the course-materials root (where pixi.toml + exercises/ live)."""
    here = Path(__file__).resolve().parent
    for d in [here, *here.parents]:
        if (d / "exercises").is_dir() and (d / "pixi.toml").is_file():
            return d
    print(r("error: can't find course-materials root (no pixi.toml + exercises/ anywhere above this script)"))
    sys.exit(2)


def resolve_exercise(arg: str, root: Path) -> Path:
    """Accept 'ex1', '1', 'ex5-dimred-1' → return the exercise directory."""
    exs = root / "exercises"
    if (exs / arg).is_dir():
        return exs / arg
    matches = sorted(p for p in exs.iterdir()
                     if p.is_dir() and p.name.startswith(arg + "-"))
    if len(matches) == 1:
        return matches[0]
    if arg.isdigit():
        return resolve_exercise(f"ex{arg}", root)
    print(r(f"error: unknown exercise {arg!r}"))
    print(f"available: {', '.join(p.name for p in sorted(exs.iterdir()) if p.is_dir())}")
    sys.exit(2)


def find_notebook(ex_dir: Path, slug: str) -> Path:
    """Find exN_<slug>.ipynb (or .py) in the exercise dir."""
    ex_num = re.match(r"ex(\d+)", ex_dir.name)
    if not ex_num:
        print(r(f"error: can't parse exercise number from {ex_dir.name}"))
        sys.exit(2)
    n = ex_num.group(1)

    for ext in (".ipynb", ".py"):
        candidate = ex_dir / f"ex{n}_{slug}{ext}"
        if candidate.exists():
            return candidate

    print(r(f"error: no submission found for slug {slug!r} in {ex_dir.name}"))
    print(f"expected: {ex_dir}/ex{n}_{slug}.ipynb  (or .py for ex3)")
    print()
    print("to create it:")
    print(f"  open {ex_dir}/starter.ipynb in VS Code")
    print(f"  File → Save As → ex{n}_{slug}.ipynb")
    sys.exit(2)


def exercise_short(ex_dir_name: str) -> str:
    """``ex1-bootstrap`` -> ``ex1``."""
    return ex_dir_name.split("-", maxsplit=1)[0] if "-" in ex_dir_name else ex_dir_name


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------

def check_not_implemented(nb_path: Path) -> tuple[bool, str]:
    src = _notebook_source(nb_path)
    if "raise NotImplementedError" in src:
        return False, "still has `raise NotImplementedError` — finish the TODO cells first"
    return True, "no unfinished TODO markers"


def check_has_outputs(nb_path: Path) -> tuple[bool, str]:
    if nb_path.suffix != ".ipynb":
        return True, "script (no outputs expected)"
    try:
        nb = json.loads(nb_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return False, f"can't parse notebook: {e}"
    code_cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    with_outputs = [c for c in code_cells if c.get("outputs")]
    if not with_outputs:
        return False, "no cell outputs — did you execute Run All?"
    return True, f"{len(with_outputs)}/{len(code_cells)} code cells have output"


def check_runs(nb_path: Path) -> tuple[bool, str, str | None]:
    """Execute the notebook end-to-end via nbconvert.

    Returns ``(ok, detail, failure_category)``. ``failure_category`` is
    ``None`` on success, otherwise one of:
    ``import-error``, ``assertion``, ``timeout``, ``runtime``.
    """
    if nb_path.suffix != ".ipynb":
        return True, "skipped (script)", None
    print(b("  executing notebook end-to-end (up to 5 min)..."))
    # Workaround for `pixi run` (0.67) stripping LD_LIBRARY_PATH from the
    # child env and not firing activation scripts. Jupyter's kernel
    # subprocess then resolves libstdc++ to the system copy, which on
    # older Debian/Ubuntu hosts lacks CXXABI_1.3.15 (needed by conda-forge
    # libicui18n). We re-establish LD_LIBRARY_PATH via a bash -c wrapper
    # because setting it on the Python subprocess env= alone isn't enough —
    # jupyter_client spawns the kernel and mangles the env.
    conda_prefix = os.environ.get("CONDA_PREFIX", "")
    nb_shell = shlex.quote(str(nb_path))
    bash_cmd = (
        f'export LD_LIBRARY_PATH="{conda_prefix}/lib${{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}}" && '
        f'exec jupyter nbconvert --to notebook --execute '
        f'--ExecutePreprocessor.timeout=300 '
        f'--output /tmp/wp7-submit-check.ipynb {nb_shell}'
    )
    try:
        subprocess.run(
            ["bash", "-c", bash_cmd],
            check=True, capture_output=True, text=True,
            timeout=360,
        )
    except subprocess.TimeoutExpired:
        return False, "execution timed out (>6 min wall-clock)", "timeout"
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or "").strip().splitlines()
        last = stderr[-1] if stderr else "(no stderr)"
        return False, f"execution failed: {last}", _categorise(stderr)
    except FileNotFoundError:
        return False, "jupyter not available in the current env", "runtime"
    return True, "runs end-to-end", None


def _categorise(stderr_lines: list[str]) -> str:
    """Best-effort classification of a failure from nbconvert stderr."""
    blob = "\n".join(stderr_lines)
    if "ModuleNotFoundError" in blob or "ImportError" in blob:
        return "import-error"
    if "AssertionError" in blob:
        return "assertion"
    if "TimeoutError" in blob or "CellTimeoutError" in blob:
        return "timeout"
    return "runtime"


def _notebook_source(path: Path) -> str:
    if path.suffix != ".ipynb":
        return path.read_text()
    try:
        nb = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return ""
    return "\n".join("".join(c.get("source", [])) for c in nb.get("cells", []))


# ---------------------------------------------------------------------------
# Email confirmation
# ---------------------------------------------------------------------------

def send_confirmation_email(nb_path: Path, cfg, submitted_at: str) -> None:
    """Send a confirmation via /usr/bin/mail. Best-effort — warns on failure.

    No-ops on:
    - ``WP7_NO_EMAIL=1`` env var (caller should also honour ``--no-email``)
    - empty email in config
    - missing ``mail`` binary
    """
    if os.environ.get("WP7_NO_EMAIL"):
        print(y("  (email suppressed by WP7_NO_EMAIL)"))
        return
    if not cfg.email:
        print(y("  (no email in ~/.wp7/config.toml — skipping confirmation)"))
        return
    mail_bin = shutil.which("mail") or shutil.which("mailx")
    if mail_bin is None:
        print(y("  (mail binary not on PATH — skipping confirmation)"))
        return

    ex_short = exercise_short(nb_path.parent.name)
    html_url = f"{SITE_URL}/submissions/{ex_short}/{cfg.slug}.html"
    subject = f"WP7 submission received — {ex_short}"
    body = (
        f"Your submission for {nb_path.parent.name} was recorded at {submitted_at}.\n"
        f"\n"
        f"Slug:     {cfg.slug}\n"
        f"Notebook: {nb_path.name}\n"
        f"Status:   PASSED all checks\n"
        f"\n"
        f"View the rendered HTML once published:\n"
        f"{html_url}\n"
    )
    try:
        subprocess.run(
            [mail_bin, "-s", subject, cfg.email],
            input=body,
            check=True,
            text=True,
            capture_output=True,
            timeout=30,
        )
        print(g(f"  ✓ confirmation email sent to {cfg.email}"))
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        # Email failure does not fail the submission.
        detail = getattr(exc, "stderr", None) or str(exc)
        print(y(f"  (email failed: {detail.strip().splitlines()[-1] if detail else exc}) — submission still recorded"))


# ---------------------------------------------------------------------------
# Submission record
# ---------------------------------------------------------------------------

def record_submission(
    nb_path: Path,
    cfg,
    checks: list[tuple[str, bool, str]],
    runs_ok: bool | None,
    failure_category: str | None,
    submitted_at: str,
) -> Path:
    """Write ``exN_<slug>.submission.json`` next to the notebook."""
    record_path = nb_path.with_suffix(".submission.json")
    record = {
        "slug": cfg.slug,
        "account": cfg.account,
        "email": cfg.email,
        "exercise": nb_path.parent.name,
        "notebook": nb_path.name,
        "size_bytes": nb_path.stat().st_size,
        "sha256": hashlib.sha256(nb_path.read_bytes()).hexdigest()[:16],
        "submitted_at": submitted_at,
        "runs_ok": runs_ok,
        "failure_category": failure_category,
        "checks": [{"name": n, "pass": p, "detail": d} for n, p, d in checks],
    }
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    return record_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("exercise", help="e.g. 'ex1', '1', 'ex5-dimred-1'")
    parser.add_argument("--skip-run", action="store_true",
                        help="Skip end-to-end notebook execution (static checks only)")
    parser.add_argument("--full-run", action="store_true",
                        help="(deprecated; execution is on by default)")
    parser.add_argument("--no-email", action="store_true",
                        help="Skip the confirmation email")
    args = parser.parse_args(argv)

    cfg = load()
    root = repo_root()
    ex_dir = resolve_exercise(args.exercise, root)
    nb_path = find_notebook(ex_dir, cfg.slug)

    print(b(f"submitting {nb_path.name} as {cfg.slug}"))
    print()

    checks: list[tuple[str, bool, str]] = []
    for name, fn in [
        ("no-NotImplementedError", check_not_implemented),
        ("has outputs",            check_has_outputs),
    ]:
        ok, detail = fn(nb_path)
        checks.append((name, ok, detail))
        icon = g("✓") if ok else r("✗")
        print(f"  {icon} {name}: {detail}")

    runs_ok: bool | None = None
    failure_category: str | None = None
    if not args.skip_run:
        ok, detail, cat = check_runs(nb_path)
        checks.append(("runs end-to-end", ok, detail))
        runs_ok = ok
        failure_category = cat
        icon = g("✓") if ok else r("✗")
        print(f"  {icon} runs end-to-end: {detail}")

    failed = [n for n, ok, _ in checks if not ok]
    print()
    if failed:
        print(r(f"✗ {len(failed)} check(s) failed: {', '.join(failed)}"))
        print("  fix them and re-run `pixi run submit`")
        return 1

    submitted_at = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    record_path = record_submission(nb_path, cfg, checks, runs_ok, failure_category, submitted_at)
    print(g(f"✓ submission recorded"))
    print(f"  notebook: {nb_path}")
    print(f"  record:   {record_path}")

    if not args.no_email:
        send_confirmation_email(nb_path, cfg, submitted_at)

    return 0


if __name__ == "__main__":
    sys.exit(main())
