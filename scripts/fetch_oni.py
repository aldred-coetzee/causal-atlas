"""Oceanic Nino Index, as published by NOAA PSL."""
from _download import download

download("https://psl.noaa.gov/data/correlation/oni.data", "oni.data")
