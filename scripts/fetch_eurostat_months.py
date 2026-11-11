"""Eight monthly Eurostat tables by country, each of a different kind: unemployment, industrial production, retail trade, electricity, nights at tourist accommodation, air passengers, first-time asylum applicants, live births. Each is asked of the dissemination API (SDMX-CSV, no key) with a key that holds the cut kept and, where the cut was chosen between two or more, those others too, so the choice can be counted again from the file. Each goes to data/raw/eurostat/<table>/; the cut itself is applied by src/causal_atlas/adapters_eurostat.py. Nothing in a download is run."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # so it runs under python -I, which leaves the script's folder off the path

from _download import RAW, download  # noqa: E402

API = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

# table: the series key, dimension by dimension in the table's own order (an empty place is every code; '+' joins codes).
KEYS = {
    "une_rt_m": "M..TOTAL.THS_PER.T.",                    # freq.s_adj.age.unit.sex.geo: all three adjustments, people in thousands
    "sts_inpr_m": "M.PRD.B-D.NSA..",                      # freq.indic_bt.nace_r2.s_adj.unit.geo: industry B-D, unadjusted, every base year
    "sts_trtu_m": "M..G47.NSA..",                         # freq.indic_bt.nace_r2.s_adj.unit.geo: retail trade G47, unadjusted, volume and value, every base year
    "nrg_cb_em": "M.AIM.E7000.GWH.",                      # freq.nrg_bal.siec.unit.geo: electricity available to the internal market
    "tour_occ_nim": "M.TOTAL.NR.I551-I553.",              # freq.c_resid.unit.nace_r2.geo: all residences, number of nights, all three kinds of accommodation
    "avia_paoc": "M.PAS.PAS_CRD+PAS_BRD.TOTAL.TOTAL.",    # freq.unit.tra_meas.tra_cov.schedule.geo: passengers carried and on board, all coverage, all schedules
    "migr_asyappctzm": "M.PER.TOTAL.T.FRST+TOTAL.TOTAL.",  # freq.unit.citizen.sex.applicant.age.geo: all citizenships, both sexes, all ages; first-time and all applicants
    "demo_fmonth": "",                                    # the whole table (freq.unit.month.geo): two megabytes
}

if __name__ == "__main__":
    for table, key in KEYS.items():
        (RAW / "eurostat" / table).mkdir(parents=True, exist_ok=True)
        url = f"{API}/{table}/{key}?format=SDMX-CSV" if key else f"{API}/{table}?format=SDMX-CSV"
        download(url, f"eurostat/{table}/{table}.csv")
