"""
Thin wrappers for multitaper spectral analysis — WP7 practicum.

Provides four functions matching the lecture conventions used in
Anton Sirota's *Machine Learning & Analysis of Neural Data* course:

- ``psd_multitaper``         — Ex 7  (univariate PSD)
- ``spectrogram_multitaper`` — Ex 8  (time-resolved spectrogram)
- ``cross_spectrum``         — Ex 9  (bivariate cross-spectral density)
- ``coherence``              — Ex 9  (magnitude-squared coherence)

All functions operate on plain NumPy arrays and return ``(freqs, ...)``
tuples.  The central parameter throughout is the *time-halfbandwidth
product* (``nw``), which governs the bias-variance trade-off of the
DPSS (Slepian) tapers.

Dependencies
------------
Required : numpy, scipy
Optional : ghostipy (faster multitaper via pyfftw; falls back to scipy)

Import pattern used in exercise starters::

    import sys
    sys.path.insert(0, '../../lib')
    from wp7_helpers import psd_multitaper

How the multitaper method works (for students)
----------------------------------------------
A standard periodogram computes |FFT(x)|^2 — one estimate, high variance.
The multitaper method reduces variance by multiplying the signal with K
orthogonal *Slepian* (DPSS) tapers, computing a periodogram for each,
and averaging.  The tapers are chosen to maximally concentrate spectral
energy within a bandwidth controlled by ``nw``.

The explicit steps (what this module does under the hood):

1. Generate K = 2*nw - 1 DPSS tapers of length N.
2. For each taper k:
   a. Multiply:   x_tapered[k] = x * taper[k]
   b. FFT:        X[k] = fft(x_tapered[k])
   c. Periodogram: P[k] = |X[k]|^2 / (fs * N)
3. Average:  PSD = mean(P[0], P[1], ..., P[K-1])

More tapers → lower variance but broader spectral peaks (more smoothing).
"""
from __future__ import annotations

import numpy as np
from scipy import signal as _signal

# ---------------------------------------------------------------------------
# Optional ghostipy import — falls back to scipy when absent
# ---------------------------------------------------------------------------
try:
    import ghostipy as _gsp

    _HAS_GHOSTIPY = True
except ImportError:
    _gsp = None  # type: ignore[assignment]
    _HAS_GHOSTIPY = False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _dpss_tapers(n: int, nw: float, ntapers: int | None = None) -> np.ndarray:
    """Compute DPSS (Slepian) tapers.

    Returns
    -------
    tapers : np.ndarray, shape (K, n)
        K orthogonal tapers, each of length n.
    """
    k = ntapers if ntapers is not None else int(2 * nw - 1)
    return _signal.windows.dpss(n, nw, Kmax=k)  # (K, n)


def _rfft_freqs(n: int, fs: float) -> np.ndarray:
    """One-sided frequency axis for a real signal of length n."""
    return np.fft.rfftfreq(n, d=1.0 / fs)


def _multitaper_psd_from_tapers(
    x: np.ndarray, tapers: np.ndarray, fs: float
) -> tuple[np.ndarray, np.ndarray]:
    """Core multitaper PSD: taper × FFT × average.

    This is the explicit version of what scipy.signal.periodogram(window=t)
    does internally, written out so students can see each step.

    Parameters
    ----------
    x : 1-D detrended signal
    tapers : (K, N) DPSS tapers
    fs : sampling rate

    Returns
    -------
    freqs : (n_freqs,)
    psd : (n_freqs,)
    """
    n = len(x)
    freqs = _rfft_freqs(n, fs)

    # Step 1: multiply signal by each taper, compute one-sided |FFT|^2
    #   x_tapered = x * taper[k]       — localise in frequency
    #   X_k       = rfft(x_tapered)     — transform to frequency domain
    #   P_k       = |X_k|^2 / (fs * N) — normalise to density (V^2/Hz)
    psds = np.empty((len(tapers), len(freqs)))
    for k, taper in enumerate(tapers):
        x_tapered = x * taper
        X_k = np.fft.rfft(x_tapered)
        P_k = (np.abs(X_k) ** 2) / (fs * n)
        # double the one-sided bins (except DC and Nyquist)
        P_k[1:-1] *= 2.0
        psds[k] = P_k

    # Step 2: average over tapers — this is the variance reduction
    return freqs, psds.mean(axis=0)


