"""Describe the table of the held data in one shape (data/table/) one series at a time and write docs/table-first-count.md: counts, gaps, flags and year-to-year memory by domain and by source. Every query here reads a single series at a time; none relates one series to another."""
import json
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data" / "table"
DOC = ROOT / "docs" / "table-first-count.md"
LEAST_PAIRS = 20  # consecutive pairs of periods, for a place's series to give a memory
IDX = "case when length(o.period) = 4 then cast(o.period as int) else cast(left(o.period, 4) as int) * 12 + cast(right(o.period, 2) as int) - 1 end"
NOTES = """## What the first count showed

- **Crops are 158 of the 259 items under code 1700.** The brief's "single crop" is read as an item with an area-harvested row; the rest are processed products and livestock products (oils, wine, milk, meat). Each crop has up to three series: yield, area harvested, production.
- **The crop file is UTF-8**, not Latin-1 as `yields.py` reads it (that only damages accents in names, which `yields.py` does not use). The table reads it as UTF-8.
- **Estimated and imputed figures are over a third of the crop values** (flag shares above). The flag is kept on every value so a finder or the referee can set them aside.
- **Eleven crop places have no Natural Earth shape**: the ended countries (Belgium-Luxembourg, Czechoslovakia, Ethiopia PDR, Sudan (former), USSR, Yugoslav SFR, Serbia and Montenegro) and four overseas departments of France. They keep the source's name and no latitude or longitude.
- **Drought exists for 184 of Natural Earth's 234 coded countries**: the rest have no half-degree cell centre inside them with a value in every month, which is the rule of the harvest test, kept as it is.
- **Fire: about 11% of burnable half-degree cells have their centre in no country** (coastal cells), so they are in no country's total. Zero burned area is common (about 29% of country-months). The makers' 1994 gap is a gap, not a zero.
- **Conflict: 0.9% of events fall outside every country shape** and are set aside; a country-month with no event has no row.
- **The climate files run well beyond the years the earlier tests used** (the sunspot series from 1749, the ocean indices from 1870, most to 2026); the table keeps every month the file holds. The manifest's "1950 to 2024" describes the window those tests used.
- **Prices**: 35 of the file's 37 countries have a staple price as collected. Values are in each country's own currency, so levels are not comparable between countries until they are brought to each series' own past.
- **World Development Indicators (added 2026-11-11): 609 of 1,498 indicators kept, by a count rule.** Kept: licence `CC BY-4.0` in the series file (9 dropped: 6 SIPRI terms, 3 CC BY 3.0 IGO) and at least 100 countries (of those that map to the table's places) each with at least 30 yearly values (880 of the 1,489 licensed indicators dropped; 885 fail the count rule whatever their licence). 215 places carry values; 217 country rows in the Bank's country file, of which the Channel Islands and Kosovo have no Natural Earth match and are set aside (23,771 values); 48 regional and income aggregates (1,539,985 values) are dropped; the file's `INX` code has no values.
- **WDI domains follow the first part of the Bank's topic, as the brief said.** Thirteen first parts became nine domains (economic policy and debt is economy, private sector and trade and trade are trade, gender and social protection are social, policy and institutions is public sector; none of the kept indicators has a topic that fits no domain). So **population is not a domain**: the 64 kept indicators whose topic names population sit under health, and the 23 under energy production and use sit under environment.
- **WDI kind and transform follow the name and unit text and the lowest value**: shares, rates and ratios (a percent sign, "per 1,000", rate, growth, ratio, share) are `rate`, `none`; indices and scores are `index`, `none`; the rest are quantities, `level` with `log` if every value is above zero, `log1p` if the lowest is zero, `none` if any is negative (302 rate, 9 index, 122 log, 99 log1p, 77 none). None is `count`: this page fills the months with no row with zero for count series only, and a missing year in a World Development Indicator is not a zero. The unit is the bracket that ends the name, else the series file's unit of measure; the bracket is sometimes not a unit ("GPI", "GDP").
- **WDI figures carry no flag here**, though many are estimates or gap-filled by the Bank or UN agencies; the file's footnotes are not used. The newest years are thin: 100,646 values in 2023, 89,512 in 2024, 57,622 in 2025, among the kept series. Education (16.5%), trade (7.2%) and infrastructure (9.0%) have the most missing inside their spans.
- **The memory of the World Development Indicators is that of trending levels** (median 0.97, lower quartile 0.85): a description of each series, not a measure of anything predictable.
- **FAOSTAT consumer prices and exchange rates (added 2026-11-11): six series, 332,489 values, by month.** `faostat_cp` holds the general and the food consumer price index (2015 = 100) and the food price inflation (percent), months only (the file has no year's-value rows), 2000-01 to 2026-06 (inflation from 2001), in 202 places; the file's weighted-average and median items are for groups of countries only and give no series. `faostat_pe` holds the official exchange rate in local currency units per US dollar by month (1970-01 to 2026-07) and by year, and the standard local currency element by year only (the restatement of old years in the current currency), in 221 places. Dropped or set aside, all counted in the notes above: 73,476 group rows in the price file (area codes 5000 and over), 111 rows with no value (flag L), the places with no Natural Earth match (Sub-Saharan Africa, a group with a low code, and French Guiana, Guadeloupe, Martinique, Mayotte, Netherlands Antilles, Reunion, the ended Czechoslovakia, Sudan (former) and Yugoslav SFR), and 1,342 exchange-rate rows where a country has two currencies in one period (a changeover; the level in local units is ambiguous there).
- **FAOSTAT price flags: X is most of the values.** In the consumer price file 54% are X (from an outside organisation, kept as `other`), 32% E and 9% I, 5% official; every food inflation value is flagged E. In the exchange rate file 99.9% are X. Base year 2015 is in the unit text; FAO rescales the whole index if it changes. The two price indices and the exchange rates are levels that trend or jump at a redenomination, so their memory is near 1.00 (inflation 0.96, a description of each series and not of anything predictable). Values in the price index run from 0.67 to 2.9 trillion (the log keeps them usable), and inflation from -67% to 372,000%.
- **Values at or below zero under a `log` transform** are the 85 zero yields; area and production, which hold many zeros, carry `log1p`.
"""
FLAGS = ("official", "estimated", "imputed", "other", "none")


