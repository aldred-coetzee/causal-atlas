"""FAOSTAT, Prices: Consumer Price Indices (domain CP) and Exchange rates (domain PE), the bulk files in long form. Unpack each into its own folder with: python -I -m zipfile -e data/raw/faostat_prices/<file>.zip data/raw/faostat_prices/<cp or pe>"""
from _download import RAW, download

(RAW / "faostat_prices").mkdir(parents=True, exist_ok=True)
download("https://bulks-faostat.fao.org/production/ConsumerPriceIndices_E_All_Data_(Normalized).zip", "faostat_prices/cp.zip")
download("https://bulks-faostat.fao.org/production/Exchange_rate_E_All_Data_(Normalized).zip", "faostat_prices/pe.zip")
