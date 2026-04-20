# WP7 — Neural Data Analysis (course materials)

Course materials for **Machine Learning & Analysis of Neural Data** — MSc Neuroscience, LMU, SS 2026. Notebooks, datasets, lecture PDFs, and the Python environment spec.

The **full documentation lives on the course site** — start there:

- 🌐 **Course site (start here):** <https://sirotalab.pages.gitlab.lrz.de/wp7-course/>
- 📘 Quick start: <https://sirotalab.pages.gitlab.lrz.de/wp7-course/quickstart/>
- 📗 HPC workflow: <https://sirotalab.pages.gitlab.lrz.de/wp7-course/workflow/>
- 📄 Exercises: <https://sirotalab.pages.gitlab.lrz.de/wp7-course/exercises/>
- 📮 How to submit: <https://sirotalab.pages.gitlab.lrz.de/wp7-course/submissions/>

---

## What's in here

Students get this tree at `~/<slug>/wp7-course-materials/` on the HPC (installed by the TA via DataLad) or by cloning to their laptop.

```
wp7-course-materials/
├── pixi.toml                 # reproducible env (pixi install gets everything)
├── pixi.lock                 # committed lockfile → fresh clones skip the solve
├── data/                     # exercise datasets (annexed)
│   ├── crcns_pvc8/           #   V1 spiking — Ex1, Ex3, Ex4
│   ├── data_RGCs/            #   RGC recordings — Ex2
│   ├── spectral/             #   LFP + spike waveshapes — Ex5, Ex6, Ex7, Ex8, Ex9
│   └── clustering/           #   Chirp responses — Ex10
├── lectures/
│   ├── mlynarski/            # Lec 01–05 + Lec 10 (Wiktor)
│   └── sirota/               # Lec 06–09 + 2023 reference PDFs (Anton)
├── exercises/
│   ├── ex1-bootstrap/        # Nonparametric tests
│   ├── ex2-encoding/         # Encoding in single neurons
│   ├── ex3-populations/      # Population activity
│   ├── ex4-decoding/         # Decoding analyses
│   ├── ex5-dimred-1/         # PCA on spike waveforms
│   ├── ex6-dimred-2/         # LFP BSS + nonlinear DR
│   ├── ex7-spectral-univariate/    # Time series analysis 1
│   ├── ex8-spectral-timeresolved/  # Time series analysis 2
│   ├── ex9-bivariate-spectral/     # Time series analysis 3
│   └── ex10-clustering/      # Latent variable models
├── scripts/                  # `pixi run` task wrappers (submit, setup-ssh, …)
├── notebooks/                # reference / exploratory notebooks
└── lib/                      # shared helper module (wp7_helpers)
```

## Common student commands

Run from inside `wp7-course-materials/`:

| Command | What it does |
|---|---|
| `pixi install` | Install the scientific stack (numpy/scipy/mne/…) into `.pixi/envs/default/` |
| `pixi run kernel-install` | Register the env as a Jupyter kernel named `wp7` — **recommended** for VS Code (Copilot, debugger, git) |
| `pixi run lab` | Launch JupyterLab inside the env (alternative to the kernel flow) |
| `pixi run submit exN` | Validate + register your submission for exercise N (executes your notebook end-to-end, emails you a confirmation) |
| `datalad update --merge && datalad get .` | Pull TA updates and fetch any new/changed files |

After `pixi run kernel-install`, open any `.ipynb` in VS Code and pick
**"Python (wp7)"** from the kernel picker. Full write-up:
[Environment — Jupyter: two ways](https://sirotalab.pages.gitlab.lrz.de/wp7-course/setup/environment/#jupyter-two-ways)
· [VS Code Remote-SSH](https://sirotalab.pages.gitlab.lrz.de/wp7-course/setup/vscode/).

See the course site for the full one-time setup (install pixi, clone, SSH, VS Code Remote) and the per-exercise walkthroughs.

## Licensing

Course notebooks and scripts: MIT (see `LICENSE` when present). Data files retain their upstream licenses — see each dataset's README (e.g. `data/crcns_pvc8/README.md` for CRCNS terms).
