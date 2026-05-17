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

Two account files are in use:
- `Budgetkonto_*.csv` — fixed household expenses (mortgage, insurance, utilities …)
- `Lønkonto_*.csv` — day-to-day spending (food, clothing, restaurants …)

### CLI
```
bank_analyse.py [-m|-y|-r] [-u] [-d CAT[:PERIOD]] [-v] [FILE ...]
```

| Flag | Meaning |
|------|---------|
| *(default)* | Monthly table: category blocks, rows = years, cols = Jan–Dec |
| `-m` | Same as default |
| `-y` | Yearly table: rows = categories, cols = years |
| `-r` | Rolling-year table: rows = categories, cols = `-4 year` … `-1 year` (oldest→newest) |
| `-u` | List unrecognised transactions (`andet`), sorted by abs(amount) ascending |
| `-d CAT[:PERIOD]` | List individual transactions for CAT; PERIOD is a prefix, e.g. `mad:2025-06` |
| `-v` | Print processing stats to stderr |

`-d` and `-u` always show `YYYY-MM` regardless of grouping mode.

### Categories

| Category | What it contains |
|----------|-----------------|
| `A-kasse` | Unemployment insurance (CA A-KASSE, AKADEMIKERNES A-KASSE) |
| `abonnement` | Subscriptions: news (Economist, Berlingske), streaming (Netflix, HBO …), GoDaddy, Bookmate |
| `andet` | Unrecognised — use `-u` to review and extend patterns |
| `bil` | Car costs: vehicle tax, fuel (Q8, Shell …), parking, repairs, workshops, bridge tolls |
| `bolig` | Home costs excl. mortgage: municipality fees, chimney sweep, VVS, paint (Flügger), owners association |
| `el-varme` | Electricity + heating: NETTOPOWER, EVIDA, Lyngby-Taarbæk Forsyning, GASTECH, Strøm |
| `ferie` | Vacation: hotels, flights, VDK-prefix (foreign card), booking.com, ski trips |
| `forsikring` | Insurance: Alm. Brand, NEXT forsikring |
| `internet` | Wired broadband only: Hiper / "Internet" subscription line |
| `mad` | Food: groceries, restaurants, takeaway (from Lønkonto, via bank Category) |
| `mobil` | Mobile subscriptions: 3, CBB Mobil, OiSTER, Telmore |
| `pension` | Pension savings: Nordnet rate pension |
| `realkredit` | Mortgage (Jyske Realkredit) + property tax loans (Ejendomsskattelån) |
| `sundhed` | Health: dentist, fitness (SATS, Fitness World), running shop, therapy, Healthwell |
| `support` | Regular personal support payments: Julia Glinska, Anton Sidorov, Svitli, Klym Jevlanov, Kovsharev, Dudikov, Vladismelnix |
| `transport` | Public transport: DSB Rejsekort, taxi, Dantaxi, Drivr |

### Classification logic (`classify()`)
Priority order (first match wins):
1. `SKIP_RE` — skip income, inter-account transfers, savings, tax payments
2. Skip positive amounts (income/refunds)
3. `GASTECH_RE` — always → `el-varme` (gas heating company, bank may mislabel as electricity)
4. MobilePay to Erik > 500 kr → `bil` (fuel reimbursement)
5. `TEXT_RULES` list — regex on the `Text` field
6. `VDK ` prefix → `ferie` (card used abroad)
7. Bank `Category` field: hotel/caravanning → `ferie`; food/café/takeaway → `mad`; parking/motor tax/gasoline → `bil`
8. Fallback → `andet`

### Workflow for improving patterns
1. Run `bank_analyse.py -u | tail -50` to see largest unrecognised transactions.
2. Annotate which category each line should go into.
3. Add patterns to `TEXT_RULES` or `SKIP_RE` in `bank_analyse.py`.
4. Re-run and verify totals shift correctly.
5. Use `-d CATEGORY` to spot-check individual transactions in a category.

Prefer generic patterns over exact string matches — e.g. `autoteknik` rather than
a specific shop name, `\bVVS\b` rather than one plumber.

### Amounts currently in `andet` that are deliberately left unclassified
Personal transfers (Eivind, Viktor, various MobilePay to named individuals),
IKEA, Elgiganten (electronics), clothing (Zara, Netlingeri), BET365 (gambling),
Visa Credit card payments, and other one-off purchases with no clear category.
