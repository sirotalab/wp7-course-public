# Conda environment

## Activate

```bash
conda activate wp7
```

That's it — the shared environment is pre-installed on the HPC with everything you need for Ex1–5.

## What's in it

numpy, scipy, matplotlib, seaborn, scikit-learn, pandas, MNE-Python, JupyterLab, marimo, ipywidgets, tqdm — plus the course helper module `wp7_helpers` from `course-materials/lib/`.

## Notebook frontends

Pick whichever you prefer:

**JupyterLab** (classic notebook interface):

```bash
jupyter lab --no-browser --port 8888
```

**[marimo](https://marimo.io)** (reactive Python notebooks):

```bash
marimo edit notebook.py --host 0.0.0.0 --port 2718
```

Both work fine for all exercises. JupyterLab uses `.ipynb` files; marimo uses plain `.py` files. Your submission should be `.ipynb` — if you work in marimo, export before submitting.

## Escape hatch

Want to experiment with extra packages? Create a personal venv that inherits everything from `wp7`:

```bash
python -m venv --system-site-packages ~/.wp7-extra
source ~/.wp7-extra/bin/activate
pip install whatever-you-want
```

To go back to plain `wp7`:

```bash
deactivate
conda activate wp7
```

!!! warning "Don't pip install into wp7"
    The `wp7` env is shared across the whole cohort. Installing or upgrading packages there breaks it for everyone. If you need something that's missing, ask your TA in the course chat.
