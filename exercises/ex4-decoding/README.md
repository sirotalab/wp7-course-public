# Exercise 4 — Decoding neural activity

## Topic

Decode which stimulus the animal was looking at from V1 population
spiking activity. You'll build a Maximum-Likelihood decoder under
independence across neurons using two different feature representations
of the same data — spike counts and time-to-first-spike — and compare
their performance. The contrast tells you what aspect of the neural
code each feature captures.

## Style

**Open-ended.** Wiktor's starter is two paragraphs of problem
description and one empty code cell. You build the train/test split,
fit the likelihood per-neuron-per-image, implement the ML decoder, and
report accuracy yourself — no scaffold beyond the recipe.

## Files in this directory

- `starter.ipynb` — Wiktor's open-ended prompt (Mlynarski, 2026).
- `README.md` — this file.

Create your working copy with `pixi run start ex4` (produces `ex4.ipynb`).
Edit that, not `starter.ipynb`.

## Data

Same CRCNS PVC-8 dataset as Ex1 and Ex3 — V1 spike-train recordings
from Adam Kohn's lab:

    ../../data/crcns_pvc8/1.mat

`resp_train` has shape `(n_cells, n_images, n_trials, n_tp)` with 1 ms
bins. Load with `scipy.io.loadmat`.

## Prerequisites

- **Lectures:** Mlynarski — Lec 04 (decoding)
- **Previous exercises:** Ex2 (encoding) + Ex3 (population activity)
- **Packages:** `numpy`, `scipy`, `matplotlib`

## Reading (optional — pick what helps)

- Quian Quiroga & Panzeri (2009) — [Extracting information from neuronal populations: information theory and decoding approaches](https://www.nature.com/articles/nrn2578) (Nat Rev Neurosci).
- Murphy — *Machine Learning: A Probabilistic Approach*, §3.5 (naive Bayes).

## Submit

```bash
pixi run submit ex4
```

See the course site's [Submissions](../../../../website/docs/submissions.md) page for the contract.
