# Exercise 5 — Unsupervised structure discovery: clustering

Apply K-means, hierarchical clustering, and mixture models to neural response data. You'll discover cell types from chirp responses and evaluate cluster quality against ground-truth labels.

## At a glance

| | |
|---|---|
| **Directory** | `course-materials/exercises/ex5-clustering/` |
| **Data** | `chirp_response.npy` (75 MB), `chirp_response_quality.npy`, `group_index.npy` |
| **Packages** | numpy, scipy, matplotlib, scikit-learn (`KMeans`, `AgglomerativeClustering`, `GaussianMixture`) |
| **Helper module** | — |
| **Prereqs** | Mlynarski lecture on clustering and latent variable models |
| **Deadline** | TBD — see [Schedule](../schedule.md) |

## First steps

```bash
conda activate wp7
mkdir -p ~/<slug>/ex5 && cd ~/<slug>/ex5
cp /storage2/wp7/course-materials/exercises/ex5-clustering/starter.ipynb ex5_<slug>.ipynb
```

Check the exercise `README.md` for data paths and tips.
