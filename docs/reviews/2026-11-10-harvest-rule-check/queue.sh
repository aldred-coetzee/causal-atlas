#!/bin/sh
# Runs each line of a job file through try.py, four at a time, each under a two-minute limit.
cd "$(dirname "$0")/../../.."
xargs -P 4 -L 1 sh -c 'PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 timeout 115 .venv/bin/python docs/reviews/2026-11-10-harvest-rule-check/try.py "$@" || echo "FAILED $*"' _ < "$1"
