# Exercises

Nine exercises matching the nine course topics — one per topic. Each has a starter notebook (or script) you'll work through during the exercise sessions.

| Ex # | Topic | Directory | Start week |
|---|---|---|---|
| 1 | [Bootstrap](ex1.md) | `ex1-bootstrap/` | TBD |
| 2 | [Encoding in individual neurons](ex2.md) | `ex2-encoding/` | TBD |
| 3 | [Neural population activity](ex3.md) | `ex3-populations/` | TBD |
| 4 | [Decoding neural activity](ex4.md) | `ex4-decoding/` | TBD |
| 5 | [Clustering](ex5.md) | `ex5-clustering/` | TBD |
| 6 | [Dimensionality reduction](ex6.md) | `ex6-dimred/` | TBD |
| 7 | [Univariate spectral analysis](ex7.md) | `ex7-spectral-univariate/` | TBD |
| 8 | [Time-resolved spectral analysis](ex8.md) | `ex8-spectral-timeresolved/` | TBD |
| 9 | [Bivariate spectral analysis](ex9.md) | `ex9-bivariate-spectral/` | TBD |

Dates will be confirmed on the [Schedule](../schedule.md) before the term starts.

!!! info "About the numbering"
    Exercise numbers match the course topic they belong to:

    1. Introduction and nonparametric hypothesis testing
    2. Encoding in individual neurons
    3. Modelling neural population activity
    4. Decoding neural activity
    5. Unsupervised structure discovery — latent variable models, clustering
    6. Unsupervised structure discovery — dimensionality reduction
    7. Spectral analysis of neural data I
    8. Spectral analysis of neural data II
    9. Spectral analysis of neural data III

    Exercises 1–5 are from Mlynarski's half of the course; exercises 6–9 are from Sirota's half.

## How an exercise works

Exercises 1 and 6–9 use Neuromatch-style starter notebooks with TODO cells, collapsible hints, and checkpoint assertions. Exercises 2–5 use Mlynarski's original format (scaffolded notebooks or Python scripts).

!!! tip "Use the hints"
    Where hints are provided, peek freely — the tiers are there so you can calibrate how much help you want.

## Helper module

Exercises 7–9 use functions from `wp7_helpers`, a thin wrapper around MNE-Python and scipy that's already importable in the `wp7` conda env:

- `wp7_helpers.psd_multitaper` (Ex7)
- `wp7_helpers.spectrogram_multitaper` (Ex8)
- `wp7_helpers.coherence`, `wp7_helpers.cross_spectrum` (Ex9)

Source: `course-materials/lib/wp7_helpers.py` — feel free to read it.

## Data files

Exercise data lives in `sourcedata/data/` (on HPC: `/storage2/arash/sirocampus/data/`). Each exercise README tells you exactly which files to load and how. Key datasets:

- **crcns_pvc8** — population spiking data, used in Ex1, Ex3, Ex4, Ex5
- **data_RGCs** — retinal ganglion cell recordings, used in Ex2
- **chirp_response** — chirp-evoked responses, used in Ex5
- **ws_data_1shank.mat** — 16-ch hippocampal LFP (1250 Hz), used in Ex7, Ex8, Ex9

## Getting started

```bash
conda activate wp7
cd ~/<slug>/ex1
cp /storage2/wp7/course-materials/exercises/ex1-bootstrap/starter.ipynb ex1_<slug>.ipynb
```

Open the notebook, read the header, and go. Repeat for Ex2–9.
