# Exercise 3 — Univariate Spectral Analysis

## Topic

Power spectral density (PSD) estimation from local field potential (LFP)
recordings.  LFP oscillations (theta ~8 Hz, gamma ~60–90 Hz, etc.) are
cardinal signatures of hippocampal network states.  You will learn how to
estimate the PSD using multitaper methods, understand the trade-off between
frequency resolution and spectral leakage, and compare different estimation
approaches (Welch, multitaper).

## Files in this directory

- `ex3.pdf` — the exercise prompt (authored by Anton Sirota)
- `starter.ipynb` — scaffolded notebook (TBD — pending Anton's 2025/2026 updates; see `planning/`)
- `README.md` — this file

## Data

16-channel hippocampal LFP recordings from the ds-wp7 dataset:

```
/storage2/arash/sirocampus/data/ds-wp7/ws_data_1shank.mat
```

The `.mat` file contains variable `lfps`, a matrix of shape
`(n_samples, 16)` recorded at **1250 Hz**.  Load with:

```python
import scipy.io
lfps = scipy.io.loadmat('path/to/ws_data_1shank.mat')['lfps']  # (n_samples, 16)
```

## Prerequisites

- **Lectures** (from `lectures/sirota/`):
  - `SpectralAnalysis_1_2023.pdf` — Fourier basics, periodogram, Welch
  - `SpectralAnalysis_2_2023.pdf` — multitaper theory, DPSS tapers
- **Previous exercises**: Ex1–2 (statistical thinking and data handling)
- **Packages**: `numpy`, `scipy`, `matplotlib`, and `lib/wp7_helpers.py`
  (specifically `wp7_helpers.psd_multitaper`).
  If `mne` is not yet installed, `wp7_helpers` falls back to `scipy.signal`
  automatically — see `lib/wp7_helpers.py` module docstring.

## Tips

- Always detrend your LFP segment before computing the PSD (remove the mean
  at minimum; `detrend="constant"` in `psd_multitaper`).
- The number of tapers `K = 2·NW − 1` controls variance reduction:
  more tapers → lower variance but wider spectral peaks.  Try NW = 2, 3, 4 and
  compare the resulting spectra.
- Plot PSD on a log–log or log-linear scale; hippocampal LFP has a 1/f
  background with oscillatory bumps on top.
- `wp7_helpers.psd_multitaper(lfp_channel, fs=1250)` returns `(freqs, psd)` —
  note the order (freqs first).
- Compare your multitaper PSD with `scipy.signal.welch` on the same data to
  see the difference in spectral smoothing.

## Also see

- Site page: [exercises/ex3](../../site/docs/exercises/ex3.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
- `lib/mtcsd.py` — full multitaper cross-spectral density matrix (all channel pairs)
- `lib/wp7_helpers.py` — thin wrappers used in Ex3–5
