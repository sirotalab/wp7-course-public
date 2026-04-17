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

## 4. Open your workspace

Your TA has already set up a workspace with all course materials at:

```
/storage2/wp7/<your-slug>/
```

A convenience symlink is in your home directory, so just:

```bash
cd ~/<your-slug>
conda activate wp7
```

The workspace contains:

```
<your-slug>/
├── course-materials/     # exercises, lectures, data, helper modules
│   ├── exercises/        #   ex1-bootstrap/, ex2-encoding/, ..., ex9-bivariate-spectral/
│   ├── data/             #   crcns_pvc8/, data_RGCs/, clustering/, spectral/
│   ├── lectures/         #   mlynarski/, sirota/
│   ├── notebooks/        #   reference notebooks
│   └── lib/              #   wp7_helpers.py
└── (your work goes here) #   ex1/, ex2/, ... — one dir per exercise
```

## 5. Do Exercise 1

```bash
cd ~/<your-slug>/course-materials/exercises/ex1-bootstrap
```

Open `starter.ipynb`, read the header cell. All nine exercises: [Exercises](exercises/index.md).

!!! tip "Working convention"
    Work directly in the exercise directories. Your changes are yours — the TA can push updates without clobbering your work because `course-materials/` is a DataLad subdataset.

## 6. Submit

See [Submissions](submissions.md) — it's a filename convention, nothing fancy.

---

## Optional — sync to your laptop

You can work entirely on the HPC (steps 1–6 are all you need). But if you want a local copy for offline work or as a backup:

### Install datalad (once)

The fastest cross-platform method is [pixi](https://pixi.sh):

```bash
curl -fsSL https://pixi.sh/install.sh | bash   # install pixi
pixi global install datalad                      # installs datalad + git-annex
```

Alternatives (conda, Homebrew, pipx) are listed on the [DataLad setup](setup/datalad.md#prerequisites) page.

### Clone your HPC workspace

```bash
datalad clone ssh://gamma3:/storage2/wp7/<your-slug>/ ~/wp7-work
cd ~/wp7-work
datalad get .
```

This pulls everything — your work and the course materials. After working on HPC, pull with `datalad update --merge && datalad get .`. After working on your laptop, push with `datalad save -m "..." && datalad push --to origin`.

Full walkthrough: **[DataLad setup](setup/datalad.md)**.

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
