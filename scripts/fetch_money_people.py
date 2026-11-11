"""Money, births and deaths by country and month: five BIS bulk files (policy rates, long consumer prices, residential property prices, credit to the non-financial sector, effective exchange rates), the Human Fertility Database's Short-Term Fertility Fluctuations (births by month, crude and adjusted), and Eurostat's deaths by month (demo_mmonth). Each BIS zip is unpacked into its own folder beside it; nothing in a download is run."""
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # so it runs under python -I, which leaves the script's folder off the path

from _download import RAW, download  # noqa: E402

BIS = ("CBPOL", "LONG_CPI", "SPP", "TC", "EER")

for d in ("bis", "hfd_stff", "eurostat_deaths"):
    (RAW / d).mkdir(parents=True, exist_ok=True)
for name in BIS:
    z = download(f"https://data.bis.org/static/bulk/WS_{name}_csv_flat.zip", f"bis/WS_{name}_csv_flat.zip")
    with zipfile.ZipFile(z) as f:
        f.extractall(RAW / "bis" / name)
download("https://www.humanfertility.org/File/GetDocumentFree/STFF/stff.csv", "hfd_stff/stff.csv")
download("https://www.humanfertility.org/File/GetDocumentFree/STFF/stffadj.csv", "hfd_stff/stffadj.csv")
download("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_mmonth?format=SDMX-CSV", "eurostat_deaths/demo_mmonth.csv")
