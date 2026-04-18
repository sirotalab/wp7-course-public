#!/usr/bin/env python3
"""Bootstrap SSH access to the lab HPC. Run once on your laptop.

What this does:

1. Prompts for your ephys account, slug, and email (saves to ``~/.wp7/config.toml``).
2. Generates an ed25519 SSH key if you don't already have one.
3. Adds the course hosts (gamma3, theta, beta) to ``~/.ssh/config`` if missing.
4. Copies your public key to gamma3 (may prompt for your HPC password).
5. Verifies passwordless login works.

Refuses to run on the HPC itself (no point — you're already there).

Platform coverage: Mac, Linux, Windows (PowerShell or Git Bash). Uses only
the stdlib + the ``ssh`` / ``ssh-keygen`` binaries that ship with every modern
OS. No ``ssh-copy-id`` dependency (Windows OpenSSH lacks it).
"""
from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

from _wp7_config import CONFIG_PATH, DEFAULT_HOST, WP7Config, load, save, summary

SSH_DIR = Path.home() / ".ssh"
SSH_CONFIG = SSH_DIR / "config"
KEY_PATH = SSH_DIR / "id_ed25519"

COURSE_HOSTS = [
    # (alias, hostname, comment)
    ("gamma3", "10.153.170.43", "course compute node — run notebooks here"),
    ("theta",  "10.153.170.1",  "head node — light editing only"),
    ("beta",   "10.153.170.3",  "git/datalad bastion"),
]

# ANSI colours (only when stdout is a TTY)
def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else s
def g(s): return _c("32", s)
def r(s): return _c("31", s)
def y(s): return _c("33", s)
def b(s): return _c("1;34", s)


# ---------------------------------------------------------------------------
# Refuse to run on HPC
# ---------------------------------------------------------------------------

def refuse_on_hpc() -> None:
    if Path("/storage2/arash/teaching/wp7").is_dir():
        print(r("error: you're already on the HPC."))
        print("setup-ssh is a laptop-side command. Your HPC account is already set up.")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Gather identity
# ---------------------------------------------------------------------------

_slug_re = re.compile(r"^[a-z0-9]+-[a-z0-9]+$")
_acct_re = re.compile(r"^ephys\d{2}$")


def prompt_identity() -> WP7Config:
    existing = load(required=False)
    if existing:
        print(b("existing config:"))
        print(summary(existing))
        choice = input("keep it? [Y/n] ").strip().lower()
        if choice in ("", "y", "yes"):
            return existing
        print()

    print(b("enter your course identity (from your TA's email):"))
    while True:
        slug = input("slug (firstname-lastname, lowercase): ").strip().lower()
        if _slug_re.match(slug):
            break
        print(r("  slug must look like 'alice-abel' (two words, hyphen, lowercase)"))
    while True:
        account = input("ephys account (e.g. ephys03): ").strip().lower()
        if _acct_re.match(account):
            break
        print(r("  account must look like 'ephysNN' where NN is two digits"))
    email = input("campus email (e.g. your.email@campus.lmu.de): ").strip()
    host = input(f"HPC host [{DEFAULT_HOST}]: ").strip() or DEFAULT_HOST

    cfg = WP7Config(slug=slug, account=account, email=email, host=host)
    save(cfg)
    print(g(f"✓ saved {CONFIG_PATH}"))
    print(summary(cfg))
    return cfg


# ---------------------------------------------------------------------------
# SSH key generation
# ---------------------------------------------------------------------------

def ensure_ssh_key(email: str) -> Path:
    if KEY_PATH.exists():
        print(g(f"✓ SSH key already exists at {KEY_PATH}"))
        return KEY_PATH

    SSH_DIR.mkdir(parents=True, exist_ok=True)
    try:
        SSH_DIR.chmod(0o700)
    except OSError:
        pass  # Windows: chmod semantics differ; ssh doesn't enforce on Windows

    print(b(f"generating ed25519 SSH key at {KEY_PATH}..."))
    print("(press Enter for no passphrase, or type one for extra protection)")
    cmd = ["ssh-keygen", "-t", "ed25519", "-C", email, "-f", str(KEY_PATH)]
    subprocess.run(cmd, check=True)
    print(g(f"✓ key generated"))
    return KEY_PATH


# ---------------------------------------------------------------------------
# ~/.ssh/config management
# ---------------------------------------------------------------------------

