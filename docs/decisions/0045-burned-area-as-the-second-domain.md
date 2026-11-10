# 0045: Burned area is the second domain, and its first use is a known answer

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

Five iterations on real data have stayed inside climate. The one result that meets rule 2 is El Niño leading drought (`results/real-enso-continents.md`), a climate-to-climate link. Twenty-five more climate series added nothing beyond it four or more months ahead (`results/real-indices-2.md`). The owner's aim is relationships between separate data sets, and the brief's question is about signals from other domains. Conflict, the outcome the project started with, is parked: published climate-to-conflict effects are below what this search can hear (`docs/reading/real-link-sizes.md`).

The review the owner read on 2026-11-09 proposed adding one data set at a time, each with a known link to rediscover first. A bounded reading chose the data set: `docs/reading/second-domain.md`.

## Decision

1. **The second domain is burned area: ESA Fire_cci FireCCILT11, version 1.1.** Monthly, global, 0.25 degree, 1982 to 2018 without 1994, from the AVHRR satellites. Fetched whole on 2026-11-10 (432 files, 7.2 GB, no account), entered in `data/manifest.toml` and `docs/data-sources.md` in the same commit as this record.
2. **Its first use is a known answer, not a discovery:** is El Niño named, blind among decoys, as a driver of burned area, and does it then improve a forecast four or more months ahead on years never read. Rule: `results/fire-enso.md`, committed before any number on burned area is computed.
3. **Before the known answer, what the search can hear on this record is measured with a planted link**, field by field. The record is 37 years against the drought file's 75, and burned area is zero for much of the year in most places, so a silence must be told apart from deafness.
4. **This sets aside one line of the brief's "Not now" list, "more domains", for this one data set.** That list says each item needs a Phase 1 result and the owner's yes. There is a Phase 1 result. The yes is read from decision 0040, as that record says: new data sets may be fetched when the work needs them, one at a time, each named with its reason. This is that reading applied, and it is his to overrule. Nothing else on the list is touched.

## Considered and not done

- **Vegetation greenness (PKU GIMMS NDVI, 1982 to 2022)** was the reading's second choice: a longer record with no missing year, but the link from drought to greenness is mostly within a season, so it tests little about leads. Not fetched.
- **NOAA's NDVI record (about 1 TB), GFED5, crop yields, food prices, dengue counts:** each dropped in the reading for size, licence, access, record length or being annual. Reasons in the reading page.
- **Registering with the Fire CCI project,** which its terms encourage and do not require. It would send an address to an outside service (rule 10). Not done.
- **Taking a size from the published link.** Chen et al. (2016) report that about half of global burned area is predictable from one ocean index; read at source, that figure is the best of 14 indices and 10 lead times on 18 annual values per cell, in sample. Only the direction and the regions are taken from it.

## Consequences

- The project now holds an outcome that is not a climate index. A pass on it would be the first cross-domain result here, though still a link others have published.
- The scored years for burned area are 2004 to 2018, fifteen years: a shorter confirmation than drought's twenty-five, with a wider interval and a coarser control.
- If the known answer is recovered, the next question is the first that is not already answered in print for this method: does local drought, cell by cell, add to a forecast of burned area beyond own history and El Niño.
- If the search is deaf on this record, that is published as a limit of the method on short, mostly-zero records, and the choice of a third data set takes it into account.
- This is the first result built on the corrected search (decision 0044), so it gets an independent fresh reader, covering that decision too.
