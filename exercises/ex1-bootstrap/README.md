# Exercise 1 — Bootstrap

## Topic

Resampling-based confidence intervals and hypothesis testing without parametric
assumptions.  You will apply the bootstrap to neural spike-train data to assess
whether observed temporal structure (inter-spike intervals) is statistically
surprising.  The bootstrap is one of the most broadly applicable tools in
quantitative neuroscience: it lets you attach uncertainty bounds to almost any
statistic, even when you cannot derive an analytic null distribution.

## Files in this directory

- `ex1.pdf` — the exercise prompt (authored by Anton Sirota)
- `starter.ipynb` — scaffolded notebook (TBD — pending Anton's 2025/2026 updates; see `planning/`)
- `README.md` — this file

## Data

Single-unit spike recordings from V1 (primary visual cortex), loaded from:

```
../../data/crcns_pvc8/2.mat
```

Data are provided via the CRCNS PVC-8 dataset.  The `.mat` file contains spike
times for one or more neurons recorded during visual stimulation.  Load with
`scipy.io.loadmat`.

## Prerequisites

- **Lectures**: no dedicated WP7 lecture — review basic probability and
  hypothesis testing (any intro stats / neural data analysis reading)
- **Previous exercises**: none (Ex1 is the entry point)
- **Packages**: `numpy`, `scipy` (especially `scipy.stats`), `matplotlib`, `tqdm`

## Tips

- Bootstrap resampling draws **with replacement**; make sure your resampling
  loop reflects that.
- Your test statistic should be computable from a single resample — keep it
  simple and interpretable (a mean, a ratio, etc.).
- The null distribution should correspond to what the data would look like if
  the temporal structure you are testing were absent — think carefully about
  what to permute or resample.
- `tqdm` wrapping your bootstrap loop is highly recommended: 1000–10 000
  resamples can take tens of seconds.
- Plot the null distribution as a histogram and mark the observed statistic with
  a vertical line — that figure is the core result.

## Also see

- Site page: [exercises/ex1](../../site/docs/exercises/ex1.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
