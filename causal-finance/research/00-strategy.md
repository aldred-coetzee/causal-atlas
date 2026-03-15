# Causal Finance — Strategy Document

> **Status:** Draft v1.0 — March 2026  
> **Account:** Trading 212 Invest (taxable)  
> **Capital:** £1,000  
> **Keep local — do not push to public repo**

---

## 1. Objective

Beat a UK easy-access savings account (currently ~4.7–5% annually) using a signal-driven ETF rotation system grounded in cross-domain causal analysis. Prioritise capital preservation over aggressive growth.

**Target:** 12–18% annually in favourable conditions. Accept 0–5% in unfavourable years rather than chase returns with increased risk.

**What this is not:** A day-trading system. Not a get-rich-quick system. A systematic, evidence-based rotation model that makes 1–2 portfolio adjustments per month based on macro and climate signals.

---

## 2. Why This Approach Is Novel

Most retail and institutional quant approaches use:
- Price/volume technical analysis
- Correlation-based signals (which break in regime changes)
- NLP sentiment from news headlines
- Standard factor models (value, momentum, quality)

This system uses **directed causal relationships with specific lag structures** — not just "these things move together" but "this causes that, 4–8 weeks later, under these conditions." The signals are derived from cross-domain data (climate indices, geopolitical risk, macroeconomic indicators) that most finance models ignore entirely.

Crucially, the chains are **explainable**. You know *why* a signal fires, which means you know when to trust it and when the mechanism has broken down.

---

## 3. ETF Universe

All ETFs are UCITS-compliant and confirmed available on Trading 212 Invest (LSE-listed, GBP-denominated). US-domiciled equivalents (GLD, QQQ) are blocked for UK retail investors under PRIIPs regulations.

| Bucket | ETF | Ticker | Role |
|--------|-----|--------|------|
| Defensive | iShares Physical Gold | IGLN | Capital preservation, geopolitical hedge |
| Macro — Energy | iShares Oil & Gas Exploration | IOGP | Upstream energy exposure |
| Macro — Agriculture | iShares Agribusiness | ISAG | Soft commodities, food system |
| Growth | iShares S&P 500 IT Sector | IITU | US technology sector |

> **Note:** EQQQ (Invesco Nasdaq-100) is an alternative to IITU with higher liquidity. Verify both are available on your Trading 212 account before committing.

---

## 4. Portfolio Structure — Three Buckets

Capital is divided into three buckets with distinct jobs, risk levels, and signal requirements.

```
£1,000 total
│
├── BUCKET 1 — DEFENSIVE (£400 / 40%)
│   ETF: IGLN (Physical Gold)
│   Job: Preserve capital. Hedge geopolitical and macro risk.
│   Signal: Geopolitical Risk (GPR) Index, VIX level
│   Touch when: GPR spikes significantly OR macro clarity improves (reduce)
│   Default: Hold. This bucket changes least often.
│
├── BUCKET 2 — MACRO (£400 / 40%)
│   ETFs: IOGP (Energy) + ISAG (Agriculture), split ~50/50 within bucket
│   Job: Capture causal signals from climate and geopolitical data
│   Signal: ENSO/ONI index, Brent crude trend, GDELT event counts
│   Touch when: Monthly rebalancing based on signal output
│   Default: Rotate between energy and agriculture based on dominant signal
│
└── BUCKET 3 — GROWTH (£200 / 20%)
    ETF: IITU (Technology)
    Job: Upside capture when macro conditions are favourable
    Signal: US 10-year TIPS yield (real interest rates)
    Touch when: Real rates falling → hold/increase. Real rates rising fast → reduce.
    Default: Hold unless TIPS signal is clearly negative
```

**Why buckets reduce risk:**
- Gold and tech are negatively correlated in risk-off environments — they partially offset each other
- No single signal failure can wipe the portfolio
- Worst case: all three fall, but gold typically cushions broad market drawdowns
- Bucket 1 acts as a floor — capital never fully deployed into volatile assets

---

## 5. Causal Signal Hypotheses

Four primary signals, in order of evidence strength:

### Signal 1 — ENSO → Agriculture ETFs
**Causal chain:** El Niño/La Niña conditions → regional crop yield disruption → soft commodity price changes → Agribusiness ETF performance  
**Lag:** 3–6 months from ENSO phase transition to market impact  
**Data source:** NOAA Oceanic Niño Index (ONI) — free, updated monthly  
**Threshold:** ONI ≥ +0.5°C for 3+ consecutive months = El Niño. Reduce ISAG exposure.  
**Evidence:** Hsiang, Meng & Cane (2011) found conflict risk doubles in El Niño years; commodity price literature documents consistent 3–6 month agricultural lags  
**Confidence:** Strong — best-evidenced chain in the research base

