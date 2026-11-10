# Reading: which record outside climate to add first

Bounded reading, 2026-11-10. One question, pulled by one decision (0045): which
openly licensed, long, monthly, gridded record outside climate has a published
lagged link from El Niño or drought large enough to be a known answer for the
search? One helper read for eight minutes (about 115k tokens); this session then
checked at source what the choice rests on. What was read by whom is marked.

## Recommended: burned area, ESA Fire_cci FireCCILT11

- **What it is.** Monthly burned area from the AVHRR satellites, global, 0.25
  degree, 1982 to 2018. Each monthly file carries the sum of burned area, its
  standard error, the fraction of the cell that can burn and the fraction of
  that which was observed. Read at source by this session: the product README
  ("FireCCILT11 is available for years 1982 to 2018 … Year 1994 is not included
  in the dataset because there was not enough input data from the LTDR Archive")
  and a file's own header.
- **Access.** Plain HTTPS from CEDA, no account: "Public data: access to these
  data is available to both registered and non-registered users" (the
  directory's licence note, read by this session). 432 files of 16.7 MB, about
  7.2 GB.
- **Licence.** ESA CCI terms for Fire_cci, read by this session: "The CCI
  datasets held on the CCI Open Data Portal may be used by any user for any
  purpose", with an acknowledgement of the ESA Climate Change Initiative and
  the Fire CCI project, and a citation of the data set's DOI. Details in
  `docs/data-sources.md`.
- **The published link.** Chen et al. 2016, Environmental Research Letters 11,
  045001 (open access; quotes read at source by a second helper, 2026-11-10):
  "about 48% of global burned area can be forecast with a correlation
  coefficient that is significant at a p < 0.01 level using a single ocean
  climate index (OCI) 3 or more months prior to the month of peak burning."
  "Equatorial Asia had the largest fractions of predictable burned area using
  an optimized 1-OCI model (92%), followed by Central America (86%). In
  contrast, Europe and Central Asia had the lowest fractions of predictable
  burned area at 29% and 33%". "Pacific Ocean indices describing the El
  Niño-Southern Oscillation were more important than indices from other ocean
  basins, accounting for about 1/3 of the total predictable global burned area."
- **How much weight those numbers bear: little.** From the same paper: the data
  were GFED4s, "18 years, from 1997 through 2014", annual burned area at 1
  degree; "We examined 14 OCIs"; the index led the peak fire month "by a period
  of between 3 and 12 months"; "we selected the regression model with the
  highest absolute values of correlation"; a cell counted as predictable "if r >
  0.59 (corresponding to p < 0.01, n = 18)". So each cell's figure is the best
  of 14 indices and 10 lead times on 18 points, tested as if it were one
  correlation, and the percentages are weighted by burned area. They are not
  out-of-sample figures: only the twelve hotspot regions were cross-validated
  ("leave-one-out"), and there the paper says a single peak such as 1997 to 1998
  was not captured. What is taken from it: El Niño leads burned area by a
  season or more in several regions, most strongly in equatorial Asia. Not
  taken: any size.
- **Not known.** Whether the link is large enough, over enough of a field, for
  this search on a record of 36 years. Chen et al. did not use this product. The
  first step of any test must measure what the search can hear on these fields.

## Known weaknesses of the product (helper's reading; the product paper, Otón et al. 2021, was read in abstract only)

- 1994 is absent, and it was a heavy fire year in Indonesia.
- Several satellites with drifting orbits; the makers' corrections cannot be
  checked here. A change of satellite could look like a change in fire.
- Pixels of about 5 km: small fires are missed, so cropland and forest-edge
  burning is under-counted.
- Agreement with the MODIS-based products is reported on annual totals
  (correlation above 0.6), not month by month.
- Cloud and smoke hide fire. The observed fraction is in each file; a dry year
  is also a clear year, so more is seen. This matters most for a link from
  drought in the same season.

## Second choice

Vegetation greenness: PKU GIMMS NDVI, AVHRR only, 1982 to 2015 (Zenodo record
8253971, CC BY 4.0, about 5 GB; helper's reading, not checked by this session).
Longer than most, openly licensed; but it is a biophysical record close to the
drought index already held, and no published size for a lagged link was found.

## Looked at and dropped (helper's reading)

- NOAA's NDVI climate record: about 1 TB.
- GFED5 burned area: 24 years, and its resolution changes within the record.
- Crop yields: annual, not monthly.
- Food prices: one global series is openly usable; the place-by-place WFP data
  was already found blocked from this box (`docs/data-sources.md`).
- Dengue case counts (OpenDengue): short and uneven by country.

## Not done

No survey of fire and climate. Chen et al. 2011 and 2017 were not opened. The
Product User Guide was not read beyond the file header and the README.
