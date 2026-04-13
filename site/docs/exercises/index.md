# Exercises

Five problem sets over the course. Each exercise is a self-contained
directory under `course-materials/exercises/` with:

- **`exN.pdf`** — the prompt
- **`starter.ipynb`** — a scaffolded notebook (no solutions)
- **`README.md`** — pointers to data, helpers, hints

| # | Topic | Directory |
|---|---|---|
| 1 | Bootstrap | `ex1-bootstrap/` |
| 2 | Dimensionality reduction | `ex2-dimred/` |
| 3 | Spectral analysis (univariate) | `ex3-spectral-univariate/` |
| 4 | Spectral analysis (time-resolved) | `ex4-spectral-timeresolved/` |
| 5 | Spectral analysis (bivariate) | `ex5-bivariate-spectral/` |

## How to work on an exercise

1. `conda activate wp7` — activate the course environment
2. Copy the starter notebook into your work area:
    ```bash
    cp /storage2/wp7/course-materials/exercises/ex1-bootstrap/starter.ipynb \
       /storage2/wp7/students/2026/ephys<NN>/<your-name>/ex1.ipynb
    ```
3. Open it in VS Code / Jupyter and work there
4. Submit following the [submissions](../submissions.md) instructions
