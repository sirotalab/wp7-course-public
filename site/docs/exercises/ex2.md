# Exercise 2 — Encoding in individual neurons

Build a linear–nonlinear encoding model for retinal ganglion cells. You'll compute spike-triggered averages, fit a Poisson GLM, and assess how well the model predicts neural responses to visual stimuli.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex2-encoding/` |
| **Data** | `data_RGCs/` (SpTimes.mat, Stim.mat, stimtimes.mat) |
| **Packages** | numpy, scipy, matplotlib |
| **Helper module** | — |
| **Prereqs** | Mlynarski lecture on encoding in individual neurons |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex2 && cd ~/<slug>/ex2
cp /storage2/wp7/course-materials/exercises/ex2-encoding/starter.ipynb ex2_<slug>.ipynb
```

Check the exercise `README.md` for data paths and tips.
