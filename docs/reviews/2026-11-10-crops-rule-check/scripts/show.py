from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]  # the repo root; put in by the project session in place of an absolute path, before this file was committed
import json, sys
for s in open(str(ROOT / "docs/reviews/2026-11-10-crops-rule-check/logs/runs.jsonl")):
    o = json.loads(s); m = o['model']; f = o['flat']
    if len(sys.argv) > 1 and not o['tag'].startswith(sys.argv[1]): continue
    print(o['tag'], o['seed'], o['variant'][:3], 'PASS' if o['passes'] else 'no', 'S %.2f/%.2f lo %.2f/%.2f beats %d/%d of %d rec %d/%d ctry %d wob %.2f term true/shift %.3f/%.3f belowcap %s linked %d secs %d lv %s' % (
        m['s']*100, f['s']*100, m['ci'][0]*100, f['ci'][0]*100, m['beats'], f['beats'], o['nshift'], m['records'], o['units'], m['countries'], m['without_best']*100,
        o['term_rms_scored_true'], o['term_rms_scored_shift_mean'], None if o['frac_claims_slope_below_cap'] is None else round(o['frac_claims_slope_below_cap'], 3), o['linked_units'], o['secs'], [l[0] for l in o['levels'].values()]))
