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

| Period | El kWh | El DKK | Gas m³ | Gas DKK |
|---------|-------:|--------:|-------:|--------:|
| 2022-11 | 537 | 1,741.34 | 241 | 2,804.41 |
| 2022-12 | 661 | 2,617.25 | 363 | 5,131.21 |
| 2023-01 | 629 | 1,434.60 | 492 | 3,874.73 |
| 2023-02 | 469 | 1,150.23 | 492 | 7,396.11 |
| 2023-03 | 520 | 1,120.07 | 499 | 2,814.51 |
| 2023-04 | 450 |   704.46 | 292 | 1,578.95 |
| 2023-05 | 442 |   629.60 | 134 |   585.68 |
| 2023-06 | 416 |   708.45 |  66 |   295.91 |
| *2023-07 … 2025-03* | *gap* | | *gap* | |
| 2025-04 | 483 | 1,153.48 | 248 | 1,563.11 |
| 2025-05 | 438 |   995.69 | 169 | 1,042.52 |
| 2025-06 | 344 |   787.63 |  92 |   586.44 |
| 2025-07 | 297 |   747.94 |  63 |   384.66 |
| 2025-08 | 355 |   871.00 |  74 |   443.00 |
| 2025-09 | 371 |   964.86 |  97 |   577.19 |
| 2025-10 | 550 | 1,508.35 | 274 | 1,669.28 |
| 2025-11 | 591 | 1,712.89 | 403 | 2,399.64 |
| 2025-12 | 761 | 2,058.58 | 363 | 2,490.36 |
| *2026-01* | *gap* | | *gap* | |
| 2026-02 | 654 | 1,340.37 | 522 | 3,363.00 |

DKK amounts are incl. VAT. Gas amounts in 2023 and some 2025 months are aconto
estimates with later quarterly corrections (see the "Korrektioner" section on
the statements), so month-to-month gas figures are approximate; electricity is
hourly metered (timeafregnet) and accurate.

### Partial-year sums (covered months only)

| Year | Months | El kWh | El DKK | Gas m³ | Gas DKK |
|------|--------|-------:|-------:|-------:|--------:|
| 2022 | Nov–Dec | 1,198 |  4,358 |   604 |  7,936 |
| 2023 | Jan–Jun | 2,926 |  5,747 | 1,975 | 16,546 |
| 2025 | Apr–Dec | 4,190 | 10,800 | 1,783 | 11,156 |
| 2026 | Feb     |   654 |  1,340 |   522 |  3,363 |

## Aconto invoices 2026 (estimated, prepaid)

| Invoice | Prepay period | Est. el kWh | El DKK | Est. gas m³ | Gas DKK | Total DKK |
|---------|---------------|------------:|-------:|------------:|--------:|----------:|
| F7797 (2026-03-27)  | 2026-03-24 – 2026-05-31 | 1,966.3 | 5,381.55 | 565.9 | 4,387.27 | 9,768.82 |
| F57906 (2026-06-26) | 2026-06-01 – 2026-08-31 | 2,614.0 | 6,773.06 | 279.3 | 2,339.97 | 9,122.78 |

The 2026 billing migration ended the monthly statement emails (last one
2026-03-16 covering Feb 2026); billing is now quarterly aconto with later
settlement.

## Electricity — complete monthly meter data (eloverblik.dk)

Source: `eloverblik_el_monthly.csv`, exported from eloverblik.dk (metered
values, målepunkt 571313174113617656). Fills the invoice gap completely.
Matches the invoice kWh figures exactly where they overlap. kWh, rounded:

| Year | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Total |
|------|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|------:|
| 2022 | 848 | 534 | 586 | 532 | 363 | 340 | 327 | 376 | 329 | 381 | 537 | 661 | 5,813 |
| 2023 | 629 | 469 | 520 | 450 | 442 | 416 | 372 | 473 | 519 | 521 | 633 | 850 | 6,295 |
| 2024 | 737 | 656 | 630 | 588 | 402 | 356 | 384 | 358 | 318 | 485 | 592 | 687 | 6,193 |
| 2025 | 617 | 509 | 623 | 483 | 438 | 344 | 297 | 355 | 371 | 550 | 591 | 761 | 5,939 |
| 2026 | 701 | 654 | 568 | 532 | 455 | 313 | 278*| | | | | | 3,500* |

\* 2026 through 26 July (partial month).

## Gas — quarterly meter readings (Mit Evida)

Source: `evida_gas_quarterly.csv`, from mit.evida.dk "Forbrugsudvikling"
(måler 1103276). Quarterly readings (first year irregular). "Forbrug" is
Evida's official consumption figure; note it runs ~7 % below the raw meter
difference (temperature/pressure correction), so use Forbrug, not deltas.

| Period | Forbrug m³ |
|--------|-----------:|
| 2022-05-01 – 2022-12-31 | 1,795 |
| 2023 Jan–Apr | 1,527 |
| 2023 May–Jun | 459 |
| 2023 Q3 | 475 |
| 2023 Q4 | 852 |
| 2024 Q1 | 1,281 |
| 2024 Q2 | 721 |
| 2024 Q3 | 384 |
| 2024 Q4 | 880 |
| 2025 Q1 | 1,365 |
| 2025 Q2 | 538 |
| 2025 Q3 | 493 |
| 2025 Q4 | 855 |
| 2026 Q1 | 1,576 |
| 2026 Q2 | 684 |

