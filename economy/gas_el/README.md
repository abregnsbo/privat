# NettoPower — el- og gasforbrug

NettoPower supplies both electricity and gas (switched from previous suppliers
2022-04-20; aftagenr. 74113617656 = el, 98002784898 = gas, address Malmmosevej 87A).

## Files

- `YYYY-MM.pdf` — monthly invoice/statement PDFs pulled from Gmail
  ("Faktura" emails from kundeservice@nettopower.dk). Filename = **email month**;
  the statement inside covers the **previous** month.
- `aconto-2026-Q*.pdf` — quarterly aconto prepayment invoices from the new
  billing system (2026 migration, "MigreretFraFBS"). Estimated forward
  consumption, not measured usage.
- `txt/` — text extracted with `pdftotext -layout` (Latin-1 encoded).
- `parse_invoices.py` — parses `txt/*.txt` into `consumption.csv` and prints
  the table below. Run: `py parse_invoices.py`.

## Usage table (measured, per consumption month)

| Period              | El kWh |   El DKK | Gas m³ |  Gas DKK |
|---------------------|-------:|---------:|-------:|---------:|
| 2022-11             |    537 | 1,741.34 |    241 | 2,804.41 |
| 2022-12             |    661 | 2,617.25 |    363 | 5,131.21 |
| 2023-01             |    629 | 1,434.60 |    492 | 3,874.73 |
| 2023-02             |    469 | 1,150.23 |    492 | 7,396.11 |
| 2023-03             |    520 | 1,120.07 |    499 | 2,814.51 |
| 2023-04             |    450 |   704.46 |    292 | 1,578.95 |
| 2023-05             |    442 |   629.60 |    134 |   585.68 |
| 2023-06             |    416 |   708.45 |     66 |   295.91 |
| *2023-07 … 2025-03* |  *gap* |          |  *gap* |          |
| 2025-04             |    483 | 1,153.48 |    248 | 1,563.11 |
| 2025-05             |    438 |   995.69 |    169 | 1,042.52 |
| 2025-06             |    344 |   787.63 |     92 |   586.44 |
| 2025-07             |    297 |   747.94 |     63 |   384.66 |
| 2025-08             |    355 |   871.00 |     74 |   443.00 |
| 2025-09             |    371 |   964.86 |     97 |   577.19 |
| 2025-10             |    550 | 1,508.35 |    274 | 1,669.28 |
| 2025-11             |    591 | 1,712.89 |    403 | 2,399.64 |
| 2025-12             |    761 | 2,058.58 |    363 | 2,490.36 |
| *2026-01*           |  *gap* |          |  *gap* |          |
| 2026-02             |    654 | 1,340.37 |    522 | 3,363.00 |

DKK amounts are incl. VAT. Gas amounts in 2023 and some 2025 months are aconto
estimates with later quarterly corrections (see the "Korrektioner" section on
the statements), so month-to-month gas figures are approximate; electricity is
hourly metered (timeafregnet) and accurate.

### Partial-year sums (covered months only)

| Year | Months  | El kWh | El DKK | Gas m³ | Gas DKK |
|------|---------|-------:|-------:|-------:|--------:|
| 2022 | Nov–Dec |  1,198 |  4,358 |    604 |   7,936 |
| 2023 | Jan–Jun |  2,926 |  5,747 |  1,975 |  16,546 |
| 2025 | Apr–Dec |  4,190 | 10,800 |  1,783 |  11,156 |
| 2026 | Feb     |    654 |  1,340 |    522 |   3,363 |

## Aconto invoices 2026 (estimated, prepaid)

| Invoice             | Prepay period           | Est. el kWh |   El DKK | Est. gas m³ |  Gas DKK | Total DKK |
|---------------------|-------------------------|------------:|---------:|------------:|---------:|----------:|
| F7797 (2026-03-27)  | 2026-03-24 – 2026-05-31 |     1,966.3 | 5,381.55 |       565.9 | 4,387.27 |  9,768.82 |
| F57906 (2026-06-26) | 2026-06-01 – 2026-08-31 |     2,614.0 | 6,773.06 |       279.3 | 2,339.97 |  9,122.78 |

