# HPC workspace

Everything course-related lives under `/storage2/wp7/` on the HPC.

## Read-only: course materials

```
/storage2/wp7/course-materials/
├── environment.yml           # conda env spec
├── lectures/                 # lecture slide PDFs
├── exercises/                # problem sets (prompts + starter notebooks)
├── notebooks/                # reference/exploratory notebooks
└── lib/                      # shared helper modules
```

This directory is read-only. You should never need to write there — copy
any file you want to modify into your own work area first.

## Your work area

You work under a per-student subdirectory inside your pooled login:

```
/storage2/wp7/students/2026/ephys<NN>/<your-name>/
```

**Why per-student subdirs?** Multiple students share each `ephysNN` pooled
account, so filesystem ownership does not identify you. The
`<your-name>/` subdir is the convention that keeps your work separate
from your roommate's.

**Don't touch other people's directories.** Even though permissions may
allow it, treat `/storage2/wp7/students/2026/ephys<NN>/<someone-else>/`
as off-limits.

## Off-HPC: datalad clone

If you'd rather work on your own laptop, you can clone the course materials:

```bash
datalad clone <clone-url-TBD> wp7-course-public
cd wp7-course-public
datalad get course-materials/exercises/ex1-bootstrap/
```

!!! warning "Clone URL pending"
    The RIA clone URL will be posted here once the sibling is configured.
