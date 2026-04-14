# Exercise 2 — Dimensionality reduction

Apply linear (PCA, ICA) and nonlinear (Isomap) dimensionality reduction to neural data — spike waveforms and LFP signals — and learn what low-dimensional structure can tell you about the brain.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex2-dimred/` |
| **Data** | `lfp.mat`, `spike_waveshapes.mat` (from `sourcedata/`) |
| **Packages** | numpy, scipy, matplotlib, scikit-learn (`PCA`, `FastICA`, `Isomap`) |
| **Helper module** | — (scikit-learn does the heavy lifting) |
| **Prereqs** | `lectures/sirota/DimReduction_1_2023.pdf`, `DimReduction_BSS.pdf`, `DimReduction_Nonlinear.pdf` |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex2 && cd ~/<slug>/ex2
cp /storage2/wp7/course-materials/exercises/ex2-dimred/starter.ipynb ex2_<slug>.ipynb
```

Check the exercise `README.md` for data paths and tips. The prompt PDF (`ex2.pdf`) is in the same directory.