The 2026 billing migration ended the monthly statement emails (last one
2026-03-16 covering Feb 2026); billing is now quarterly aconto with later
settlement.

## Electricity — complete monthly meter data (eloverblik.dk)

Source: `eloverblik_el_monthly.csv`, exported from eloverblik.dk (metered
values, målepunkt 571313174113617656). Fills the invoice gap completely.
Matches the invoice kWh figures exactly where they overlap. kWh, rounded:

| Year |  Jan |  Feb |  Mar |  Apr |  May |  Jun |  Jul |  Aug |  Sep |  Oct |  Nov |  Dec |  Total | kr/kWh |
|------|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-------:|-------:|
| 2022 |  848 |  534 |  586 |  532 |  363 |  340 |  327 |  376 |  329 |  381 |  537 |  661 |  5,813 |  3.64ᵃ |
| 2023 |  629 |  469 |  520 |  450 |  442 |  416 |  372 |  473 |  519 |  521 |  633 |  850 |  6,295 |  1.96ᵇ |
| 2024 |  737 |  656 |  630 |  588 |  402 |  356 |  384 |  358 |  318 |  485 |  592 |  687 |  6,193 |      – |
| 2025 |  617 |  509 |  623 |  483 |  438 |  344 |  297 |  355 |  371 |  550 |  591 |  761 |  5,939 |  2.58ᶜ |
| 2026 |  701 |  654 |  568 |  532 |  455 |  313 | 278* |      |      |      |      |      | 3,500* |  2.05ᵈ |

\* 2026 through 26 July (partial month).
kr/kWh = average all-in electricity price (energy + transport + el-afgift,
incl. moms) from the NettoPower invoices: billed el DKK ÷ kWh for the
invoice-covered months only — ᵃ Nov–Dec 2022 (energy crisis), ᵇ Jan–Jun
2023, ᶜ Apr–Dec 2025, ᵈ Feb 2026 only. 2024 has no invoice price data.

## Gas — quarterly meter readings (Mit Evida)

Source: `evida_gas_quarterly.csv`, from mit.evida.dk "Forbrugsudvikling"
(måler 1103276). Quarterly readings (first year irregular). "Forbrug" is
Evida's official consumption figure; note it runs ~7 % below the raw meter
difference (temperature/pressure correction), so use Forbrug, not deltas.

| Period                  | Forbrug m³ | Gas price kr/m³ | Distrib. kr/m³ | Total kr/m³ |
|-------------------------|-----------:|----------------:|---------------:|------------:|
| 2022-05-01 – 2022-12-31 |      1,795 |           13.1¹ |            5.0 |        18.1 |
| 2023 Jan–Apr            |      1,527 |             8.8 |            5.3 |        14.1 |
| 2023 May–Jun            |        459 |             4.4 |            5.7 |        10.1 |
| 2023 Q3                 |        475 |        4.5 est. |            5.6 |        10.1 |
| 2023 Q4                 |        852 |        5.9 est. |            5.4 |        11.3 |
| 2024 Q1                 |      1,281 |        4.5 est. |            6.6 |        11.1 |
| 2024 Q2                 |        721 |        4.5 est. |            6.6 |        11.1 |
| 2024 Q3                 |        384 |        5.7 est. |            6.5 |        12.2 |
| 2024 Q4                 |        880 |        6.0 est. |            6.6 |        12.6 |
| 2025 Q1                 |      1,365 |        6.4 est. |            5.7 |        12.1 |
| 2025 Q2                 |        538 |             6.3 |            5.7 |        12.0 |
| 2025 Q3                 |        493 |             6.0 |            5.7 |        11.7 |
| 2025 Q4                 |        855 |             6.3 |            5.7 |        12.0 |
| 2026 Q1                 |      1,576 |            6.4² |            5.7 |        12.2 |
| 2026 Q2                 |        684 |            7.8³ |            5.7 |        13.5 |