def connect():
    """DuckDB over the three Parquet tables, with each observation's period as a whole number and its value on the scale the series table names."""
    con = duckdb.connect()
    con.execute("set threads=3")
    for t in ("series", "place", "obs"):
        con.execute(f"create view {t} as select *{', split_part(source, chr(46), 1) as grp' if t == 'series' else ''} from read_parquet('{TABLE / (t + '.parquet')}')")
    con.execute(f"""create table o as select o.series_id, place_id, {IDX} as idx, value, coalesce(flag, 'none') as flag, s.grp as source, s.domain, s.kind, s.transform, s.period as step
        from obs o join series s using (series_id)""")
    return con


def span(con):
    """Per series and place: values present, periods in the place's own span (first to last), for the share missing inside the span."""
    con.execute("""create table sp as select series_id, place_id, any_value(source) as source, any_value(domain) as domain, any_value(kind) as kind, count(*) as present, max(idx) - min(idx) + 1 as expected from o group by 1, 2""")


def by(con, key):
    """Counts of series, values, the share missing inside each place's span and the share of values by flag, grouped by `key` (domain or source)."""
    group = {"domain": "domain", "source": "grp"}[key]
    rows = con.execute(f"""select s.{group}, count(distinct s.series_id), min(s."first"), max(s."last"), sum(sp.present), 1 - sum(sp.present) / sum(sp.expected)
        from series s join sp on sp.series_id = s.series_id group by 1 order by 1""").fetchall()
    shares = {r[0]: r[1:] for r in con.execute(f"""select {key}, {", ".join(f"avg((flag = '{f}')::int)" for f in FLAGS)} from o group by 1""").fetchall()}
    return [(*r, *shares[r[0]]) for r in rows]


