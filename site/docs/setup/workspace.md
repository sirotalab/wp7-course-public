# HPC workspace

## Your shared HPC login

You log in as `ephysNN` — a pooled account shared with a few classmates. Which one is yours? Check the [interactive SSH tool](../tools/ssh-setup.html) or the [quick-start lookup](../quickstart.md).

## Your personal workspace

Each student gets a directory at:

```
/storage2/wp7/<slug>/
```

where `<slug>` is your name in `firstname-lastname` form (e.g. `alice-abel`).

A convenience symlink is already set up in your ephys home, so:

```bash
cd ~/<slug>
```

drops you straight into `/storage2/wp7/<slug>/`. That's your home base for the course.

## Where to put your work

Create one sub-directory per exercise:

```
/storage2/wp7/<slug>/ex1/
/storage2/wp7/<slug>/ex6/
/storage2/wp7/<slug>/ex7/
...
```

The TA picks up your submissions from there at grading time. See [Submissions](../submissions.md) for the naming convention.

## Your workspace is a DataLad dataset

The TA initializes your workspace as a [DataLad](https://www.datalad.org/) dataset at the start of the course. This means you can clone it to your laptop and sync changes in both directions over SSH — useful as a backup or for working offline.

- Text files (`.ipynb`, `.py`, `.md`) are tracked in plain git — you get readable diffs.
- Large binary files (`.mat`, `.npy`, figures) go through git-annex — content-addressed, deduped.

If you want to use this, see the [DataLad setup](datalad.md#flow-2-your-work-bidirectional-sync) page. It's entirely optional — you can ignore datalad and just work on the HPC via VS Code.

## Why peer reads are open

Shared UIDs make within-account privacy impossible at the POSIX level, and we've decided that's a feature: reading other people's solutions is genuinely useful for learning. Don't be shy about peeking; don't be shy about being peeked at.

!!! note "Ground rules"
    - **Stay in your lane** — don't write outside your own `<slug>/` directory.
    - **Don't lock others out** — don't `chmod 700` your directory. It kills peer reads and defeats the point.
