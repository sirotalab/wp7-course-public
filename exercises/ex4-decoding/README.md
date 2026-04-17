# Exercise 4 — Decoding Neural Activity

## Topic

Neural decoding: reconstructing stimulus identity or behavioural variables from
population spiking activity.  You will implement Bayesian and linear decoders,
evaluate their performance with cross-validation, and explore how decoding
accuracy depends on population size and temporal resolution.

## Files in this directory

- `starter.ipynb` — scaffolded notebook (from Mlynarski SS25 Exercise_04)
- `README.md` — this file

## Data

Population spiking data from the crcns_pvc8 dataset:

```
../../data/crcns_pvc8/
```

Same dataset as Ex1 (Bootstrap) and Ex3 (Populations).

## Prerequisites

- **Lectures**: Mlynarski — Decoding neural activity
- **Previous exercises**: Ex1 (bootstrap), Ex2 (encoding), Ex3 (populations)
- **Packages**: `numpy`, `scipy`, `matplotlib`, `scikit-learn`

## Tips

- Start with a simple maximum-likelihood decoder before moving to more complex
  approaches.
- Cross-validation is essential — always report test-set accuracy, not
  training-set accuracy.
- Confusion matrices reveal which stimuli are easily decoded and which are
  confused with each other.
- Try varying the number of neurons in your decoder to see how population size
  affects performance.

## Also see

- Site page: [exercises/ex4](../../site/docs/exercises/ex4.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
