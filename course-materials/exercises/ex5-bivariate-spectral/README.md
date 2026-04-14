# Exercise 5 — Bivariate Spectral Analysis

## Topic

Coherence quantifies the degree of phase-consistent coupling between two neural
signals as a function of frequency.  Unlike correlation (which integrates over
all frequencies), coherence is frequency-resolved and tells you *at which
oscillation frequency* two signals communicate.  You will compute magnitude-
squared coherence between pairs of LFP channels and interpret the results in
terms of hippocampal network coupling.  Understanding coherence is prerequisite
for modern analyses of inter-areal communication in systems neuroscience.

## Files in this directory

- `ex5.pdf` — the exercise prompt (authored by Anton Sirota)
- `starter.ipynb` — scaffolded notebook (TBD — pending Anton's 2025/2026 updates; see `planning/`)
- `README.md` — this file

## Data

16-channel hippocampal LFP recordings from the ds-wp7 dataset:

```
/storage2/arash/sirocampus/data/ds-wp7/ws_data_1shank.mat
```

Variable `lfps`, shape `(n_samples, 16)`, sampling rate **1250 Hz**.
(Same data as Ex3 and Ex4.)

```python
import scipy.io
lfps = scipy.io.loadmat('path/to/ws_data_1shank.mat')['lfps']
```

## Prerequisites

- **Lectures** (from `lectures/sirota/`):
  - `SpectralAnalysis_2_2023.pdf` — multitaper theory, cross-spectrum
  - `SpectralAnalysis_3_2023.pdf` — coherence definition and interpretation
- **Previous exercises**: Ex3 (univariate PSD) and Ex4 (spectrogram) — bivariate
  spectra build directly on the univariate methods you practiced there.
- **Packages**: `numpy`, `scipy`, `matplotlib`, `lib/wp7_helpers.py`
  (specifically `wp7_helpers.coherence` and `wp7_helpers.cross_spectrum`)

## Tips

- `wp7_helpers.coherence(x, y, fs, nperseg)` returns `(freqs, Cxy)` where
  `Cxy ∈ [0, 1]` by definition.  Values near 1 mean a stable phase relationship
  at that frequency; values near 0 mean independence.
- Coherence is **not** the same as correlation: two channels can be strongly
  correlated in the time domain but coherent only at a narrow band of frequencies.
- Always estimate a **null distribution** to assess significance: shuffle one
  signal in time (or use trial-shuffled coherence) to get a coherence baseline
  for uncoupled signals.  Observed coherence peaks should exceed that baseline.
- `wp7_helpers.cross_spectrum(x, y, fs, nperseg)` returns the complex CSD; its
  phase gives the average phase lag between the two channels at each frequency.
- Be careful about the segment length `nperseg`: too short → poor frequency
  resolution; too long → fewer independent segments → overconfident coherence
  estimates.

## Also see

- Site page: [exercises/ex5](../../site/docs/exercises/ex5.md)
- [Submissions](../../../site/docs/submissions.md) — filename convention
- `lib/wp7_helpers.py` — `coherence`, `cross_spectrum`, `psd_multitaper`
- `lib/mtcsd.py` — full multitaper cross-spectral density matrix (all pairs)
