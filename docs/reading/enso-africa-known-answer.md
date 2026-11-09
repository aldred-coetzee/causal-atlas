# Reading: the accepted link from ENSO to African rainfall and drought

Read 2026-11-09, one question, for the known-answer test on ONI and SPEI-3.
Every claim below carries the page opened and a short quote. The main source
is a 2025 review by 30 authors, read in full (Cai et al., *Nature Reviews
Earth & Environment* 6, 503–520, [1]). Its numbers are rainfall regressed on a
normalised Niño3.4 index, **at zero lag, season against the same season**,
1948–2023. They are rainfall, not SPEI.

## 1–2. Where, when, which sign, how strong (Africa)

| Region (box as given) | Season | El Niño sign | Strength quoted | Source |
|---|---|---|---|---|
| Southern Africa, 15–35° S, 15–40° E | DJF (strongest); also OND and MAM after | **Drier** | DJF −0.37 mm/day per °C; OND −0.15; MAM −0.19. DJF r = −0.69 in 1971–2010 | [1] |
| East Africa, 7° S–5° N, 29–42° E (short rains) | OND; persists into DJF | **Wetter** | OND +0.38 mm/day per °C; DJF +0.29. r = 0.61 in 1970–2010 | [1] |
| Sahel, 11–15° N, 17° W–40° E | JAS (El Niño developing) | **Drier** | −0.42 mm/day per °C; r ≈ −0.43 (1931–70), −0.59 (1971–2010), high-pass filtered | [1] |
| Guinea coast | JJA–JAS | Drier (via Atlantic Niña) | not quantified | [1] |
| Ethiopian plateau | boreal summer | Drier, in many years | not quantified | [1] |

Quotes from [1]:
- Southern Africa: *"For El Niño, warmer and drier conditions dominate across southern Africa … averaging 0.28 °C °C−1 and −0.37 mm day−1 °C−1 when averaged over 35–15° S, 15–40° E."*
- East Africa: *"anomalously high rainfall occurs during the short rain season in East Africa … +0.38 mm day−1 °C−1 (7° S to 5° N, 29–42° E)."*
- Sahel: *"strong warming and drying occur during the El Niño developing months … reaching 0.38 °C °C−1 and −0.42 mm day−1 °C−1."*
- Guinea coast: an El Niño drives cool eastern Atlantic SSTs, *"promoting dry anomalies over the Guinea coast and wet anomalies over the Sahel"*. So the Sahel has two pathways of opposite sign.
- Ethiopia: *"many drought years over the Ethiopian plateau coincide with an El Niño"*.
- La Niña: *"The opposite impacts occur during La Niña"* (DJF), with the asymmetries under section 5.

