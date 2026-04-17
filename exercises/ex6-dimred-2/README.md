# Exercise 6 — Dimensionality Reduction 2 (LFP BSS + Nonlinear)

## Topic

Blind source separation via FastICA on multichannel local field potentials
(LFP), theta-triggered analysis, frequency-band effects, denoising, and
nonlinear dimensionality reduction (Isomap, t-SNE).

## Files in this directory

- `starter.ipynb` — scaffolded Neuromatch-style notebook
- `README.md` — this file

## Data

Multichannel LFP from a linear probe (for BSS tasks) and spike waveshapes
(for the nonlinear bonus):

```
../../data/spectral/lfp.mat
../../data/spectral/spike_waveshapes.mat
```

## Prerequisites

- **Lectures**: Anton — Dimensionality Reduction 2 (Lec 06: BSS + Nonlinear)
- **Previous exercises**: **Ex5 required** (establishes PCA baseline); Ex1–4 for data handling
- **Packages**: `numpy`, `scipy`, `matplotlib`, `scikit-learn` (`FastICA`, `Isomap`, `TSNE`)

## Tips

- **Spatial profiles** — each column of the ICA mixing matrix `A` is one IC's projection across channels. Laminar sources look smooth and localised; EMG artifacts look broad or flat.
- **IC non-uniqueness** — unlike PCA, ICA components aren't ordered by variance; re-runs may permute/flip them.
- **Theta-triggered averaging** — band-pass at 5–12 Hz, find local minima, extract windows, average across epochs. A coherent IC will show a clear phase-locked structure.
- **Nonlinear methods** — Isomap needs a connected k-NN graph; t-SNE is sensitive to perplexity. Subsample for speed (~5k points).

## Also see

- Site page: [exercises/ex6](../../../site/exercises/ex6.md)
- [Submissions](../../../site/submissions.md)
- Builds on Ex5 (DimRed 1)
