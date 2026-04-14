# Exercise 5 — Bivariate spectral analysis

Measure frequency-resolved coupling between pairs of LFP channels using coherence and cross-spectral density. You'll build a null distribution to test whether the coupling you see is real.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex5-bivariate-spectral/` |
| **Data** | `ws_data_1shank.mat` (same 16-ch LFP as Ex3–4); advanced: `data96.mat` (96-ch) |
| **Packages** | numpy, scipy, matplotlib |
| **Helper module** | `wp7_helpers.coherence`, `wp7_helpers.cross_spectrum` — see `course-materials/lib/wp7_helpers.py` |
| **Prereqs** | All three `lectures/sirota/SpectralAnalysis_*` PDFs |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex5 && cd ~/<slug>/ex5
cp /storage2/wp7/course-materials/exercises/ex5-bivariate-spectral/starter.ipynb ex5_<slug>.ipynb
```

This exercise builds on Ex3 and Ex4. See the `README.md` for data paths, the 96-channel bonus option, and tips on interpreting coherence values. Prompt: `ex5.pdf`.