**Lag.** [1] uses concurrent seasons, so the accepted answer is **0 to about 3 months**
between the index and the rainfall. The ONI is itself a three-month mean
peaking around November to January, and SPEI-3 sums three months, so the
response should peak with ONI at lag 0 to +2 months in DJF–MAM over southern
Africa and in OND–DJF over East Africa. For SPEI specifically, the Vicente-Serrano
et al. 2011 abstract (seen only through OpenAlex's copy of the abstract, [2]) says:
*"in areas of South Africa, Australia and Southeast Asia, the effects were more obvious some months later, and at longer time scales."*
It also says *"severe drought conditions are associated with more than 70% of ENSO events"* in some areas (which ones not checked) and
*"Lags detected … may help forecasting … up to one year before"*. Full text not opened (publisher blocked).

The 1987 Ropelewski and Halpert summary map (NOAA bulletin, [3]) gives
southern Africa **dry, Nov(0) to May(+1)**, read from a scanned map, so the
months are approximate. Its caption: *"the most likely months of occurrence"*;
and *"Not every indicated anomaly occurs with every ENSO event."*

## 3. Little or no signal (negative controls)

- The 1987 map marks **North Africa and the Mediterranean "INDETERMINATE"** and draws no region over the Sahara or central Africa [3] (read from the map).
- [1]: in MAM after an El Niño there is *"little wet anomaly in off-equatorial East Africa"*.
- Central Africa (Congo basin) and the Sahara: no stated ENSO link found in [1]; **not checked** as a stated null. The Sahara is also near-rainless, so SPEI there is unstable and should be excluded, not used as a control.

## 4. Outside Africa (for a later check on another continent)

From the 1987 map [3], months read from a scan and approximate; strengths **not checked**:

| Region | El Niño sign | Months |
|---|---|---|
| Indonesia, Papua New Guinea, northern and eastern Australia | Dry | roughly Jun(0)–Nov(0), Australia parts into Mar(+1) |
| Northeast Brazil, northern South America | Dry | roughly Jul(0)–Mar(+1) |
| Southeast South America (southern Brazil, Uruguay) | Wet | Nov(0)–Feb(+1) |
| India | Dry | Jun(0)–Sep(0) |

The Ropelewski and Halpert page at IRI [4] confirms the Australia entry only:
*"dry conditions in Northern and Eastern Australia were highly probable"*. NOAA CPC [5]: El Niño brings *"Suppressed convective rainfall … across Indonesia"*.

## 5. Complications to disclose

- **Indian Ocean Dipole (East Africa).** *"part of ENSO's impact during SON is conveyed via the IOD, which by itself also exerts a similar impact to that of ENSO"* [1]. A blind search may name the IOD, or nothing, rather than ONI over East Africa.
- **Non-stationarity.** Southern Africa DJF: *"correlations between ENSO and DJF rainfall are 0.15 … far lower than correlations of −0.69 … from 1971–2010"* [1]. (The 0.15 is printed positive; it may mean near zero.) East Africa r = 0.30 then 0.61; the link weakened after 2000 with a weaker ENSO–IOD tie [1]. A 1950-onward run sits mostly in the strong period.
- **Asymmetry.** Southern Africa DJF: EP El Niño −0.70 mm/day, CP El Niño −0.003 [1]; *"generally opposite but asymmetric impacts between El Niño and La Niña"* [1]. SPEI: *"negative anomalies were much higher for El Niño events than for La Niña"* (abstract, via search summary only; not checked at source).
- **Event-to-event failure.** The Angola Low *"barely weakened during the 1997/98 El Niño, meaning that an expected drought did not eventuate over southern Africa"* [1].
- **CRU TS station coverage**, which SPEIbase inherits [6]: *"regions uninformed by observations are not left missing but instead are replaced by the published climatology"*, with *"the unavoidable side effect of decreasing variance"*. Precipitation's 450 km correlation decay distance means *"regions with sparse support have patchy coverage"*. Cells with no station have zero anomaly, which damps any signal. The `stn` variable in CRU TS gives station counts and could mask such cells; SPEIbase does not carry it.

## URLs opened

1. Cai et al. 2025, full text: https://www.atmos.albany.edu/facstaff/zhou/pdf/pdf_papers/Cai_et_al_2025.pdf (DOI 10.1038/s43017-025-00705-7); supplement: https://repository.library.noaa.gov/view/noaa/71705/noaa_71705_DS2.pdf
2. Vicente-Serrano et al. 2011, abstract only: https://api.openalex.org/works/doi:10.1029/2011JD016039
3. NOAA Central Region Technical Attachment 87-6 (1987), Ropelewski and Halpert map: https://repository.library.noaa.gov/view/noaa/33759/noaa_33759_DS1.pdf
4. https://iridl.ldeo.columbia.edu/maproom/ENSO/New/ropelewskihalpert.html
5. https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ensofaq.shtml
6. Harris et al. 2020, CRU TS v4: https://www.osti.gov/servlets/purl/1624279 (DOI 10.1038/s41597-020-0453-3)

Tried and blocked or missing: Mason and Goddard 2001 and Ropelewski and Halpert 1987 (AMS),
the Vicente-Serrano 2011 full text (Wiley, CORE, Vigo copy), Davey et al. 2014 (ScienceDirect),
and the Australian Bureau of Meteorology. Nicholson and Kim 1997, Lindesay 1988 and Indeje et al. 2000
were not opened.

## Checked at source by the project session, 2026-11-09

Re-read in the full text of [1] after this page was written: the southern
Africa box and its December to February figure, the East Africa box and its
October to December figure, the October to December figure for southern
Africa, and the two correlations for southern Africa (0.15 and -0.69). All
as quoted above. The other entries are as the reading agent reported them.
