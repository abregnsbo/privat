#!/usr/bin/env python3
"""
Analyse bank CSV exports from Jyske Bank (Budgetkonto + Lønkonto).
Categorises transactions and reports totals by period.

Usage:
  bank_analyse.py [-m|-y|--running N] [-u] [-d CAT[:PERIOD]] [-v] FILE ...

Examples:
  bank_analyse.py -m Budgetkonto_*.csv Lønkonto_*.csv
  bank_analyse.py --running 1 Budgetkonto_*.csv Lønkonto_*.csv
  bank_analyse.py -u Budgetkonto_*.csv Lønkonto_*.csv
  bank_analyse.py -d mad:2025-06 Lønkonto_*.csv
"""

import argparse
import csv
import glob
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

TODAY = date.today()

# --- Transactions to skip entirely (income + inter-account transfers) -----------
SKIP_RE = re.compile(
    r"^Lønoverf[øo]rsel$"
    r"|^Lønkonto$"
    r"|^Budgetkonto$"
    r"|^Til L[øo]nkonto"
    r"|B[øo]rne- og Ungeydelse"
    r"|FK-Feriepenge"
    r"|^Rente$"
    r"|OVERSKYDENDE SKAT"
    r"|Velliv Foreningen"
    r"|Skrotningsgodtg[øo]relse"
    r"|Larysa Lunar Bank"
    r"|restskat|^skat \d{4}\b"
    r"|^Til Opsparingskonto",
    re.IGNORECASE,
)

# GASTECH is a gas (heating) company — always el-varme regardless of bank category
GASTECH_RE = re.compile(r"GASTECH", re.IGNORECASE)

# --- Text-pattern rules: first match wins ---------------------------------------
TEXT_RULES = [
    ("el-varme", re.compile(
        r"EVIDA|LYNGBY-TAARB[ÆAæa]K FORSYNING|NETTOPOWER|\bStr[øo]m\b",
        re.IGNORECASE)),
    ("forsikring", re.compile(
        r"ALM\.?\s*BRAND FORSIKR|NEXT\s+forsikring",
        re.IGNORECASE)),
    ("A-kasse", re.compile(
        r"CA A-KASSE|AKADEMIKERNES A-KASSE",
        re.IGNORECASE)),
    ("pension", re.compile(
        r"\bNordnet\b",
        re.IGNORECASE)),
    ("internet", re.compile(
        r"^Internet$|\bHIPER\b",
        re.IGNORECASE)),
    ("mobil", re.compile(
        r"MobilePay\s+3\b"
        r"|CBB MOBIL|OISTER|OiSTER|TELMORE|NUUDAY|YOUSEE",
        re.IGNORECASE)),
    ("realkredit", re.compile(
        r"JYSKE REALKREDIT|Ejendomsskattel[åa]n",
        re.IGNORECASE)),
    ("bolig", re.compile(
        r"FURES[ØO]KVART"
        r"|LYNGBY-TAARB[ÆAæa]K KOMMUNE"
        r"|SKORSTENSFEJERMESTER|KHI SKORSTENSFEJ"
        r"|bl[øo]dg[øo]ringsanl[æa]g"
        r"|^bolig:|^hus:"
        r"|DKBRANDE\.DK|Aqua\s+Danmark"
        r"|WOODYWOOD|MyreExpressen|\bVVS\b"
        r"|FLUGGER|FLÜGGER|R[øo]VERK[øo]B",
        re.IGNORECASE)),
    ("transport", re.compile(
        r"taxa|taxi|rejsekort|DRIVR|DANTAXI",
        re.IGNORECASE)),
    ("bil", re.compile(
        r"SKATTESTYRELSEN MOTOR"
        r"|Ford Focus|\bT.cross\b"
        r"|^bil:"
        r"|skrotpr[æa]mie|bilk[øo]b|bilk[æa]b"
        r"|EasyPark|EASY PARK"
        r"|STOREB[ÆAæa]LT|[ØO]RESUNDSBRON|BROBIZZ|ØRESUND"
        r"|Fartb[øo]de|fartb[øo]de|parkeringssedl"
        r"|Q8 |SHELL |CIRCLE K|STATOIL|UNO.X|OK BENZIN|BENZIN"
        r"|DSB AUTO|AUTOPASS"
        r"|autoværksted|autovaerksted|autoteknik|autocenter"
        r"|GO.?ON\s+VIRUM",
        re.IGNORECASE)),
    ("sundhed", re.compile(
        r"tandl[æa]ge|TANDLAGE"
        r"|FITNESS WORLD|\bSATS\b|\bfitness\b|first fitness"
        r"|loebeshop|HEALTHWELL|\bterapi\b|GODZHAEVA",
        re.IGNORECASE)),
    ("support", re.compile(
        r"JULIA GLINSKA|Svitli|Anton Sido[rt]ov|Kovsharev"
        r"|DUDIKOV|Klym Jevlanov|VLADISMELNIX",
        re.IGNORECASE)),
    ("abonnement", re.compile(
        r"Economist|Berlingske|\bB\.DK\b"
        r"|BOOKMATE|SAXO\.COM|GODADDY"
        r"|NETFLIX|HBO |DISNEY\+?|VIAPLAY|TV 2 PLAY|DPLAY"
        r"|YOUTUBE|SPOTIFY|APPLE.*MUSIC",
        re.IGNORECASE)),
    ("ferie", re.compile(
        r"^skiferie|\bferie\b"
        r"|STANSTED|AIRPORT|LUFTHAVN"
        r"|RYANAIR|\bSAS\b|NORWEGIAN|EASYJET|WIZZ AIR|TRANSAVIA|FLIXBUS"
        r"|LONDON TOWER|FERRYHOPPER|LA CIME|DICE\.FM|HOSTDOMUS|lastminute"
        r"|UFFIZI|CARREFOUR"
        r"|PAYPAL\s*\*STANSTED"
        r"|hotel|BKG\*|booking\.com|\bBOOKING\b"
        r"|flybillet|flyrejse|\bRejser\b|Travellink"
        r"|GOITSCHEL|SESTRIERE|\bMAEVA\b|kiwi\.com",
        re.IGNORECASE)),
]


