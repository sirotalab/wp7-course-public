# Quick start

Welcome to WP7! This is the 5-minute path from "I just got enrolled" to "I'm running the first exercise on the HPC." If anything here breaks, drop a line in the course chat or check the longer [Setup](setup/ssh.md) pages.

## Step 1 — Find your pooled login

The cohort shares **10 accounts** on the HPC: `ephys01` through `ephys10`. You don't get a personal account — multiple students share each login, and you'll work in a subfolder named after yourself under the shared home.

Which one is yours? It's decided **alphabetically**, so everyone can look it up the same way.

### 👉 Easiest: the interactive lookup tool

Open the **[Interactive SSH setup page](tools/ssh-setup.html)** — paste the cohort roster, type your name, and it spits out your `ephysNN` account plus a ready-to-paste SSH config snippet tailored to your OS (macOS / Linux / Windows tabs).

### The fair-share rule (so you know what the tool is doing)

1. Sort the cohort by full name (case-insensitive).
2. Divide the list of N students as evenly as possible across the 10 accounts. If N doesn't divide by 10, the first few accounts get one extra student.
3. Read off your slot.

That's it — same rule for any cohort size, whether you're 7 students or 23.

### Prefer Python?

If you'd rather not trust the JavaScript, here's the same algorithm you can run in a notebook cell:

```python
def assign_accounts(students: list[str], n_accounts: int = 10) -> dict[str, str]:
    """Fair-share alphabetical assignment of students to ephys01..ephysNN."""
    roster = sorted(students, key=str.casefold)
    n = len(roster)
    base, extra = divmod(n, n_accounts)          # base per account, +1 for the first `extra`
    out, idx = {}, 0
    for acct in range(1, n_accounts + 1):
        size = base + (1 if acct <= extra else 0)
        for _ in range(size):
            if idx < n:
                out[roster[idx]] = f"ephys{acct:02d}"
                idx += 1
    return out


cohort = [
    "Alice Abel",
    "Bob Brahe",
    "Carmen Curie",
    # ... paste the full roster here
]
print(assign_accounts(cohort))
```

The result is a `{student_name: "ephysNN"}` dict. Find your name, note the account, move on.

!!! note "Cohort-of-15 example"
    With 15 students, `divmod(15, 10) = (1, 5)`, so accounts **01–05 get 2 students each** and **06–10 get 1 student each**. With 10 students it's one-to-one. With 23 students, `divmod(23, 10) = (2, 3)`, so accounts 01–03 get 3 students and 04–10 get 2 students.

Arash will also post the final frozen mapping in the course chat once the roster is confirmed — that's the authoritative version if it disagrees with your local run (e.g. late enrolments).

## Step 2 — Generate an SSH key and log in

On your laptop (Linux, macOS, or Windows with Git Bash / PowerShell):

```bash
ssh-keygen -t ed25519 -C "your.email@campus.lmu.de"
```

Accept the default path. A passphrase is optional but recommended.

Then create (or edit) `~/.ssh/config` and paste this — **replacing `ephysXX` with the account from Step 1**:

```sshconfig
Host gamma3
  HostName 10.153.170.43
  User ephysXX
  Port 22

Host theta
  HostName 10.153.170.1
  User ephysXX
  Port 22

Host beta
  HostName 10.153.170.3
  User ephysXX
  Port 22
```

- **`gamma3`** — our dedicated compute node for the course. This is where you'll run notebooks.
- **`theta`** — the head node. Fine for `cd` / `ls` / light editing, but no heavy computation.
- **`beta`** — the git/datalad bastion. You only need it if you're cloning the course materials from off-HPC.

First login uses the password you were given at the start of the course:

```bash
ssh gamma3
```

Then from the remote shell, immediately upload your public key so you don't have to retype the password every time:

```bash
# logout first
exit

# back on your laptop
ssh-copy-id gamma3

# test it
ssh gamma3   # should log in without asking for a password
```

Having trouble? The long version is on the [SSH setup page](setup/ssh.md), including off-campus (VPN) instructions.

## Step 3 — Open VS Code Remote (recommended)

The easiest way to actually *work* on the HPC is VS Code with the Remote-SSH extension, which gives you a normal editor + terminal + notebook interface on your laptop while the code runs on gamma3. Full walkthrough: [VS Code Remote-SSH](setup/vscode.md).

TL;DR: install the `Remote - SSH` extension, press `F1`, type "Connect to Host", pick `gamma3`. If your `~/.ssh/config` is set up, it just works.

## Step 4 — Pick up the course materials

Once you're on `gamma3`:

```bash
cd /storage2/wp7/course-materials
ls
```

This is the read-only drop of the course (lectures, exercise prompts, starter notebooks, helper modules). The canonical version lives in the `wp7-course-public` repo — if you prefer to clone and work off-HPC, see [HPC workspace](setup/workspace.md).

Activate the course conda environment:

```bash
conda activate wp7
```

All the packages you need for Ex1–5 are already installed. If anything is missing, flag it in the course chat — don't `pip install` into `wp7` yourself, it's shared.

## Step 5 — Do Exercise 1

```bash
cd /storage2/wp7/course-materials/exercises/ex1-bootstrap
```

Open the starter notebook, read `README.md`, and have fun. The [Exercises overview](exercises/index.md) has links to all five.

## Step 6 — Submit

Submissions are a filename convention, nothing fancy. See [Submissions](submissions.md).

---

## One-page cheat sheet

| Need | Where |
|---|---|
| SSH details, off-campus access | [Setup → SSH](setup/ssh.md) |
| VS Code Remote-SSH walkthrough | [Setup → VS Code Remote](setup/vscode.md) |
| Conda environment | [Setup → Conda](setup/conda.md) |
| Your per-student workspace on HPC | [Setup → HPC workspace](setup/workspace.md) |
| Course schedule | [Schedule](schedule.md) |
| Exercise prompts and starter notebooks | [Exercises](exercises/index.md) |
| How to submit | [Submissions](submissions.md) |

Welcome aboard! 🧠
