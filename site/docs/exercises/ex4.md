# Exercise 4 — Decoding neural activity

Reconstruct stimulus identity from population spiking activity. You'll implement Bayesian and linear decoders, evaluate with cross-validation, and explore how decoding accuracy depends on population size.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex4-decoding/` |
| **Data** | `crcns_pvc8/` (same dataset as Ex1 and Ex3) |
| **Packages** | numpy, scipy, matplotlib, scikit-learn |
| **Helper module** | — |
| **Prereqs** | Mlynarski lecture on decoding; Ex2 and Ex3 recommended |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex4 && cd ~/<slug>/ex4
cp /storage2/wp7/course-materials/exercises/ex4-decoding/starter.ipynb ex4_<slug>.ipynb
```

Check the exercise `README.md` for data paths and tips.
