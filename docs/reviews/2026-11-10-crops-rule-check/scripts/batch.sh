#!/bin/bash
# usage: batch.sh LISTFILE ; each line: TAG SEED NSHIFT VARIANT JSON
cd "$(dirname "$0")/../../../.."  # the repo root; put in by the project session in place of an absolute path
while read -r tag seed n var js; do
  [ -z "$tag" ] && continue
  PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 .venv/bin/python docs/reviews/2026-11-10-crops-rule-check/scripts/rv.py "$tag" "$seed" "$n" "$var" "$js" || echo "FAIL $tag $seed"
done < "$1"
