# VS Code Remote-SSH

The recommended way to work on WP7 exercises is **VS Code** running a Remote-SSH
session into the HPC. Your files stay on the HPC (in `/storage2/wp7/...`), your
notebooks run on a compute node, and the editor UI runs on your laptop.

!!! info "Source"
    Based on `/storage/share/sirocampus/docs/how-to/ssh/vscode-setup.md` and
    `/storage/share/sirocampus/docs/reference/server/vscode-remote.md`. If this
    page disagrees with the lab docs, trust the lab docs.

## 1. Install VS Code + extensions (on your laptop)

- [VS Code](https://code.visualstudio.com/)
- `Remote - SSH` (`ms-vscode-remote.remote-ssh`)
- `Python` (`ms-python.python`)
- `Jupyter` (`ms-toolsai.jupyter`)

From the terminal:

```bash
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

## 2. Make sure plain SSH works first

Do not attempt VS Code Remote-SSH until `ssh gamma3` (or whichever alias you
configured in [SSH setup](ssh.md)) logs in passwordless. VS Code just drives
your ssh client; if the underlying ssh is broken, VS Code will be broken too.

## 3. Connect

1. In VS Code press `F1` (or `Ctrl+Shift+P`), type and select
   **`Remote-SSH: Connect to Host…`**
2. Pick `gamma3` (or whichever node was assigned to your cohort — `gamma1`–
   `gamma4` are compute nodes, any is fine).
3. First time: VS Code installs a small server into `~/.vscode-server` on the
   remote. Wait ~30 s.

## 4. Open your work folder

Use **File → Open Folder** and enter your work area:

```
/storage2/wp7/students/2026/ephys<NN>/<your-firstname-lowercase>
```

Replace `<NN>` with your assigned pooled login and `<your-firstname-lowercase>`
with… your first name in lowercase. This is the per-student convention — see
[HPC workspace](workspace.md) for why.

Click **"Yes, I trust the authors"** when prompted.

## 5. Activate the `wp7` conda env in the VS Code terminal

Open the integrated terminal (`` Ctrl+` `` or `Ctrl+J`), then:

```bash
conda activate wp7
```

See [Conda environment](conda.md) for details on what's inside.

## 6. Point VS Code at the `wp7` interpreter

Press `F1` → **`Python: Select Interpreter`** → pick the one whose path ends
in `.../envs/wp7/bin/python`. (Typically
`/storage/share/python/environments/Anaconda3/envs/wp7/bin/python`.)

## 7. Set the Jupyter kernel to `wp7`

When you open an `.ipynb` file, click the kernel name in the top-right, choose
**Python Environments**, and select `wp7`.

## Where to land — `gamma` vs `theta` vs `beta`

| Task | Node |
|---|---|
| Running exercise notebooks, long computations | `gamma1`–`gamma4` (pick one that isn't saturated) |
| Light file browsing / `ls` / `du` | `theta` (head node — **do not** run heavy jobs here) |
| `datalad clone` from off-HPC / RIA bastion | `beta` (you'll rarely need it from VS Code) |

## Port forwarding (if you want Jupyter Lab instead of VS Code notebooks)

VS Code's built-in notebook UI is what most students use. If you prefer Jupyter
Lab, press `F1` → **`Remote-SSH: Forward Port…`** → `8888`, then start
`jupyter lab --no-browser --port 8888` on the remote and open
`http://localhost:8888` in your laptop browser.
