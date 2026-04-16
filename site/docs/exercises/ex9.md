# Exercise 9 — Bivariate spectral analysis

Measure frequency-resolved coupling between pairs of LFP channels using coherence and cross-spectral density. You'll build a null distribution to test whether the coupling you see is real.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex9-bivariate-spectral/` |
| **Data** | `ws_data_1shank.mat` (same 16-ch LFP as Ex7–8); advanced: `data96.mat` (96-ch) |
| **Packages** | numpy, scipy, matplotlib |
| **Helper module** | `wp7_helpers.coherence`, `wp7_helpers.cross_spectrum` — see `course-materials/lib/wp7_helpers.py` |
| **Prereqs** | All three `lectures/sirota/SpectralAnalysis_*` PDFs |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex9 && cd ~/<slug>/ex9
cp /storage2/wp7/course-materials/exercises/ex9-bivariate-spectral/starter.ipynb ex9_<slug>.ipynb
```

This exercise builds on Ex7 and Ex8. See the `README.md` for data paths, the 96-channel bonus option, and tips on interpreting coherence values. Prompt: `ex9.pdf`.
