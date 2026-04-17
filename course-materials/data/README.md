# Exercise datasets

All data files for the WP7 exercises, tracked via git-annex.

On the HPC these are already present. If you cloned with DataLad, run
`datalad get data/` to fetch the actual file contents.

| Directory | Contents | Size | Used by |
|-----------|----------|------|---------|
| `crcns_pvc8/` | V1 population spiking (10 sessions) | 305 MB | Ex1, Ex3, Ex4 |
| `data_RGCs/` | Retinal ganglion cell recordings | 1.7 MB | Ex2 |
| `clustering/` | Chirp responses + ground-truth labels | 72 MB | Ex5 |
| `spectral/` | Hippocampal LFP + spike waveforms | 49 MB | Ex6, Ex7, Ex8, Ex9 |

## Loading

```python
import scipy.io
import numpy as np

# .mat files (Ex1-4, Ex6-9)
data = scipy.io.loadmat('../data/crcns_pvc8/1.mat')

# .npy files (Ex5)
chirp = np.load('../data/clustering/chirp_response.npy')
```

From an exercise notebook, data is at `../data/<dataset>/`.