Gas price = NettoPower's billed gas cost ÷ billed m³ (incl. moms, from
`consumption.csv`) — the **supply** price only.
Distrib. = the Evida bill per m³: distribution (~1.2–1.8 kr) + state
afgifter (~3.3 kr) + nødforsyningstarif, incl. moms — quarterly averages
from Forsyningstilsynet's component statistics; cross-checked against
actual Evida payments ÷ consumption (5.1–5.6 kr/m³ per year).
Total = gas price + distrib. — the full cost per m³ delivered.
¹ Nov–Dec 2022 invoices only (energy-crisis peak). ² Feb 2026 invoice
only. ³ Aconto rate from invoice F7797, not settled actuals.
"est." = invoice gap; estimated from Forsyningstilsynet's monthly
naturgasprisstatistik ("Gaspris" component, quarterly average × 1.25 moms;
Excel at forsyningstilsynet.dk → naturgasprisstatistik). Calibration: the
FT average matches NettoPower's billed price in mid-2023 (4.35 vs 4.41)
but NettoPower billed 20–35 % **above** the FT average through 2025, so
the gap estimates are likely lower bounds for what NettoPower charged.

Yearly: **2023: 3,313 m³ · 2024: 3,266 m³ · 2025: 3,251 m³** · 2026 H1: 2,260 m³
(2022 from May: 1,795 m³; meter at supplier switch 2022-04-19: 26,174).

## Gas consumption analysis: hot water is the anomaly (2026-07)

Context: family of 4, 170 m² house from 1972, roof insulated, modern thermo
windows, gas boiler + hot water tank 20+ years old (tank insulation OK),
water softener installed (serviced 2023-06). Two adult sons shower a lot.

**3,300 m³/year is roughly double the norm** (family of 4 in 150 m² from
2002: ~1,700 m³; couple in 100 m² from 1970: ~1,350 m³ — DGC/OK figures).
But the split matters:

- **Summer quarters (Jul–Sep, zero heating) run 384–493 m³ ≈ 4–5 m³/day**,
  vs. ~1 m³/day typical DHW for 4 people. Non-heating baseline extrapolates
  to **~1,400–1,600 m³/year vs. a ~350–400 m³ norm** — the excess is hot
  water / standing losses, worth ~15,000 kr/year at ~12.5 kr/m³ all-in.
- Space heating = rest ≈ 1,700–1,800 m³ ≈ ~115 kWh/m²/year — **normal** for
  a roof-insulated 1972 house. The building shell is not the problem.

Energy per event (gas incl. boiler losses): 10-min shower ≈ 0.4 m³ (~5 kr),
20-min shower ≈ 0.8 m³ (~10 kr), bathtub ≈ 0.65 m³ (~8 kr). Two daily
long showers ≈ 550–650 m³/year — a large share, likely not all of it.

Suspects for the remaining baseline: hot-water circulation loop running
24/7 (up to 300–800 m³/yr), old boiler short-cycling on summer DHW load
(seasonal efficiency can drop to 50–60 %), limescale on the heat-exchanger
coil (typ. 5–15 % penalty; hard-water area, but softener limits new
build-up; pre-softener scale remains until descaled). Tank standing losses
ruled less likely (insulation OK).

Diagnostic meter tests (meter 1103276 reads to the litre):

1. Overnight 23:00–07:00, no draws, heating off → standing + circulation
   loss. > ~0.3 m³/night is a problem.
2. Reheat after a big draw-down: ~160 L × 45 K ≈ 0.75 m³ at 100 % boiler
   efficiency; 1.2–1.4 m³ ⇒ ~55–60 % → descale or replace. Kettling
   (rumbling at reheat) = audible scale symptom.
3. Meter before/after one of the boys' showers → kr per shower.
4. Compare a week with the boys home vs. away → their share vs. system's.

Strategy: before investing in the gas installation, consider a heat-pump
water heater (~12–15,000 kr): heat via gas costs ~1.3–1.5 kr/kWh real,
via DHW heat pump ~0.75 kr/kWh — kills most of the summer baseline,
payback < 2 years, and decouples DHW from the ageing boiler.

## Payments (from Budgetkonto CSV, 2023-03-17 – 2026-05-17)

