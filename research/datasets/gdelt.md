# GDELT — Global Database of Events, Language, and Tone

> Deep-dive research for Causal Atlas. Findings as of March 2025.

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

## 12. Sources

### Official Documentation

| Resource | URL |
|---|---|
| GDELT Project homepage | https://www.gdeltproject.org |
| GDELT Blog (primary documentation) | https://blog.gdeltproject.org |
| Data access page | https://www.gdeltproject.org/data.html |
| GDELT 2.0 overview | https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/ |
| Event Codebook V2.0 (PDF) | http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf |
| GKG Codebook V2.1 (PDF) | http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf |
| GCAM Master Codebook | http://data.gdeltproject.org/documentation/GCAM-MASTER-CODEBOOK.TXT |
| CAMEO Manual | http://data.gdeltproject.org/documentation/CAMEO.Manual.1.1b3.pdf |
| Datasets overview (Feb 2016) | https://blog.gdeltproject.org/the-datasets-of-gdelt-as-of-february-2016/ |

### API Documentation

| API | Blog Post / Reference |
|---|---|
| DOC 2.0 API | https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ |
| GEO 2.0 API | https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/ |
| TV API | https://blog.gdeltproject.org/gdelt-2-0-television-api-debuts/ |
| Context 2.0 API | https://blog.gdeltproject.org/announcing-the-gdelt-context-2-0-api/ |
| GDELT Summary (web UI) | https://summary.gdeltproject.org |
| GDELT Analysis Service | http://analysis.gdeltproject.org/ |

### BigQuery

| Resource | Detail |
|---|---|
| Project ID | `gdelt-bq` |
| GDELT 2.0 dataset | `gdeltv2` |
| GDELT 1.0 dataset | `full` |
| Key tables | `gdeltv2.events`, `gdeltv2.eventmentions`, `gdeltv2.gkg` |

### Python Libraries

| Library | URL |
|---|---|
| gdeltPyR (pip: `gdelt`) | https://github.com/linwoodc3/gdeltPyR |
| google-cloud-bigquery | https://pypi.org/project/google-cloud-bigquery/ |

### Academic References

| Citation | Relevance |
|---|---|
| Leetaru, K. & Schrodt, P.A. (2013). "GDELT: Global Data on Events, Location, and Tone, 1979–2012." ISA Annual Convention. | Original GDELT paper; methodology description |
| Hammond, J. & Weidmann, N.B. (2014). "Using Machine-Coded Event Data for Causal Inference." *Journal of Peace Research*. | Geocoding quality assessment |
| Ward, M.D. et al. (2013). Comparison of GDELT and ICEWS for conflict prediction. | Quality comparison with ICEWS |
| Steinert-Threlkeld, Z.C. (2018). Validation of GDELT protest data. | Protest event validation |
| Schrodt, P.A. (2012). "CAMEO: Conflict and Mediation Event Observations Event and Actor Codebook." | CAMEO taxonomy documentation |

### Lookup Files

All available at `https://www.gdeltproject.org/data/lookups/`:
- `CAMEO.eventcodes.txt`, `CAMEO.goldsteinscale.txt`, `CAMEO.country.txt`, `FIPS.country.txt`, `CAMEO.type.txt`, `CAMEO.knowngroup.txt`, `CAMEO.ethnic.txt`, `CAMEO.religion.txt`

### Normalisation Files

Available at `http://data.gdeltproject.org/normfiles/`:
- `daily.csv`, `daily_country.csv`, `monthly.csv`, `monthly_country.csv`, `yearly.csv`, `yearly_country.csv`

---

*Last verified: March 2025*
