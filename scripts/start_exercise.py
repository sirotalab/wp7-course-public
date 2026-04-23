#!/usr/bin/env python3
"""Create your working copy of an exercise from its starter file.

Usage::

    pixi run start ex1
    pixi run start ex5
    python scripts/start_exercise.py ex5 --force

Copies ``starter.ipynb`` (or ``starter.py`` for ex3) to ``exN.ipynb``
(or ``ex3.py``) inside the exercise directory. Refuses to overwrite an
existing target unless ``--force`` is passed.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else s


def g(s: str) -> str: return _c("32", s)
def r(s: str) -> str: return _c("31", s)


def resolve_exercise_dir(ex: str, exercises_root: Path) -> Path:
    matches = sorted(
        p for p in exercises_root.iterdir()
        if p.is_dir() and p.name.startswith(ex + "-")
    )
    if len(matches) == 1:
        return matches[0]
    available = ", ".join(
        p.name for p in sorted(exercises_root.iterdir()) if p.is_dir()
    )
    print(r(f"error: no exercise directory matches {ex!r}"), file=sys.stderr)
    print(f"available: {available}", file=sys.stderr)
    sys.exit(2)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("exercise", help="Exercise id, e.g. 'ex1' or 'ex10'.")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite an existing working copy.")
    args = ap.parse_args(argv)

    if not re.fullmatch(r"ex\d{1,2}", args.exercise):
        print(r(f"error: expected 'exN' (e.g. ex1, ex10), got {args.exercise!r}"),
              file=sys.stderr)
        return 2

    public_root = Path(__file__).resolve().parents[1]
    ex_dir = resolve_exercise_dir(args.exercise, public_root / "exercises")

    if args.exercise == "ex3":
        starter, target = ex_dir / "starter.py", ex_dir / "ex3.py"
    else:
        starter = ex_dir / "starter.ipynb"
        target = ex_dir / f"{args.exercise}.ipynb"

    if not starter.exists():
        print(r(f"error: starter file missing: {starter}"), file=sys.stderr)
        return 1

    if target.exists() and not args.force:
        print(r(f"error: {target} already exists. Pass --force to overwrite."),
              file=sys.stderr)
        return 1

    shutil.copy2(starter, target)
    print(g(str(target.resolve())))
    print(f"open in VS Code: code {target.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
