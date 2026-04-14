"""
Pedagogically thin wrappers over MNE-Python / scipy.signal for WP7 Ex3–5.

These wrappers present a small, stable API matching Anton Sirota's lecture
conventions, so students can concentrate on the neuroscience rather than
API surface details.  When *mne* is installed (recommended), ``psd_multitaper``
delegates to ``mne.time_frequency.psd_array_multitaper``.  All other functions
use ``scipy.signal`` with DPSS (Slepian) tapers and are fully transparent.

Intended for import in Ex3 (univariate PSD), Ex4 (spectrogram), Ex5 (coherence).

Install mne with::

    mamba install -c conda-forge mne   # or: pip install mne

See also ``lib/mtcsd.py`` for the full cross-spectral density matrix (all channel
pairs) used in advanced exercises.
"""
from __future__ import annotations

import warnings

import numpy as np
from scipy import signal as _signal

# ---------------------------------------------------------------------------
# Optional MNE import — graceful fallback to scipy.signal when absent
# ---------------------------------------------------------------------------
try:
    import mne as _mne
    _HAS_MNE = True
except ImportError:
    _mne = None  # type: ignore[assignment]
    _HAS_MNE = False
    warnings.warn(
        "mne is not installed; wp7_helpers.psd_multitaper falls back to "
        "scipy.signal with DPSS tapers.  "
        "Install with: mamba install -c conda-forge mne",
        FutureWarning,
        stacklevel=2,
    )


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
        concentration and frequency resolution; typical values 2–4.
        Frequency resolution ≈ ``2 * nw / (nperseg / fs)`` Hz.
    ntapers : int or None
        Number of DPSS tapers.  Defaults to ``2 * nw - 1`` (optimal choice).
    detrend : str
        Detrending applied before spectral estimation; passed to
        ``scipy.signal.detrend``.  Use ``"constant"`` (removes mean) or
        ``"linear"``.

    Returns
    -------
    freqs : np.ndarray, shape (n_freqs,)
        Frequency axis in Hz.
    psd : np.ndarray, shape (n_freqs,)
        One-sided power spectral density in signal_unit² / Hz.

    Notes
    -----
    Wraps ``mne.time_frequency.psd_array_multitaper`` (MNE ≥ 1.0) when mne is
    available — the most numerically stable multitaper implementation for
    neuroscience data.  Falls back to ``scipy.signal.windows.dpss`` +
    ``scipy.signal.periodogram`` averaged over K tapers.  Both paths produce
    equivalent estimates for the same nw/ntapers settings.
    """
    ntapers_k: int = ntapers if ntapers is not None else int(2 * nw - 1)
    n_seg: int = len(x) if nperseg is None else min(nperseg, len(x))

    if _HAS_MNE:
        # mne.time_frequency.psd_array_multitaper(x, sfreq, bandwidth, ...)
        # bandwidth = full frequency smoothing in Hz = 2 * nw / (n_seg / fs)
        bandwidth = 2.0 * nw / (n_seg / fs)
        result = _mne.time_frequency.psd_array_multitaper(
            x[:n_seg],
            sfreq=fs,
            fmin=0.0,
            fmax=fs / 2.0,
            bandwidth=bandwidth,
            low_bias=True,
            normalization="length",
            verbose=False,
        )
        psds, freqs = result[0], result[1]
        return freqs, np.atleast_1d(psds).squeeze()

    # scipy fallback: K DPSS tapers, average periodogram over tapers
    tapers = _signal.windows.dpss(n_seg, nw, Kmax=ntapers_k)  # (K, n_seg), unit-norm
    xd = _signal.detrend(x[:n_seg], type=detrend)
    # scipy.signal.periodogram with a unit-norm window gives correct density units
    psds_list = [
        _signal.periodogram(xd, fs=fs, window=t, scaling="density")[1] for t in tapers
    ]
    freqs, _ = _signal.periodogram(xd, fs=fs, window=tapers[0], scaling="density")
    return freqs, np.mean(psds_list, axis=0)


def spectrogram_multitaper(
    x: np.ndarray,
    fs: float,
    window_sec: float,
    overlap: float = 0.5,
    nw: float = 3.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Time-resolved multitaper spectrogram via a sliding window.

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
        Fractional overlap between consecutive windows (0–1).  Default 0.5.
    nw : float
        Time-halfbandwidth product passed to ``psd_multitaper``.

    Returns
    -------
    freqs : np.ndarray, shape (n_freqs,)
        Frequency axis in Hz.
    times : np.ndarray, shape (n_times,)
        Centre time of each window in seconds.
    S : np.ndarray, shape (n_freqs, n_times)
        Spectrogram power in signal_unit² / Hz.

    Notes
    -----
    Calls ``psd_multitaper`` on each sliding window.  No direct MNE equivalent
    exists for an array-based spectrogram (``mne.time_frequency.tfr_array_*``
    uses a different epoch-based API), so the sliding window is explicit here —
    which is useful for understanding the time–frequency trade-off.
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
        Complex cross-spectral density in signal_unit² / Hz.  The phase of
        ``Pxy`` encodes the phase lead of *x* over *y*.

    Notes
    -----
    Uses ``scipy.signal.csd`` with DPSS taper averaging — averages over the K
    Slepian tapers (same approach as ``mtcsd.py`` in ``lib/``).  No direct MNE
    equivalent exists for a simple array-based multitaper CSD.
    """
    ntapers_k: int = int(2 * nw - 1)
    tapers = _signal.windows.dpss(nperseg, nw, Kmax=ntapers_k)  # (K, nperseg), unit-norm
    # Average CSD over K tapers; each taper is passed as a custom window
    csds = [
        _signal.csd(x, y, fs=fs, nperseg=nperseg, window=t, scaling="density")[1]
        for t in tapers
    ]
    freqs, _ = _signal.csd(x, y, fs=fs, nperseg=nperseg, window=tapers[0], scaling="density")
    return freqs, np.mean(csds, axis=0)


