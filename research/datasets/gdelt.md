# GDELT — Global Database of Events, Language, and Tone

> Deep-dive research for Causal Atlas. Findings as of March 2025; significantly expanded March 2026.

---

## 1. Overview

The **Global Database of Events, Language, and Tone (GDELT)** is the largest open dataset of global human society, monitoring print, broadcast, and web news media across more than 100 languages. It identifies events, actors, themes, emotions, locations, and narratives from news coverage worldwide and encodes them into a structured, queryable format.

| Attribute | Detail |
|---|---|
| **Creator** | Kalev H. Leetaru (Foreign Policy Magazine Top 100 Global Thinker 2013) |
| **Institutional affiliations** | Georgetown University (Yahoo! Fellowship); supported by Google (Ideas, Cloud, News), BBC Monitoring, National Academies, LexisNexis, JSTOR, Internet Archive, NSF |
| **Initial release** | GDELT 1.0 launched 2013 (with historical data back to 1979) |
| **GDELT 2.0 launch** | 19 February 2015 |
| **Website** | https://www.gdeltproject.org |
| **Blog (primary documentation)** | https://blog.gdeltproject.org |
| **Scale** | 500+ million event records; processes 500K–1M articles daily |
| **Event taxonomy** | CAMEO (Conflict and Mediation Event Observations) — 300+ event types in 20 root categories |

GDELT is not a primary data source — it is a **media-derived event dataset**. Events are extracted from news articles using automated natural language processing. This is a fundamental distinction: GDELT measures what the media *reports*, not necessarily what *happens*.

### Three Core Data Streams (GDELT 2.0)

1. **Event Database** — Structured records of "who did what to whom, where, and when" using the CAMEO event taxonomy. 58 fields per record.
2. **Mentions Table** — Tracks every mention of every event across all monitored sources, with confidence scores, sentiment, and character offsets. Links events to the articles that mention them.
3. **Global Knowledge Graph (GKG)** — Extracts persons, organisations, locations, themes, emotions (2,300+ via GCAM), counts, quotes, and imagery from each article. Far richer than the Event table.

---

## 2. Coverage

### Temporal Range

| Version | Start Date | End Date | Update Frequency |
|---|---|---|---|
| GDELT 1.0 Events | 1 January 1979 | Present | Daily (by 6 AM EST) |
| GDELT 2.0 Events | 19 February 2015 | Present | Every 15 minutes |
| GDELT 2.0 GKG | 19 February 2015 | Present | Every 15 minutes |
| GDELT 2.0 Mentions | 19 February 2015 | Present | Every 15 minutes |
| Visual GKG (VGKG) | December 2015 | Present | Every 15 minutes |
| American TV GKG | July 2009 | Present | Daily (48-hour embargo) |

**Historical note:** GDELT 1.0 data from 1979–March 2013 is provided as monthly/yearly bulk files. From April 2013 onward, daily files are available. GDELT 2.0 was initially forward-looking from Feb 2015; historical backfill to 1979 was planned but the 1.0 archive remains the primary historical source.

### Spatial Extent

- **Global** — no geographic restrictions
- Sources from 100+ languages, with 65 languages actively machine-translated in real time (covering 98.4% of non-English material)
- Geocoding references "more than 9 million places on earth" via the GNS/GNIS gazetteers

### Source Volume

- Monitors hundreds of thousands of news outlets globally
- Major wire services (AP, AFP, Reuters), broadcasters (BBC, CNN), and web-native sources
- Coverage density is **not uniform** — strong Western/English-language bias (see Quality section)

---

## 3. Access Methods

GDELT provides multiple access paths, each suited to different use cases.

### 3.1 Bulk CSV Downloads (Raw Data)

The primary raw data distribution mechanism. Files are tab-delimited (despite `.CSV` extension), ZIP-compressed.

| Dataset | Index URL | File Naming |
|---|---|---|
| GDELT 1.0 Events | `http://data.gdeltproject.org/events/index.html` | `YYYYMMDD.export.CSV.zip` (daily) or `YYYY.zip` / `YYYYMM.zip` (historical) |
| GDELT 1.0 GKG | `http://data.gdeltproject.org/gkg/index.html` | `YYYYMMDD.gkg.csv.zip` |
| GDELT 2.0 (all tables) | Master file lists (see below) | `YYYYMMDDHHMMSS.export.CSV.zip` (15-min intervals) |

**GDELT 2.0 Master File Lists** (updated every 15 minutes):

- English events/mentions/GKG: `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt`
- Translingual events/mentions/GKG: `http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt`
- Last 15 minutes only (English): `http://data.gdeltproject.org/gdeltv2/lastupdate.txt`
- Last 15 minutes only (Translingual): `http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt`

Each line in the master file list contains: `file_size md5_hash download_url`

**Download size guidance:** A single day of GDELT 2.0 data (all 96 fifteen-minute intervals) is approximately 500 MB uncompressed.

### 3.2 Google BigQuery

GDELT is available as a public dataset in Google BigQuery, updated every 15 minutes. This is the recommended path for analytical queries over the full dataset.

| BigQuery Table | Description |
|---|---|
| `gdelt-bq.gdeltv2.events` | GDELT 2.0 Event records |
| `gdelt-bq.gdeltv2.eventmentions` | GDELT 2.0 Mentions |
| `gdelt-bq.gdeltv2.gkg` | GDELT 2.0 Global Knowledge Graph |
| `gdelt-bq.full.events` | GDELT 1.0 Events (1979–present) |
| `gdelt-bq.full.gkg` | GDELT 1.0 GKG |
| `gdelt-bq.extra.sourcesbycountry` | Source outlet metadata |
| `gdelt-bq.gdeltv2.gkg_gcam` | GCAM emotional measures (nested) |

**Pricing:** BigQuery charges per query based on data scanned. The full events table is multiple TB. Use date partitioning (`_PARTITIONTIME`) or `SQLDATE` filters to control costs. The first 1 TB/month of querying is free under Google Cloud's free tier.

**Sample BigQuery SQL:**

```sql
-- Count events by country in a specific month
SELECT ActionGeo_CountryCode, COUNT(*) as event_count
FROM `gdelt-bq.gdeltv2.events`
WHERE SQLDATE BETWEEN 20240101 AND 20240131
  AND ActionGeo_CountryCode IS NOT NULL
GROUP BY ActionGeo_CountryCode
ORDER BY event_count DESC
LIMIT 20;

-- Conflict events (CAMEO root codes 18-20) with coordinates
SELECT GLOBALEVENTID, SQLDATE, EventCode,
       ActionGeo_Lat, ActionGeo_Long, ActionGeo_FullName,
       GoldsteinScale, AvgTone, NumMentions
FROM `gdelt-bq.gdeltv2.events`
WHERE EventRootCode IN ('18', '19', '20')
  AND SQLDATE BETWEEN 20240601 AND 20240630
  AND ActionGeo_Lat IS NOT NULL;

-- GKG themes related to food security
SELECT DATE, V2Themes, V2Locations, V2Tone
FROM `gdelt-bq.gdeltv2.gkg`
WHERE V2Themes LIKE '%FOOD_SECURITY%'
  AND DATE BETWEEN 20240101000000 AND 20240131235959;
```

### 3.3 DOC 2.0 API (Full-Text Search)

Searches the full text of articles monitored by GDELT. Returns article metadata, not raw event records.

- **Endpoint:** `https://api.gdeltproject.org/api/v2/doc/doc`
- **Default time window:** Last 3 months (rolling), with archive back to January 2017
- **Max results:** 250 per query
- **Rate limits:** Not officially published; practical limit ~1 request/second for sustained use
- **Authentication:** None required
- **Response formats:** HTML, CSV, JSON, JSONP, RSS, JSONFeed

**Key parameters:**

| Parameter | Description | Example |
|---|---|---|
| `query` | Search terms with operators | `"food crisis" sourcecountry:KE` |
| `mode` | Output type | `artlist`, `timelinevol`, `timelinetone`, `tonechart` |
| `format` | Response format | `json`, `csv`, `html` |
| `timespan` | Time window | `24h`, `7d`, `3m` |
| `STARTDATETIME` | Start (YYYYMMDDHHMMSS) | `20240101000000` |
| `ENDDATETIME` | End (YYYYMMDDHHMMSS) | `20240131235959` |
| `MAXRECORDS` | Result limit (max 250) | `250` |
| `SORT` | Sort order | `dateDesc`, `toneDesc`, `hybridRel` |

**Query operators:**

- `"exact phrase"` — phrase search
- `(term1 OR term2)` — boolean OR
- `-term` — exclude
- `domain:bbc.co.uk` — restrict to domain
- `sourcelang:arabic` — filter by source language
- `sourcecountry:US` — filter by source country
- `theme:FOOD_SECURITY` — GKG theme filter
- `tone>5` or `tone<-5` — sentiment filter
- `near10:"drought conflict"` — proximity search (words within N words)
- `imagetag:fire` — search by AI-detected image content

**Example URL:**
```
https://api.gdeltproject.org/api/v2/doc/doc?query="food crisis" sourcecountry:KE&mode=timelinevol&format=json&timespan=3m
```

### 3.4 GEO 2.0 API (Geographic Search)

Returns geographic data suitable for mapping.

- **Endpoint:** `https://api.gdeltproject.org/api/v2/geo/geo`
- **Default time window:** Last 24 hours (max 7 days)
- **Authentication:** None
- **Response formats:** HTML (interactive map), GeoJSON, CSV, RSS, JSONFeed

**Key modes:** `PointData`, `Country`, `SourceCountry`, `ADM1`, and image variants of each.

**Example URL:**
```
https://api.gdeltproject.org/api/v2/geo/geo?query="earthquake"&mode=PointData&format=GeoJSON&timespan=7d
```

### 3.5 Context 2.0 API (Sentence-Level Search)

Returns individual sentences matching queries, not full articles. All search terms must appear in the same sentence.

- **Endpoint:** `https://api.gdeltproject.org/api/v2/context/context`
- **Time window:** Last 72 hours only
- **Max results:** 200 per query
- **Formats:** CSV, JSON, RSS

### 3.6 TV API (Television News)

Searches closed-caption transcripts from US and selected international TV news.

- **Endpoint:** `https://api.gdeltproject.org/api/v2/tv/tv`
- **Coverage:** 2+ million hours from 163 stations, July 2009–present
- **Search unit:** 15-second broadcast clips
- **Modes:** `ClipGallery`, `TimelineVol`, `WordCloud`, `StationChart`, `ShowChart`

### 3.7 GDELT Summary

A non-technical web interface wrapping the APIs: https://summary.gdeltproject.org

### 3.8 GDELT Analysis Service

Cloud-based visualisation and export tool: http://analysis.gdeltproject.org/

---

## 4. Schema — Event Database (GDELT 2.0)

The Event table has **58 columns** (GDELT 1.0 has 57 — GDELT 2.0 adds `SOURCEURL`). All files are **tab-delimited**, no header row, no quoting.

### 4.1 Complete Event Table Schema

