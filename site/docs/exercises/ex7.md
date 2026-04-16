# Exercise 7 — Univariate spectral analysis

Estimate power spectral density using the multitaper method and test for rhythmic activity in single LFP channels. You'll compare Welch and multitaper estimators on 16-channel hippocampal recordings.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex7-spectral-univariate/` |
| **Data** | `ws_data_1shank.mat` (16-ch LFP, 1250 Hz) |
| **Packages** | numpy, scipy, matplotlib |
| **Helper module** | `wp7_helpers.psd_multitaper` — see `course-materials/lib/wp7_helpers.py` |
| **Prereqs** | `lectures/sirota/SpectralAnalysis_1_2023.pdf`, `SpectralAnalysis_2_2023.pdf` |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex7 && cd ~/<slug>/ex7
cp /storage2/wp7/course-materials/exercises/ex7-spectral-univariate/starter.ipynb ex7_<slug>.ipynb
```

The starter imports `wp7_helpers` for you. Check the `README.md` for data loading and parameter tips. Prompt: `ex7.pdf`.
