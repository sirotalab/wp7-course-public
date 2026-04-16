"""
Thin wrappers for multitaper spectral analysis — WP7 practicum.

Provides four functions matching the lecture conventions used in
Anton Sirota's *Machine Learning & Analysis of Neural Data* course:

- ``psd_multitaper``         — Ex 3  (univariate PSD)
- ``spectrogram_multitaper`` — Ex 4  (time-resolved spectrogram)
- ``cross_spectrum``         — Ex 5  (bivariate cross-spectral density)
- ``coherence``              — Ex 5  (magnitude-squared coherence)

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
    ntapers_k: int = ntapers if ntapers is not None else int(2 * nw - 1)
    n_seg: int = len(x) if nperseg is None else min(nperseg, len(x))
    xd = _signal.detrend(x[:n_seg], type=detrend)

    if _HAS_GHOSTIPY:
        # ghostipy uses bandwidth in Hz: bw = 2 * nw * fs / n_seg
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

    # scipy fallback: K DPSS tapers, average periodogram over tapers
    tapers = _signal.windows.dpss(n_seg, nw, Kmax=ntapers_k)  # (K, n_seg)
    psds = [
        _signal.periodogram(xd, fs=fs, window=t, scaling="density")[1]
        for t in tapers
    ]
    freqs = _signal.periodogram(xd, fs=fs, window=tapers[0], scaling="density")[0]
    return freqs, np.mean(psds, axis=0)


def spectrogram_multitaper(
    x: np.ndarray,
    fs: float,
    window_sec: float,
    overlap: float = 0.5,
    nw: float = 3.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Time-resolved multitaper spectrogram via a sliding window.

    Calls ``psd_multitaper`` on each sliding window.  This explicit loop
    is useful for understanding the time-frequency resolution trade-off.

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
    nperseg: int = int(window_sec * fs)
    step: int = max(1, int(nperseg * (1.0 - overlap)))
    onsets = np.arange(0, len(x) - nperseg + 1, step)
    times = (onsets + nperseg / 2.0) / fs

    spectra = []
    for onset in onsets:
        seg = x[onset : onset + nperseg]
        freqs, psd = psd_multitaper(seg, fs=fs, nw=nw)
        spectra.append(psd)

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

    Uses ``scipy.signal.csd`` with DPSS taper averaging: the CSD is
    computed for each Slepian taper and averaged over K tapers.

    Parameters
    ----------
    x : np.ndarray, shape (n_samples,)
        First time series.
    y : np.ndarray, shape (n_samples,)
        Second time series; same length as *x*.
    fs : float
        Sampling frequency in Hz.
    nperseg : int
        Segment length in samples; also the taper length.
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
    ntapers_k: int = int(2 * nw - 1)
    tapers = _signal.windows.dpss(nperseg, nw, Kmax=ntapers_k)
    csds = [
        _signal.csd(x, y, fs=fs, nperseg=nperseg, window=t, scaling="density")[1]
        for t in tapers
    ]
    freqs, _ = _signal.csd(
        x, y, fs=fs, nperseg=nperseg, window=tapers[0], scaling="density"
    )
    return freqs, np.mean(csds, axis=0)


def coherence(
    x: np.ndarray,
    y: np.ndarray,
    fs: float,
    nperseg: int,
    nw: float = 3.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Magnitude-squared coherence between two signals.

    Builds on ``cross_spectrum``::

        Cxy[f] = |Pxy[f]|**2 / (Pxx[f] * Pyy[f])

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
        Time-halfbandwidth product passed to ``cross_spectrum``.

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
    freqs, Pxy = cross_spectrum(x, y, fs, nperseg, nw)
    _, Pxx = cross_spectrum(x, x, fs, nperseg, nw)
    _, Pyy = cross_spectrum(y, y, fs, nperseg, nw)
    denom = np.clip(Pxx.real * Pyy.real, a_min=1e-30, a_max=None)
    Cxy = np.abs(Pxy) ** 2 / denom
    return freqs, np.clip(Cxy, 0.0, 1.0)