| # | Field Name | Type | Description |
|---|---|---|---|
| 1 | `GLOBALEVENTID` | Integer | Globally unique event identifier |
| 2 | `SQLDATE` | Integer | Date in YYYYMMDD format |
| 3 | `MonthYear` | Integer | YYYYMM |
| 4 | `Year` | Integer | YYYY |
| 5 | `FractionDate` | Float | Fractional year (e.g., 2024.5 = July 2024) |
| **Actor 1 Fields** | | | |
| 6 | `Actor1Code` | String | CAMEO actor code (e.g., `GOVUSA`) |
| 7 | `Actor1Name` | String | Actor name as found in text |
| 8 | `Actor1CountryCode` | String | 3-char CAMEO country code |
| 9 | `Actor1KnownGroupCode` | String | Known group code (e.g., `IGO`, `MIL`) |
| 10 | `Actor1EthnicCode` | String | Ethnic group code |
| 11 | `Actor1Religion1Code` | String | Primary religion code |
| 12 | `Actor1Religion2Code` | String | Secondary religion code |
| 13 | `Actor1Type1Code` | String | Primary actor type (e.g., `GOV`, `MIL`, `REB`) |
| 14 | `Actor1Type2Code` | String | Secondary actor type |
| 15 | `Actor1Type3Code` | String | Tertiary actor type |
| **Actor 2 Fields** | | | |
| 16–25 | `Actor2Code` ... `Actor2Type3Code` | String | Same structure as Actor 1 |
| **Event Classification** | | | |
| 26 | `IsRootEvent` | Boolean (0/1) | Whether this is the "root" event of the article |
| 27 | `EventCode` | String | Full CAMEO event code (e.g., `190`) |
| 28 | `EventBaseCode` | String | Base-level code (e.g., `190`) |
| 29 | `EventRootCode` | String | Root-level code (e.g., `19`) |
| 30 | `QuadClass` | Integer | Quad classification: 1=Verbal Cooperation, 2=Material Cooperation, 3=Verbal Conflict, 4=Material Conflict |
| 31 | `GoldsteinScale` | Float | Goldstein conflict-cooperation score (-10.0 to +10.0) |
| 32 | `NumMentions` | Integer | Total mentions across all source documents |
| 33 | `NumSources` | Integer | Number of distinct source outlets |
| 34 | `NumArticles` | Integer | Number of distinct articles |
| 35 | `AvgTone` | Float | Average tone of all articles (-100 to +100; typically -10 to +10 in practice) |
| **Actor 1 Geography** | | | |
| 36 | `Actor1Geo_Type` | Integer | Location type: 0=No geo, 1=Country, 2=US State, 3=US City, 4=World City, 5=World State |
| 37 | `Actor1Geo_FullName` | String | Full location name |
| 38 | `Actor1Geo_CountryCode` | String | FIPS 10-4 country code (2-char) |
| 39 | `Actor1Geo_ADM1Code` | String | Admin-1 (state/province) code |
| 40 | `Actor1Geo_Lat` | Float | Latitude (WGS84) |
| 41 | `Actor1Geo_Long` | Float | Longitude (WGS84) |
| 42 | `Actor1Geo_FeatureID` | String | GNS/GNIS feature ID for the location |
| **Actor 2 Geography** | | | |
| 43–48 | `Actor2Geo_Type` ... `Actor2Geo_FeatureID` | | Same structure as Actor 1 Geography |
| **Action Geography** | | | |
| 49 | `ActionGeo_Type` | Integer | Location type (same coding as Actor1Geo_Type) |
| 50 | `ActionGeo_FullName` | String | Full location name where event occurred |
| 51 | `ActionGeo_CountryCode` | String | FIPS 10-4 country code |
| 52 | `ActionGeo_ADM1Code` | String | Admin-1 code |
| 53 | `ActionGeo_Lat` | Float | Latitude (WGS84) |
| 54 | `ActionGeo_Long` | Float | Longitude (WGS84) |
| 55 | `ActionGeo_FeatureID` | String | GNS/GNIS feature ID |
| **Metadata** | | | |
| 56 | `DATEADDED` | Integer | YYYYMMDDHHMMSS — when this event was added to GDELT |
| 57 | `SOURCEURL` | String | URL of the source article (GDELT 2.0 only) |

### 4.2 Mentions Table Schema (GDELT 2.0 only)

The Mentions table tracks every time a previously identified event is mentioned in a source document.

| # | Field Name | Type | Description |
|---|---|---|---|
| 1 | `GLOBALEVENTID` | Integer | Links to Events table |
| 2 | `EventTimeDate` | Integer | YYYYMMDDHHMMSS of the event |
| 3 | `MentionTimeDate` | Integer | YYYYMMDDHHMMSS of the mention |
| 4 | `MentionType` | Integer | 1=Web, 2=Citation, 3=Social, 4=TV |
| 5 | `MentionSourceName` | String | Source outlet identifier |
| 6 | `MentionIdentifier` | String | URL or citation reference |
| 7 | `SentenceID` | Integer | Sentence number in article |
| 8 | `Actor1CharOffset` | Integer | Character offset of Actor 1 |
| 9 | `Actor2CharOffset` | Integer | Character offset of Actor 2 |
| 10 | `ActionCharOffset` | Integer | Character offset of action |
| 11 | `InRawText` | Integer | 1 if extracted from raw text |
| 12 | `Confidence` | Integer | Extraction confidence (0–100) |
| 13 | `MentionDocLen` | Integer | Document length in characters |
| 14 | `MentionDocTone` | Float | Tone of the specific document |
| 15 | `MentionDocTranslationInfo` | String | Translation metadata (if translated) |
| 16 | `Extras` | String | Reserved for future fields |

### 4.3 GKG Table Schema (GDELT 2.0, V2.1 format)

The GKG is tab-delimited with complex semicolon-delimited and hash-delimited subfields within columns.

