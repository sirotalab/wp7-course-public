# Conda environment

The course uses the lab's shared `wp7` conda environment.

## On HPC

```bash
conda activate wp7
```

That's it. The environment is at `/storage/share/python/environments/Anaconda3/envs/wp7`
and is pre-configured with everything needed for the exercises.

## Off-HPC (local machine)

If you want to work on the exercises locally, recreate the environment from
the snapshot:

```bash
mamba env create -f course-materials/environment.yml -n wp7
conda activate wp7
```

The `course-materials/environment.yml` file is a snapshot of the HPC `wp7`
env. See the [HPC workspace](workspace.md) page for how to get
`course-materials/` onto your local machine.

!!! note
    Off-HPC use is optional — you can do the whole course from VS Code
    Remote-SSH on the HPC.
