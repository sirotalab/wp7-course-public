# Sync course data to your laptop

You don't *have* to do this — working directly on the HPC via [VS Code Remote-SSH](vscode.md) is the main path. But if you want an offline copy for travel, train rides, or a local history of the course, everything is published as [DataLad](https://www.datalad.org/) datasets you can clone over SSH.

There are two independent data flows:

| Flow | What | Direction |
|------|------|-----------|
| **Course materials** | Lectures, exercise starters, helper modules | TA → you (read-only) |
| **Your work** | Your notebooks, outputs, reports | HPC ↔ laptop (bidirectional) |

Both use **datalad** on your laptop. The setup below covers installing the toolchain and cloning both flows.

---

## Prerequisites

1. SSH to the lab gateway is working passwordless (finish [SSH setup](ssh.md) first — verify with `ssh beta exit`).
2. Install **datalad** and **git-annex** on your laptop:

    === "pixi (recommended, cross-platform)"

        [pixi](https://pixi.sh) is a single-binary package manager that installs datalad + git-annex from conda-forge with no existing Python or conda needed.

        ```bash
        # Install pixi (one-time):
        curl -fsSL https://pixi.sh/install.sh | bash

        # Install datalad (pulls git-annex automatically):
        pixi global install datalad
        ```

    === "conda / mamba"

        ```bash
        conda install -c conda-forge datalad
        ```

    === "macOS (Homebrew)"

        ```bash
        brew install datalad git-annex
        ```

    === "Linux (pipx + distro git-annex)"

        ```bash
        sudo apt install git-annex    # or dnf/pacman equivalent
        pipx install datalad
        ```

    === "Windows"

        Use WSL2 and follow the Linux or pixi instructions. Native Windows works but is finicky — we don't support it.

    Verify with `datalad --version` and `git annex version`.

---

## Flow 1 — Course materials (read-only)

This gives you a clone of the course materials: lectures, exercise starters, notebooks, and helper modules. You can pull updates but you cannot push back — it's a one-way mirror.

### 1. Clone

```bash
datalad clone ria+ssh://beta:/storage/share/git/ria-store#~wp7-course-public wp7-course
cd wp7-course
```

This pulls the tree structure and git history (~a few MB) but **not** the large file contents yet. Notebook files, PDFs, and `.mat` files appear as symlinks into an empty annex until you `get` them.

The `beta` hostname resolves via your `~/.ssh/config` (the `Host beta` entry from [SSH setup](ssh.md#2-configure-sshconfig)), so your ephys account and IP are used automatically.

### 2. Fetch content on demand

```bash
# Just the lecture slides
datalad get course-materials/lectures/

# All exercise materials, notebooks, helper modules
datalad get course-materials/exercises/ course-materials/notebooks/ course-materials/lib/

# Everything at once
datalad get .
```

`datalad get` is how annexed content actually arrives on disk. Run it on whichever subtree you care about; re-run after updates to pull changed files.

### 3. Stay up to date

When the TA pushes new material:

```bash
datalad update --merge
datalad get .     # re-pull anything that changed
```

### 4. Free up space

```bash
# Drop annexed content you no longer need (the tree stays; re-get later):
datalad drop course-materials/lectures/

# Or remove the whole clone:
cd ..
datalad remove -d wp7-course
```

---

## Flow 2 — Your work (bidirectional sync)

This syncs your personal exercise notebooks and outputs between the HPC and your laptop. Each student has their own dataset — there is no cross-contamination between students, even if you share an `ephysNN` login.

!!! info "Your TA initializes the HPC side"
    The TA creates a datalad dataset in your work directory (`/storage2/wp7/<your-slug>/`) at the start of the course. You just clone it.

### 1. Clone your work directory

```bash
datalad clone ssh://gamma3:/storage2/wp7/<your-slug>/ ~/wp7-work
cd ~/wp7-work
datalad get .
```

Replace `<your-slug>` with your first-last name slug (e.g. `alice-abel`). The `gamma3` hostname resolves via the same `~/.ssh/config` you set up for the course.

### 2. After working on the HPC — pull to laptop

```bash
cd ~/wp7-work
datalad update --merge
datalad get .
```

### 3. After working on your laptop — push to HPC

```bash
cd ~/wp7-work
datalad save -m "local edits"
datalad push --to origin
```

Both directions use the existing SSH key. No new credentials, no extra infrastructure.

### What gets version-tracked?

| Type | Stored in |
|------|-----------|
| `.ipynb`, `.py`, `.md`, `.csv`, `.txt` | Plain git (readable diffs) |
| `.mat`, `.npy`, large figures, binary outputs | git-annex (content-addressed, deduped) |

This split is automatic — the dataset is configured with `text2git` so text files are always diffable.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Permission denied (publickey)` | Your key isn't on the server. Re-run `ssh-copy-id beta` from [SSH setup step 4](ssh.md#4-install-your-public-key-so-you-dont-retype-the-password). |
| `datalad: command not found` after install | Restart your shell, or check that pixi/conda bin dir is on `$PATH`. |
| `git-annex: not found` | If you used pipx, install `git-annex` separately — `pixi global install git-annex` or your distro package manager. |
| `ERROR: ria+ssh:// … not found` | Double-check the alias spelling: `#~wp7-course-public` (tilde is literal). |
| First `datalad get` feels slow | It's serial by default. Add `--jobs 4` to parallelize: `datalad get -J 4 .` |
| `Host key verification failed` | First time via datalad's SSH. Run `ssh beta exit` once interactively to accept the host key, then retry. |
| Flow 2 push rejected | Someone else on the same `ephysNN` account may have pushed. Run `datalad update --merge` first, then retry. |

## Where to go next

- [How the data flows](infrastructure.md) — architecture diagrams and step-by-step walkthrough of what happens when material gets published or you sync your work.
- Back to the [Quick start](../quickstart.md) if you just wanted an overview.
- [VS Code Remote-SSH](vscode.md) is the recommended way to *run* the exercises — your local clone is best for reading and as a backup.
