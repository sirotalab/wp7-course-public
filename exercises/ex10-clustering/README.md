# Exercise 10 — Latent Variable Models & Clustering

## Topic

Unsupervised discovery of cell types and response classes using clustering
algorithms and latent-variable models.  You will apply K-means, hierarchical
clustering, and Gaussian mixture models to neural response data, evaluate
cluster quality, and relate discovered clusters to known cell-type labels.

## Files in this directory

- `starter.ipynb` — scaffolded notebook (from Mlynarski SS25 Exercise_05)
- `README.md` — this file

## Data

Chirp-response data:

```
../../data/clustering/chirp_response.npy           # (n_cells, n_timepoints) — 75 MB
../../data/clustering/chirp_response_quality.npy   # quality metrics
../../data/clustering/group_index.npy              # ground-truth group labels
```

Load with `numpy.load`.

## Prerequisites

- **Lectures**: Wiktor — Latent variable models (Lec 10)
- **Previous exercises**: Ex1–9 (full course background)
- **Packages**: `numpy`, `scipy`, `matplotlib`, `scikit-learn` (`KMeans`, `AgglomerativeClustering`, `GaussianMixture`)

## Tips

- Normalize response traces before clustering — different neurons have different
  baseline firing rates.
- The elbow method and silhouette scores help choose K, but don't over-interpret
  them — real neural data rarely has perfectly separated clusters.
- Compare your discovered clusters to the ground-truth `group_index` using the
  adjusted Rand index or mutual information.
- Hierarchical clustering dendrograms are useful for visualizing the
  relationships between clusters.

## Also see

- Site page: [exercises/ex10](../../../site/exercises/ex10.md)
- [Submissions](../../../site/submissions.md) — filename convention
