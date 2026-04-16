# Exercise 2 — Encoding in Individual Neurons

## Topic

Single-neuron encoding models: how individual retinal ganglion cells (RGCs)
represent visual stimuli.  You will build a linear–nonlinear (LN) model that
predicts spike rates from the stimulus, estimate the spike-triggered average
(STA), and assess model quality using cross-validated predictions.

## Files in this directory

- `starter.ipynb` — scaffolded notebook (from Mlynarski SS25 Exercise_02)
- `README.md` — this file

## Data

Retinal ganglion cell recordings in `data_RGCs/`:

```
sourcedata/data/crcns_pvc8/data_RGCs/SpTimes.mat    # spike times
sourcedata/data/crcns_pvc8/data_RGCs/Stim.mat        # stimulus frames
sourcedata/data/crcns_pvc8/data_RGCs/stimtimes.mat   # stimulus timing
```

Load with `scipy.io.loadmat`.

## Prerequisites

- **Lectures**: Mlynarski — Encoding in individual neurons
- **Previous exercises**: Ex1 (bootstrap) — statistical testing background
- **Packages**: `numpy`, `scipy`, `matplotlib`

## Tips

- The spike-triggered average (STA) is a simple but powerful first model of
  neuronal selectivity — it tells you what the neuron "likes" to see.
- Cross-validate your LN model: fit on one half of the data, predict on the other.
- Compare Poisson GLM predictions with simple STA-based estimates.

## Also see

- Site page: [exercises/ex2](../../site/docs/exercises/ex2.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