Yearly: **2023: 3,313 m³ · 2024: 3,266 m³ · 2025: 3,251 m³** · 2026 H1: 2,260 m³
(2022 from May: 1,795 m³; meter at supplier switch 2022-04-19: 26,174).

## Payments (from Budgetkonto CSV, 2023-03-17 – 2026-05-17)

Actual bank payments, from `../Budgetkonto_2023-03-17-2026-05-17.csv`.
`BS NETTOPOWER APS` is the combined el + gas supply bill (not separable);
`BS EVIDA SERVICE (NORD) A/S` is the separate gas distribution/transport bill,
which comes on top of NettoPower's gas price.

| Date | NettoPower DKK | | Date | Evida DKK |
|------------|----------:|-|------------|---------:|
| 2023-09-01 | 12,203.82 | | 2023-04-11 | 6,215.50 |
| 2023-12-01 | 27,988.38 | | 2023-07-06 | 1,140.55 |
| 2024-09-02 | 19,013.78 | | 2023-08-07 | 3,975.75 |
| 2024-12-02 | 20,179.26 | | 2023-11-06 | 7,150.10 |
| 2025-01-02 | 21,452.03 | | 2024-02-06 | 6,233.61 |
| 2025-04-01 | 14,205.35 | | 2024-05-06 | 2,235.85 |
| 2025-07-01 | 10,445.36 | | 2024-08-06 | 2,196.36 |
| 2025-10-01 | 13,693.00 | | 2024-11-06 | 6,121.42 |
| 2026-01-02 | 13,566.51 | | 2025-02-06 | 6,023.73 |
| 2026-04-01 |  9,768.82 | | 2025-05-06 | 2,385.43 |
|            |           | | 2025-08-06 | 1,626.61 |
|            |           | | 2025-11-06 | 6,563.08 |
|            |           | | 2026-02-06 | 5,860.64 |
|            |           | | 2026-05-06 | 3,604.49 |

Per year (payment date, not consumption period):

| Year | NettoPower DKK | Evida DKK | Sum |
|------|---------------:|----------:|--------:|
| 2023 (from 17/3) | 40,192.20 | 18,481.90 | 58,674.10 |
| 2024 | 39,193.04 | 16,787.24 | 55,980.28 |
| 2025 | 59,795.74 | 16,598.85 | 76,394.59 |
| 2026 (to 17/5) | 23,335.33 |  9,465.13 | 32,800.46 |
| **Total** | **162,516.31** | **61,333.12** | **223,849.43** |

Caveats when comparing with the usage table:

- Payments are quarterly aconto (prepaid) with later settlement, so payment
  dates lag/lead the consumption they cover.
- There are **no** NettoPower payments Mar–Aug 2023 or Jan–Aug 2024: bills in
  those periods were drawn from the prepaid "Min NettoPower konto" saldo
  (46,878 kr in Nov 2022, visible on the old statements) rather than via
  Betalingsservice. Payment sums therefore understate consumption cost in
  2023–24 by roughly that drawdown.

## Reconstruction risk analysis (2026-07-26)

NettoPower is under reconstruction (rekonstruktion); prepayments cover
through 2026-08-31. Analysis of aconto billed vs. expected actual usage:

The 2026 aconto invoices assume **10,460 kWh/year** electricity
("Estimeret årsforbrug"), but metered history shows **~6,000 kWh/year** —
a ~75 % overestimate on every el aconto. Gas estimates are roughly correct.

| | Billed (est.) | Expected actual | Over/(under)paid |
|---|---|---|---|
| F7797 (24/3–31/5) el | 1,966 kWh / 5,381.55 kr | ~1,133 kWh (metered) | +2,280 kr |
| F7797 gas | 566 m³ / 4,387.27 kr | ~641 m³ | −580 kr |
| F57906 (1/6–31/8) el | 2,614 kWh / 6,773.06 kr | ~1,005 kWh (proj.) | +4,170 kr |
| F57906 gas | 279 m³ / 2,339.97 kr | ~324 m³ (proj.) | −370 kr |
| **Net credit by 31 Aug 2026** | | | **≈ +5,500 kr** |

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

## Supplier switch to DCC Energi (planned, 2026-07)

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

| | Electricity | Gas |
|---|---|---|
| Målepunkts-ID (aftagenr.) | 571313174113617656 (74113617656) | 571515198002784898 (98002784898) |
| Målernummer | 21265781 | 1103276 (Evida) |
| Expected annual usage | **6,000 kWh** | **3,300 m³** |
| | *(do NOT accept NettoPower's inflated 10,460 kWh estimate)* | |

- Start date: **2026-09-01** (prepayment at NettoPower runs to 31 Aug; their
  next ~10,000 kr aconto would hit ~1 Sep).
- NettoPower notice: 15 workdays → cancel both agreements by ~2026-08-07
  (kundenr. 152240 / ref. N9484384, kundeservice@nettopower.dk).
- On switch: photo the gas meter reading; check Betalingsservice ~1 Sep and
  reject any NettoPower collection; demand slutafregning (~5,500 kr expected
  credit, see risk analysis above).

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
