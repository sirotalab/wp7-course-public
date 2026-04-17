# Exercise 3 — Modelling Neural Population Activity

## Topic

Population-level analysis of neural spiking data.  You will build firing-rate
matrices from spike trains, visualize population responses across trials and
stimuli, and analyse how information is distributed across neurons in a
population.

## Files in this directory

- `starter.py` — scaffolded Python script (from Mlynarski SS25 Exercise_03)
- `README.md` — this file

Note: this exercise uses a Python script rather than a Jupyter notebook.
Run it section-by-section in your IDE or convert to a notebook with
`jupytext --to notebook starter.py` if you prefer.

## Data

Population spiking data from the crcns_pvc8 dataset:

```
../../data/crcns_pvc8/
```

Same dataset as Ex1 (Bootstrap). See the starter script for loading instructions.

## Prerequisites

- **Lectures**: Mlynarski — Modelling neural population activity
- **Previous exercises**: Ex1 (bootstrap), Ex2 (encoding)
- **Packages**: `numpy`, `scipy`, `matplotlib`

## Tips

- Build a firing-rate matrix (neurons x time-bins) first — choose a bin width
  that balances temporal resolution against spike-count sparsity.
- Raster plots across trials for a single neuron, and across neurons for a
  single trial, reveal complementary structure.
- Think about trial-to-trial variability: how reliable is each neuron's response?

## Also see

- Site page: [exercises/ex3](../../site/docs/exercises/ex3.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