def places_by(con, key):
    """Places that hold at least one value, per group, counted from the place level (world counts as one)."""
    return dict(con.execute(f"select {key}, count(distinct place_id) from o group by 1").fetchall())


def memory(con):
    """The year-to-year (month-to-month) memory of each place's series on its own: the correlation of its transformed values with its values one period before, pairs of consecutive periods only. A log needs a value above zero, so other values are set aside and counted; a count series has the periods with no row filled with zero, between the series' first and last period, for places that have any row (the source records events, not their absence)."""
    con.execute("""create table t as select series_id, place_id, idx, source, domain,
        case transform when 'log' then ln(value) when 'log1p' then ln(1 + value) else value end as y from o where transform <> 'log' or value > 0""")
    con.execute("""create table dense as select g.series_id, g.place_id, i.idx, g.source, g.domain, coalesce(t.y, 0) as y from
        (select series_id, place_id, any_value(source) as source, any_value(domain) as domain from o where kind = 'count' group by 1, 2) g
        join (select series_id, min(idx) as lo, max(idx) as hi from o where kind = 'count' group by 1) r using (series_id)
        cross join unnest(generate_series(r.lo, r.hi)) as i(idx)
        left join (select * from t) t on t.series_id = g.series_id and t.place_id = g.place_id and t.idx = i.idx""")
    con.execute("""create table m0 as select * from t where series_id not in (select series_id from series where kind = 'count') union all select * from dense""")
    con.execute(f"""create table acf as select series_id, place_id, any_value(source) as source, any_value(domain) as domain, count(*) as pairs, corr(y, prev) as r from
        (select *, lag(y) over w as prev, idx - lag(idx) over w as gap from m0 window w as (partition by series_id, place_id order by idx)) where gap = 1 group by 1, 2 having count(*) >= {LEAST_PAIRS} and stddev_pop(y) > 0 and stddev_pop(prev) > 0""")


def memory_by(con, key):
    """Number of series-and-place units with a memory, and the lower quartile, median and upper quartile of their memory, by `key`."""
    return con.execute(f"select {key}, count(*), quantile_cont(r, 0.25), median(r), quantile_cont(r, 0.75) from acf group by 1 order by 1").fetchall()


def per_series(con):
    """One line per series: places, values, share missing inside the place spans, and the median memory over its places."""
    return con.execute(f"""select s.series_id, s.domain, s.source, s.period as step, s.kind, s.transform, s."first", s."last", count(distinct sp.place_id) as places, sum(sp.present) as v, 1 - sum(sp.present) / sum(sp.expected) as missing,
        (select median(r) from acf a where a.series_id = s.series_id) as memory from series s join sp using (series_id) group by all order by 1""").fetchall()


def prices_alone(con):
    """One line for each series of the two FAOSTAT price files: places, places with at least 120 monthly values, first and last period, values, share missing inside the place spans, shares of values by flag, and the median memory over its places."""
    sources = "('faostat_cp', 'faostat_pe')"
    rows = con.execute(f"""select s.series_id, s.period, count(*), count(*) filter (where sp.present >= 120 and s.period = 'month'), s."first", s."last", sum(sp.present), 1 - sum(sp.present) / sum(sp.expected),
        (select median(r) from acf a where a.series_id = s.series_id) from series s join sp using (series_id) where s.source in {sources} group by all order by 1""").fetchall()
    shares = {r[0]: r[1:] for r in con.execute(f"select series_id, {', '.join(f"avg((flag = '{f}')::int)" for f in FLAGS[:4])} from o where source in {sources} group by 1").fetchall()}
    return [(*r[:-1], *shares[r[0]], r[-1]) for r in rows]


def pct(x):
    return "" if x is None else f"{100 * x:.1f}%"


def num(x):
    return "" if x is None else f"{x:.2f}"