### Signal 2 — Geopolitical Risk Index → Gold
**Causal chain:** GPR index spike → safe haven demand → gold price rise → IGLN outperformance  
**Lag:** 1–3 weeks (faster than most other signals)  
**Data source:** Caldara & Iacoviello GPR Index — free, monthly updates (daily version available)  
**Threshold:** GPR significantly above 12-month average = increase Bucket 1 weighting  
**Evidence:** Well-documented in academic literature; gold's safe haven property is one of the most robust findings in commodity finance  
**Confidence:** Strong

### Signal 3 — Real Interest Rates → Technology ETFs
**Causal chain:** Rising US real rates → higher discount rate for future earnings → growth/tech stock derating → IITU underperformance  
**Lag:** 2–6 weeks for rate expectations to transmit to equity valuations  
**Data source:** FRED (Federal Reserve) — US 10-year TIPS yield, free, daily updates  
**Threshold:** TIPS yield rising consistently over 4+ weeks = reduce Bucket 3  
**Evidence:** Standard discounted cash flow mechanics; dominant regime driver for tech valuations 2022–present  
**Confidence:** Strong — mechanism is theoretically clear, empirically validated

### Signal 4 — Oil Price Trend + Geopolitical Events → Energy ETFs
**Causal chain:** Brent crude price trend + geopolitical event density in oil-producing regions → energy sector revenue expectations → IOGP performance  
**Lag:** 1–4 weeks  
**Data source:** Brent crude (Yahoo Finance API, free); GDELT event counts (free, 15-minute updates)  
**Threshold:** Brent in sustained uptrend AND GPR elevated in MENA/Russia → hold/increase IOGP  
**Evidence:** Well-established oil-equity relationship; less novel but reliable  
**Confidence:** Moderate — conflicting signals possible (demand vs supply drivers)

---

## 6. Monthly Process

The full monthly rebalancing takes approximately 30 minutes.

**Step 1 — Check signals (15 min)**

| Signal | Source | What to check |
|--------|--------|---------------|
| ENSO/ONI | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php | Current ONI value and trend |
| GPR Index | https://www.matteoiacoviello.com/gpr.htm | Current value vs 12-month average |
| TIPS Yield | https://fred.stlouisfed.org/series/DFII10 | Direction over past 4 weeks |
| Brent Crude | Yahoo Finance (BZ=F) | 4-week trend: up, down, or flat |

**Step 2 — Model output (5 min)**

Map signals to suggested allocation shifts:

| Condition | Action |
|-----------|--------|
| GPR elevated + VIX rising | Increase Bucket 1 (gold), reduce Bucket 3 (tech) |
| El Niño active | Reduce ISAG within Bucket 2, increase IOGP or move to gold |
| TIPS yield rising fast | Reduce Bucket 3 (tech) |
| All signals neutral | Hold current allocation, no trades |
| GPR falling + TIPS falling + La Niña | Reduce gold, increase ISAG and IITU |

**Step 3 — Execute (5 min)**

Only trade if suggested shift is >5% of total portfolio (i.e., >£50). Smaller shifts don't justify the friction of a trade.

Maximum 2 trades per month.

**Step 4 — Log (5 min)**

Record in a simple log file:
- Date
- Signal readings
- Decision made (and why)
- Trades executed
- Portfolio value

The log is essential. It's the only way to know if the system is working or if you're just getting lucky.

---

## 7. Risk Management

**Position sizing:** No single ETF ever exceeds 50% of portfolio. Bucket 1 (gold) is the floor and should never go below 25% unless there is an exceptionally strong risk-on signal.

**Maximum drawdown tolerance:** If total portfolio falls more than 15% from peak, pause the system, do not rebalance, review what signal failed and why before resuming.

**Leverage:** None. Trading 212 Invest account only. No CFDs, no margin.

**FX costs:** IGLN, IOGP, ISAG, IITU are all GBP-denominated on LSE. Trading 212 charges 0.15% FX conversion on non-GBP assets. All four ETFs are priced in GBP so this should not apply — confirm in the app before trading.

