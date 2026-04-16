# Quick start

From "just enrolled" to "first exercise running on the HPC" in 5 minutes. If anything breaks, ask in the course chat or see the longer [Setup](setup/ssh.md) pages.

## 1. Register for a pooled login

The cohort shares 10 accounts on the HPC (`ephys01`–`ephys10`). The TA assigns them centrally after registration closes.

Open the **[SSH setup page](tools/ssh-setup.html)** and click **Open registration form** to submit your name and email via Google Forms. You'll receive your account, temporary password, and SSH config snippet by email once the roster is processed.

## 2. Generate an SSH key and log in

On your laptop:

```bash
ssh-keygen -t ed25519 -C "your.email@campus.lmu.de"
```

Paste the config snippet from the TA's email into `~/.ssh/config`, then:

```bash
ssh gamma3           # first login, temporary password
exit
ssh-copy-id gamma3   # install your public key
ssh gamma3           # should connect without a password
```

The three hosts in the snippet:

- **`gamma3`** — course compute node. Run notebooks here.
- **`theta`** — head node. Light editing only, no heavy compute.
- **`beta`** — git/datalad bastion. Only needed for off-HPC clones.

Full walkthrough (including off-campus VPN): [SSH setup](setup/ssh.md).

## 3. VS Code Remote (recommended)

Install the **Remote - SSH** extension, press `F1`, pick **Connect to Host → gamma3**. Done. Full walkthrough: [VS Code Remote-SSH](setup/vscode.md).

## 4. Course materials and environment

```bash
cd /storage2/wp7/course-materials
conda activate wp7
```

The directory is read-only; the `wp7` env has everything for Ex1–5. Don't `pip install` into it — it's shared. Missing a package? Flag it in the chat.

## 5. Do Exercise 1

```bash
cd /storage2/wp7/course-materials/exercises/ex1-bootstrap
```

Open the starter notebook, read its `README.md`. All five exercises: [Exercises](exercises/index.md).

## 6. Submit

See [Submissions](submissions.md) — it's a filename convention, nothing fancy.

---

## Optional — sync to your laptop

You can work entirely on the HPC (steps 1–6 are all you need). But if you want a local copy for offline reading or a backup of your own work, install [DataLad](https://www.datalad.org/) on your laptop and clone over SSH. There are two independent flows:

### Install datalad (once)

The fastest cross-platform method is [pixi](https://pixi.sh):

```bash
curl -fsSL https://pixi.sh/install.sh | bash   # install pixi
pixi global install datalad                      # installs datalad + git-annex
```

Alternatives (conda, Homebrew, pipx) are listed on the [DataLad setup](setup/datalad.md#prerequisites) page.

### Clone course materials (read-only)

```bash
datalad clone ria+ssh://beta:/storage/share/git/ria-store#~wp7-course-public wp7-course
cd wp7-course
datalad get .
```

Pull updates any time with `datalad update --merge && datalad get .`

### Clone your HPC work (bidirectional)

```bash
datalad clone ssh://gamma3:/storage2/wp7/<your-slug>/ ~/wp7-work
cd ~/wp7-work
datalad get .
```

After working on HPC, pull with `datalad update --merge`. After working on your laptop, push with `datalad save -m "..." && datalad push --to origin`.

Full walkthrough for both flows: **[DataLad setup](setup/datalad.md)**.

---

## Cheat sheet

| Need | Where |
|---|---|
| SSH, off-campus access | [Setup → SSH](setup/ssh.md) |
| VS Code Remote-SSH | [Setup → VS Code Remote](setup/vscode.md) |
| Conda environment | [Setup → Conda](setup/conda.md) |
| Per-student workspace | [Setup → HPC workspace](setup/workspace.md) |
| Sync to laptop (DataLad) | [Setup → DataLad](setup/datalad.md) |
| Architecture & data flows | [Setup → How the data flows](setup/infrastructure.md) |
| Schedule | [Schedule](schedule.md) |
| Exercises | [Exercises](exercises/index.md) |
| Submissions | [Submissions](submissions.md) |
