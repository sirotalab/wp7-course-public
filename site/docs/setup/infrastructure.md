# How the data flows

This page explains where your files actually live and how they move between the HPC and your laptop. You don't need to read this to use the course — but if you're curious about what happens under the hood, here's the full picture.

## Two independent datasets

The course uses two separate [DataLad](https://www.datalad.org/) datasets. They share no git history and have no sibling relationship to each other.

### Course materials (read-only)

```
 TA working copy              RIA store (beta)            your laptop
 ┌──────────────────┐  push   ┌──────────────────┐ clone  ┌──────────────┐
 │ public/           │ ──────▶│ /storage/share/  │◀────── │ ~/wp7-course │
 │   course-materials│  ria   │ git/ria-store/   │ ria+ssh│              │
 │   site/           │        │                  │───────▶│  (read-only) │
 └──────────────────┘        └──────────────────┘  get   └──────────────┘
```

- The **TA** maintains course materials in a private repo and pushes to a lab-internal RIA store on `beta`.
- **You** clone from that store and pull updates. You never push back — it's a one-way mirror.
- The RIA store is a content-addressed object store. Large files (PDFs, `.mat` data) are served through git-annex over the same SSH connection you already use.
- On the HPC, course materials are also available directly at `/storage2/wp7/course-materials/` — no datalad needed when you're already logged in.

### Your work (bidirectional)

```
 your HPC workspace                          your laptop
 ┌──────────────────────┐     clone          ┌──────────────┐
 │ /storage2/wp7/       │◀──────────────────│ ~/wp7-work   │
 │ <your-slug>/         │  ssh://gamma3:... │              │
 │                      │                   │              │
 │                      │  update --merge   │              │
 │  (origin)            │──────────────────▶│  (clone)     │
 │  updateInstead       │      pull         │              │
 │                      │                   │              │
 │                      │◀──────────────────│              │
 └──────────────────────┘   save + push     └──────────────┘
```

- The **TA** creates your personal dataset at `/storage2/wp7/<your-slug>/` at the start of the course.
- **You** clone it to your laptop via plain SSH — no store, no extra infrastructure.
- Push from your laptop updates the HPC worktree in-place (the dataset is configured with `receive.denyCurrentBranch = updateInstead`).
- Text files (`.ipynb`, `.py`, `.md`) live in plain git. Binary files (`.mat`, `.npy`, large figures) go through git-annex.

---

## What happens when the TA publishes new material

Here's the concrete sequence when, say, Exercise 7 starters are ready:

### 1. TA adds files on the HPC

```bash
# In the TA's private repo:
cp -r ~/new-ex7-starters/ public/course-materials/exercises/ex7-spectral-univariate/
```

The new files land in `public/course-materials/exercises/ex7-spectral-univariate/` — starter notebook, `README.md`, sample data.

### 2. TA saves and pushes

```bash
cd public/
datalad save -m "add ex7 spectral analysis starters"
datalad push --to ria
```

`datalad save` stages everything into git (text files) or git-annex (binaries) and commits.
`datalad push --to ria` sends the commit and any new annex objects to the RIA store on `beta`.

At this point the new content is in the store but students don't have it yet.

### 3. Students pull on the HPC

Nothing to do — `/storage2/wp7/course-materials/` is a symlink to the TA's working copy. The moment the TA saves, the files appear on the HPC for everyone. Students on VS Code Remote-SSH see them immediately.

### 4. Students update their laptop clone (if they have one)

```bash
cd ~/wp7-course
datalad update --merge    # fetch the new commit
datalad get .             # download any new annexed content
```

`update --merge` pulls the git history. `get` fetches the actual bytes for any new large files via the RIA store over SSH.

---

## What happens when you sync your own work

### Scenario: you worked on the HPC, want to pull to laptop

You edited `ex7/ex7_alice-abel.ipynb` on gamma3 via VS Code Remote-SSH and ran some cells.

```bash
# On your laptop:
cd ~/wp7-work
datalad update --merge
datalad get .
```

Your laptop now has the latest version of the notebook, including any output cells and figures.

### Scenario: you worked on your laptop, want to push to HPC

You worked offline and want your changes back on the HPC before the deadline.

```bash
# On your laptop:
cd ~/wp7-work
datalad save -m "ex7 finished"
datalad push --to origin
```

The push updates the HPC worktree in-place — no merge needed on the HPC side. The TA sees your submission at `/storage2/wp7/<your-slug>/ex7/` at grading time.

### Scenario: you worked in both places

You edited on the HPC *and* on your laptop without syncing in between. On the next push or pull, datalad (git) will ask you to merge. In practice this is rare if you follow the rule: **pull before you start working, push when you're done.**

---

## Key terms

| Term | What it means here |
|------|-------------------|
| **RIA store** | A content-addressed object store that datalad uses to distribute large files. Lives at `/storage/share/git/ria-store` on `beta`. Think of it as a shared locker for PDFs and datasets. |
| **git-annex** | The layer under datalad that handles large files. Text files go in plain git; binaries go in annex. You interact with datalad, not git-annex directly. |
| **updateInstead** | A git setting on your HPC workspace that lets pushes from your laptop update the working tree immediately — no need to log in and `git checkout` after pushing. |
| **sibling** | Datalad's name for a remote — a place where a copy of the dataset lives. Your laptop clone has `origin` (the HPC). The course materials have `ria` (the store on beta). |