Actual bank payments, from `../Budgetkonto_2023-03-17-2026-05-17.csv`.
`BS NETTOPOWER APS` is the combined el + gas supply bill (not separable);
`BS EVIDA SERVICE (NORD) A/S` is the separate gas distribution/transport bill,
which comes on top of NettoPower's gas price.

| Date       | NettoPower DKK |   | Date       | Evida DKK |
|------------|---------------:|---|------------|----------:|
| 2023-09-01 |      12,203.82 |   | 2023-04-11 |  6,215.50 |
| 2023-12-01 |      27,988.38 |   | 2023-07-06 |  1,140.55 |
| 2024-09-02 |      19,013.78 |   | 2023-08-07 |  3,975.75 |
| 2024-12-02 |      20,179.26 |   | 2023-11-06 |  7,150.10 |
| 2025-01-02 |      21,452.03 |   | 2024-02-06 |  6,233.61 |
| 2025-04-01 |      14,205.35 |   | 2024-05-06 |  2,235.85 |
| 2025-07-01 |      10,445.36 |   | 2024-08-06 |  2,196.36 |
| 2025-10-01 |      13,693.00 |   | 2024-11-06 |  6,121.42 |
| 2026-01-02 |      13,566.51 |   | 2025-02-06 |  6,023.73 |
| 2026-04-01 |       9,768.82 |   | 2025-05-06 |  2,385.43 |
|            |                |   | 2025-08-06 |  1,626.61 |
|            |                |   | 2025-11-06 |  6,563.08 |
|            |                |   | 2026-02-06 |  5,860.64 |
|            |                |   | 2026-05-06 |  3,604.49 |

Per year (payment date, not consumption period):

| Year             | NettoPower DKK |     Evida DKK |            Sum |
|------------------|---------------:|--------------:|---------------:|
| 2023 (from 17/3) |      40,192.20 |     18,481.90 |      58,674.10 |
| 2024             |      39,193.04 |     16,787.24 |      55,980.28 |
| 2025             |      59,795.74 |     16,598.85 |      76,394.59 |
| 2026 (to 17/5)   |      23,335.33 |      9,465.13 |      32,800.46 |
| **Total**        | **162,516.31** | **61,333.12** | **223,849.43** |

Caveats when comparing with the usage table:

- Payments are quarterly aconto (prepaid) with later settlement, so payment
  dates lag/lead the consumption they cover.
- There are **no** NettoPower payments Mar–Aug 2023 or Jan–Aug 2024: bills in
  those periods were drawn from the prepaid "Min NettoPower konto" saldo
  (46,878 kr in Nov 2022, visible on the old statements) rather than via
  Betalingsservice. Payment sums therefore understate consumption cost in
  2023–24 by roughly that drawdown.

## Reconstruction risk analysis (2026-07-26)

*Outcome: NettoPower went konkurs 2026-07-28, and el had already been
transferred to Energy Nordic 2026-06-30 — see the "Energy Nordic interlude"
section below for the updated claim (~7,300–7,500 kr against the konkursbo).*

NettoPower is under reconstruction (rekonstruktion); prepayments cover
through 2026-08-31. Analysis of aconto billed vs. expected actual usage:

The 2026 aconto invoices assume **10,460 kWh/year** electricity
("Estimeret årsforbrug"), but metered history shows **~6,000 kWh/year** —
a ~75 % overestimate on every el aconto. Gas estimates are roughly correct.

| Invoice / fuel               | Billed (est.)            | Expected actual      | Over/(under)paid |
|------------------------------|--------------------------|----------------------|-----------------:|
| F7797 (24/3–31/5) el         | 1,966 kWh / 5,381.55 kr  | ~1,133 kWh (metered) |        +2,280 kr |
| F7797 gas                    |   566 m³  / 4,387.27 kr  |   ~641 m³            |          −580 kr |
| F57906 (1/6–31/8) el         | 2,614 kWh / 6,773.06 kr  | ~1,005 kWh (proj.)   |        +4,170 kr |
| F57906 gas                   |   279 m³  / 2,339.97 kr  |   ~324 m³  (proj.)   |          −370 kr |
| **Net credit by 31 Aug 2026**|                          |                      | **≈ +5,500 kr**  |

