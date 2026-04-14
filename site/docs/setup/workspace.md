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
/storage2/wp7/<slug>/ex2/
...
```

The TA picks up your submissions from there at grading time — no git push, no upload, no Gradescope. See [Submissions](../submissions.md) for the naming convention.

## Why peer reads are open

Shared UIDs make within-account privacy impossible at the POSIX level, and we've decided that's a feature: reading other people's solutions is genuinely useful for learning. Don't be shy about peeking; don't be shy about being peeked at.

!!! note "Ground rules"
    - **Stay in your lane** — don't write outside your own `<slug>/` directory.
    - **Don't lock others out** — don't `chmod 700` your directory. It kills peer reads and defeats the point.
