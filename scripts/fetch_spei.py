"""SPEIbase, 3-month SPEI, global 0.5 degree netCDF, latest version."""
from _download import download

download("https://spei.csic.es/spei_database/nc/spei03.nc", "spei03.nc")
