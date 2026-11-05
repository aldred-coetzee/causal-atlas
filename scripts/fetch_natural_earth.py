"""Natural Earth 1:10m countries, for the land mask and country lookup."""
from _download import download

download("https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip", "ne_10m_admin_0_countries.zip")
