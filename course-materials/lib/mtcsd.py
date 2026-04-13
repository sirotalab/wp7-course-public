import numpy as np
from scipy import fft
from scipy.signal import windows, detrend

def mtcsd(x, fs=1, nperseg=256, nfft=None, noverlap=None, nw=3, ntapers=None, detrend_method='constant', progress_report=False):
    """
    Compute the pair-wise cross-spectral density for all channels in an array using Slepian tapers. Adapted from
    the mtcsd function in the labbox Matlab toolbox (authors: Partha Mitra, Ken Harris).
    
    Parameters
    ----------
    x : ndarray
        2D array of signals across which to compute CSD, columns should correspond to channels
    fs : float (default = 1)
        sampling frequency
    nperseg : int, None (default = None)
        number of data points per segment, if None nperseg is set to 256
    nfft : int, None (default = None)
        number of points to include in scipy.fft.fft, if None nfft is set to 2 * nperseg, if nfft > nperseg data 
        will be zero-padded
    noverlap : int, None (default = None)
        amout of overlap between consecutive segments, if None noverlap is set to nperseg / 2
    nw : int (default = 3)
        time-frequency bandwidth for Slepian tapers, passed on to scipy.signal.windows.dpss
    ntapers : int, None (default = None)
        number of tapers, passed on to scipy.signal.windows.dpss, if None ntapers is set to nw * 2 - 1 (as 
        suggested by original authors)
    detrend_method : {'constant', 'linear'} (default = 'constant')
        method used by scipy.signal.detrend to detrend each segment
        
    Returns
    -------
    f : ndarray
        frequency bins
    csd : ndarray
        full cross-spectral density matrix
    """
    
    assert x.ndim == 2, "Data array must be 2D"
    
    # set some default for parameters values     
    if nfft is None:
        nfft = nperseg * 2
    
    if noverlap is None:
        noverlap = nperseg / 2
        
    if ntapers is None:
        ntapers = 2 * nw - 1
        
    stepsize = nperseg - noverlap
    nsegs = int(np.floor(len(x) / stepsize))

    fftnorm = np.sqrt(2 / nfft) # value taken from original matlab function
    csdnorm = ntapers * nsegs
    
    # initialize csd matrix
    csd = np.zeros((x.shape[1], x.shape[1], nfft), dtype='complex128')
    
    # get FFT frequency bins
    f = fft.fftfreq(nfft, 1/fs)
    
    # get tapers
    tapers = windows.dpss(nperseg, nw, Kmax=ntapers)

    # loop over segments
    for seg_ind in range(nsegs):
        # report for-loop progress  
        if progress_report:
            print('%d'%(100*(seg_ind+1)/nsegs)+'%', end='\r')

        # prepare segment
        i0 = int(seg_ind * stepsize)
        i1 = int(seg_ind * stepsize + nperseg)
        if i1 > len(x): # stop if segment is out of range of data
            break
        seg = x[i0:i1, :]
        seg = detrend(seg, type=detrend_method, axis=0)
    
        # apply tapers
        tapered_seg = np.full((len(tapers), seg.shape[0], seg.shape[1]), np.nan)
        for taper_ind, taper in enumerate(tapers):
            tapered_seg[taper_ind] = (seg.T * taper).T    
        
        # compute FFT for each channel-taper combination
        pxx = fft.fft(tapered_seg, n=nfft, axis=1) / fftnorm
        
        # fill upper triangle of csd matrix by averaging values over all tapers and segments
        # normalization factor takes care of the number of tapers and segments
        for ch1 in range(x.shape[-1]): # loop over all unique channel combinations
            for ch2 in range(ch1, x.shape[-1]):
                # compute csd bewteen channels, sum over tapers, normalize
                csd[ch1, ch2, :] += (pxx[:, :, ch1] * np.conjugate(pxx[:, :, ch2])).sum(axis=0) / csdnorm
                
    # fill lower triangle of csd matrix with complex conjugate of upper triangle
    for ch1 in range(x.shape[-1]):
        for ch2 in range(ch1 + 1, x.shape[-1]):
            csd[ch2, ch1, :] = np.conjugate(csd[ch1, ch2, :])
    
    return f, csd
    
