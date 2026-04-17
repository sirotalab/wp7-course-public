# WP7 course materials (2026)

Student-facing files for the WP7 Neural Data Analysis course
(MSc Neuroscience, LMU).

This dataset is installed into each student's HPC workspace as a
DataLad subdataset. Students see it at `~/<slug>/course-materials/`.

## Layout

```
course-materials/
├── environment.yml           # snapshot of the lab `wp7` conda env
├── data/                     # exercise datasets (annexed)
│   ├── crcns_pvc8/           #   V1 spiking — Ex1, Ex3, Ex4
│   ├── data_RGCs/            #   RGC recordings — Ex2
│   ├── spectral/             #   LFP + spike waveshapes — Ex5, Ex6, Ex7, Ex8, Ex9
│   └── clustering/           #   Chirp responses — Ex10
├── lectures/
│   ├── mlynarski/            # Lec 01–05 + Lec 10 (Wiktor)
│   └── sirota/               # Lec 06–09 + 2023 reference PDFs (Anton)
├── exercises/
│   ├── ex1-bootstrap/        # Nonparametric tests
│   ├── ex2-encoding/         # Encoding in single neurons
│   ├── ex3-populations/      # Population activity
│   ├── ex4-decoding/         # Decoding analyses
│   ├── ex5-dimred-1/         # PCA on spike waveforms
│   ├── ex6-dimred-2/         # LFP BSS + nonlinear DR
│   ├── ex7-spectral-univariate/    # Time series analysis 1
│   ├── ex8-spectral-timeresolved/  # Time series analysis 2
│   ├── ex9-bivariate-spectral/     # Time series analysis 3
│   └── ex10-clustering/      # Latent variable models
├── notebooks/                # reference / exploratory notebooks
└── lib/                      # shared helper modules (wp7_helpers)
```
