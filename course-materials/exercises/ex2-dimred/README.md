# Exercise 2 — Dimensionality Reduction

## Topic

Linear and nonlinear dimensionality reduction applied to neural population
activity.  High-dimensional spike-count or firing-rate matrices recorded from
tens to hundreds of neurons live on lower-dimensional manifolds that reflect the
underlying computation.  You will compare classical linear methods (PCA) with
nonlinear approaches (e.g., UMAP or Isomap) and interpret the resulting
low-dimensional representations in terms of the animal's behavior or stimulus
conditions.

## Files in this directory

- `ex2.pdf` — the exercise prompt (authored by Anton Sirota)
- `starter.ipynb` — scaffolded notebook (TBD — pending Anton's 2025/2026 updates; see `planning/`)
- `README.md` — this file

## Data

Population spiking data from the ds-wp7 dataset at:

```
/storage2/arash/sirocampus/data/ds-wp7/spikes.mat
/storage2/arash/sirocampus/data/ds-wp7/spike_waveshapes.mat
```

`spikes.mat` contains spike times and neuron identities; `spike_waveshapes.mat`
contains spike waveforms for quality assessment.  Load with `scipy.io.loadmat`.
You will need to bin spikes into a (neurons × time-bins) firing-rate matrix
before applying dimensionality reduction.

## Prerequisites

- **Lectures** (from `lectures/sirota/`):
  - `DimReduction_1_2023.pdf` — PCA and linear subspace methods
  - `DimReduction_BSS.pdf` — blind source separation (ICA)
  - `DimReduction_Nonlinear.pdf` — UMAP, Isomap, t-SNE
- **Previous exercises**: Ex1 (bootstrap) — useful for assessing explained-variance significance
- **Packages**: `numpy`, `scipy`, `matplotlib`, `scikit-learn` (PCA, Isomap), optionally `umap-learn` (UMAP)

## Tips

- Build the firing-rate matrix first: choose a bin width (e.g., 50–100 ms) that
  balances temporal resolution against spike-count sparsity.
- Variance explained by principal components does not necessarily mean
  *interpretable* components — compare plots with behavior labels before
  concluding anything.
- UMAP and Isomap are sensitive to hyperparameters (number of neighbours,
  minimum distance); show results for at least two parameter settings.
- `umap-learn` may not be installed in the shared `wp7` environment yet — check
  `planning/env-audit-2026-04.md` for status and fall back to `sklearn.manifold.Isomap`
  or `sklearn.manifold.TSNE` if needed.
- Colour your low-dimensional scatter plots by a behavioural or stimulus variable
  to give the reduction biological meaning.

## Also see

- Site page: [exercises/ex2](../../site/docs/exercises/ex2.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