- The Mar–May period is fully consumed but was **not settled** on the June
  invoice — that ~1,700 kr net credit sits unsettled at NettoPower.
- Position as of 2026-07-26 is larger (~7,500–8,000 kr) because ~1 month of
  prepaid Jun–Aug energy was still unconsumed; it declines to ~5,500 kr by
  31 Aug. This credit is an unsecured claim if the reconstruction fails.
- Assumptions: Apr–May gas interpolated from quarterly meter readings
  (±300–400 kr); summer 2026 projected from the stable usage history; the
  old-system account assumed ~settled at the Q1 2026 migration (Q1 prepaid
  13,566.51 kr vs. ~14,300 kr actual cost — close to break-even).
- Next quarterly aconto (~1 Sep 2026) would be another ~10,000 kr computed
  from the same inflated el estimate. No binding period on the contract.

## Supplier switch to DCC Energi (signed, start 2026-09-01)

*Status 2026-08-22: agreement with DCC Energi in place, switch registered in
DataHub with start 01-09-2026 — verified on eloverblik's "Leverandøroversigt",
which lists DCC Energi "Fra 31. aug. 2026" (the 31/8 date is DataHub's UTC
rendering of 01-09 00:00 local). NettoPower agreements terminated by email
2026-07-26.*

Candidate replacement supplier after the NettoPower reconstruction:
**DCC Energi A/S** (dccenergi.dk) — owned 60 % by DCC plc (Dublin, FTSE 100)
and 40 % by DLG; 250+ employees, runs all Shell stations in DK. Solid
counterparty, unlike NettoPower.

- **El**: spot + 7.5 øre/kWh markup, 25 kr/md subscription (intro: 6 months
  free), green power +3.5 øre/kWh optional, no binding. Trustpilot 4.4.
- **Gas**: variable, ~4 kr/m³ (Dec 2025 level), 0 kr/md subscription, some
  products 6 months binding. Evida distribution remains separate.
- **Billing**: monthly aconto with subsequent settlement — ~1 month float
  (~1,500–2,500 kr) vs. NettoPower's quarterly ~10,000 kr.

Signup details:

|                           | Electricity                      | Gas                              |
|---------------------------|----------------------------------|----------------------------------|
| Målepunkts-ID (aftagenr.) | 571313174113617656 (74113617656) | 571515198002784898 (98002784898) |
| Målernummer               | 21265781                         | 1103276 (Evida)                  |
| Expected annual usage     | **6,000 kWh**                    | **3,300 m³**                     |

Do NOT accept NettoPower's inflated 10,460 kWh el estimate at signup.

- Start date: **2026-09-01** (prepayment at NettoPower runs to 31 Aug; their
  next ~10,000 kr aconto would hit ~1 Sep).
- NettoPower notice: 15 workdays → cancel both agreements by ~2026-08-07
  (kundenr. 152240 / ref. N9484384, kundeservice@nettopower.dk).
- On switch: photo the gas meter reading; check Betalingsservice ~1 Sep and
  reject any NettoPower collection; demand slutafregning (~5,500 kr expected
  credit, see risk analysis above).

## Energy Nordic interlude (el only, 2026-06-30 – 2026-08-31)

The el supply was transferred **without consent** from NettoPower to Energy
Nordic (energynordic.dk, kundenr. K7232665, aftalenr. A4952) effective
**2026-06-30** — so NettoPower delivered el only through 29 June of the
prepaid Jun–Aug quarter (F57906). Gas was not transferred. DCC Energi takes
over from 2026-09-01 as planned.

Invoices received (both unpaid as of 2026-08-22; manual payment code, not BS):

| Invoice | Date / due | Content | Amount |
|---------|------------|---------|-------:|
| F19294 (`energy_nordic_juni_aug.pdf`) | 08-07 / 16-07 | 30 Jun actual 10 kWh (27.33) + Jul–Aug aconto 1,112 kWh (1,759.29) | 1,786.62 |
| F23659 (`energy_nordic_faktura.pdf`) | 19-08 / 01-09 | Jul actual 345 kWh (607.89) − Jul-share of aconto (750.28) + Sep aconto 552 kWh (969.42) | 827.03 |
| **Total invoiced** | | | **2,613.65** |

