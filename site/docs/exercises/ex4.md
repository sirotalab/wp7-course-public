# Exercise 4 — Time-resolved spectral analysis

Build spectrograms to see how oscillation power changes over time. You'll explore the time–frequency tradeoff and identify theta, ripple, and other activity patterns in the same hippocampal LFP from Ex3.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex4-spectral-timeresolved/` |
| **Data** | `ws_data_1shank.mat` (same 16-ch LFP as Ex3) |
| **Packages** | numpy, scipy, matplotlib |
| **Helper module** | `wp7_helpers.spectrogram_multitaper` — see `course-materials/lib/wp7_helpers.py` |
| **Prereqs** | `lectures/sirota/SpectralAnalysis_1_2023.pdf`, `SpectralAnalysis_2_2023.pdf`, `SpectralAnalysis_3_2023.pdf` |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex4 && cd ~/<slug>/ex4
cp /storage2/wp7/course-materials/exercises/ex4-spectral-timeresolved/starter.ipynb ex4_<slug>.ipynb
```

Make sure you're comfortable with Ex3 first — Ex4 builds directly on it. See the `README.md` for window-size tips and the prompt PDF `ex4.pdf`.
