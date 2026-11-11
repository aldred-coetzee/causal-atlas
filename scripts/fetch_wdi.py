"""World Bank World Development Indicators, the bulk CSV (every indicator, country and year). The address redirects to the Bank's file host; the file is replaced in place by each release. Unpack with: python -I -m zipfile -e data/raw/wdi/WDI_CSV.zip data/raw/wdi"""
from _download import RAW, download

(RAW / "wdi").mkdir(parents=True, exist_ok=True)
download("https://databank.worldbank.org/data/download/WDI_CSV.zip", "wdi/WDI_CSV.zip")
