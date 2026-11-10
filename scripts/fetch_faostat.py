"""FAOSTAT, Crops and livestock products (domain QCL), every country and year, the bulk file in long form. Unpack with: python -I -m zipfile -e data/raw/faostat_qcl.zip data/raw/faostat"""
from _download import download

download("https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip", "faostat_qcl.zip")
