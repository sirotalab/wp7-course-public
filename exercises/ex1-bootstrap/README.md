# Exercise 1 — Bootstrap

## Topic

Resampling-based hypothesis testing without parametric assumptions. You will apply
the bootstrap to V1 spike-train data and test whether observed temporal structure
in inter-spike intervals (ISIs) is statistically surprising. The bootstrap is one
of the most broadly applicable tools in quantitative neuroscience — it attaches
uncertainty bounds to almost any statistic, even when no analytic null exists.

## Style

**Open-ended** — the starter gives you a question, a dataset, and a sketch of
the sections. Your task is to explore and decide: which test statistic? which
shuffling scheme? which neuron? Each section has a "peek if stuck" collapsible
with a skeleton; use it only after you've tried on your own. No autograder.

## Files in this directory

- `starter.ipynb` — Neuromatch-style scaffold (open the header first — it has prereqs and reading links)
- `README.md` — this file

## Data

Single-unit recordings from V1 (primary visual cortex), [CRCNS PVC-8](https://crcns.org/data-sets/vc/pvc-8):

```
../../data/crcns_pvc8/2.mat
```

The `.mat` file contains `resp_train`, a 4-D binary array of shape
`(n_cells, n_images, n_trials, n_tp)`. Load with `scipy.io.loadmat`.

## Prerequisites

- **Lectures**: Wiktor — Introduction & nonparametric testing (Lec 01a, 01b)
- **Previous exercises**: none (Ex1 is the entry point)
- **Packages**: `numpy`, `scipy`, `matplotlib`

## Reading (optional — pick what helps)

- Murphy — *Machine Learning: A Probabilistic Approach*, §4.1–4.3, §6.5 (bootstrap).
- MacKay — *Information Theory, Inference and Learning Algorithms*, Ch. 29 (Monte Carlo).
- Efron & Tibshirani (1986) — [Bootstrap methods for standard errors, confidence intervals, and other measures of statistical accuracy](https://projecteuclid.org/journals/statistical-science/volume-1/issue-1/Bootstrap-Methods-for-Standard-Errors-Confidence-Intervals-and-Other-Measures/10.1214/ss/1177013815.full).
- [SciPy `bootstrap` API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) (reference only — write your own loop for this exercise).

## Also see

- Site page: [exercises/ex1](../../../site/exercises/ex1.md)
- [Submissions](../../../site/submissions.md) — filename convention
- [Resources](../../../site/resources.md) — broader reading list