BLOCK_MARKER_START = "# --- wp7-course SSH hosts (managed) ---"
BLOCK_MARKER_END   = "# --- /wp7-course SSH hosts ---"


def managed_block(account: str) -> str:
    lines = [BLOCK_MARKER_START]
    for alias, hostname, comment in COURSE_HOSTS:
        lines.extend([
            f"# {comment}",
            f"Host {alias}",
            f"  HostName {hostname}",
            f"  User {account}",
            f"  Port 22",
            "",
        ])
    lines.append(BLOCK_MARKER_END)
    return "\n".join(lines)


def update_ssh_config(account: str) -> None:
    SSH_DIR.mkdir(parents=True, exist_ok=True)
    current = SSH_CONFIG.read_text() if SSH_CONFIG.exists() else ""
    block = managed_block(account)

    # Re-entrant: replace existing managed block, or append
    if BLOCK_MARKER_START in current and BLOCK_MARKER_END in current:
        new = re.sub(
            rf"{re.escape(BLOCK_MARKER_START)}.*?{re.escape(BLOCK_MARKER_END)}",
            block,
            current,
            count=1,
            flags=re.DOTALL,
        )
        action = "updated"
    else:
        sep = "" if not current or current.endswith("\n\n") else ("\n\n" if current.endswith("\n") else "\n\n")
        new = current + sep + block + "\n"
        action = "added"

    # Back up before write
    if SSH_CONFIG.exists():
        backup = SSH_CONFIG.with_suffix(".wp7-backup")
        if not backup.exists():  # only keep the first backup
            shutil.copy2(SSH_CONFIG, backup)
    SSH_CONFIG.write_text(new)
    try:
        SSH_CONFIG.chmod(0o600)
    except OSError:
        pass
    print(g(f"✓ {action} ~/.ssh/config (block with gamma3 / theta / beta)"))


# ---------------------------------------------------------------------------
# Public key transfer — cross-platform
# ---------------------------------------------------------------------------

def copy_public_key(host: str) -> None:
    pubkey_path = KEY_PATH.with_suffix(".pub")
    if not pubkey_path.exists():
        print(r(f"error: {pubkey_path} missing — key generation failed"))
        sys.exit(1)

    pubkey = pubkey_path.read_text().strip()

    print(b(f"\ninstalling public key on {host}..."))
    print(y(f"(you'll be prompted for your HPC password — the one you set on first login)"))

    # Single command works on all platforms: pipe pubkey over SSH and append
    # to authorized_keys, creating .ssh with correct perms if absent.
    remote_cmd = (
        "mkdir -p ~/.ssh && chmod 700 ~/.ssh && "
        "cat >> ~/.ssh/authorized_keys && "
        "chmod 600 ~/.ssh/authorized_keys"
    )
    result = subprocess.run(
        ["ssh", host, remote_cmd],
        input=pubkey + "\n",
        text=True,
    )
    if result.returncode != 0:
        print(r(f"\nerror: public key install failed (exit {result.returncode})"))
        print("manual fallback — on the HPC, run:")
        print(f"  echo '{pubkey}' >> ~/.ssh/authorized_keys")
        print(f"  chmod 600 ~/.ssh/authorized_keys")
        sys.exit(result.returncode)
    print(g("✓ public key installed"))


# ---------------------------------------------------------------------------
# Verify passwordless
# ---------------------------------------------------------------------------

def verify_login(host: str) -> None:
    print(b(f"\nverifying passwordless login to {host}..."))
    result = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host, "echo ok"],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and "ok" in result.stdout:
        print(g(f"✓ ssh {host} works without a password"))
    else:
        print(y(f"! passwordless login not working yet"))
        print(f"  stderr: {result.stderr.strip()}")
        print(f"  try manually: ssh {host}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    refuse_on_hpc()
    print(b("WP7 course — SSH setup\n"))

    cfg = prompt_identity()
    print()
    ensure_ssh_key(cfg.email)
    print()
    update_ssh_config(cfg.account)
    copy_public_key(cfg.host)
    verify_login(cfg.host)

    print()
    print(g("done. Next step:"))
    print(f"  {b('pixi run code')}    # open VS Code Remote to your HPC workspace")
    return 0


if __name__ == "__main__":
    sys.exit(main())
