#!/usr/bin/env python3
"""Open VS Code Remote-SSH to your HPC workspace.

Runs on the laptop; wraps ``code --remote ssh-remote+<host> /storage2/wp7/<slug>``.
Reads your identity from ``~/.wp7/config.toml`` (created by ``pixi run setup-ssh``).

Refuses to run on the HPC itself (no point).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from _wp7_config import load


def refuse_on_hpc() -> None:
    if Path("/storage2/wp7").is_dir():
        print("error: you're on the HPC — no need to 'open VS Code remote'.", file=sys.stderr)
        print("just open the folder locally: `code ~/<slug>`", file=sys.stderr)
        sys.exit(1)


def find_code_binary() -> str:
    """Return the name of the VS Code launcher on the current OS."""
    for candidate in ("code", "code.cmd", "code-insiders", "code-insiders.cmd"):
        if shutil.which(candidate):
            return candidate
    print(
        "error: VS Code isn't on your PATH.\n"
        "  install from https://code.visualstudio.com/ and make sure 'code' is on PATH:\n"
        "    - Mac: run 'Shell Command: Install \"code\" command in PATH' from the Command Palette\n"
        "    - Windows/Linux: the installer usually adds it automatically\n",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> int:
    refuse_on_hpc()
    cfg = load()
    code = find_code_binary()

    cmd = [code, "--remote", f"ssh-remote+{cfg.host}", cfg.hpc_path]
    print(f"launching: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
