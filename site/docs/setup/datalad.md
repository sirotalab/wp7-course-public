# Clone the course materials to your laptop

You don't *have* to do this — working directly on the HPC via [VS Code Remote-SSH](vscode.md) is the main path. But if you want an offline copy for travel, train rides, or just a local git history of the course, the materials are published as a [DataLad](https://www.datalad.org/) dataset you can clone over SSH.

!!! info "One-way mirror"
    The clone is **read-only from your side**. You can `datalad update` to pull the TA's changes, but you cannot push back. If you want to version your own work, commit locally and push to a repo **you own** — never back to the lab.

## Prerequisites

1. SSH to `beta` is working passwordless (finish [SSH setup](ssh.md) first — verify with `ssh beta exit`).
2. DataLad and git-annex are installed on your laptop:

    === "Linux / macOS (conda)"

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

        Use WSL2 and follow the Linux instructions. Native Windows works but is finicky — we don't support it.

    Verify with `datalad --version` and `git annex version`.

## 1. Clone the superdataset

```bash
datalad clone ria+ssh://beta:/storage2/wp7/ria-store#~wp7-course-public wp7-course
cd wp7-course
```

This pulls the tree structure and git history (~a few MB) but **not** the large file contents yet. Notebook files, PDFs, and `.mat` files appear as symlinks into an empty annex until you `get` them.

The `beta` hostname resolves via your `~/.ssh/config` (the `Host beta` entry from [SSH setup](ssh.md#2-configure-sshconfig)), so your ephys account and IP are used automatically.

## 2. Fetch content on demand

```bash
# Just the lecture slides (~71 MB)
datalad get course-materials/lectures/

# All exercise materials, notebooks, helper modules
datalad get course-materials/exercises/ course-materials/notebooks/ course-materials/lib/

# Everything at once
datalad get .
```

`datalad get` is how annexed content actually arrives on disk. Run it on whichever subtree you care about; re-run after `datalad update` to pull changed files.

## 3. Stay up to date

When the TA pushes a new starter notebook or a lecture fix:

```bash
datalad update --merge
datalad get course-materials/     # re-pull anything that changed
```

`datalad update --merge` is the datalad equivalent of `git pull` for both the superdataset and any subdatasets. It's non-destructive as long as you haven't committed over the upstream history.

## 4. Free up space

```bash
# Drop the local copy of annexed content you no longer need.
# The tree stays; run `datalad get` to pull it back later.
datalad drop course-materials/lectures/

# Or nuke the whole clone:
cd ..
datalad remove -d wp7-course
```

## 5. Work on your own copy

Inside the clone, you can `git commit` or `datalad save` on top of the course history — reshuffle files, take notes, add scratch notebooks. None of it goes back to the lab.

If you want your own work versioned elsewhere, add a personal git remote (a private GitLab project, a bare repo on a USB stick, whatever) and push there:

```bash
git remote add personal git@gitlab.lrz.de:<you>/wp7-notes.git
git push personal main
```

The lab's `origin` stays read-only; your `personal` remote is yours.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Permission denied (publickey)` | Your key isn't on `beta`. Re-run `ssh-copy-id beta` from [SSH setup step 4](ssh.md#4-install-your-public-key). |
| `datalad: command not found` after install | Restart your shell, or check that your conda/pipx bin dir is on `$PATH`. |
| `git-annex: not found` | Install `git-annex` separately — `conda install -c conda-forge git-annex` or your distro package manager. |
| `ERROR: ria+ssh:// … not found` | Double-check the alias spelling: `#~wp7-course-public` (tilde is literal). |
| First `datalad get` feels slow | It's serial by default over SSH. Add `--jobs 4` to parallelize: `datalad get -J 4 course-materials/`. |
| `Host key verification failed` | First time connecting via datalad's SSH. Run `ssh beta exit` once interactively to accept the host key, then retry. |

## Where to go next

- Back to the [Quick start](../quickstart.md) if you just wanted an overview.
- [VS Code Remote-SSH](vscode.md) is still the recommended way to *do* the exercises — your local clone is best for reading and experimenting, not for running notebooks that need the lab datasets.
