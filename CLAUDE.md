# Claude Code — Project Notes

## Repository
Personal non-professional life — private finances, household expenses.

## Main script: `economy/bank_analyse.py`

Reads Jyske Bank CSV exports and categorises transactions into expense groups.
Run from the `economy/` directory (picks up all `*.csv` files automatically) or
pass explicit file paths.

### Input CSV format
Semicolon-delimited, UTF-8 with BOM. Columns:
```
Date;Text;Amount;Balance;Reconciled;AccountNumber;AccountName;MainCategory;Category;Comment
```
- **Date**: `DD.MM.YYYY`
- **Amount**: American number format — comma = thousands separator, period = decimal (`1,234.56`)
- **MainCategory / Category**: bank-assigned labels, used as fallback hints for food/parking etc.
- **CSV order**: sorted newest-first. The script uses this order directly for balance calculation — first row = most recent (end balance), last row = oldest (start balance).

Two account files are in use:
- `Budgetkonto_*.csv` — fixed household expenses (mortgage, insurance, utilities …)
- `Lønkonto_*.csv` — day-to-day spending (food, clothing, restaurants …)

### CLI
```
bank_analyse.py [-m|-y|-r] [-u|-U] [-d CAT[:PERIOD]] [-s PATTERN] [-v] [FILE ...]
```

| Flag | Meaning |
|------|---------|
| *(default)* | Yearly table: rows = categories, cols = years |
| `-m` | Monthly table: category blocks, rows = years, cols = Jan–Dec (also shows salary/transfers/other-income) |
| `-y` | Same as default |
| `-r` | Rolling-year table: rows = categories, cols = `-4 year` … `-1 year` (oldest→newest) |
| `-u` | List `andet` transactions aggregated by text (count + total) |
| `-U` | List `andet` transactions individually (one line per transaction) |
| `-d CAT[:PERIOD]` | List individual transactions for CAT; PERIOD is a prefix, e.g. `mad:2025-06` |
| `-s PATTERN` | Search all transactions by text regex, show category assigned |
| `-v` | Print processing stats and balance reconciliation to stderr |

`-d` and `-u` always show `YYYY-MM` regardless of grouping mode.

A reconciliation error (balance vs. categorised totals discrepancy > 0.01) is **always** printed to stderr, not just under `-v`.

### Categories

#### Expense categories (stored as positive totals)
| Category | What it contains |
|----------|-----------------|
| `A-kasse` | Unemployment insurance (CA A-KASSE, AKADEMIKERNES A-KASSE) |
| `abonnement` | Subscriptions: news (Economist, Berlingske), streaming (Netflix, HBO, SkyShowtime …), GoDaddy, Bookmate |
| `andet` | Unrecognised — use `-u` to review and extend patterns |
| `bil` | Car costs: vehicle tax, fuel (Q8, Shell …), parking, repairs, workshops, bridge tolls |
| `bolig` | Home costs excl. mortgage: municipality fees, chimney sweep, VVS, paint (Flügger), owners association |
| `el-varme` | Electricity + heating: NETTOPOWER, EVIDA, Lyngby-Taarbæk Forsyning, GASTECH, Strøm |
| `ferie` | Vacation: hotels, flights, VDK-prefix (foreign card), booking.com, ski trips |
| `forsikring` | Insurance: Alm. Brand, NEXT forsikring, Velliv |
| `internet` | Wired broadband only: Hiper / "Internet" subscription line |
| `mad` | Food: groceries, restaurants, takeaway (from Lønkonto, via bank Category) |
| `mobil` | Mobile subscriptions: 3, CBB Mobil, OiSTER, Telmore |
| `pension` | Pension savings: Nordnet rate pension |
| `realkredit` | Mortgage (Jyske Realkredit) |
| `sundhed` | Health: dentist, fitness (SATS, Fitness World), running shop, therapy, Healthwell, iHerb |
| `support` | Regular personal support payments: Julia Glinska, Anton Sidorov, Svitli, Klym Jevlanov, Kovsharev, Dudikov, Vladismelnix, DeepStateUA, MonodirectFJ |
| `transport` | Public transport: DSB Rejsekort, taxi, Dantaxi, Drivr |

#### Income/transfer categories (stored as raw signed amounts — not in expense totals)
| Category | What it contains |
|----------|-----------------|
| `salary` | Salary, holiday pay, tax refunds (OVERSKYDENDE SKAT, restskat, Overf. Skattestyrels, Til Frivillig ind skat), DTU/NTG income |
| `transfers` | Inter-account transfers (Lønkonto ↔ Budgetkonto ↔ Opsparingskonto), Overførsel, Larysa Lunar Bank |
| `other-income` | Child benefit, interest, and any other unrecognised positive amounts |

In `-y`/`-r`/`-m` output, after the expense block: `total-exp`, then `salary` / `transfers` / `other-income`, then `total-income`.

### Classification logic (`classify()`)
Priority order (first match wins):
1. Hard-coded override: `Axel Bogdan Bregnsbo` + amount 38495 → `salary`
2. Hard-coded override: 2024-03 `Faktura` 12000 kr → `ferie`
3. `GASTECH_RE` — always → `el-varme`
4. MobilePay to Erik, 450–800 kr, non-round amount → `bil` (fuel reimbursement)
5. `Til L-T Kommune`, 400–1000 kr → `bil` (parking ticket)
6. `TEXT_RULES` list — regex on the `Text` field (first match wins)
7. `VDK ` prefix → `ferie` (card used abroad), with exceptions:
   - `Lygten Bazar`, `Mariam M Marked`, `MOB.PAY*(FOOD|CAFE)` → `mad`
   - `Zara`, `HM`, `Zalando`, `Apotek`, `nogler og haele` → `andet`
8. `\bMagasin\b` → `andet`
9. Bank `Category` field: hotel/caravanning → `ferie`; food/café/takeaway → `mad`; parking/motor tax/gasoline → `bil`
10. Fallback → `andet`; if amount > 0 → `other-income`

### Balance reconciliation
The script tracks opening and closing balances from the CSV files:
- Uses **CSV row order** (not date sort) to find start/end balances — avoids same-date ambiguity.
- `bal_start` = last CSV row's balance minus that row's amount (balance before oldest transaction).
- `bal_end` = first CSV row's balance (balance after most recent transaction).
- Discrepancy = `(bal_end − bal_start) − (total_income − total_expenses)` — should be ~0.

### Workflow for improving patterns
1. Run `bank_analyse.py -u | tail -50` to see largest unrecognised transactions.
2. Annotate which category each line should go into.
3. Add patterns to `TEXT_RULES` (or VDK exceptions in `classify()`) in `bank_analyse.py`.
4. Re-run and verify totals shift correctly.
5. Use `-d CATEGORY` to spot-check individual transactions in a category.

Prefer generic patterns over exact string matches — e.g. `autoteknik` rather than
a specific shop name, `\bVVS\b` rather than one plumber.

### Amounts currently in `andet` that are deliberately left unclassified
Personal transfers (Eivind, Viktor, various MobilePay to named individuals),
IKEA, Elgiganten (electronics), clothing (Zara, Zalando, Netlingeri), BET365 (gambling),
Visa Credit card payments, pharmacies (Apotek), and other one-off purchases with no clear category.