def md(head, rows):
    """A Markdown table."""
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def main():
    con = connect()
    span(con)
    memory(con)
    notes = json.loads((TABLE / "notes.json").read_text()) if (TABLE / "notes.json").exists() else {}
    size = {t: con.execute(f"select count(*) from {t}").fetchone()[0] for t in ("series", "place", "obs")}
    zero = con.execute("""select domain, count(*) filter (where transform = 'log' and value <= 0), count(*) filter (where transform = 'log'), count(*) filter (where value = 0), count(*) from o group by 1 order by 1""").fetchall()
    out = [f"# The held data in one shape: first count, each series alone\n\nWritten by `scripts/count_table.py` from `data/table/` (not committed; `scripts/build_table.py` makes it). {size['series']} series, {size['place']} places, {size['obs']:,} observations. Nothing in this page sets one series beside another: every number is about a series on its own, or about a group of series counted, never related.\n"]
    for key in ("domain", "source"):
        n = places_by(con, key)
        rows = [(r[0], r[1], n[r[0]], r[2], r[3], f"{r[4]:,}", pct(r[5]), *[pct(x) for x in r[6:]]) for r in by(con, key)]
        out.append(f"## By {key}\n\n" + md((key, "series", "places", "first", "last", "values", "missing inside span", *[f"flag {f}" for f in FLAGS]), rows) + "\n")
    out.append("The span is each place's own, first to last period it has a value. For the conflict counts a missing month means no recorded event (the source lists events, not their absence). Flags exist in the crop source and the two FAOSTAT price sources (`faostat_cp`, `faostat_pe`); everything else reads `none`. Places are those with at least one value in the group; `world` is one place. The 26 climate files (the ONI and the 25 others) are one source line, `candidates` holding the 25; each is listed alone in `data/table/series_description.csv`.\n")
    for key in ("domain", "source"):
        rows = [(r[0], r[1], num(r[2]), num(r[3]), num(r[4])) for r in memory_by(con, key)]
        out.append(f"## Memory by {key}\n\nThe correlation of a place's series with itself one period before (a year for yearly series, a month for monthly), after the log the series table names; lower quartile, median and upper quartile over the series-and-place units that have at least {LEAST_PAIRS} consecutive pairs.\n\n" + md((key, "units", "lower quartile", "median", "upper quartile"), rows) + "\n")
    out.append("Memory of a level that trends is high because of the trend alone; this is a description of each series, not a measure of anything predictable. For the conflict counts the months with no row are taken as zero for this one number.\n")
    rows = [(r[0], r[1], r[2], r[3], r[4], r[5], f"{r[6]:,}", pct(r[7]), *[pct(x) for x in r[8:12]], num(r[12])) for r in prices_alone(con)]
    out.append("## FAOSTAT consumer prices and exchange rates, each series alone\n\n" + md(("series", "step", "places", "places with 120+ monthly values", "first", "last", "values", "missing inside span", "flag official", "flag estimated", "flag imputed", "flag other", "memory (median over places)"), rows) + "\n\nFlag `other` is FAOSTAT's X, a figure from an outside organisation. Memory is the correlation of each place's series with itself one period before, after the log the series table names, as above.\n")
    out.append("## Values the log cannot take\n\n" + md(("domain", "log-series values at or below zero", "values of log series", "values equal to zero", "all values"), [(r[0], f"{r[1]:,}", f"{r[2]:,}", f"{r[3]:,}", f"{r[4]:,}") for r in zero]) + "\n\nA value at or below zero in a series whose transform is `log` is left out of the memory number and nowhere else.\n")
    out.append("## What the build set aside\n\n```\n" + json.dumps(notes, indent=1, sort_keys=True) + "\n```\n")
    out.append(NOTES)
    DOC.write_text("\n".join(out))
    lines = per_series(con)
    (TABLE / "series_description.csv").write_text("series_id,domain,source,step,kind,transform,first,last,places,values,missing,memory\n" + "\n".join(",".join("" if v is None else str(v) for v in r) for r in lines) + "\n")
    print(f"wrote {DOC.name} and series_description.csv", file=sys.stderr)


if __name__ == "__main__":
    main()