| # | Field Name | Description |
|---|---|---|
| 1 | `GKGRECORDID` | Unique record identifier (YYYYMMDDHHMMSS-[seq]-[type]) |
| 2 | `DATE` | YYYYMMDDHHMMSS timestamp |
| 3 | `SourceCollectionIdentifier` | 1=Web, 2=Citation, 3=Social, etc. |
| 4 | `SourceCommonName` | Domain name or outlet identifier |
| 5 | `DocumentIdentifier` | URL of the source document |
| 6 | `V1Counts` | Semicolon-delimited count objects (type#count#objectname#geo...) |
| 7 | `V2.1Counts` | Enhanced counts with character offsets |
| 8 | `V1Themes` | Semicolon-delimited GKG theme list |
| 9 | `V2EnhancedThemes` | Themes with character offsets |
| 10 | `V1Locations` | Semicolon-delimited locations (type#name#countrycode#adm1#lat#long#featureid) |
| 11 | `V2EnhancedLocations` | Locations with character offsets |
| 12 | `V1Persons` | Semicolon-delimited person names |
| 13 | `V2EnhancedPersons` | Persons with character offsets |
| 14 | `V1Organizations` | Semicolon-delimited organisation names |
| 15 | `V2EnhancedOrganizations` | Organisations with character offsets |
| 16 | `V1.5Tone` | Comma-delimited: Tone, PositiveScore, NegativeScore, Polarity, ActivityReferenceDensity, SelfGroupReferenceDensity, WordCount |
| 17 | `V2.1EnhancedDates` | Date references found in text with character offsets |
| 18 | `V2GCAM` | GCAM emotional/thematic scores (comma-delimited key:value pairs). 24 measurement packages, 2,300+ dimensions |
| 19 | `V2.1SharingImage` | URL of the article's social sharing image |
| 20 | `V2.1RelatedImages` | Semicolon-delimited URLs of all images in article |
| 21 | `V2.1SocialImageEmbeds` | Embedded social media image URLs |
| 22 | `V2.1SocialVideoEmbeds` | Embedded social media video URLs |
| 23 | `V2.1Quotations` | Extracted quotations with character offsets and speaker attribution |
| 24 | `V2.1AllNames` | All proper names with character offsets |
| 25 | `V2.1Amounts` | Extracted numerical amounts with units and character offsets |
| 26 | `V2.1TranslationInfo` | Source language and translation metadata |
| 27 | `V2ExtrasXML` | Additional metadata in XML format |

### 4.4 CAMEO Event Code Hierarchy

The CAMEO taxonomy has 20 root categories organised into 4 "quad classes":

**Verbal Cooperation (QuadClass 1):**

| Root Code | Category |
|---|---|
| 01 | Make public statement |
| 02 | Appeal |
| 03 | Express intent to cooperate |
| 04 | Consult |
| 05 | Engage in diplomatic cooperation |

**Material Cooperation (QuadClass 2):**

| Root Code | Category |
|---|---|
| 06 | Engage in material cooperation |
| 07 | Provide aid |
| 08 | Yield |

**Verbal Conflict (QuadClass 3):**

| Root Code | Category |
|---|---|
| 09 | Investigate |
| 10 | Demand |
| 11 | Disapprove |
| 12 | Reject |
| 13 | Threaten |

**Material Conflict (QuadClass 4):**

| Root Code | Category |
|---|---|
| 14 | Protest |
| 15 | Exhibit force posture |
| 16 | Reduce relations |
| 17 | Coerce |
| 18 | Assault |
| 19 | Fight |
| 20 | Use unconventional mass violence |

Each root code has 2-digit and 3-digit subcodes for finer granularity (e.g., `14` → `141` Demonstrate → `1411` Demonstrate for leadership change). The full code table is available at: `https://www.gdeltproject.org/data/lookups/CAMEO.eventcodes.txt`

### 4.5 Goldstein Scale

The Goldstein Scale maps each CAMEO event code to a numerical conflict-cooperation score:

- **+10.0** = maximum cooperation (e.g., military cooperation agreements)
- **0.0** = neutral
- **-10.0** = maximum conflict (e.g., use of weapons of mass destruction)

Typical ranges by root code:
- Aid provision (07): +7.0 to +9.0
- Diplomatic meetings (04): +1.0 to +3.0
- Threats (13): -4.0 to -6.0
- Armed combat (19): -8.0 to -10.0

Lookup table: `https://www.gdeltproject.org/data/lookups/CAMEO.goldsteinscale.txt`

### 4.6 Reference/Lookup Files

| File | URL |
|---|---|
| CAMEO country codes | `https://www.gdeltproject.org/data/lookups/CAMEO.country.txt` |
| FIPS country codes | `https://www.gdeltproject.org/data/lookups/FIPS.country.txt` |
| Actor type codes | `https://www.gdeltproject.org/data/lookups/CAMEO.type.txt` |
| Known group codes | `https://www.gdeltproject.org/data/lookups/CAMEO.knowngroup.txt` |
| Ethnic group codes | `https://www.gdeltproject.org/data/lookups/CAMEO.ethnic.txt` |
| Religion codes | `https://www.gdeltproject.org/data/lookups/CAMEO.religion.txt` |
| Event codes | `https://www.gdeltproject.org/data/lookups/CAMEO.eventcodes.txt` |
| Goldstein scale | `https://www.gdeltproject.org/data/lookups/CAMEO.goldsteinscale.txt` |
| CSV headers (daily) | `https://www.gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt` |
| CSV headers (historical) | `https://www.gdeltproject.org/data/lookups/CSV.header.historical.txt` |

---

## 5. Spatial Detail

### Geocoding Method

GDELT uses automated geocoding based on textual place-name mentions in articles, matched against the **GNS (GeoNames Server)** and **GNIS (Geographic Names Information System)** gazetteers, covering over 9 million named places worldwide.

### Three Geographic Anchors Per Event

Each event record has **three independent geographic references**:

1. **Actor1Geo** — Location associated with Actor 1 (often the actor's home country/city)
2. **Actor2Geo** — Location associated with Actor 2
3. **ActionGeo** — Location where the event action occurred (most relevant for spatial analysis)

For Causal Atlas, **`ActionGeo_Lat`/`ActionGeo_Long`** is the primary field of interest.

### Geo_Type Values

| Value | Meaning | Precision |
|---|---|---|
| 0 | No geographic information | N/A |
| 1 | Country | Country centroid |
| 2 | US State / equivalent | State centroid |
| 3 | US City / equivalent | City-level (~few km) |
| 4 | World city | City-level (~few km) |
| 5 | World state/province | Province centroid |

### Coordinate System

- **Datum:** WGS84
- **Precision:** Coordinates are derived from gazetteer lookups, so precision depends on the Geo_Type. City-level entries are typically the centroid of the populated place. Country-level entries use the country centroid.
- **Country codes:** FIPS 10-4 (not ISO 3166) — this is a critical interoperability note. FIPS and ISO codes differ for many countries.

### Geocoding Caveats

- When an article mentions multiple places, GDELT selects the most relevant location based on context, but this is imperfect.
- Geocoding to country centroid (Geo_Type=1) is common, meaning many events appear at the exact geometric centre of a country — this can create misleading point clusters.
- The FeatureID field links to GNS/GNIS records and can be used for disambiguation when multiple cities share a name.

### Mapping to PRIO-GRID

GDELT's WGS84 lat/long coordinates can be mapped to PRIO-GRID 0.5° cells via:
```python
import math
prio_row = math.floor((lat + 90) / 0.5)
prio_col = math.floor((lon + 180) / 0.5)
prio_gid = prio_row * 720 + prio_col + 1  # approximate; verify against PRIO-GRID docs
```

**Caution:** Events geocoded only to country level (Geo_Type=1) should be filtered out or handled separately for grid-cell analysis, as they will all cluster at the country centroid.

---

## 6. Temporal Detail

### Event Date vs. Publication Date

GDELT records two distinct timestamps:

| Field | Format | Meaning |
|---|---|---|
| `SQLDATE` | YYYYMMDD | Date the event is reported to have occurred (as interpreted from article text) |
| `DATEADDED` | YYYYMMDDHHMMSS | Timestamp when GDELT processed the article and added the event |

For time-series analysis, `SQLDATE` is the event date and `DATEADDED` reflects processing time. The gap between them reflects media reporting lag.

### Resolution

- **GDELT 1.0:** Daily resolution for event dates; daily file updates
- **GDELT 2.0:** Daily resolution for event dates (`SQLDATE` is YYYYMMDD, no sub-day precision); 15-minute update intervals for `DATEADDED`
- **GKG:** `DATE` field is YYYYMMDDHHMMSS, providing 15-minute temporal binning for article processing

### Temporal Aggregation for Causal Atlas

For monthly analysis aligned with the Causal Atlas primary temporal unit:
- Aggregate events by `SQLDATE` month (YYYYMM from `MonthYear` field)
- Count events, average GoldsteinScale, sum mentions, etc. per grid cell per month
- The `NumMentions` field can serve as a proxy for event significance/salience

---

## 7. Quality — Known Biases, Gaps, and Limitations

GDELT's automated, media-derived nature introduces several well-documented biases that are critical to understand for any analytical use.

### 7.1 Media Attention Bias

GDELT measures **media coverage**, not ground truth. Events that receive more media attention generate more GDELT records. This creates systematic biases:

- **Western/English-language over-representation:** Despite monitoring 100+ languages, English-language sources dominate. GDELT 2.0's machine translation of 65 languages partially mitigates this, but source monitoring density remains uneven.
- **Urban bias:** Events in major cities receive more coverage than rural events.
- **Conflict-type bias:** Spectacular events (bombings, large protests) are over-represented relative to slow-onset events (drought, chronic poverty).
- **"CNN effect":** International attention spikes around certain crises while ignoring others of comparable magnitude.

### 7.2 Geocoding Errors

- Estimated 20–30% of events are geocoded only to country level (Geo_Type=1), placing them at the country centroid.
- Ambiguous place names (e.g., "Springfield" exists in many US states, "Georgia" is both a US state and a country) can lead to misattribution.
- The gazetteer-based approach cannot handle novel or informal place references.
- Events described with relative spatial references ("near the border," "in the north") may be geocoded to a named place that is not the actual event location.

### 7.3 Event Coding Errors

- GDELT uses automated NLP (specifically the TABARI/PETRARCH family of event coders) to extract CAMEO events. These systems have known error rates.
- **Duplicate events:** The same real-world event reported by 50 outlets generates multiple GDELT event records. The `NumMentions`, `NumSources`, and `NumArticles` fields partially address this, and the Mentions table in GDELT 2.0 provides full deduplication traceability.
- **False positives:** Hypothetical events, historical references, and fictional narratives in news articles can be incorrectly coded as new events.
- **Actor misidentification:** Automated actor coding can confuse entities with similar names.
- **Temporal displacement:** An article published today about events from last month may be coded with today's date rather than the actual event date.

### 7.4 Source Expansion Over Time

A fundamental issue for longitudinal analysis: GDELT's source base has expanded dramatically over time. An increase in event counts from 2000 to 2020 partly reflects a real increase in global events but largely reflects the expansion of monitored news sources. **Raw event counts are not directly comparable across time periods.**

The normalization files attempt to address this:
- `http://data.gdeltproject.org/normfiles/daily.csv`
- `http://data.gdeltproject.org/normfiles/monthly.csv`
- `http://data.gdeltproject.org/normfiles/yearly.csv`

These provide total event counts per time period, allowing computation of event type proportions rather than raw counts.

### 7.5 Academic Critique

Key academic papers examining GDELT's quality:

- **Hammond & Weidmann (2014):** "Using Machine-Coded Event Data for Causal Inference: The Importance of Temporal and Spatial Granularity." Found significant geocoding errors and recommended caution when using GDELT for sub-national analysis. *(Journal of Peace Research)*
- **Ward et al. (2013):** Compared GDELT to ICEWS (Integrated Crisis Early Warning System) and found GDELT has higher volume but lower precision for conflict prediction tasks.
- **Leetaru & Schrodt (2013):** The original GDELT paper. "GDELT: Global Data on Events, Location, and Tone, 1979–2012." Describes methodology and acknowledges automated coding limitations. *(ISA Annual Convention)*
- **Steinert-Threlkeld (2018):** Showed GDELT protest data correlates with known protest events but with substantial noise.

### 7.6 Comparison with ACLED

| Dimension | GDELT | ACLED |
|---|---|---|
| Data source | Automated NLP from news | Human-coded from news + local reports |
| Precision | Lower (automated) | Higher (expert coders) |
| Volume | Very high (~500K events/day) | Lower (~500–2000 events/week) |
| Geographic precision | Often country-level | Precise coordinates for most events |
| Latency | 15 minutes | Days to weeks |
| Event types | 300+ CAMEO categories | ~30 categories |
| Cost | Free | Free for academic/humanitarian use |
| Best for | Trend detection, high-frequency monitoring | Rigorous conflict analysis |

### 7.7 Recommendations for Use

- **Never use raw event counts for trend analysis** without normalisation
- **Filter by `IsRootEvent=1`** to reduce duplicate counting
- **Filter by `Geo_Type >= 3`** (or >= 4 for non-US) for meaningful sub-national spatial analysis
- **Use `NumMentions`** as a proxy for event salience/confidence
- **Cross-validate** with curated datasets (ACLED, UCDP) for conflict events
- **GDELT is best used for:** relative comparisons (this month vs. last month in the same region), rapid event detection, media attention tracking, and as a complementary signal alongside curated data

---

## 8. Licence and Terms of Use

GDELT data is available for **unlimited and unrestricted use for any academic, commercial, or governmental purpose**, free of charge.

**Requirements:**
- **Citation:** Users must cite the GDELT Project and include a link to https://www.gdeltproject.org in any publications or products.
- **No redistribution restrictions:** There is no prohibition on redistributing derived datasets.

**Suggested citation:**
> Leetaru, Kalev, and Philip A. Schrodt. "GDELT: Global data on events, location, and tone, 1979–2012." ISA Annual Convention 2.4 (2013): 1-49.

**Note:** While GDELT itself is open, some downstream access methods have their own terms:
- **Google BigQuery:** Subject to Google Cloud pricing (query costs after free tier)
- **Source articles:** GDELT provides URLs but does not redistribute article full text. Accessing the original articles is subject to each publisher's terms.

---

## 9. Interoperability with Other Datasets

### Shared Identifiers and Linkages

| Other Dataset | Linkage Method | Notes |
|---|---|---|
| **PRIO-GRID** | Lat/long → 0.5° grid cell | ActionGeo coordinates map to PRIO-GRID cells. Filter Geo_Type >= 3 for meaningful results. |
| **ACLED** | Geo + date matching; no direct ID link | Both use lat/long; different event taxonomies. Can cross-validate conflict events in same region/time. |
| **UCDP-GED** | Geo + date matching | UCDP events can be matched to GDELT events for validation. |
| **ISO countries** | Requires FIPS→ISO conversion | GDELT uses FIPS 10-4 codes; most other datasets use ISO 3166-1 alpha-2/3. Conversion table needed. |
| **World Bank / FAO** | Country-level matching via FIPS→ISO | After code conversion, aggregate GDELT by country for comparison. |
| **CHIRPS / NDVI** | Grid-cell overlay | GDELT point events → raster grid cells for environment-conflict analysis. |
| **WFP food prices** | Market location + time matching | Match GDELT food security events to WFP market prices by proximity. |

### FIPS to ISO Country Code Conversion

This is a critical interoperability issue. GDELT uses FIPS 10-4 codes (e.g., `UK` for the United Kingdom) while most other datasets use ISO 3166 (e.g., `GB`). Many codes differ. The GDELT lookup file at `https://www.gdeltproject.org/data/lookups/FIPS.country.txt` can be used to build a conversion table.

### GKG Themes for Cross-Domain Linking

The GKG theme taxonomy includes themes directly relevant to other Causal Atlas data sources:

- `FOOD_SECURITY`, `FAMINE`, `FOOD_PRICES` → Links to WFP, FAO data
- `NATURAL_DISASTER`, `EARTHQUAKE`, `DROUGHT`, `FLOOD` → Links to EM-DAT, USGS, CHIRPS
- `HEALTH_PANDEMIC`, `DISEASE`, `EPIDEMIC` → Links to WHO, ProMED
- `DISPLACEMENT`, `REFUGEES`, `MIGRATION` → Links to UNHCR, IOM data
- `ENVIRONMENTAL_POLLUTION`, `AIR_QUALITY` → Links to OpenAQ
- `CONFLICT`, `ARMED_CONFLICT`, `PROTEST` → Links to ACLED, UCDP

---

## 10. Python Access — Libraries, Wrappers, and Code Examples

### 10.1 gdeltPyR

The primary Python library for accessing GDELT bulk data.

**Installation:**
```bash
pip install gdelt
```

**Basic usage:**
```python
import gdelt

# Initialize for GDELT 2.0
gd = gdelt.gdelt(version=2)

# Fetch events for a specific date
events = gd.Search('2024 Jan 15', table='events')
print(events.columns.tolist())  # All 58 columns
print(events.shape)

# Fetch full day of events (all 96 15-min intervals)
full_day = gd.Search('2024 Jan 15', table='events', coverage=True)

# Fetch GKG data
gkg = gd.Search('2024 Jan 15', table='gkg', coverage=True)

# Fetch Mentions table
mentions = gd.Search('2024 Jan 15', table='mentions', coverage=True)

# Date range query
events_range = gd.Search(['2024 Jan 01', '2024 Jan 07'], table='events', coverage=True)

# Get translingual (machine-translated) sources
translated = gd.Search('2024 Jan 15', table='events', translation=True, coverage=True)

# Output as GeoDataFrame (requires geopandas)
geo_events = gd.Search('2024 Jan 15', table='events', output='gpd')
```

**Supported parameters:**

| Parameter | Values | Description |
|---|---|---|
| `version` | `1` or `2` | GDELT version |
| `date` | String or list | Date(s) to query |
| `table` | `'events'`, `'gkg'`, `'mentions'` | Data table |
| `coverage` | `True`/`False` | Get all 15-min files for the day (v2 only) |
| `translation` | `True`/`False` | Use translingual files (v2 only) |
| `output` | `'json'`, `'csv'`, `'gpd'` | Output format |

**Performance note:** A full day of GDELT 2.0 events (~500 MB) processes in ~36 seconds on a 4-core/16 GB system.

**Limitations:**
- Downloads and parses CSV files in memory — large date ranges can exhaust RAM
- No built-in BigQuery integration
- Python 3 only
- Some 15-minute intervals may be missing (library warns)

### 10.2 BigQuery via google-cloud-bigquery

For analytical queries over the full dataset, BigQuery is the recommended approach.

```python
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

# Monthly conflict event counts by country
query = """
SELECT
    MonthYear,
    ActionGeo_CountryCode,
    COUNT(*) as event_count,
    AVG(GoldsteinScale) as avg_goldstein,
    AVG(AvgTone) as avg_tone,
    SUM(NumMentions) as total_mentions
FROM `gdelt-bq.gdeltv2.events`
WHERE EventRootCode IN ('18', '19', '20')
  AND SQLDATE BETWEEN 20230101 AND 20231231
  AND ActionGeo_Type >= 3
GROUP BY MonthYear, ActionGeo_CountryCode
ORDER BY MonthYear, event_count DESC
"""

df = client.query(query).to_dataframe()
```

**BigQuery setup requirements:**
1. Google Cloud account (free tier available)
2. Enable BigQuery API
3. Create service account or use `gcloud auth application-default login`
4. Install: `pip install google-cloud-bigquery pandas-gbq`

### 10.3 Direct API Access with requests

```python
import requests
import json

# DOC API — timeline of food crisis coverage in Kenya
url = "https://api.gdeltproject.org/api/v2/doc/doc"
params = {
    "query": '"food crisis" sourcecountry:KE',
    "mode": "timelinevol",
    "format": "json",
    "timespan": "3m"
}
response = requests.get(url, params=params)
data = response.json()

# GEO API — earthquake mentions as GeoJSON
url = "https://api.gdeltproject.org/api/v2/geo/geo"
params = {
    "query": "earthquake",
    "mode": "PointData",
    "format": "GeoJSON",
    "timespan": "7d"
}
response = requests.get(url, params=params)
geojson = response.json()

# Context API — sentences mentioning drought and conflict
url = "https://api.gdeltproject.org/api/v2/context/context"
params = {
    "query": "drought conflict",
    "mode": "artlist",
    "format": "json",
    "timespan": "72h",
    "MAXRECORDS": 200
}
response = requests.get(url, params=params)
sentences = response.json()
```

### 10.4 Bulk Download Script

```python
"""Download and parse GDELT 2.0 data for a date range."""
import requests
import pandas as pd
import zipfile
import io
from datetime import datetime, timedelta

GDELT2_MASTER = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
EVENT_COLUMNS = [
    'GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate',
    'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode',
    'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',
    'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code',
    'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode',
    'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code',
    'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code',
    'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode',
    'QuadClass', 'GoldsteinScale', 'NumMentions', 'NumSources',
    'NumArticles', 'AvgTone',
    'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode',
    'Actor1Geo_ADM1Code', 'Actor1Geo_Lat', 'Actor1Geo_Long',
    'Actor1Geo_FeatureID',
    'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode',
    'Actor2Geo_ADM1Code', 'Actor2Geo_Lat', 'Actor2Geo_Long',
    'Actor2Geo_FeatureID',
    'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode',
    'ActionGeo_ADM1Code', 'ActionGeo_Lat', 'ActionGeo_Long',
    'ActionGeo_FeatureID',
    'DATEADDED', 'SOURCEURL'
]

def get_event_files_for_date(date_str: str) -> list[str]:
    """Get all GDELT 2.0 event file URLs for a given date (YYYYMMDD)."""
    resp = requests.get(GDELT2_MASTER)
    urls = []
    for line in resp.text.strip().split('\n'):
        parts = line.split()
        if len(parts) == 3:
            url = parts[2]
            if date_str in url and '.export.CSV.zip' in url:
                urls.append(url)
    return urls

def download_and_parse(url: str) -> pd.DataFrame:
    """Download a single GDELT ZIP file and parse to DataFrame."""
    resp = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        csv_name = z.namelist()[0]
        with z.open(csv_name) as f:
            df = pd.read_csv(f, sep='\t', header=None,
                           names=EVENT_COLUMNS, dtype=str,
                           low_memory=False)
    return df

# Example: download one day
urls = get_event_files_for_date('20240115')
frames = [download_and_parse(u) for u in urls]
day_events = pd.concat(frames, ignore_index=True)
print(f"Downloaded {len(day_events)} events from {len(urls)} files")
```

### 10.5 Gridding GDELT Events for Causal Atlas

```python
"""Aggregate GDELT events to 0.5° grid cells (PRIO-GRID compatible)."""
import pandas as pd
import numpy as np

def assign_grid_cell(df: pd.DataFrame,
                     lat_col: str = 'ActionGeo_Lat',
                     lon_col: str = 'ActionGeo_Long',
                     resolution: float = 0.5) -> pd.DataFrame:
    """Assign each event to a 0.5-degree grid cell."""
    df = df.copy()
    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')

    # Filter to events with valid sub-national coordinates
    df = df[pd.to_numeric(df['ActionGeo_Type'], errors='coerce') >= 3]
    df = df.dropna(subset=[lat_col, lon_col])

    # Assign grid cell
    df['grid_row'] = np.floor((df[lat_col] + 90) / resolution).astype(int)
    df['grid_col'] = np.floor((df[lon_col] + 180) / resolution).astype(int)
    df['grid_id'] = df['grid_row'] * int(360 / resolution) + df['grid_col']

    return df

def monthly_grid_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate events by month and grid cell."""
    df['GoldsteinScale'] = pd.to_numeric(df['GoldsteinScale'], errors='coerce')
    df['AvgTone'] = pd.to_numeric(df['AvgTone'], errors='coerce')
    df['NumMentions'] = pd.to_numeric(df['NumMentions'], errors='coerce')

    summary = df.groupby(['MonthYear', 'grid_id']).agg(
        event_count=('GLOBALEVENTID', 'count'),
        conflict_count=('QuadClass', lambda x: (x.astype(int) == 4).sum()),
        cooperation_count=('QuadClass', lambda x: (x.astype(int) <= 2).sum()),
        avg_goldstein=('GoldsteinScale', 'mean'),
        avg_tone=('AvgTone', 'mean'),
        total_mentions=('NumMentions', 'sum'),
        grid_lat=('ActionGeo_Lat', 'mean'),
        grid_lon=('ActionGeo_Long', 'mean'),
    ).reset_index()

    return summary
```

---

## 11. Relevance to Causal Atlas

### Primary Domains

GDELT is relevant to multiple Causal Atlas domains:

| Domain | GDELT Signal | Relevant Fields/Filters |
|---|---|---|
| **Conflict** | Armed conflict, protests, violence | EventRootCode 14–20, QuadClass 3–4 |
| **Political instability** | Government actions, diplomatic events | EventRootCode 01–05, Actor types GOV/MIL |
| **Food security** | Media coverage of food crises | GKG themes: FOOD_SECURITY, FAMINE |
| **Natural disasters** | Coverage of earthquakes, floods, droughts | GKG themes: NATURAL_DISASTER, EARTHQUAKE |
| **Health** | Epidemic/pandemic coverage | GKG themes: HEALTH_PANDEMIC, DISEASE |
| **Migration** | Displacement and refugee coverage | GKG themes: DISPLACEMENT, REFUGEES |
| **Economic** | Economic events, sanctions, trade | EventRootCode 06, 08, 16; GKG: ECON_* themes |

### Causal Chains GDELT Can Illuminate

1. **Climate event → media attention → political response:** Track how weather events lead to news coverage, then to government statements/actions (CAMEO codes 01–05)
2. **Conflict escalation sequences:** Time-lagged patterns from verbal conflict (QuadClass 3) to material conflict (QuadClass 4)
3. **Food price spikes → protests:** Correlate WFP price data with GDELT protest events (root code 14) in the same region
4. **Natural disaster → displacement → conflict:** Track disaster coverage → migration themes → conflict events with spatial and temporal lags
5. **Media attention as a leading indicator:** Spikes in GDELT GKG themes (food security, disease) may precede peaks in domain-specific datasets

### Recommended Use Within Causal Atlas

GDELT should be used as a **complementary signal**, not a primary ground-truth source:

1. **Use GDELT for:** High-frequency event monitoring (15-min), media attention tracking, broad thematic trend detection, rapid cross-domain correlation discovery
2. **Use curated sources for validation:** Cross-validate GDELT conflict signals with ACLED/UCDP, disaster signals with EM-DAT, food security signals with WFP/FAO
3. **GKG over Events table:** The GKG provides richer thematic and emotional data. The GCAM emotional scores (2,300+ dimensions) are unique to GDELT and valuable for sentiment-based causal analysis.
4. **Normalise before comparing:** Always use event proportions or per-article rates, never raw counts, for longitudinal analysis

### Data Volume Estimates for Causal Atlas

| Scope | Approximate Size |
|---|---|
| 1 month of GDELT 2.0 events (global) | ~15 GB uncompressed |
| 1 year of GDELT 2.0 events (global) | ~180 GB uncompressed |
| Filtered to conflict events (QuadClass 4) with sub-national geo | ~5% of total ≈ 9 GB/year |
| Monthly grid-cell aggregation (0.5°) | ~100 MB/year |

---

## 12. GDELT 3.0 and Latest Developments

> **Verified:** March 2026. Source: https://blog.gdeltproject.org/gdelt-3-0-coming-soon/

### GDELT 3.0 Infrastructure Transition

GDELT 3.0 represents a major infrastructure upgrade that began rolling out in late 2020. The transition is phased:

| Component | Status (March 2026) |
|-----------|-------------------|
| Global Difference Graph | Transitioned to 3.0 |
| Visual Global Knowledge Graph (VGKG) | Transitioned to 3.0 |
| Core web monitoring and processing | Transitioning in phases |
| Event Database | Available in both 2.0 and 3.0 formats |
| Global Knowledge Graph | Available in both 2.0 and 3.0 formats |

### What's New in 3.0

**1-Minute JSON Updates:**
- Both Event and GKG datasets now available in **JSON-formatted files updated every minute** (in addition to the existing 15-minute CSV files)
- This is a major improvement for near-real-time monitoring applications

**Backward Compatibility (Critical):**
- All GDELT 2.0 datasets **continue indefinitely in their exact present form**
- No changes to file format, file location, or delivery schedule
- Existing code requires **no modifications** — GDELT 2.0 users can continue as-is
- The 2.0 CSV files continue to update every 15 minutes

**Expanded Monitoring:**
- New outlets added to the monitored source base
- New supported languages (specific languages not disclosed)
- Globally distributed infrastructure for improved reliability

**Visual Global Knowledge Graph Upgrade:**
- The VGKG has been upgraded to the new 3.0 infrastructure
- Opens possibilities for future image-analysis capabilities as visual content becomes more important to understanding global events

### Implications for Causal Atlas

- The 1-minute JSON updates enable higher-frequency monitoring if needed, though our primary temporal unit is monthly
- No migration effort required — existing GDELT 2.0 access patterns continue to work
- JSON format may be easier to parse than tab-delimited CSV for new ingestion pipelines
- Monitor the GDELT blog for announcements of new capabilities

---

## 13. Complete CAMEO Event Code Taxonomy

The CAMEO (Conflict and Mediation Event Observations) taxonomy defines **310 event codes** organized hierarchically under **20 root categories**. Each event has a 2-digit root code, a 3-digit base code, and an optional 4-digit specific code.

### The 20 Root Categories

| Root Code | Category | QuadClass | Goldstein Range | Description |
|-----------|----------|-----------|-----------------|-------------|
| **01** | MAKE PUBLIC STATEMENT | 1 (Verbal Cooperation) | -0.4 to +3.4 | Public remarks, declarations, commentary |
| **02** | APPEAL | 1 (Verbal Cooperation) | +1.0 to +3.4 | Requests for cooperation, aid, protection |
| **03** | EXPRESS INTENT TO COOPERATE | 1 (Verbal Cooperation) | +4.0 to +7.4 | Stated intention to engage in cooperation |
| **04** | CONSULT | 1 (Verbal Cooperation) | +1.0 to +5.2 | Meetings, phone calls, visits, discussions |
| **05** | ENGAGE IN DIPLOMATIC COOPERATION | 2 (Material Cooperation) | +2.8 to +7.4 | Praise, endorse, defend, mediate |
| **06** | ENGAGE IN MATERIAL COOPERATION | 2 (Material Cooperation) | +4.0 to +8.3 | Economic, military, judicial cooperation; intelligence sharing |
| **07** | PROVIDE AID | 2 (Material Cooperation) | +7.0 to +8.3 | Humanitarian, military, economic aid; grant asylum |
| **08** | YIELD | 2 (Material Cooperation) | +5.0 to +7.4 | Concede, comply, release, ease sanctions |
| **09** | INVESTIGATE | 3 (Verbal Conflict) | -0.4 to +1.0 | Investigate, inspect, monitor |
| **10** | DEMAND | 3 (Verbal Conflict) | -3.4 to -5.0 | Demands for cooperation, aid, rights, change |
| **11** | DISAPPROVE | 3 (Verbal Conflict) | -2.2 to -5.0 | Criticize, denounce, accuse, complain |
| **12** | REJECT | 3 (Verbal Conflict) | -4.0 to -5.0 | Reject proposals, refuse to cooperate |
| **13** | THREATEN | 3 (Verbal Conflict) | -5.8 to -7.0 | Threaten with sanctions, force, restrictions |
| **14** | PROTEST | 4 (Material Conflict) | -6.5 to -6.5 | Demonstrations, strikes, boycotts, obstruction |
| **15** | EXHIBIT MILITARY POSTURE | 4 (Material Conflict) | -7.2 to -7.2 | Military mobilisation, exercises, fortification |
| **16** | REDUCE RELATIONS | 4 (Material Conflict) | -4.4 to -7.0 | Reduce diplomatic relations, expel, boycott |
| **17** | COERCE | 4 (Material Conflict) | -7.0 to -8.3 | Seize, detain, impose sanctions, ban travel |
| **18** | ASSAULT | 4 (Material Conflict) | -8.3 to -9.2 | Physical assault, sexual violence, torture, kill |
| **19** | FIGHT | 4 (Material Conflict) | -9.2 to -10.0 | Conventional military force: small arms, artillery, air strikes |
| **20** | USE UNCONVENTIONAL MASS VIOLENCE | 4 (Material Conflict) | -10.0 | Mass killings, ethnic cleansing, chemical/biological weapons |

### Quad Classification System

The 20 root codes map to 4 "quad classes" used for high-level aggregation:

| QuadClass | Meaning | Root Codes | Goldstein Range |
|-----------|---------|------------|-----------------|
| 1 | Verbal Cooperation | 01–04 | Positive (low) |
| 2 | Material Cooperation | 05–08 | Positive (high) |
| 3 | Verbal Conflict | 09–13 | Negative (low) |
| 4 | Material Conflict | 14–20 | Negative (high) |

### Selected Sub-Codes (Conflict-Relevant for Causal Atlas)

| Code | Description | Goldstein |
|------|-------------|-----------|
| 1411 | Demonstrate or rally | -6.5 |
| 1412 | Conduct hunger strike | -6.5 |
| 1413 | Conduct strike or boycott | -6.5 |
| 1414 | Obstruct passage or block | -6.5 |
| 1451 | Demonstrate military or police power | -6.5 |
| 1711 | Impose restrictions on political freedoms | -7.0 |
| 1712 | Ban political parties or politicians | -7.0 |
| 1721 | Impose curfew | -8.3 |
| 1722 | Impose state of emergency | -8.3 |
| 1723 | Arrest, detain | -8.3 |
| 1724 | Expel or deport | -8.3 |
| 1811 | Abduct, hijack, take hostage | -8.3 |
| 1812 | Physically assault | -8.3 |
| 1813 | Conduct torture | -9.0 |
| 1814 | Kill by physical assault | -9.0 |
| 1822 | Conduct suicide or car bombing | -9.2 |
| 1823 | Carry out roadside attack | -9.2 |
| 1831 | Assassinate | -9.0 |
| 1911 | Impose blockade | -9.2 |
| 1912 | Occupy territory | -9.2 |
| 1931 | Fight with small arms and light weapons | -10.0 |
| 1932 | Fight with artillery and tanks | -10.0 |
| 1941 | Conduct air or missile strike | -10.0 |
| 2001 | Engage in mass expulsion | -10.0 |
| 2002 | Engage in mass killing | -10.0 |
| 2003 | Engage in ethnic cleansing | -10.0 |

### Lookup Files

The complete CAMEO code lists are available at:
- Event codes: `https://www.gdeltproject.org/data/lookups/CAMEO.eventcodes.txt`
- Goldstein scale: `https://www.gdeltproject.org/data/lookups/CAMEO.goldsteinscale.txt`
- Machine-readable format: https://github.com/tenthe/CAMEO-Event-Data-Codebook

---

## 14. GKG Themes Taxonomy

### Scale

The GKG theme taxonomy contains **over 2,500 distinct themes** as of 2026, composed of:

| Source | Approximate Count | Description |
|--------|-------------------|-------------|
| **World Bank Taxonomy** | ~2,200 themes | Covers agriculture, education, health, governance, social development, urban development, water, etc. |
| **GDELT Core Themes** | ~150+ themes | Conflict, disaster, health, migration, environment, economy, etc. |
| **Custom/Emerging Themes** | Growing | Added periodically as new topics emerge (100+ added in a single 2019 update) |

### Themes Relevant to Causal Atlas Domains

| Domain | Key GKG Themes | Notes |
|--------|---------------|-------|
| **Conflict** | `CONFLICT`, `ARMED_CONFLICT`, `CIVIL_WAR`, `INSURGENCY`, `TERRORISM`, `PROTEST`, `RIOT` | Direct conflict monitoring |
| **Food Security** | `FOOD_SECURITY`, `FAMINE`, `FOOD_PRICES`, `HUNGER`, `MALNUTRITION`, `CROP_FAILURE` | Cross-validate with WFP data |
| **Natural Disasters** | `NATURAL_DISASTER`, `EARTHQUAKE`, `DROUGHT`, `FLOOD`, `CYCLONE`, `TSUNAMI`, `WILDFIRE` | Cross-validate with EM-DAT |
| **Health** | `HEALTH_PANDEMIC`, `DISEASE`, `EPIDEMIC`, `EBOLA`, `CHOLERA`, `MALARIA`, `COVID19` | Cross-validate with WHO |
| **Migration** | `DISPLACEMENT`, `REFUGEES`, `MIGRATION`, `INTERNALLY_DISPLACED`, `ASYLUM` | Cross-validate with UNHCR |
| **Environment** | `ENVIRONMENTAL_POLLUTION`, `AIR_QUALITY`, `DEFORESTATION`, `CLIMATE_CHANGE`, `WATER_SCARCITY` | Cross-validate with OpenAQ |
| **Economy** | `ECON_*` (multiple), `INFLATION`, `UNEMPLOYMENT`, `POVERTY`, `TRADE`, `SANCTIONS` | Cross-validate with World Bank |
| **Governance** | `ELECTION`, `CORRUPTION`, `HUMAN_RIGHTS`, `RULE_OF_LAW`, `DEMOCRACY` | Contextual signals |

### Theme Lookup File

The current themes lookup is available at:
- `http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_CategoryList.xlsx`
- Updated periodically — check https://blog.gdeltproject.org for announcements of new theme additions

### Using Themes in Queries

**BigQuery example — food security media attention by country:**
```sql
SELECT
    DATE(PARSE_TIMESTAMP('%Y%m%d%H%M%S', CAST(DATE AS STRING))) AS date,
    Locations,
    COUNT(*) as article_count
FROM `gdelt-bq.gdeltv2.gkg`
WHERE Themes LIKE '%FOOD_SECURITY%'
  AND DATE > 20240101000000
GROUP BY date, Locations
ORDER BY article_count DESC
LIMIT 100
```

---

## 15. GCAM (Global Content Analysis Measures) — Deep Dive

### Overview

GCAM is the emotional and thematic content analysis component of GDELT. It runs **18 content analysis systems** totaling **over 2,230 latent dimensions** on every news article monitored by GDELT, in near-real-time.

GCAM represents the "Language and Tone" portions of the GDELT acronym (Global Database of Events, Language, and Tone).

### The 18 Content Analysis Systems

| # | System | Dimensions | Focus |
|---|--------|------------|-------|
| 1 | **WordNet Affect 1.0** | ~280 | Emotion categories (anger, joy, fear, surprise, etc.) |
| 2 | **WordNet Affect 1.1** | ~280 | Extended emotion taxonomy |
| 3 | **Linguistic Inquiry and Word Count (LIWC)** | ~80 | Psycholinguistic categories (anxiety, certainty, power, etc.) |
| 4 | **General Inquirer V1.02** (Harvard IV-4) | ~180 | Psychosocial categories (positive, negative, strong, weak, etc.) |
| 5 | **Lexicoder Sentiment Dictionary** | ~2 | Positive and negative sentiment |
| 6 | **Lexicoder Topic Dictionaries** | ~50 | Policy topics (economy, health, immigration, etc.) |
| 7 | **Loughran & McDonald Financial Sentiment** | ~6 | Financial text sentiment (positive, negative, uncertainty, litigious, etc.) |
| 8 | **Opinion Observer** | ~4 | Polarity detection |
| 9 | **Regressive Imagery Dictionary** | ~43 | Primary/secondary process thinking, emotions |
| 10 | **Roget's Thesaurus (1911)** | ~1,000 | 1,000 semantic categories |
| 11 | **SentiWordNet 3.0** | ~3 | Positivity, negativity, objectivity scores |
| 12 | **SentiWords** | ~1 | Continuous sentiment score |
| 13 | **Subjectivity Lexicon** | ~4 | Strong/weak subjective, positive/negative |
| 14 | **Body Boundary Dictionary** | ~20 | Body-related imagery |
| 15 | **WordNet Domains 3.2** | ~170 | Domain categorization (sport, medicine, law, etc.) |
| 16 | **WordNet 3.1 Lexical Categories** | ~26 | Lexical categorization (noun types, verb types, etc.) |
| 17 | **Forest Values** | ~10 | Environmental/forest values |
| 18 | **GDELT GKG Themes** | Varies | GDELT's own thematic extraction |

### Multilingual Support

GCAM natively assesses emotions in **15 languages** without requiring machine translation:
Arabic, Basque, Catalan, Chinese, French, Galician, German, Hindi, Indonesian, Korean, Pashto, Portuguese, Russian, Spanish, and Urdu.

Articles in other languages are processed after machine translation to English.

### GCAM Code Structure

Each GCAM dimension is identified by a code in the format `cXX.YY`:
- `XX` = content analysis system number (e.g., `c5` = Lexicoder Sentiment)
- `YY` = dimension number within that system

**Examples:**
| GCAM Code | System | Dimension |
|-----------|--------|-----------|
| `c1.1` | WordNet Affect 1.0 | Joy |
| `c1.4` | WordNet Affect 1.0 | Anger |
| `c5.1` | Lexicoder Sentiment | Positive |
| `c5.2` | Lexicoder Sentiment | Negative |
| `c6.4` | LIWC | Anxiety |
| `c6.5` | LIWC | Anger |
| `c6.6` | LIWC | Sadness |
| `c9.1` | General Inquirer | Positive |
| `c9.2` | General Inquirer | Negative |

### Score Types

Each GCAM dimension reports two values:
- **Word Count**: Number of words in the article matching the dimension's dictionary
- **Score/Density**: Proportion of total words matching (word count / total article words)

### Data Access

GCAM scores are embedded in the **GKG 2.0** data stream. In the GKG tab-delimited files, GCAM occupies column V2.1GCAM (column 18 in 0-indexed format), containing semicolon-separated `code:count:score` triplets.

### The GCAM Master Codebook

Complete reference for all 2,230+ dimensions:
`http://data.gdeltproject.org/documentation/GCAM-MASTER-CODEBOOK.TXT`

### Relevance for Causal Atlas

GCAM provides a unique capability: measuring the **emotional temperature** of media coverage at planetary scale. Potential applications:

- Track anxiety/fear in coverage of a region before conflict events (leading indicator?)
- Measure shifts in tone around food security or health crises
- Compare emotional intensity of coverage across regions for the same event type
- Use GCAM sentiment as a control variable when analysing GDELT event counts

---

## 16. Tone Measurement Methodology

### AvgTone Field

The `AvgTone` field in the GDELT Event Database measures the **average tone** of all documents mentioning an event in the first 15-minute update interval when the event was first detected.

### Score Range

| Range | Interpretation |
|-------|---------------|
| -100 to -10 | Extremely negative (rare) |
| -10 to -5 | Very negative |
| -5 to -1 | Moderately negative |
| -1 to +1 | Neutral |
| +1 to +5 | Moderately positive |
| +5 to +10 | Very positive |
| +10 to +100 | Extremely positive (rare) |

**Typical range:** Most events fall between **-10 and +10**, with 0 as neutral.

### Computation

The exact NLP algorithm for computing individual document tone scores is **not publicly disclosed**. What is known:
- Each article mentioning the event receives a tone score based on sentiment analysis of the article text
- The `AvgTone` for the event is the arithmetic mean of all document-level tone scores
- The computation runs in the first 15-minute update cycle when the event appears

### Interpreting Tone

Tone is a measure of **media framing**, not objective severity. GDELT suggests:
- A riot event with slightly negative tone (~-2) likely reflects a minor occurrence
- The same event type with extremely negative tone (~-8) suggests far greater perceived severity
- Tone acts as a proxy for the **perceived impact** or **salience** of an event

### Tone in the GKG

The GKG provides a richer tone measurement via the `V1.5Tone` field (column 16), containing 6 comma-separated values:
1. Average tone
2. Positive score
3. Negative score
4. Polarity (positive - negative)
5. Activity Reference Density
6. Self/Group Reference Density

### Limitations

- Tone is biased by the source's editorial position — the same event gets different tone scores from different outlets
- English-language bias: tone computation works best on English text
- Machine-translated articles may have distorted tone scores
- Tone measures media perception, not ground truth severity

---

## 17. Visual Global Knowledge Graph (VGKG)

> Source: https://blog.gdeltproject.org/announcing-the-new-gdelt-visual-global-knowledge-graph-vgkg/

### Overview

The VGKG extends GDELT's analysis from text to **images**, applying deep learning via the **Google Cloud Vision API** to categorize news imagery at scale.

### Processing Scale

- **500,000 to 1,000,000 images processed daily** from news sources worldwide
- Updated every **15 minutes** (CSV files released at ~0–5, ~15–20, ~30–35, ~40–45 minutes past each hour)
- Covers nearly every event type and topic from almost every corner of the earth

### Annotations Produced

Each image undergoes multiple analysis passes:

| Annotation Type | Description | Example Output |
|----------------|-------------|----------------|
| **Object/Activity Tagging** | Identifies objects, activities, and backgrounds | "military vehicle", "crowd", "fire", "building" |
| **OCR (Text Recognition)** | Reads text in images (signs, banners, documents) | Reads handwritten Arabic on protest signs |
| **Facial Sentiment** | Detects emotional expressions in faces | Joy, sorrow, anger, surprise (per face detected) |
| **Landmark Detection** | Identifies famous locations | "Eiffel Tower", "Tahrir Square" |
| **Content-Based Geolocation** | Estimates image location from visual cues | Coordinates inferred from landmarks/scenery |
| **Logo Detection** | Identifies organizational logos | "Red Cross", "United Nations" |
| **SafeSearch** | Content moderation flags | Violence, adult content, medical imagery flags |

### Data Access

| Method | Detail |
|--------|--------|
| **BigQuery** | Table: `gdelt-bq:gdeltv2.cloudvision` |
| **CSV files** | Tab-delimited, gzip-compressed, updated every 15 minutes |
| **File format** | Documented in VGKG V1.0 Alpha codebook |

### Limitations

- Labeled as **"alpha/experimental"** — GDELT explicitly states that "mistaken categorizations represent computer algorithm errors, NOT editorial statements"
- Deep learning image recognition has inherent error rates, particularly for:
  - Images from unfamiliar cultural contexts
  - Low-quality news imagery
  - Ambiguous scenes
- Not suitable as ground truth — best used as a supplementary signal

### Relevance for Causal Atlas

The VGKG could provide:
- Visual evidence tracking (e.g., satellite imagery of destruction, protest crowd sizes)
- Cross-validation of text-based event detection with visual confirmation
- However, the alpha status and error rates suggest it should be a low-priority integration

---

## 18. BigQuery Cost Estimates for Causal Atlas Queries

### GDELT Dataset Sizes in BigQuery

| Dataset | Table | Approximate Size |
|---------|-------|-----------------|
| GDELT 2.0 Events | `gdelt-bq.gdeltv2.events` | ~1.5 TB (growing) |
| GDELT 2.0 Event Mentions | `gdelt-bq.gdeltv2.eventmentions` | ~3 TB (growing) |
| GDELT 2.0 GKG | `gdelt-bq.gdeltv2.gkg` | ~2.65 TB per year (growing) |
| GDELT 1.0 Events | `gdelt-bq.full.events` | ~500 GB |
| GDELT VGKG | `gdelt-bq.gdeltv2.cloudvision` | ~1 TB (growing) |

### BigQuery Pricing (as of 2026)

- **On-demand:** $6.25 per TB of data scanned
- **First 1 TB per month:** Free
- **Storage:** $0.02/GB/month (active), $0.01/GB/month (long-term)
- Charges are rounded up to the nearest MB, with a 10 MB minimum per table referenced

### Cost Estimates for Typical Causal Atlas Queries

| Query Type | Data Scanned | Estimated Cost | Notes |
|-----------|-------------|----------------|-------|
| Monthly conflict events by country, 1 year | ~1.5 TB (full events table scan) | ~$9.38 | Full table scan if not using partitioned tables |
| Same query with partitioned table (1 year) | ~150 GB | ~$0.94 | Use `_PARTITIONTIME` filter |
| Same query with partitioned table (1 month) | ~12 GB | Free (under 1 TB) | |
| GKG food security themes, 1 month | ~220 GB | ~$1.38 | GKG table is much larger |
| GKG food security themes, 7 days with table decorator | ~54 GB | Free (under 1 TB) | Table decorators dramatically reduce scan |
| Full GKG scan, 1 year | ~2.65 TB | ~$16.56 | Avoid this — use filters |

### Cost Optimization Strategies

1. **Use partitioned tables:** GDELT provides partitioned BigQuery tables (`gdelt-bq.gdeltv2.events_partitioned`). Filtering by `_PARTITIONTIME` restricts scans to relevant date ranges.

2. **Table decorators:** Limit scans to recent data using BigQuery's snapshot decorators. A 7-day GKG decorator reduces 2.65 TB to ~54 GB.

3. **Column selection:** Always `SELECT` only needed columns rather than `SELECT *`.

4. **Dry runs:** Use `bq query --dry_run` to estimate cost before running.

5. **Caching:** BigQuery caches query results for 24 hours — re-running the same query is free.

6. **Materialized views:** For repeated analyses, create materialized views of filtered/aggregated data.

### Performance Benchmarks

| Operation | Time | Data Processed |
|-----------|------|----------------|
| Query 423 GB of event data | ~8.6 seconds | 423 GB |
| Query 15 GB via partitioned table (15 days) | ~2 seconds | 15 GB |
| Count unique URLs across 35 billion rows | ~4 minutes | Multiple TB |
| Complex georeferencing on multi-TB dataset | ~tens of seconds | Multi-TB |
| Parse 8.9 TB JSON archive into 321 billion values | ~2.5 minutes | 8.9 TB |

---

## 19. GDELT's Systematic Biases — Detailed Analysis

### 19.1 English-Language and Western Bias

**The core problem:** Despite monitoring 100+ languages and machine-translating 65 languages, GDELT's source monitoring density is heavily weighted toward English-language and Western media.

**Quantified evidence:**
- US media is disproportionately overrepresented in GDELT's source base
- A comparative study found that GDELT's top news sources and those of the Event Registry platform "did not overlap at all" — suggesting GDELT's source selection is not representative of the global media landscape (ONS, 2023)
- Western reporting perspective introduces systematic bias in how events are framed, which actors are named, and which events are deemed newsworthy

**Implications:**
- Events in countries with limited English-language media presence are under-represented
- The same real-world event magnitude produces fewer GDELT records in non-Western countries
- Tone scores are biased by Western editorial perspectives
- Countries with lower press freedom scores have systematically lower event counts

### 19.2 Geocoding Accuracy

**Country centroid problem:**
- Estimated 20–30% of events are geocoded only to country level (`Geo_Type=1`), placing them at the country's geometric centroid
- This creates **false hotspots** at country centroids. Example: Kaduna (near Nigeria's centroid) appears as a kidnapping hotspot in GDELT data, but this reflects geocoding default behavior, not actual event concentration (Source: OpenNews/Simpson, 2014)
- For a country like Nigeria, events that mention "Nigeria" but no specific city will all cluster at the centroid coordinates

**Place name ambiguity:**
- "Springfield" exists in dozens of US states
- "Georgia" is both a US state and a Caucasus country
- Gazetteer-based matching cannot resolve novel or informal references ("near the border," "in the north")

**Quantified accuracy:**
- One analysis found the overall accuracy rate of key GDELT fields to be **approximately 55%** (Solvang et al., 2025, via MDPI Data journal)
- Sub-national geocoding reliability varies enormously by country and data density

### 19.3 The "Echo Chamber" / Duplication Problem

This is GDELT's most fundamental quality issue for event-level analysis.

**How it works:**
- A single real-world event reported by 50 news outlets generates **multiple GDELT event records** — potentially 50+ records for one actual event
- The Chibok schoolgirl kidnapping (a single event) produced **151 simultaneous GDELT records** on April 14, 2014
- FiveThirtyEight reported 2,285 kidnappings in Nigeria's first 4 months of 2014 based on GDELT — but this counted **news stories about kidnappings**, not actual kidnapping events
- GDELT is fundamentally a **repository of media reports, not discrete events** (Simpson, 2014)

**Why it matters:**
- Raw event counts are meaningless without deduplication
- Trend analysis on raw counts conflates media attention changes with actual event frequency changes
- The echo chamber effect is amplified for high-profile events that receive sustained media coverage

**Partial mitigations built into GDELT:**
- `NumMentions` — count of mentions in the first 15-minute window (higher = more coverage = potentially more significant event, but also potentially more duplication)
- `NumSources` — count of unique source domains
- `NumArticles` — count of unique articles
- `IsRootEvent` — flag indicating the "root" version of an event (filtering on `IsRootEvent=1` reduces but does not eliminate duplication)
- The Mentions table in GDELT 2.0 provides full traceability from events to individual article mentions

### 19.4 Event Coding Errors

- **False positives:** Hypothetical events ("if war breaks out"), historical references ("the 2003 invasion"), and fictional narratives can be incorrectly coded as new events
- **Actor misidentification:** Automated actor coding confuses entities with similar names
- **Temporal displacement:** Articles published today about last month's events may be coded with today's date
- **Category errors:** The automated CAMEO coding has inherent error rates — exact error rates are not publicly disclosed but academic studies suggest significant misclassification
- Data redundancy measured at approximately **20%** across the dataset

### 19.5 Source Expansion Artifact

GDELT's monitored source base has expanded dramatically over time. This creates a **fundamental confound** for longitudinal analysis:

- An increase in GDELT event counts from 2005 to 2025 partly reflects real changes in global events
- But it **largely reflects** the expansion of monitored news sources and languages
- Raw event counts are **not directly comparable across time periods**

**Normalization files** (critical for any time-series use):
- Daily: `http://data.gdeltproject.org/normfiles/daily.csv`
- Monthly: `http://data.gdeltproject.org/normfiles/monthly.csv`
- Yearly: `http://data.gdeltproject.org/normfiles/yearly.csv`
- Country-level variants also available (daily_country, monthly_country, yearly_country)

**Correct approach:** Always compute event **proportions** (event count / total events) rather than raw counts for trend analysis.

### 19.6 Algorithmic Transparency

The UK Office for National Statistics assessed GDELT and noted: "Only one of the algorithms that extract and compile the data is described in detail, making it impossible to reconstruct the process." The events database involves "aggregation of individual news articles into events, adding a further layer of unexplained complexity" (ONS, 2023).

---

## 20. Deduplication Strategies for GDELT

### Why Deduplication Is Essential

GDELT's data redundancy is approximately **20%**, and for high-profile events, duplication can be vastly higher (100+ records for a single event). Any analytical use of GDELT requires a deduplication strategy.

### Published Deduplication Strategies (DDS)

Recent academic research (Solvang et al., 2025; Oswald et al., 2025) has proposed five deduplication strategies of increasing strictness:

| Strategy | Method | Fields Matched | Strictness |
|----------|--------|---------------|------------|
| **DDS1** | Baseline | No deduplication | None |
| **DDS2** | Same-URL + Location + Date | URL, Date, Latitude, Longitude, EventRootCode | Moderate |
| **DDS3** | Same-URL + Location within year | URL, Latitude, Longitude, EventRootCode (within same year) | Moderate-High |
| **DDS4** | DDS3 + Actor matching | Apply DDS3 first, then merge rows with same Actor1, Actor2, Date, Location, EventRootCode | High |
| **DDS5** | DDS3 + Actor matching (date-relaxed) | Apply DDS3 first, then merge rows with same Actor1, Actor2, Location, EventRootCode (date-relaxed) | Very High |

### Practical Deduplication Approach for Causal Atlas

```python
"""
GDELT deduplication pipeline for Causal Atlas.
Uses a multi-step approach combining built-in fields and custom deduplication.
"""
import pandas as pd
import numpy as np


def deduplicate_gdelt(df: pd.DataFrame, strategy: str = "moderate") -> pd.DataFrame:
    """
    Deduplicate GDELT events using a tiered approach.

    Parameters:
        df: Raw GDELT events DataFrame
        strategy: "light", "moderate", or "strict"
    """
    df = df.copy()
    original_count = len(df)

    # Step 1: Filter to root events only (built-in GDELT dedup)
    df = df[df["IsRootEvent"].astype(int) == 1]
    print(f"After IsRootEvent filter: {len(df)} ({len(df)/original_count:.1%})")

    if strategy == "light":
        return df

    # Step 2: Remove events with same SOURCEURL, date, location, and event code
    df["dedup_key_2"] = (
        df["SOURCEURL"].fillna("")
        + "|" + df["SQLDATE"].astype(str)
        + "|" + df["ActionGeo_Lat"].fillna("").astype(str)
        + "|" + df["ActionGeo_Long"].fillna("").astype(str)
        + "|" + df["EventRootCode"].fillna("").astype(str)
    )
    df = df.drop_duplicates(subset=["dedup_key_2"], keep="first")
    print(f"After URL+date+location dedup: {len(df)} ({len(df)/original_count:.1%})")

    if strategy == "moderate":
        return df.drop(columns=["dedup_key_2"])

    # Step 3 (strict): Also merge by actor pair + location + event code
    df["dedup_key_3"] = (
        df["Actor1Code"].fillna("")
        + "|" + df["Actor2Code"].fillna("")
        + "|" + df["SQLDATE"].astype(str)
        + "|" + df["ActionGeo_Lat"].fillna("").astype(str)
        + "|" + df["ActionGeo_Long"].fillna("").astype(str)
        + "|" + df["EventRootCode"].fillna("").astype(str)
    )
    # Keep the record with the most mentions (likely most reliable)
    df["NumMentions"] = pd.to_numeric(df["NumMentions"], errors="coerce").fillna(0)
    df = df.sort_values("NumMentions", ascending=False).drop_duplicates(
        subset=["dedup_key_3"], keep="first"
    )
    print(f"After actor+date+location dedup: {len(df)} ({len(df)/original_count:.1%})")

    return df.drop(columns=["dedup_key_2", "dedup_key_3"])
```

### Validation

Deduplication effectiveness should be validated by comparing GDELT event counts against a reference dataset (ACLED or ICEWS) for the same region/time period. After deduplication, GDELT and ACLED conflict event counts should be in the same order of magnitude (though GDELT will still be higher due to broader event scope).

---

## 21. GDELT vs ACLED: Side-by-Side Case Studies

### Case Study 1: Nigeria Kidnapping Data (2014)

This is the most extensively documented example of GDELT-ACLED divergence.

| Metric | GDELT | ACLED | Ground Truth |
|--------|-------|-------|--------------|
| Kidnapping events, Nigeria, Jan–Apr 2014 | 2,285 (per FiveThirtyEight) | ~50–80 (estimated) | Unknown |
| Events on April 14, 2014 (Chibok kidnapping) | 151 | 1 | 1 |
| What it actually measured | News stories about kidnappings | Distinct kidnapping events | — |

**Root cause:** GDELT counted media reports, not discrete events. The Chibok schoolgirl abduction was one event that generated massive global media coverage. GDELT recorded each article as a separate "event."

**Geocoding issue:** GDELT showed Kaduna state as a kidnapping hotspot. But Kaduna is near Nigeria's geographic centroid — it was the default geocode when NLP could not extract a specific location from the article text.

**Lesson:** For event-level conflict analysis at sub-national resolution, ACLED is reliable; GDELT requires extensive deduplication and geocoding quality filters before it can be used for event counting.

### Case Study 2: General Conflict Event Comparison

From ACLED's own comparison working paper (2019):

| Dimension | GDELT | ACLED |
|-----------|-------|-------|
| Event identification | Automated NLP — identifies "who did what to whom" from article text | Human researcher reads article and codes discrete event |
| Actor coding | Automated extraction — frequent misidentification | Expert-coded with regional knowledge |
| Location precision | Gazetteer lookup — often country-level | Human geocoding — typically settlement-level |
| Fatalities | Not coded as a field | Conservatively estimated, explicitly recorded |
| Duplicates | Inherent — one event = many records | Merged — multiple reports coded as one event |
| Source languages | 100+ (machine-translated) | 20+ (human multilingual researchers) |

### When to Use Which

| Use Case | Recommended Dataset | Rationale |
|----------|-------------------|-----------|
| Rigorous conflict event counting | ACLED | Human-coded, deduplicated, geocoded |
| Sub-national spatial analysis | ACLED | Higher geocoding precision |
| Fatality estimation | ACLED (or UCDP-GED) | Explicitly coded field |
| High-frequency trend detection | GDELT | 15-minute updates vs weekly |
| Media attention measurement | GDELT | This is what GDELT actually measures well |
| Cross-domain thematic monitoring | GDELT (GKG) | 2,500+ themes across all domains |
| Emotional/sentiment analysis | GDELT (GCAM) | 2,230+ sentiment dimensions — unique capability |
| Broad geographic scanning | GDELT | Global, real-time, no access restrictions |
| Academic publication on conflict | ACLED or UCDP-GED | Peer-reviewed methodology, accepted by journals |

---

## 22. Dataset Size and Performance Reference

### Full GDELT Dataset Size (2026 Estimates)

| Component | Records | Uncompressed Size | BigQuery Size |
|-----------|---------|-------------------|---------------|
| Event Database (1979–2026) | ~700+ million records | ~30+ TB | ~1.5 TB |
| Event Mentions (2015–2026) | ~5+ billion records | ~50+ TB | ~3+ TB |
| GKG (2015–2026) | ~1+ billion records | ~25+ TB (2.5 TB/year) | ~2.65 TB/year |
| GKG (2013–2015, v1) | ~300 million records | ~5 TB | ~2 TB |
| VGKG (2016–2026) | ~3+ billion images | ~10+ TB | ~1+ TB |
| **Total** | — | **~120+ TB** | **~10+ TB** |

### Daily Data Volume

| Stream | Daily Records | Daily Size (compressed) |
|--------|---------------|------------------------|
| Events | ~500K–1M records | ~500 MB |
| GKG | ~500K–1M articles | ~2–3 GB |
| Mentions | ~5M+ mentions | ~1–2 GB |
| VGKG | ~500K–1M images | ~1 GB |

### Query Time Benchmarks (BigQuery)

| Query | Data Scanned | Time |
|-------|-------------|------|
| Full events table scan (1 year) | ~150 GB (partitioned) | ~5–10 seconds |
| Filtered events (1 country, 1 year) | ~15 GB | ~2 seconds |
| GKG theme search (7 days) | ~54 GB | ~3–5 seconds |
| Full GKG scan (1 year) | ~2.65 TB | ~30–60 seconds |
| Complex aggregation on multi-TB data | Multi-TB | ~tens of seconds |

---

## 23. Worked Example: Region Filtering, Deduplication, PRIO-GRID Aggregation

```python
"""
Complete GDELT pipeline for Causal Atlas:
  1. Download GDELT 2.0 events for a date range
  2. Filter to a specific region and conflict events
  3. Deduplicate
  4. Filter to sub-national geocoding quality
  5. Assign PRIO-GRID cells
  6. Aggregate to monthly grid-cell summaries
  7. Save as Parquet
"""

import requests
import pandas as pd
import numpy as np
import zipfile
import io
from pathlib import Path
from datetime import datetime, timedelta


# --- Column definitions ---

EVENT_COLUMNS = [
    'GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate',
    'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode',
    'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',
    'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code',
    'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode',
    'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code',
    'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code',
    'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode',
    'QuadClass', 'GoldsteinScale', 'NumMentions', 'NumSources',
    'NumArticles', 'AvgTone',
    'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode',
    'Actor1Geo_ADM1Code', 'Actor1Geo_Lat', 'Actor1Geo_Long',
    'Actor1Geo_FeatureID',
    'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode',
    'Actor2Geo_ADM1Code', 'Actor2Geo_Lat', 'Actor2Geo_Long',
    'Actor2Geo_FeatureID',
    'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode',
    'ActionGeo_ADM1Code', 'ActionGeo_Lat', 'ActionGeo_Long',
    'ActionGeo_FeatureID',
    'DATEADDED', 'SOURCEURL'
]


# --- FIPS to ISO country code mapping (subset) ---

FIPS_TO_ISO = {
    'NI': 'NGA', 'ET': 'ETH', 'SO': 'SOM', 'SU': 'SDN', 'OD': 'SSD',
    'CG': 'COD', 'CF': 'COG', 'KE': 'KEN', 'UG': 'UGA', 'BY': 'BDI',
    'RW': 'RWA', 'BC': 'BWA', 'SF': 'ZAF', 'SY': 'SYR', 'YM': 'YEM',
    'IZ': 'IRQ', 'AF': 'AFG', 'PK': 'PAK', 'UP': 'UKR', 'RS': 'RUS',
    'ML': 'MLI', 'UV': 'BFA', 'NG': 'NER', 'CD': 'TCD', 'CM': 'CMR',
    # Add more as needed from CAMEO.country.txt
}


# --- Step 1: Download events ---

def download_gdelt_day(date_str: str) -> pd.DataFrame:
    """Download all GDELT 2.0 event files for a date (YYYYMMDD)."""
    master_url = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
    resp = requests.get(master_url, timeout=60)
    urls = []
    for line in resp.text.strip().split('\n'):
        parts = line.split()
        if len(parts) == 3 and date_str in parts[2] and '.export.CSV.zip' in parts[2]:
            urls.append(parts[2])

    frames = []
    for url in urls:
        try:
            r = requests.get(url, timeout=60)
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                csv_name = z.namelist()[0]
                with z.open(csv_name) as f:
                    df = pd.read_csv(f, sep='\t', header=None,
                                     names=EVENT_COLUMNS, dtype=str,
                                     low_memory=False)
            frames.append(df)
        except Exception as e:
            print(f"  Error downloading {url}: {e}")

    if not frames:
        return pd.DataFrame(columns=EVENT_COLUMNS)

    return pd.concat(frames, ignore_index=True)


def download_gdelt_range(start: str, end: str) -> pd.DataFrame:
    """Download GDELT events for a date range (YYYYMMDD format)."""
    start_dt = datetime.strptime(start, '%Y%m%d')
    end_dt = datetime.strptime(end, '%Y%m%d')
    frames = []
    current = start_dt
    while current <= end_dt:
        date_str = current.strftime('%Y%m%d')
        print(f"Downloading {date_str}...")
        day_df = download_gdelt_day(date_str)
        frames.append(day_df)
        current += timedelta(days=1)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# --- Step 2: Filter to region and conflict ---

def filter_conflict_events(
    df: pd.DataFrame,
    country_fips: str | None = None,
    lat_range: tuple | None = None,
    lon_range: tuple | None = None,
) -> pd.DataFrame:
    """Filter to conflict events (QuadClass 4) in a specific region."""
    df = df.copy()

    # Convert types
    df['QuadClass'] = pd.to_numeric(df['QuadClass'], errors='coerce')
    df['ActionGeo_Type'] = pd.to_numeric(df['ActionGeo_Type'], errors='coerce')
    df['ActionGeo_Lat'] = pd.to_numeric(df['ActionGeo_Lat'], errors='coerce')
    df['ActionGeo_Long'] = pd.to_numeric(df['ActionGeo_Long'], errors='coerce')
    df['IsRootEvent'] = pd.to_numeric(df['IsRootEvent'], errors='coerce')
    df['GoldsteinScale'] = pd.to_numeric(df['GoldsteinScale'], errors='coerce')
    df['AvgTone'] = pd.to_numeric(df['AvgTone'], errors='coerce')
    df['NumMentions'] = pd.to_numeric(df['NumMentions'], errors='coerce')

    # Filter to material conflict events
    df = df[df['QuadClass'] == 4]

    # Filter to sub-national geocoding (Geo_Type >= 3 for non-US, >= 4 for world cities)
    df = df[df['ActionGeo_Type'] >= 3]

    # Filter by country if specified
    if country_fips:
        df = df[df['ActionGeo_CountryCode'] == country_fips]

    # Filter by lat/lon bounding box if specified
    if lat_range:
        df = df[(df['ActionGeo_Lat'] >= lat_range[0]) & (df['ActionGeo_Lat'] <= lat_range[1])]
    if lon_range:
        df = df[(df['ActionGeo_Long'] >= lon_range[0]) & (df['ActionGeo_Long'] <= lon_range[1])]

    return df.dropna(subset=['ActionGeo_Lat', 'ActionGeo_Long'])


# --- Step 3: Deduplicate ---

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Apply moderate deduplication strategy."""
    original = len(df)

    # Keep root events only
    df = df[df['IsRootEvent'] == 1]

    # Deduplicate by source URL + date + location + event code
    df['_dedup'] = (
        df['SOURCEURL'].fillna('')
        + '|' + df['SQLDATE'].astype(str)
        + '|' + df['ActionGeo_Lat'].astype(str)
        + '|' + df['ActionGeo_Long'].astype(str)
        + '|' + df['EventRootCode'].fillna('').astype(str)
    )
    df = df.drop_duplicates(subset=['_dedup'], keep='first')
    df = df.drop(columns=['_dedup'])

    print(f"Deduplication: {original} -> {len(df)} ({len(df)/original:.1%} retained)")
    return df


# --- Step 4: Assign PRIO-GRID cells ---

def assign_grid(df: pd.DataFrame, resolution: float = 0.5) -> pd.DataFrame:
    """Assign events to 0.5-degree PRIO-GRID cells."""
    df = df.copy()
    ncols = int(360 / resolution)
    df['grid_row'] = np.floor((df['ActionGeo_Lat'] + 90) / resolution).astype(int)
    df['grid_col'] = np.floor((df['ActionGeo_Long'] + 180) / resolution).astype(int)
    df['prio_gid'] = df['grid_row'] * ncols + df['grid_col']
    return df


# --- Step 5: Monthly aggregation ---

def aggregate_monthly_grid(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to monthly grid-cell summaries."""
    return df.groupby(['MonthYear', 'prio_gid']).agg(
        event_count=('GLOBALEVENTID', 'count'),
        conflict_events=('QuadClass', lambda x: (x == 4).sum()),
        protest_events=('EventRootCode', lambda x: (x == '14').sum()),
        fight_events=('EventRootCode', lambda x: (x == '19').sum()),
        assault_events=('EventRootCode', lambda x: (x == '18').sum()),
        avg_goldstein=('GoldsteinScale', 'mean'),
        avg_tone=('AvgTone', 'mean'),
        total_mentions=('NumMentions', 'sum'),
        unique_sources=('SOURCEURL', 'nunique'),
        grid_lat=('ActionGeo_Lat', 'mean'),
        grid_lon=('ActionGeo_Long', 'mean'),
    ).reset_index()


# --- Step 6: Save ---

def save_parquet(df: pd.DataFrame, path: str):
    """Save to Parquet."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, engine='pyarrow', compression='snappy', index=False)
    print(f"Saved {len(df)} rows to {path}")


# --- Full pipeline ---

def run_gdelt_pipeline(
    start_date: str,
    end_date: str,
    country_fips: str = 'NI',  # Nigeria
    output_dir: str = './data/gdelt',
):
    """Run the complete GDELT conflict pipeline."""
    print(f"=== GDELT Pipeline: {country_fips} from {start_date} to {end_date} ===")

    raw = download_gdelt_range(start_date, end_date)
    print(f"Downloaded {len(raw)} raw events")

    filtered = filter_conflict_events(raw, country_fips=country_fips)
    print(f"Filtered to {len(filtered)} conflict events")

    deduped = deduplicate(filtered)
    gridded = assign_grid(deduped)
    monthly = aggregate_monthly_grid(gridded)

    iso = FIPS_TO_ISO.get(country_fips, country_fips)
    output = f"{output_dir}/{iso.lower()}_{start_date}_{end_date}_gdelt_monthly.parquet"
    save_parquet(monthly, output)

    print(f"\nSummary:")
    print(f"  Grid cells: {monthly['prio_gid'].nunique()}")
    print(f"  Months: {monthly['MonthYear'].nunique()}")
    print(f"  Total events: {monthly['event_count'].sum()}")


# Usage:
# run_gdelt_pipeline('20240101', '20240131', country_fips='NI')
```

---

## 24. Sources

### Official Documentation

| Resource | URL |
|---|---|
| GDELT Project homepage | https://www.gdeltproject.org |
| GDELT Blog (primary documentation) | https://blog.gdeltproject.org |
| Data access page | https://www.gdeltproject.org/data.html |
| GDELT 2.0 overview | https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/ |
| GDELT 3.0 announcement | https://blog.gdeltproject.org/gdelt-3-0-coming-soon/ |
| VGKG upgrade to 3.0 | https://blog.gdeltproject.org/visual-global-knowledge-graph-upgrading-to-gdelt-3-0-infrastructure/ |
| Event Codebook V2.0 (PDF) | http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf |
| GKG Codebook V2.1 (PDF) | http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf |
| GCAM Master Codebook | http://data.gdeltproject.org/documentation/GCAM-MASTER-CODEBOOK.TXT |
| GCAM introduction blog | https://blog.gdeltproject.org/introducing-the-global-content-analysis-measures-gcam/ |
| CAMEO Manual v1.1b3 | http://data.gdeltproject.org/documentation/CAMEO.Manual.1.1b3.pdf |
| CAMEO codes (machine-readable) | https://github.com/tenthe/CAMEO-Event-Data-Codebook |
| VGKG V1.0 Alpha codebook | http://data.gdeltproject.org/documentation/GDELT-Visual_Global_Knowledge_Graph-V1.0Alpha.pdf |
| VGKG announcement blog | https://blog.gdeltproject.org/announcing-the-new-gdelt-visual-global-knowledge-graph-vgkg/ |
| Datasets overview (Feb 2016) | https://blog.gdeltproject.org/the-datasets-of-gdelt-as-of-february-2016/ |
| GKG themes lookup (Nov 2021) | https://blog.gdeltproject.org/new-november-2021-gkg-2-0-themes-lookup/ |
| World Bank taxonomy in GKG | https://blog.gdeltproject.org/world-bank-group-topical-taxonomy-now-in-gkg/ |
| BigQuery table decorators (cost) | https://blog.gdeltproject.org/using-bigquery-table-decorators-to-lower-query-cost/ |
| Partitioned BigQuery tables | https://blog.gdeltproject.org/announcing-partitioned-gdelt-bigquery-tables/ |
| BigQuery demos compilation | https://blog.gdeltproject.org/a-compilation-of-gdelt-bigquery-demos/ |
| GDELT dataset size analysis | https://blog.gdeltproject.org/creating-a-planetary-scale-open-dataset-just-how-big-is-gdelt/ |

### API Documentation

| API | Blog Post / Reference |
|---|---|
| DOC 2.0 API | https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ |
| GEO 2.0 API | https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/ |
| TV API | https://blog.gdeltproject.org/gdelt-2-0-television-api-debuts/ |
| Context 2.0 API | https://blog.gdeltproject.org/announcing-the-gdelt-context-2-0-api/ |
| GDELT Summary (web UI) | https://summary.gdeltproject.org |
| GDELT Analysis Service | http://analysis.gdeltproject.org/ |
| TV News Visual Explorer | https://api.gdeltproject.org/api/v2/tvv/tvv |

### BigQuery

| Resource | Detail |
|---|---|
| Project ID | `gdelt-bq` |
| GDELT 2.0 dataset | `gdeltv2` |
| GDELT 1.0 dataset | `full` |
| Key tables | `gdeltv2.events`, `gdeltv2.eventmentions`, `gdeltv2.gkg`, `gdeltv2.cloudvision` |
| Partitioned events | `gdeltv2.events_partitioned` |
| BigQuery pricing | $6.25/TB scanned (first 1 TB/month free) |

### Python Libraries

| Library | URL |
|---|---|
| gdeltPyR (pip: `gdelt`) | https://github.com/linwoodc3/gdeltPyR |
| google-cloud-bigquery | https://pypi.org/project/google-cloud-bigquery/ |
| GDELT HuggingFace datasets | https://huggingface.co/datasets/dwb2023/gdelt-mentions-2025-v2 |

### Academic References

| Citation | Relevance |
|---|---|
| Leetaru, K. & Schrodt, P.A. (2013). "GDELT: Global Data on Events, Location, and Tone, 1979–2012." ISA Annual Convention. | Original GDELT paper; methodology description |
| Hammond, J. & Weidmann, N.B. (2014). "Using Machine-Coded Event Data for Causal Inference." *Journal of Peace Research*. | Geocoding quality assessment |
| Ward, M.D. et al. (2013). Comparison of GDELT and ICEWS for conflict prediction. | Quality comparison with ICEWS |
| Steinert-Threlkeld, Z.C. (2018). Validation of GDELT protest data. | Protest event validation |
| Schrodt, P.A. (2012). "CAMEO: Conflict and Mediation Event Observations Event and Actor Codebook." | CAMEO taxonomy documentation |
| Simpson, E. (2014). "GDELT and the Problem of Decontextualized Data." *Source: An OpenNews Project*. https://source.opennews.org/articles/gdelt-decontextualized-data/ | Nigeria kidnapping case study; reports-vs-events problem |
| ONS (2023). "GDELT Data Quality Note." UK Office for National Statistics. https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/methodologies/globaldatabaseofeventslanguageandtonegdeltdataqualitynote | Algorithmic transparency, source coverage, quality assessment |
| Solvang et al. (2025). "Research on the Development and Application of the GDELT Event Database." *Data* (MDPI), 10(10), 158. https://www.mdpi.com/2306-5729/10/10/158 | 55% accuracy rate, 20% redundancy, deduplication strategies |
| Oswald et al. (2025). "Deduplication of the media-based event databases." *Journal of Computational Social Science*. https://link.springer.com/article/10.1007/s42001-025-00409-4 | DDS1-DDS5 deduplication strategies; comparison with ACLED/ICEWS |
| Weidmann & Rød (2019). *The Internet and Political Protest in Autocracies.* Oxford University Press. | GDELT bias in non-democratic contexts |

### Lookup Files

All available at `https://www.gdeltproject.org/data/lookups/`:
- `CAMEO.eventcodes.txt`, `CAMEO.goldsteinscale.txt`, `CAMEO.country.txt`, `FIPS.country.txt`, `CAMEO.type.txt`, `CAMEO.knowngroup.txt`, `CAMEO.ethnic.txt`, `CAMEO.religion.txt`

### Normalisation Files

Available at `http://data.gdeltproject.org/normfiles/`:
- `daily.csv`, `daily_country.csv`, `monthly.csv`, `monthly_country.csv`, `yearly.csv`, `yearly_country.csv`

### GKG Theme Lists

- Full theme list: `http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_CategoryList.xlsx`
- GitHub community list: https://github.com/CatoMinor/GDELT-GKG-Themes

---

*Last verified: March 2026*