def _multitaper_csd_from_tapers(
    x: np.ndarray, y: np.ndarray, tapers: np.ndarray, fs: float
) -> tuple[np.ndarray, np.ndarray]:
    """Core multitaper cross-spectral density.

    Same logic as ``_multitaper_psd_from_tapers`` but computes
    conj(X) * Y instead of |X|^2.

    Parameters
    ----------
    x, y : 1-D detrended signals (same length)
    tapers : (K, N) DPSS tapers
    fs : sampling rate

    Returns
    -------
    freqs : (n_freqs,)
    csd : (n_freqs,), complex
    """
    n = len(x)
    freqs = _rfft_freqs(n, fs)

    csds = np.empty((len(tapers), len(freqs)), dtype=complex)
    for k, taper in enumerate(tapers):
        Xk = np.fft.rfft(x * taper)
        Yk = np.fft.rfft(y * taper)
        Ck = np.conj(Xk) * Yk / (fs * n)
        Ck[1:-1] *= 2.0
        csds[k] = Ck

    return freqs, csds.mean(axis=0)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def psd_multitaper(
    x: np.ndarray,
    fs: float,
    nperseg: int | None = None,
    nw: float = 3.0,
    ntapers: int | None = None,
    detrend: str = "constant",
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate the power spectral density with Slepian (DPSS) multitapers.

    Parameters
    ----------
    x : np.ndarray, shape (n_samples,)
        Input time series (1-D).
    fs : float
        Sampling frequency in Hz.
    nperseg : int or None
        Segment length in samples.  ``None`` uses the full signal length
        (recommended for a single-block multitaper estimate).
    nw : float
        Time-halfbandwidth product.  Controls the trade-off between spectral
        concentration and frequency resolution; typical values 2--4.
        Frequency resolution ~ ``2 * nw / (nperseg / fs)`` Hz.
    ntapers : int or None
        Number of DPSS tapers.  Defaults to ``2 * nw - 1`` (optimal choice).
    detrend : str
        Detrending applied before spectral estimation:
        ``"constant"`` (removes mean) or ``"linear"``.

    Returns
    -------
    freqs : np.ndarray, shape (n_freqs,)
        Frequency axis in Hz.
    psd : np.ndarray, shape (n_freqs,)
        One-sided power spectral density in signal_unit**2 / Hz.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> x = rng.standard_normal(1000)
    >>> freqs, psd = psd_multitaper(x, fs=1000.0, nw=4.0)
    >>> freqs[0], freqs[-1]
    (0.0, 500.0)
    """
    n_seg = len(x) if nperseg is None else min(nperseg, len(x))
    xd = _signal.detrend(x[:n_seg], type=detrend)

    if _HAS_GHOSTIPY:
        ntapers_k = ntapers if ntapers is not None else int(2 * nw - 1)
        bandwidth = 2.0 * nw * fs / n_seg
        psd, freqs = _gsp.mtm_spectrum(
            xd,
            bandwidth,
            fs=fs,
            n_tapers=ntapers_k,
            min_lambda=0.0,
            remove_mean=False,
        )
        return freqs, psd

    tapers = _dpss_tapers(n_seg, nw, ntapers)
    return _multitaper_psd_from_tapers(xd, tapers, fs)


def spectrogram_multitaper(
    x: np.ndarray,
    fs: float,
    window_sec: float,
    overlap: float = 0.5,
    nw: float = 3.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Time-resolved multitaper spectrogram via a sliding window.

    Slides a window of length ``window_sec`` across the signal and calls
    ``psd_multitaper`` on each segment.  The explicit loop makes the
    time–frequency resolution trade-off visible: shorter windows give
    finer time resolution but coarser frequency resolution, and vice versa.

    Parameters
    ----------
    x : np.ndarray, shape (n_samples,)
        Input time series (1-D).
    fs : float
        Sampling frequency in Hz.
    window_sec : float
        Analysis window duration in seconds.  Longer windows give finer
        frequency resolution but coarser time resolution.
    overlap : float
        Fractional overlap between consecutive windows (0--1).  Default 0.5.
    nw : float
        Time-halfbandwidth product passed to ``psd_multitaper``.

    Returns
    -------
    freqs : np.ndarray, shape (n_freqs,)
        Frequency axis in Hz.
    times : np.ndarray, shape (n_times,)
        Centre time of each window in seconds.
    S : np.ndarray, shape (n_freqs, n_times)
        Spectrogram power in signal_unit**2 / Hz.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.random.default_rng(0).standard_normal(10000)
    >>> freqs, times, S = spectrogram_multitaper(x, fs=1000.0, window_sec=0.5)
    >>> S.shape[0] == len(freqs) and S.shape[1] == len(times)
    True
    """
    nperseg = int(window_sec * fs)
    step = max(1, int(nperseg * (1.0 - overlap)))
    onsets = np.arange(0, len(x) - nperseg + 1, step)
    times = (onsets + nperseg / 2.0) / fs

    # Pre-compute tapers once — reused for every window
    tapers = _dpss_tapers(nperseg, nw)

    spectra = []
    for onset in onsets:
        seg = _signal.detrend(x[onset : onset + nperseg], type="constant")
        if _HAS_GHOSTIPY:
            _, psd = psd_multitaper(seg, fs=fs, nw=nw, detrend="constant")
        else:
            _, psd = _multitaper_psd_from_tapers(seg, tapers, fs)
        spectra.append(psd)

    freqs = _rfft_freqs(nperseg, fs)
    S = np.array(spectra).T  # (n_freqs, n_times)
    return freqs, times, S


def cross_spectrum(
    x: np.ndarray,
    y: np.ndarray,
    fs: float,
    nperseg: int,
    nw: float = 3.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Multitaper cross-spectral density between two signals.

    Segments the signals into overlapping blocks of length ``nperseg``
    (Welch-style), applies DPSS tapers to each block, and averages the
    cross-periodograms over both segments and tapers.

    Parameters
    ----------
    x : np.ndarray, shape (n_samples,)
        First time series.
    y : np.ndarray, shape (n_samples,)
        Second time series; same length as *x*.
    fs : float
        Sampling frequency in Hz.
    nperseg : int
        Segment length in samples.  Controls the frequency resolution
        and the number of independent segments used for averaging.
    nw : float
        Time-halfbandwidth product.

    Returns
    -------
    freqs : np.ndarray, shape (n_freqs,)
        Frequency axis in Hz.
    Pxy : np.ndarray, shape (n_freqs,), complex
        Complex cross-spectral density in signal_unit**2 / Hz.  The phase
        of ``Pxy`` encodes the phase lead of *x* over *y*.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> x, y = rng.standard_normal(2000), rng.standard_normal(2000)
    >>> freqs, Pxy = cross_spectrum(x, y, fs=1000.0, nperseg=500)
    >>> Pxy.dtype
    dtype('complex128')
    """
    tapers = _dpss_tapers(nperseg, nw)
    return _welch_mt_csd(x, y, tapers, fs, nperseg)


def coherence(
    x: np.ndarray,
    y: np.ndarray,
    fs: float,
    nperseg: int,
    nw: float = 3.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Magnitude-squared coherence between two signals.

    Computes::

        Cxy[f] = |Pxy[f]|^2 / (Pxx[f] * Pyy[f])

    where Pxy is the cross-spectral density and Pxx, Pyy are the
    auto-spectral densities.  All three are estimated with the same
    DPSS tapers and segment structure, ensuring consistency.

    Parameters
    ----------
    x : np.ndarray, shape (n_samples,)
        First time series (e.g., LFP channel 1).
    y : np.ndarray, shape (n_samples,)
        Second time series (e.g., LFP channel 2).
    fs : float
        Sampling frequency in Hz.
    nperseg : int
        Segment (window) length in samples.  Longer windows give more
        reliable estimates but lower temporal resolution.
    nw : float
        Time-halfbandwidth product.

    Returns
    -------
    freqs : np.ndarray, shape (n_freqs,)
        Frequency axis in Hz.
    Cxy : np.ndarray, shape (n_freqs,), real
        Magnitude-squared coherence in [0, 1].  Values near 1 indicate
        a stable phase relationship; values near 0 indicate independence.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> x, y = rng.standard_normal(2000), rng.standard_normal(2000)
    >>> freqs, Cxy = coherence(x, y, fs=1000.0, nperseg=500)
    >>> 0.0 <= Cxy.min() and Cxy.max() <= 1.0
    True
    """
    # Compute tapers once — shared across Pxy, Pxx, Pyy
    tapers = _dpss_tapers(nperseg, nw)

    freqs, Pxy = _welch_mt_csd(x, y, tapers, fs, nperseg)
    _, Pxx = _welch_mt_csd(x, x, tapers, fs, nperseg)
    _, Pyy = _welch_mt_csd(y, y, tapers, fs, nperseg)

    denom = np.clip(Pxx.real * Pyy.real, a_min=1e-30, a_max=None)
    Cxy = np.abs(Pxy) ** 2 / denom
    return freqs, np.clip(Cxy, 0.0, 1.0)


# ---------------------------------------------------------------------------
# Welch-style multitaper CSD (used by cross_spectrum and coherence)
# ---------------------------------------------------------------------------

def _welch_mt_csd(
    x: np.ndarray,
    y: np.ndarray,
    tapers: np.ndarray,
    fs: float,
    nperseg: int,
    overlap_frac: float = 0.5,
) -> tuple[np.ndarray, np.ndarray]:
    """Welch + multitaper CSD: segment → taper → FFT → average.

    Segments x and y into overlapping blocks, applies every DPSS taper
    to each block, and averages the cross-periodograms over all
    (segment, taper) pairs.

    This gives two independent sources of variance reduction:
    - **Segments** (Welch): more independent time blocks → lower variance
    - **Tapers** (multitaper): orthogonal spectral windows → lower variance

    Parameters
    ----------
    x, y : 1-D arrays, same length
    tapers : (K, nperseg) DPSS tapers
    fs : sampling rate
    nperseg : segment length
    overlap_frac : fractional overlap between segments (default 0.5)

    Returns
    -------
    freqs : (n_freqs,)
    csd : (n_freqs,), complex
    """
    step = max(1, int(nperseg * (1.0 - overlap_frac)))
    onsets = np.arange(0, len(x) - nperseg + 1, step)
    freqs = _rfft_freqs(nperseg, fs)
    n_freqs = len(freqs)

    csd_accum = np.zeros(n_freqs, dtype=complex)
    count = 0

    for onset in onsets:
        xseg = _signal.detrend(x[onset : onset + nperseg], type="constant")
        yseg = _signal.detrend(y[onset : onset + nperseg], type="constant")
        for taper in tapers:
            Xk = np.fft.rfft(xseg * taper)
            Yk = np.fft.rfft(yseg * taper)
            Ck = np.conj(Xk) * Yk / (fs * nperseg)
            Ck[1:-1] *= 2.0
            csd_accum += Ck
            count += 1

    return freqs, csd_accum / count