def coherence(
    x: np.ndarray,
    y: np.ndarray,
    fs: float,
    nperseg: int,
    nw: float = 3.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Magnitude-squared coherence between two signals.

    Parameters
    ----------
    x : np.ndarray, shape (n_samples,)
        First time series (e.g., LFP channel 1).
    y : np.ndarray, shape (n_samples,)
        Second time series (e.g., LFP channel 2 or a spike-train proxy).
    fs : float
        Sampling frequency in Hz.
    nperseg : int
        Segment (window) length in samples.  Coherence ∈ [0, 1] by definition;
        longer windows give more reliable estimates but lower temporal resolution.
    nw : float
        Time-halfbandwidth product passed to ``cross_spectrum``.

    Returns
    -------
    freqs : np.ndarray, shape (n_freqs,)
        Frequency axis in Hz.
    Cxy : np.ndarray, shape (n_freqs,), real
        Magnitude-squared coherence ∈ [0, 1].  Values near 1 indicate a stable
        phase relationship at that frequency; values near 0 indicate independence.

    Notes
    -----
    Builds on ``cross_spectrum`` as the building block:
    ``Cxy[f] = |Pxy[f]|² / (Pxx[f] · Pyy[f])``
    where ``Pxx`` and ``Pyy`` are the auto-spectra (real-valued).
    No direct MNE array-based equivalent; ``mne.connectivity`` operates on
    Epochs objects rather than raw arrays.
    """
    freqs, Pxy = cross_spectrum(x, y, fs, nperseg, nw)
    _, Pxx = cross_spectrum(x, x, fs, nperseg, nw)
    _, Pyy = cross_spectrum(y, y, fs, nperseg, nw)
    # Auto-spectra are real-valued; clip denominator to avoid divide-by-zero
    denom = np.clip(Pxx.real * Pyy.real, a_min=1e-30, a_max=None)
    Cxy = np.abs(Pxy) ** 2 / denom
    return freqs, np.clip(Cxy, 0.0, 1.0)