**Tax:** Capital gains allowance is £3,000/year (2025/26). At £1,000 starting capital, you would need 300% gains before CGT applies. Not a concern at current scale. Keep records of all trades for self-assessment if the portfolio grows significantly.

---

## 8. Current Market Context (March 2026)

> This section to be updated monthly. Snapshot at strategy inception.

**Gold (IGLN):** Near all-time highs. GPR index is elevated due to trade war escalation, tariff uncertainty, USD weakness. The defensive signal has already fired — gold has run 15–20% in 2026. Buying now means entering after the move.

**Energy (IOGP):** Mixed signals. Tariff uncertainty is suppressing global growth expectations (bearish demand). Geopolitical risk in Middle East provides supply-side floor. Net signal: unclear. Hold, do not increase.

**Agriculture (ISAG):** Interesting. La Niña conditions present. Trade war disruption to US/China agricultural commodity flows is a real signal. Cautiously neutral to slightly positive.

**Technology (IITU):** Caution warranted. Tariff-driven inflation expectations → rising real rate expectations → headwind for growth stock valuations. TIPS signal currently flashing caution on Bucket 3.

**Overall assessment at inception:** Conditions are unusually uncertain. Not an ideal entry point.

---

## 9. Six-Week Paper Trading Plan

**Do not deploy real money until the paper trading phase is complete.**

The £1,000 sits in Trading 212's uninvested cash, earning ~4.7% annually (~£4/month) while the system is validated.

| Week | Activity |
|------|----------|
| 1 | Set up Trading 212 practice account. Deploy virtual allocation per bucket structure above. Record starting positions. |
| 2 | Check all four signals. Note readings. No action yet — just observing. |
| 3 | First virtual rebalancing decision. Apply the monthly process. Execute virtual trades if signals indicate. |
| 4 | Check signals again. Note whether week 2 readings were predictive. |
| 5 | Second virtual rebalancing. Evaluate: are the signals coherent? Did the model suggest sensible trades? |
| 6 | Review: What would real returns have been? What failed? What worked? Is the system ready? |
| Week 7 | Decision point — deploy real money if: (a) signals are clearer than at inception, (b) paper trading has not revealed fundamental flaws in the approach, OR continue paper trading if conditions remain highly uncertain. |

**The goal of paper trading is not to make virtual money. It is to stress-test the process so that when real money is at risk, you have confidence in the system.**

---

## 10. What Success Looks Like

**Year 1 realistic scenarios:**

| Scenario | Annual Return | What it means |
|----------|--------------|---------------|
| Bear case | -5% to 0% | Global recession, all asset classes fall. Gold cushions but doesn't prevent losses. |
| Base case | 5–12% | Signals fire correctly 60–70% of the time. Modest outperformance of savings rate. |
| Bull case | 12–20% | Several strong signal cycles, good execution. Meaningful outperformance. |

**The savings account comparison:**
A 5% savings account on £1,000 returns £50/year with zero risk. This system targets beating that — but in any single year it might not. The edge is probabilistic and shows up more clearly over 2–3 years than in any individual month.

**Hardware funding timeline:**
At 15% annual return on £1,000: £150/year in gains. This does not fund a £500 machine quickly through returns alone. The more realistic path is parallel saving (£50–100/month from income) while running this system. The system is primarily about learning the methodology and building a track record — not as a primary income source at this capital level.

---

## 11. Next Steps

1. Set up Trading 212 practice account
2. Create `02-signal-hypotheses.md` — detailed research on each signal with historical validation
3. Create `03-data-sources.md` — API endpoints, update frequencies, Python fetch code for each signal
4. Create `04-backtest-methodology.md` — how to test signals historically before relying on them
5. Build signal tracking spreadsheet (simple, updated monthly)
6. Begin 6-week paper trading phase

---

## 12. Related Research

This strategy draws on the causal chain research in the Causal Atlas project (private repo). Relevant files:

- `research/03-causal-chains.md` — Sections 5 (commodity prices → instability), 18 (ENSO → multi-domain cascade)
- `research/01-landscape-analysis.md` — GDELT as data source for geopolitical signal
- `research/04-statistical-methods.md` — PCMCI methodology underlying signal detection

The finance application is a narrower, more tractable version of the broader Causal Atlas methodology — same causal discovery approach, applied to a smaller set of well-evidenced chains with clear financial targets.

---

*Last updated: March 2026*  
*Next review: April 2026 (after first paper trading month)*