def classify(text: str, bank_main_cat: str, bank_cat: str, amount: float) -> str | None:
    """Return category name, or None to skip this transaction."""
    # Skip income and inter-account transfers
    if SKIP_RE.search(text):
        return None
    # Only track expenses (negative amounts); positive = income/refund
    if amount >= 0:
        return None

    if GASTECH_RE.search(text):
        return "el-varme"

    # MobilePay to Erik over 500 kr = fuel reimbursement
    if re.search(r"\bErik\b", text, re.IGNORECASE) and amount < -500:
        return "bil"

    # Fixed text-pattern rules
    for cat, rx in TEXT_RULES:
        if rx.search(text):
            return cat

    # VDK prefix = card used abroad → ferie
    if text.startswith("VDK "):
        return "ferie"

    # Bank-category rules (primarily useful for Lønkonto daily spending)
    bc = bank_cat.lower()
    bm = bank_main_cat.lower()
    if "hotel" in bc or "caravanning" in bc:
        return "ferie"
    if bm == "food" or "café, restaurant" in bc or "take away" in bc:
        return "mad"
    if "parking" in bc or "motor vehicle tax" in bc or "gasoline" in bc:
        return "bil"

    return "andet"


# --- CSV parsing ----------------------------------------------------------------

def _parse_amount(s: str) -> float:
    """Convert number string to float: '1,234.56' → 1234.56 (comma = thousands separator)"""
    return float(s.strip().replace(",", "") or "0")


def _parse_date(s: str) -> date:
    """Parse DD.MM.YYYY."""
    d, m, y = s.strip().split(".")
    return date(int(y), int(m), int(d))


