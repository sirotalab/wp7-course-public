#!/usr/bin/env bash
# Sourced by `pixi run` / `pixi shell` on every activation.
#
# Workaround for conda-forge's newer libstdc++ losing to a system /usr/lib
# copy when Python imports extensions that need libicu (e.g. sqlite3 → _sqlite3
# → libicui18n). Without this, jupyter kernels crash on start with
#   "libstdc++.so.6: version `CXXABI_1.3.15' not found"
# on hosts with gcc-12-era system libstdc++ (gamma3, 2026-04).
#
# Prepending the env's lib dir forces the newer conda-forge libstdc++ to win.
echo "pixi_activate.sh fired, CONDA_PREFIX=$CONDA_PREFIX" >&2
export LD_LIBRARY_PATH="${CONDA_PREFIX}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
