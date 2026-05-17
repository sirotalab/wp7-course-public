# Exercise 3 — Modelling neural population activity

## Topic

Population-level spike statistics on V1 recordings: response variability,
noise correlations, and dimensionality reduction via PCA. You'll quantify
trial-to-trial variability (Fano factors, CVs), inspect correlation
structure across neurons, then convolve trial-by-trial spike trains with
a Gaussian kernel to obtain instantaneous firing rates and project them
into a PCA space to see trajectory structure across stimuli.

## Style

**Open-ended.** Wiktor's starter gives you the dataset, three numbered
problem blocks (variability, noise correlations, neural dynamics in PCA
space), and one block of scaffold code to get you started loading and
plotting rasters. You decide which neurons to look at, how to summarize
variability, and how to visualise the PCA space.

## Files in this directory

- `starter.py` — Wiktor's open-ended prompt (Mlynarski, 2026). Note: ships
  as a `.py` percent-format script rather than a notebook — most of the
  work is numerical and a plain script keeps it tidy.
- `README.md` — this file.

Create your working copy with `pixi run start ex3` (produces `ex3.py`).
Edit that, not `starter.py`.

## Data

V1 spike-train recordings from the [CRCNS PVC-8](https://crcns.org/data-sets/vc/pvc-8)
dataset (Kohn lab), same as Ex1:

    ../../data/crcns_pvc8/1.mat

The `.mat` file contains `resp_train` (shape `(n_cells, n_images, n_trials, n_tp)`,
1 ms bins) and `images` (the stimuli). Load with `scipy.io.loadmat`.

## Prerequisites

- **Lectures:** Mlynarski — Lec 03 (neural population activity)
- **Previous exercises:** Ex1 (data handling) + Ex2 (encoding)
- **Packages:** `numpy`, `scipy`, `matplotlib`, `scikit-learn` (`PCA`)

## Reading (optional — pick what helps)

- Cunningham & Yu (2014) — [Dimensionality reduction for large-scale
  neural recordings](https://www.nature.com/articles/nn.3776) (Nature Neuroscience).
- Stringer et al (2019) — [High-dimensional geometry of population
  responses in visual cortex](https://www.nature.com/articles/s41586-019-1346-5).

## Submit

```bash
pixi run submit ex3
```

See the course site's [Submissions](../../../../website/docs/submissions.md) page for the contract. Note: Ex3 ships as `.py`, so `pixi run submit ex3` reads `ex3.py` rather than `ex3.ipynb`.