def read_csv(path: str):
    """Yield transaction dicts from a Jyske Bank semicolon CSV export."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header row
        for row in reader:
            if len(row) < 3 or not row[0].strip():
                continue
            try:
                yield {
                    "date":     _parse_date(row[0]),
                    "text":     row[1].strip(),
                    "amount":   _parse_amount(row[2]),
                    "main_cat": row[7].strip() if len(row) > 7 else "",
                    "cat":      row[8].strip() if len(row) > 8 else "",
                }
            except (ValueError, IndexError):
                continue


# --- Main -----------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Categorise Jyske Bank CSV transactions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("files", nargs="*", metavar="FILE",
                    help="CSV export files (default: all *.csv in current directory)")

    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("-m", "--month", action="store_true",
                     help="Group by calendar month YYYY-MM")
    grp.add_argument("-y", "--year", action="store_true",
                     help="Group by calendar year YYYY (default)")
    grp.add_argument("-r", "--running", action="store_true",
                     help="Group by rolling 12-month windows relative to today"
                          " (last 12 months, 12-24 months ago, …)")

    ap.add_argument("-u", "--unrecognized", action="store_true",
                    help="List all transactions that fell into 'andet'")
    ap.add_argument("-d", metavar="CAT[:PERIOD]",
                    help="Show individual transactions for category CAT;"
                         " optionally filter to PERIOD prefix, e.g. -d mad:2025-06")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="Print processing summary to stderr")
    args = ap.parse_args()

    files = args.files or glob.glob("*.csv")
    if not files:
        ap.error("no CSV files found in current directory")

    def period_key(d: date) -> str:
        if args.running:
            n = (TODAY - d).days // 365
            return f"-{n + 1} year"
        if args.year:
            return str(d.year)
        return f"{d.year}-{d.month:02d}"

    # Parse -d argument
    det_cat = det_period = None
    if args.d:
        parts = args.d.split(":", 1)
        det_cat = parts[0].lower()
        det_period = parts[1] if len(parts) > 1 else None

    totals:   dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    andet_tx: list[tuple] = []
    detail_tx: list[tuple] = []
    n_total = n_skip = 0

    for fpath in files:
        for row in read_csv(fpath):
            n_total += 1
            d = row["date"]



            cat = classify(row["text"], row["main_cat"], row["cat"], row["amount"])
            if cat is None:
                n_skip += 1
                continue

            p = period_key(d)
            totals[cat][p] += -row["amount"]  # store as positive expense sum

            if cat == "andet":
                andet_tx.append((d, p, row["text"], row["amount"]))

            if det_cat and cat == det_cat:
                if det_period is None or p.startswith(det_period):
                    detail_tx.append((d, p, row["text"], row["amount"]))

    if args.verbose:
        cats = n_total - n_skip
        print(f"Processed {n_total} rows; skipped {n_skip}; categorised {cats}",
              file=sys.stderr)

    # --- Output -----------------------------------------------------------------

    if det_cat:
        for d, p, text, amt in sorted(detail_tx):
            print(f"{d.year}-{d.month:02d}\t{text}\t{amt:.2f}")
        return

    if args.unrecognized:
        print(f"{len(andet_tx)} transactions in 'andet':")
        for d, p, text, amt in sorted(andet_tx, key=lambda x: abs(x[3])):
            print(f"  {d.year}-{d.month:02d}  {text:<55}  {amt:>10.2f}")
        return

    # --- Tabular output --------------------------------------------------------
    all_cats = sorted(totals)
    all_periods = sorted({p for cat_data in totals.values() for p in cat_data})
    cat_w = max(len(c) for c in all_cats)

    MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if not args.year and not args.running:
        # One unified table: category blocks, rows = years, columns = months Jan–Dec
        years = sorted({p[:4] for p in all_periods})
        col_w = 8
        label_w = cat_w + 1 + 4  # "category year" prefix width
        hdr = f"{'':>{label_w}}" + "".join(f"{m:>{col_w}}" for m in MONTH_ABBR)
        print(hdr)
        print("-" * len(hdr))
        for cat in all_cats:
            print(f"{cat}")
            for yr in years:
                vals = [totals[cat].get(f"{yr}-{m:02d}", 0.0) for m in range(1, 13)]
                if not any(vals):
                    continue
                row = f"{'':>{cat_w + 1}}{yr:4}"
                for v in vals:
                    row += f"{v:{col_w},.0f}" if v else f"{'':>{col_w}}"
                print(row)
            print()

    else:
        # --year or --running: rows = categories, columns = periods
        if args.running:
            # sort oldest (-4 year) → newest (-1 year)
            cols = sorted(all_periods, key=lambda p: int(p.split()[0]))
        else:
            cols = all_periods  # already sorted chronologically

        col_w = max(10, max(len(p) for p in cols) + 2)
        hdr = f"{'':>{cat_w}}" + "".join(f"{p:>{col_w}}" for p in cols)
        sep = "-" * len(hdr)
        print(hdr)
        print(sep)
        for cat in all_cats:
            row = f"{cat:>{cat_w}}"
            for p in cols:
                v = totals[cat].get(p, 0.0)
                row += f"{v:{col_w},.0f}" if v else f"{'':>{col_w}}"
            print(row)


if __name__ == "__main__":
    main()
