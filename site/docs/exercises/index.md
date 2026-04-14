# Exercises

Five exercises across the term, each a self-contained Neuromatch-style notebook.

| # | Topic | Directory | Start week |
|---|-------|-----------|------------|
| 1 | [Bootstrap](ex1.md) | `ex1-bootstrap/` | TBD |
| 2 | [Dimensionality reduction](ex2.md) | `ex2-dimred/` | TBD |
| 3 | [Univariate spectral analysis](ex3.md) | `ex3-spectral-univariate/` | TBD |
| 4 | [Time-resolved spectral analysis](ex4.md) | `ex4-spectral-timeresolved/` | TBD |
| 5 | [Bivariate spectral analysis](ex5.md) | `ex5-bivariate-spectral/` | TBD |

Dates will be confirmed on the [Schedule](../schedule.md) before the term starts.

## How an exercise works

Every starter notebook follows the same Neuromatch-inspired template:

1. **Header cell** — topic name, learning objectives, estimated time.
2. **Sections** — each one has a *Think about it* prompt, a **Your Turn** TODO cell where you write code, collapsible hints (3 tiers: nudge → approach → near-solution), and a checkpoint assertion that sanity-checks your answer.
3. **Reflection cell** at the end — summarize what you learned.

!!! tip "Use the hints"
    The hint tiers are there so you can calibrate how much help you want. Peeking is not cheating — it's the whole point of the format.

## Helper module

Exercises 3–5 use functions from `wp7_helpers`, a thin wrapper around MNE-Python and scipy that's already importable in the `wp7` conda env:

- `wp7_helpers.psd_multitaper` (Ex3)
- `wp7_helpers.spectrogram_multitaper` (Ex4)
- `wp7_helpers.coherence`, `wp7_helpers.cross_spectrum` (Ex5)

Source: `course-materials/lib/wp7_helpers.py` — feel free to read it.

## Data files

Exercise data lives in `sourcedata/data/` (on HPC: `/storage2/arash/sirocampus/data/ds-wp7/`). Each exercise README tells you exactly which `.mat` file to load and how.

## Getting started

```bash
conda activate wp7
cd ~/<slug>/ex1
cp /storage2/wp7/course-materials/exercises/ex1-bootstrap/starter.ipynb ex1_<slug>.ipynb
```

Open the notebook, read the header, and go. Repeat for Ex2–5.
