# WP7 course materials

Student-facing files for the WP7 Neural Data Analysis course
(MSc Neuroscience, LMU).

On HPC these live under `/storage2/wp7/course-materials/`. Off-HPC
they are available via `datalad clone` — see `site/docs/setup/workspace.md`
for the clone URL (once configured).

## Layout

```
course-materials/
├── environment.yml           # snapshot of the lab `wp7` conda env
├── lectures/
│   ├── sirota/               # Anton's lecture PDFs
│   └── mlynarski/            # Wiktor's lecture PDFs
├── exercises/
│   ├── ex1-bootstrap/
│   ├── ex2-encoding/
│   ├── ex3-populations/
│   ├── ex4-decoding/
│   ├── ex5-clustering/
│   ├── ex6-dimred/
│   ├── ex7-spectral-univariate/
│   ├── ex8-spectral-timeresolved/
│   └── ex9-bivariate-spectral/
├── notebooks/                # reference / exploratory notebooks
└── lib/                      # shared helper modules (wp7_helpers)
```
