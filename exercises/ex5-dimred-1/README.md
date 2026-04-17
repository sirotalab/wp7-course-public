# Exercise 5 — Dimensionality Reduction 1 (Spike Waveforms)

## Topic

Linear dimensionality reduction applied to multichannel spike waveforms.
You will apply PCA per-channel and in full space, cluster spike types with
Gaussian Mixture Models, and compare with ICA.

## Files in this directory

- `ex5.pdf` — exercise prompt (authored by Anton Sirota)
- `starter.ipynb` — scaffolded Neuromatch-style notebook
- `README.md` — this file

## Data

Multichannel spike waveforms from a silicon probe recording:

```
../../data/spectral/spike_waveshapes.mat
```

Load with `scipy.io.loadmat`. The variable `spk` has shape `(n_spikes, n_channels, n_samples)`.

## Prerequisites

- **Lectures**: Anton — Dimensionality Reduction 1 (Lec 05)
- **Previous exercises**: Ex1–4 (basic handling of neural data)
- **Packages**: `numpy`, `scipy`, `matplotlib`, `scikit-learn` (`PCA`, `FastICA`, `GaussianMixture`)

## Tips

- **Centre before PCA** — PCA finds directions of maximum variance around the mean; uncentered data conflates mean and variance.
- **Eigenspectrum** tells you the intrinsic dimensionality — look for elbows.
- **BIC** penalises complex models; lowest BIC ≈ best GMM fit without overfitting.
- **Full-space PCA** (`n_spikes × (n_ch × n_samples)`) captures joint channel+time structure; per-channel PCA loses cross-channel correlations.

## Also see

- Site page: [exercises/ex5](../../../site/exercises/ex5.md)
- [Submissions](../../../site/submissions.md)
- Continues in Ex6 (LFP Blind Source Separation)
