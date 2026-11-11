# Three sources of events and disease by country and month

Read at source and fetched on 2026-11-11 by `scripts/fetch_events.py`; shaped by `src/causal_atlas/adapters_events.py`, tested in `tests/test_adapters_events.py`. Coverage below is counted from the files, each series alone. Nothing here sets one series beside another. All three are usable now; OpenDengue carries a licence caveat.

## 1. USGS earthquake catalogue (ComCat)

- **Address.** API `https://earthquake.usgs.gov/fdsnws/event/1/query`, one CSV a year, `eventtype=earthquake`, magnitude 4.5 and above, 1973 to 2025.
- **Licence.** "USGS-authored or produced data and information are considered to be in the U.S. Public Domain." The same page notes that not everything on USGS sites is public domain, and asks for the credit "U.S. Geological Survey" (https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits).
- **Citation asked for.** "U.S. Geological Survey, 2017, Advanced National Seismic System (ANSS) Comprehensive Catalog of Earthquake Events and Products", https://doi.org/10.5066/F7MS3QZH (https://earthquake.usgs.gov/data/comcat/references.php).
- **Fetched.** 53 files `m4.5_1973.csv` to `m4.5_2025.csv`, 49,018,526 bytes in all. Per-file SHA-256 values are in `data/raw/usgs_quakes/SHA256SUMS`, and the fetch prints them. The SHA-256 of that list is `a916e76608c8cb8358ecf4306c51f8167a21b7a2b9f5ccfdff25383f79b63aca`. The files hold 287,309 distinct events. No year came near the API's 20,000-event limit; the most was 9,584, in 2011.
- **Floor and first year.** ComCat's own pages state no magnitude of completeness.
  - **First year.** The availability page (https://earthquake.usgs.gov/data/comcat/availability.php, "as of October 20, 2020") gives the US PDE contribution from 1973-01-01; the earlier years come from other catalogues (ISC-GEM to 2010, ISC-GEM supplement 1904 to 1972). So 1973 is the first year, where one maker's record begins.
  - **NEIC's goal.** The NEIC page (https://www.usgs.gov/natural-hazards/earthquake-hazards/national-earthquake-information-center-neic) gives the present aim: "a goal of about M4.5 global completeness". That is today's aim, not the history.
  - **Counts by year.** Counted from the files, magnitude 4.5 and above rises from about 3,300 a year (1973–82) to about 7,400 (2012–25). The USGS FAQ says more earthquakes are located "because there are more seismic instruments", so 4.5 is not comparable through time.
  - **Other floors.** At 5.0 and above, the means are about 1,510 a year (1973–82) and about 1,720 (2012–25). The same two means are about 375 and 460 at 5.5 and above, and about 93 and 136 at 6.0 and above.
  - **Choice.** The floor is **magnitude 5.0, from 1973**, because it changes least from end to end. The ratio of counts at 5.0 and at 5.5 is about 4.0 in 1973–82 and 3.8 in 2012–25. If 5.0 were missing small events early on, this ratio would be lower in the early years, and it is not.
  - **The 5.0 dip.** Counts at 5.0 sag by up to a quarter in 1997–2003 (1,077 to 1,366 a year; 2000 is 1,494). Counted by decade in the file, the 1990s and 2000s are when Mwc joins and then replaces mb as the most common magnitude type at 5.0 and above. That mix of magnitude types is the main threat to comparability. It is counted here and not corrected.
  - **Context only.** The ISC-GEM study (Michael 2014, https://www.usgs.gov/publications/how-complete-isc-gem-global-earthquake-catalog) is about a different catalogue. It is not used for the floor.
- **Shape.** Three series by month of origin (UTC):
  - earthquakes by country (the shape holding the epicentre);
  - summed seismic moment by country, from each event's catalogue magnitude as 10^(1.5 M + 9.1) N m;
  - earthquakes anywhere, as a world series.
- **Zero rule.** The catalogue watches the whole earth, so every country-month from 1973-01 to 2025-12 is written, with zero where no event was recorded.
- **Coverage.** 234 places, 1973-01 to 2025-12, 148,824 country-months per country series, of which 139,663 are zero.
  - 87,867 events reach the floor. 17,995 lie inside a country's shape. 69,872 (80%) are at sea or outside every shape; they are counted only in the world series (636 months).
- **Known biases.**
  - A country's count depends on where its border meets the sea. Coastal subduction events often fall offshore.
  - Magnitude types change over time, as above.
  - The moment formula is meant for moment magnitude. Applied to mb it understates large events, because mb saturates near 6.
  - A large aftershock sequence fills one month (2004, 2011).
  - ComCat is live, and reviewed events are revised, so a later fetch will not match byte for byte.

## 2. Mass Mobilization protest data, version 5

- **Address.** https://doi.org/10.7910/DVN/HTTWYL (Harvard Dataverse, version 5.1, released 2022-10-10).
- **Licence.** CC0 1.0 (http://creativecommons.org/publicdomain/zero/1.0), stated in the dataset's record at https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/HTTWYL.
- **Citation asked for.** Clark, David; Regan, Patrick, 2016, "Mass Mobilization Protest Data", https://doi.org/10.7910/DVN/HTTWYL, Harvard Dataverse, V5, UNF:6:F/k8KUqKpCa5UssBbL/gzg== [fileUNF].
- **Fetched.**
  - `mmALL_073120_csv.csv`: 15,058,276 bytes, SHA-256 `5906226e24c9892482b0b9133b0b36519e5f7b833b036c7c2fab8bba6e431a9d`. Its MD5 matches the record's.
  - Users' manual `MM_users_manual_0515.pdf`: 122,934 bytes, SHA-256 `03541007078e661e4df11863f5c62fbe9adb3f745e91547446d05737fcf7cd45`. Its MD5 matches the record's.
- **What it counts.** In the manual's terms, a protest is 50 or more people making a demand of the government. Coding is by "protest-country-year", from a January-to-December news search for each country.
  - The file has 17,145 rows: 15,239 protests, and 1,906 rows marking a country-year searched with none found.
  - It covers 1990 to 2020-03, with 166 country names.
  - There is no United States row.
- **Shape.** Three series by month of the protest's start:
  - protests;
  - protests where the protesters used violence;
  - protests the state met with beatings, shootings or killings (any of its seven response fields).
- **Places.** Polity country codes are written out as ISO codes, then matched to Natural Earth.
  - Set aside and counted (236 protests): states that ended or split (USSR 60, Yugoslavia 36, Yugoslavia then Serbia and Montenegro 103, Czechoslovakia 4, East Germany 11, West Germany 2), and Kosovo (20), which has no Natural Earth match.
- **Zero rule.** Every month of a country-year that has a row in the file is written, with zero where no protest started. 2020 runs only to March. Country-years with no row are not written.
- **Coverage.** 159 places, 1990-01 to 2020-03, 56,646 country-months.
  - 15,003 protests: 3,978 violent, 1,865 met with force.
  - 47,873 country-months are zero.
- **Known biases.**
  - The counts depend on a handful of English-language papers and wires, which give most attention to the countries they cover.
  - A long protest counts once, in its start month.
  - Rallies, armed rebel action and communal disputes are not coded.
  - Sudan before 2011 includes South Sudan.
  - Some countries have gaps in years.

## 3. OpenDengue, V1.3.1

- **Licence, settled as far as it can be.**
  - The release's own record (https://api.figshare.com/v2/articles/24259573, version 5, published 2026-11-03 with the V1.3.1 files) states "CC BY 4.0" (https://creativecommons.org/licenses/by/4.0/), as do all its earlier versions.
  - The GitHub repository has no licence file, and its release notes state none. The site's footer says CC BY 4.0.
  - The data descriptor (https://pmc.ncbi.nlm.nih.gov/articles/PMC10940302/, "Citation and data licence") says "OpenDengue data is made available under a creative commons CC BY-SA licence" and "all adaptations of the OpenDengue dataset must also be made available under the same terms".
  - The release itself states CC BY 4.0, so it was fetched. Because the makers' own paper asks for share-alike, honour CC BY-SA for anything derived and published from it, until they say otherwise.
- **Citation asked for.**
  - The descriptor: https://doi.org/10.1038/s41597-024-03120-7.
  - And the release: "Clarke J, Lim A, Gupte P, Pigott DM, van Panhuis WG, Brady OJ. OpenDengue: data from the OpenDengue database. Version [1.3.1]. figshare; 2026. Available from: https://doi.org/10.6084/m9.figshare.24259573."
- **Fetched.** Each MD5 matches the record's.

  | File | Bytes | SHA-256 |
  |---|---|---|
  | `National_extract_V1_3_1.zip` | 330,958 | `c588335f25f2202e4f87d271381f385c76ffd4dcb68348f40c2a6fcab8889d4e` |
  | unpacked to `national/National_extract_V1_3_1.csv` | 4,191,115 | `b9381e3f1dca5828330878c2b9ccb02629019b2b8554defe2f2c7ee0917c5cb1` |
  | `Temporal_extract_V1_3_1.zip` | 55,205,724 | `6bb4dbec3d891e444047354619d7bc7003e29e2f9f9cfcec29130fe605c126a2` |
  | `metadata_main.json` | 4,627 | `e93e29b541a5ac3e13be337937b6257c2c09f0dfc4fb80d5c179246ec5584600` |

  The temporal extract is held for later sub-national work and is not shaped.
- **What it holds (national file).** 29,540 rows, all national, covering 128 ISO codes from 1924-01-20 to 2025-04-30:
  - 22,883 rows by week (all Sunday to Saturday);
  - 3,166 rows by whole calendar month;
  - 3,491 rows by calendar year.
- **Shape.** Two series: dengue cases by month and by year.
  - **A month** comes from the source's month row. Otherwise it comes from its weeks, a week going to the month that holds its middle day, and only when every such week is present: 817 months lacked some weeks and are not written.
  - **A year** comes from the source's year row (3,304). Otherwise it is the sum of twelve written months (540). The two routes never both applied.
  - **Flag.** `imputed` where any part is marked "(Imputed)" or "(Zero filling)" in the source's id; these marks appear only on weekly rows.
- **Zero rule.** A zero is written only where the source wrote one, and nothing where it has no record. The makers say that for some countries "it is unclear if this is a record of absence of dengue or an absence in reporting".
- **Places.** 945 rows of seven overseas territories (BES, GLP, GUF, MTQ, MYT, REU, TKL) have no country of their own in Natural Earth. They are set aside and counted, not added to France, the Netherlands or New Zealand.
- **Coverage.**
  - Month series: 118 places, 1993-01 to 2025-04, 7,796 values; 1,505 are zero and 471 are flagged.
  - Year series: 118 places, 1955 to 2024, 3,844 values; 1,174 are zero and 95 are flagged.
- **Known biases.**
  - Case definitions differ by source: suspected, probable, confirmed, or combinations.
  - Reporting effort changes over time.
  - Zeros in the PAHO data were filled by the makers.
  - Early US weekly records are sparse, so its months start late.

## Proposed entries for `data/manifest.toml` (text only, not applied)

```toml
[usgs_quakes]
source_url = "https://earthquake.usgs.gov/fdsnws/event/1/query (format=csv, eventtype=earthquake, minmagnitude=4.5, one query a year 1973-2025)"
fetch_script = "scripts/fetch_events.py"
version = "ComCat as queried 2026-11-11 (a live catalogue)"
licence = "U.S. Public Domain for USGS-authored data; credit U.S. Geological Survey; cite ANSS ComCat, https://doi.org/10.5066/F7MS3QZH"
fetched = "2026-11-11"
sha256 = "a916e76608c8cb8358ecf4306c51f8167a21b7a2b9f5ccfdff25383f79b63aca"  # of SHA256SUMS, the list of the 53 yearly files
coverage = "Global, 1973-01 to 2025-12; 287,309 events of M4.5+, 87,867 of M5.0+ (the floor used), 17,995 of them inside a country's shape"
known_biases = "No stated completeness; M4.5 counts more than double with more stations; M5.0 sags about a fifth in 1996-2003 as the reported magnitude type shifts; 80% of events at sea; live catalogue, revised"

[mass_mobilization]
source_url = "https://dataverse.harvard.edu/api/access/datafile/4291456?format=original"
fetch_script = "scripts/fetch_events.py"
version = "5.1, released 2022-10-10"
licence = "CC0 1.0; cite Clark and Regan 2016, https://doi.org/10.7910/DVN/HTTWYL"
fetched = "2026-11-11"
sha256 = "5906226e24c9892482b0b9133b0b36519e5f7b833b036c7c2fab8bba6e431a9d"
codebook_sha256 = "03541007078e661e4df11863f5c62fbe9adb3f745e91547446d05737fcf7cd45"
coverage = "166 countries named, 1990-01 to 2020-03; 15,239 protests; no United States"
known_biases = "A few English-language papers and wires; start month only; states that ended (USSR, Yugoslavia, Czechoslovakia, the Germanys) and Kosovo set aside; Sudan before 2011 includes South Sudan"

[opendengue]
source_url = "https://ndownloader.figshare.com/files/71041980"
fetch_script = "scripts/fetch_events.py"
version = "V1.3.1 (figshare record 24259573, version 5, 2026-11-03)"
licence = "CC BY 4.0 as stated on the release's record; the data descriptor says CC BY-SA, so share-alike is honoured for published derivatives; cite https://doi.org/10.1038/s41597-024-03120-7 and https://doi.org/10.6084/m9.figshare.24259573"
fetched = "2026-11-11"
sha256 = "c588335f25f2202e4f87d271381f385c76ffd4dcb68348f40c2a6fcab8889d4e"
coverage = "National extract: 128 ISO codes, 1924-01 to 2025-04, weekly, monthly and yearly rows; shaped 118 countries, months 1993-01 to 2025-04, years 1955 to 2024"
known_biases = "Case definitions differ by source; zeros filled by the makers in PAHO data are flagged imputed; absence of a record is not absence of dengue"
```
