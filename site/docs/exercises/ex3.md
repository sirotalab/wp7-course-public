# Exercise 3 — Modelling neural population activity

Analyse population-level spiking data: build firing-rate matrices, visualize responses across trials and stimuli, and explore how information is distributed across neurons.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex3-populations/` |
| **Data** | `crcns_pvc8/` (same dataset as Ex1) |
| **Packages** | numpy, scipy, matplotlib |
| **Helper module** | — |
| **Prereqs** | Mlynarski lecture on neural population activity |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex3 && cd ~/<slug>/ex3
cp /storage2/wp7/course-materials/exercises/ex3-populations/starter.py ex3_<slug>.py
```

Note: this exercise uses a Python script rather than a notebook. Run it section-by-section in your IDE, or convert with `jupytext --to notebook starter.py`.
