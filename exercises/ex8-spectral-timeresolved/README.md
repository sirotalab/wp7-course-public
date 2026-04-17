# Exercise 8 — Time-Resolved Spectral Analysis

## Topic

Multitaper spectrograms reveal how neural oscillation power evolves over time.
Unlike a single PSD estimate (Ex7), a spectrogram slides a short analysis window
across the recording and computes the PSD of each window, producing a
time–frequency representation.  You will learn how window length and overlap
govern the time–frequency resolution trade-off, and apply spectrogram analysis
to detect transient oscillatory events (e.g., hippocampal sharp-wave ripples or
theta bursts) in LFP data.

## Files in this directory

- `ex8.pdf` — the exercise prompt (authored by Anton Sirota)
- `starter.ipynb` — scaffolded notebook (TBD — pending Anton's 2025/2026 updates; see `planning/`)
- `README.md` — this file

## Data

16-channel hippocampal LFP recordings from the ds-wp7 dataset:

```
../../data/spectral/ws_data_1shank.mat
```

Variable `lfps`, shape `(n_samples, 16)`, sampling rate **1250 Hz**.
(Same data as Ex7.)

```python
import scipy.io
lfps = scipy.io.loadmat('../../data/spectral/ws_data_1shank.mat')['lfps']
```

## Prerequisites

- **Lectures** (from `lectures/sirota/`):
  - `SpectralAnalysis_1_2023.pdf` — Fourier and Welch basics
  - `SpectralAnalysis_2_2023.pdf` — multitaper theory
  - `SpectralAnalysis_3_2023.pdf` — time-resolved spectral analysis
- **Previous exercises**: Ex7 (univariate PSD) — Ex8 extends Ex7 to the
  time-resolved case; make sure you understand `psd_multitaper` first.
- **Packages**: `numpy`, `scipy`, `matplotlib`, `lib/wp7_helpers.py`
  (specifically `wp7_helpers.spectrogram_multitaper`)

## Tips

- `wp7_helpers.spectrogram_multitaper(x, fs, window_sec, overlap)` returns
  `(freqs, times, S)` where `S` has shape `(n_freqs, n_times)` — ready to plot
  with `plt.pcolormesh(times, freqs, S)`.
- Window length is the fundamental trade-off: shorter windows (e.g., 0.2 s) give
  fine time resolution but blurry frequency resolution; longer windows (1–2 s)
  resolve individual oscillatory frequencies but smear transient events.
- Visualise the spectrogram on a log power scale (`np.log10(S)` or `10 * np.log10(S)`)
  to compress the dynamic range.
- Theta (~8 Hz) and ripple (~150 Hz) bands should be visible as horizontal
  bands of elevated power; their temporal modulation is the story.
- For display, limit the frequency axis to a relevant range (e.g., 1–200 Hz)
  and the color scale to avoid a few high-power bins dominating the colormap.

## Also see

- Site page: [exercises/ex8](../../site/docs/exercises/ex8.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
- `lib/wp7_helpers.py` — `spectrogram_multitaper` and `psd_multitaper`
