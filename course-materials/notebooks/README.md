# Reference Notebooks

Supplementary worked examples and theory exposition for the WP7 practicum.
These are **not** exercise solutions — they are standalone learning material
that complements the exercise starters.

| Notebook | Topic | Prerequisites |
|----------|-------|---------------|
| `multitaper_spectral_analysis.ipynb` | Periodogram, Welch, multitaper PSD, NW trade-off, filtering, depth-wise spectra | Lectures SA-1, SA-2 |
| `coherence_and_cross_spectra.ipynb` | Cross-spectral density, coherency, laminar coherence, spike–LFP coupling, circular statistics | Lectures SA-2, SA-3; Ex7–8 |

## Running

All notebooks run in the `wp7` environment with zero additional dependencies
beyond what the exercises require (`numpy`, `scipy`, `matplotlib`,
`wp7_helpers` from `../lib/`).

```bash
# Execute a notebook (from this directory)
jupyter nbconvert --execute multitaper_spectral_analysis.ipynb --to notebook
```

## Data

Both notebooks use the same hippocampal LFP dataset as Exercises 7–9:

```
/storage2/arash/sirocampus/data/ds-wp7/ws_data_1shank.mat   (16-ch LFP, 1250 Hz)
/storage2/arash/sirocampus/data/ds-wp7/spikes.mat            (spike times + cluster IDs)
```
