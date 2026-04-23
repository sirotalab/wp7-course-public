# Exercise 1 — Bootstrap

## Topic

Resampling-based hypothesis testing without parametric assumptions. You will
apply the bootstrap to V1 spike-train data and test hypotheses about temporal
structure, correlations, or rate modulations that you propose yourself. The
bootstrap is one of the most broadly applicable tools in quantitative
neuroscience — it attaches uncertainty bounds to almost any statistic, even
when no analytic null exists.

## Style

**Open-ended.** The starter gives you a dataset and a procedural recipe
(state hypothesis → pick test statistic → build null by shuffling → compare).
You decide which hypothesis to test, which statistic to compute, and which
shuffling scheme destroys the structure you're probing. Extra credit for
creative hypotheses. No autograder.

## Files in this directory

- `starter.ipynb` — Wiktor's open-ended prompt (Młynarski, 2026).
- `README.md` — this file.

Create your working copy with `pixi run start ex1` (produces `ex1.ipynb`).
Edit that, not `starter.ipynb`.

## Data

Single-unit recordings from V1 (primary visual cortex),
[CRCNS PVC-8](https://crcns.org/data-sets/vc/pvc-8):

    ../../data/crcns_pvc8/1.mat

The `.mat` file contains `resp_train`, a 4-D binary array of shape
`(n_cells, n_images, n_trials, n_tp)`. Load with `scipy.io.loadmat`.

## Prerequisites

- **Lectures:** Młynarski — Introduction & nonparametric testing (Lec 01)
- **Previous exercises:** none — Ex1 is the entry point.
- **Packages:** `numpy`, `scipy`, `matplotlib`

## Reading (optional — pick what helps)

- Murphy — *Machine Learning: A Probabilistic Approach*, §4.1–4.3, §6.5 (bootstrap).
- MacKay — *Information Theory, Inference and Learning Algorithms*, Ch. 29 (Monte Carlo).
- Efron & Tibshirani (1986) — [Bootstrap methods for standard errors, confidence intervals, and other measures of statistical accuracy](https://projecteuclid.org/journals/statistical-science/volume-1/issue-1/Bootstrap-Methods-for-Standard-Errors-Confidence-Intervals-and-Other-Measures/10.1214/ss/1177013815.full).
- [SciPy `bootstrap` API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) — reference only; write your own loop for this exercise.

## Submit

```bash
pixi run submit ex1
```

See the course site's [Submissions](../../../../website/docs/submissions.md) page for the full contract.