Actually owed = measured consumption only (avg ~1.76–1.80 kr/kWh all-in):

| Period | kWh | DKK |
|--------|----:|----:|
| 30 Jun (actual, Radius) | 10 | 27.33 |
| Jul (actual, Radius) | 345 | 607.89 |
| Aug (171.06 kWh metered through 20/8 + ~13.5 kWh/day × 11 days) | ~320 | ~580 |
| **Fair total** | ~675 | **~1,215** |

August detail (eloverblik, 2026-08-22): 1–10 Aug ≈ 3.7 kWh/day (house
empty), 11–20 Aug ≈ 13.5 kWh/day — projection uses the latter.

Overcharge in the invoices ≈ 1,400 kr: Sep aconto 969.42 (supply ends 31/8,
DCC from 1/9) + Aug aconto overshoot (~1,009 billed vs ~580 expected).

Timeline:

- **2026-06-30**: el supply transferred to Energy Nordic without consent.
- **2026-07-26**: written termination of the NettoPower agreement emailed to
  NettoPower (receipt confirmed by auto-reply, "handled in 3–5 workdays";
  never answered). Copy kept — key evidence.
- **2026-07-28**: NettoPower declared **konkurs** (bankrupt).
- **2026-08-22**: demand email sent to kundeservice@energynordic.dk:
  1. confirm in writing that supply ends 31-08-2026 and that the DataHub
     switch to DCC Energi (start 01-09) is not opposed;
  2. credit the Sep aconto (969.42 kr) on F23659;
  3. issue a slutafregning per 31-08 on Radius-metered data instead of the
     F19294 Aug aconto;
  4. the actual consumption (~1,215 kr) will be paid **as soon as points 1–3
     are confirmed in writing** — both invoices on hold until then, no
     dunning fees accepted while pending. Any credit to be paid out, not
     offset. Response deadline 31-08-2026, otherwise Ankenævnet på
     Energiområdet.

Notice-period defense (the fork): either the transfer without consent means
no contract terms/notice apply — or, if Energy Nordic claims to have taken
over the NettoPower contract, the 26-07 termination satisfies even a
"current month + 1 month" notice by 31-08. Both branches end the agreement
31-08-2026. Do NOT enroll in Betalingsservice with Energy Nordic.

Consequence for the NettoPower claim: F57906's el prepayment (6,773.06 kr
for Jun–Aug) now covers only June ~303 kWh (~700 kr), so the claim grows
from ~5,500 to **~7,300–7,500 kr** — now an unsecured claim against the
**konkursbo** (file it with the kurator; demand slutafregning per
2026-06-29 for el and 2026-08-31 for gas).

## Known gaps

- **2023-07 … 2025-03** (21 months) and **2026-01**: invoice emails in this
  period contained no PDF ("log ind på din selvbetjening"), and the NettoPower
  portal no longer has these invoices after their accounting-system change —
  per-month kWh/m³ for this period is not recoverable from NettoPower. The
  payments table above is the best available proxy for cost in the gap.
- **Both usage gaps are now filled**: electricity monthly via eloverblik,
  gas quarterly via Mit Evida (gas meter is only read quarterly, so monthly
  gas granularity exists solely in the NettoPower invoice estimates).
- Exact metered data alternatives: eloverblik.dk (el) and Mit Evida (gas).

## eloverblik.dk / Mit Evida access

- El målepunkts-ID (aftagenummer): **571313174113617656** (short form
  74113617656), målernummer 21265781, netselskab Radius.
- El webadgangskode: **2bri5qru** (printed as "Webaccesskode" on the
  2022–2023 invoices; issued by the netselskab — request a new one from
  Radius if rejected).
- Gas målepunkts-ID: 571515198002784898 (short form 98002784898) — gas data
  is on Mit Evida (login via one-time email code), not eloverblik.
