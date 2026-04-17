# lib/ -- WP7 helper modules

Thin wrappers for multitaper spectral analysis, matching the conventions
in Anton Sirota's lecture series.  Students import these from exercise
notebooks via:

```python
import sys
sys.path.insert(0, '../../lib')
from wp7_helpers import psd_multitaper
```

## wp7_helpers.py

| Function | Exercise | Description |
|----------|----------|-------------|
| `psd_multitaper` | Ex 7 | Power spectral density via DPSS multitapers |
| `spectrogram_multitaper` | Ex 8 | Sliding-window multitaper spectrogram |
| `cross_spectrum` | Ex 9 | Multitaper cross-spectral density (complex) |
| `coherence` | Ex 9 | Magnitude-squared coherence in [0, 1] |

All functions accept plain NumPy arrays and return `(freqs, ...)` tuples.
The central parameter is `nw` (time-halfbandwidth product), which controls
the bias-variance trade-off of the Slepian tapers.

### Dependencies

- **Required:** numpy, scipy
- **Optional:** ghostipy (faster multitaper via pyfftw; falls back to scipy)
