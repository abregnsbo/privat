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

from __future__ import annotations

import argparse
import csv
import glob
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

TODAY = date.today()

# --- Real income: salary, benefits, tax refunds ---------------------------------
INCOME_RE = re.compile(
    r"L[øo]noverf[øo]rsel"
    r"|\bSalary\b"
    r"|B[øo]rne- og Ungeydelse"
    r"|FK-Feriepenge"
    r"|OVERSKYDENDE SKAT|SKATTEFORVALTNINGEN"
    r"|Danmarks Tekniske"
    r"|NTG A/S",
    re.IGNORECASE,
)

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
    r"|^Til Opsparingskonto"
    r"|^Fra Opsparingskonto",
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
        r"ALM\.?\s*BRAND FORSIKR|NEXT\s+forsikring|Police\s+\d+",
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
        r"|CBB MOBIL|OISTER|OiSTER|TELMORE|NUUDAY|YOUSEE|FLEXII|UNOTEL",
        re.IGNORECASE)),
    ("realkredit", re.compile(
        r"JYSKE REALKREDIT",
        re.IGNORECASE)),
    ("bolig", re.compile(
        r"FURES[ØO]KVART"
        r"|LYNGBY-TAARB[ÆAæa]K KOMMUNE"
        r"|SKORSTENSFEJERMESTER|KHI SKORSTENSFEJ"
        r"|bl[øo]dg[øo]ringsanl[æa]g"
        r"|^bolig:|^hus:"
        r"|DKBRANDE\.DK|Aqua\s+Danmark"
        r"|WOODYWOOD|MyreExpressen|\bVVS\b"
        r"|FLUGGER|FLÜGGER|R[øo]VERK[øo]B|Pudser|Ejendomsskattel[åa]n|LEAKBOT"
        r"|\bHARALD\s+NYBORG\b|\bSilvan\b|\bJOHANNESFOG",
        re.IGNORECASE)),
    ("ferie", re.compile(
        r"LONDON.?TAXI",
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
        r"|Fartb[øo]de|fartb[øo]de|parkeringssedl|p-b[øo]de"
        r"|Q8 |SHELL |CIRCLE K|STATOIL|UNO.X|OK BENZIN|BENZIN|\bDK OK\b|\bF24\b"
        r"|DSB AUTO|AUTOPASS"
        r"|autoværksted|autovaerksted|autoteknik|autocenter|Autohuset"
        r"|GO.?ON|CARGLASS|bilsyn|TANK KAI DIGE",
        re.IGNORECASE)),
    ("sundhed", re.compile(
        r"tandl[æa]ge|TANDLAGE"
        r"|FITNESS WORLD|\bSATS\b|\bfitness\b|first fitness"
        r"|loebeshop|HEALTHWELL|\bterapi\b|GODZHAEVA"
        r"|MASSAGE.TID|I care massage|MMSPORTSSTORE|SPORTSTIMING|PURE.?GYM|FitnessX",
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
        r"|GOITSCHEL|SESTRIERE|\bMAEVA\b|kiwi\.com|AUTOST DIREZIONE",
        re.IGNORECASE)),
]


def classify(text: str, bank_main_cat: str, bank_cat: str, amount: float) -> str | None:
    """Return category name, or None to skip this transaction."""
    if SKIP_RE.search(text):
        return None

    if GASTECH_RE.search(text):
        return "el-varme"

    # MobilePay to Erik: fuel reimbursement if 600–900 and not a round amount (not ending in 00 or 50)
    if re.search(r"\bErik\b", text, re.IGNORECASE):
        abs_amt = abs(amount)
        if 450 <= abs_amt <= 800 and round(abs_amt) % 100 not in (0, 50):
            return "bil"

    # Til L-T Kommune in 400–1000 range = parking ticket
    if re.search(r"Til L-T\s+Kommune", text, re.IGNORECASE) and -1000 <= amount <= -400:
        return "bil"

    # Fixed text-pattern rules
    for cat, rx in TEXT_RULES:
        if rx.search(text):
            return cat

    # VDK prefix = card used abroad → ferie (with exceptions)
    if text.startswith("VDK "):
        if re.search(r"Lygten Bazar", text, re.IGNORECASE):
            return "mad"
        if re.search(r"Zara|\bHM\b", text, re.IGNORECASE):
            return "andet"
        return "ferie"

    # Explicit andet overrides — prevent bank-category fallback from misfiring
    if re.search(r"\bMagasin\b", text, re.IGNORECASE):
        return "andet"

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


def remove_transfers(files_txs: list[list[dict]]) -> list[dict]:
    """Cancel matching cross-account debit/credit pairs (same date, same absolute amount)."""
    tagged: list[tuple[int, dict]] = []
    for fi, txs in enumerate(files_txs):
        for tx in txs:
            tagged.append((fi, tx))

    groups: dict[tuple, list[int]] = defaultdict(list)
    for i, (fi, tx) in enumerate(tagged):
        groups[(tx["date"], round(abs(tx["amount"]), 2))].append(i)

    to_remove: set[int] = set()
    for indices in groups.values():
        by_file: list[list[int]] = [[], []]
        for i in indices:
            by_file[tagged[i][0]].append(i)
        for neg_fi, pos_fi in ((0, 1), (1, 0)):
            negs = [i for i in by_file[neg_fi] if tagged[i][1]["amount"] < 0]
            poss = [i for i in by_file[pos_fi] if tagged[i][1]["amount"] > 0]
            for j in range(min(len(negs), len(poss))):
                to_remove.add(negs[j])
                to_remove.add(poss[j])

    return [tx for i, (_, tx) in enumerate(tagged) if i not in to_remove]


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
                    help="List 'andet' transactions aggregated by text (count + total)")
    ap.add_argument("-U", action="store_true",
                    help="List 'andet' transactions individually (one line per transaction)")
    ap.add_argument("-d", metavar="CAT[:PERIOD]",
                    help="Show individual transactions for category CAT;"
                         " optionally filter to PERIOD prefix, e.g. -d mad:2025-06")
    ap.add_argument("-s", metavar="PATTERN",
                    help="Regex search all transactions by text, showing assigned category")
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
        if args.month:
            return f"{d.year}-{d.month:02d}"
        return str(d.year)  # default: yearly

    # Parse -d argument
    det_cat = det_period = None
    if args.d:
        parts = args.d.split(":", 1)
        det_cat = parts[0].lower()
        det_period = parts[1] if len(parts) > 1 else None

    search_re = re.compile(args.s, re.IGNORECASE) if args.s else None

    totals:       dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    salary:       dict[str, float] = defaultdict(float)
    transfers:    dict[str, float] = defaultdict(float)
    other_income: dict[str, float] = defaultdict(float)
    andet_tx:  list[tuple] = []
    detail_tx: list[tuple] = []
    search_tx: list[tuple] = []
    n_total = n_skip = 0

    files_txs = [list(read_csv(f)) for f in files]
    all_rows = remove_transfers(files_txs) if len(files) == 2 else [tx for txs in files_txs for tx in txs]

    for row in all_rows:
        n_total += 1
        d = row["date"]
        p = period_key(d)

        # Determine effective category once per transaction
        if row["amount"] > 0 and (
            INCOME_RE.search(row["text"])
            or (re.search(r"Axel Bogdan Bregnsbo", row["text"], re.IGNORECASE)
                and round(row["amount"]) == 38495)
        ):
            eff_cat = "salary"
        elif (d.year == 2024 and d.month == 3
              and re.search(r"Faktura", row["text"], re.IGNORECASE)
              and round(abs(row["amount"])) == 12000):
            eff_cat = "ferie"
        else:
            eff_cat = classify(row["text"], row["main_cat"], row["cat"], row["amount"]) or "skip"
            if eff_cat == "andet" and row["amount"] > 0:
                if re.search(r"Overf[øo]rsel", row["text"], re.IGNORECASE):
                    eff_cat = "transfers"
                else:
                    eff_cat = "other-income"

        if search_re and search_re.search(row["text"]):
            search_tx.append((d, row["text"], row["amount"], eff_cat))

        if eff_cat == "salary":
            salary[p] += row["amount"]
            if det_cat == "salary":
                if det_period is None or p.startswith(det_period):
                    detail_tx.append((d, p, row["text"], row["amount"]))
            n_skip += 1
            continue

        if eff_cat == "transfers":
            transfers[p] += row["amount"]
            if det_cat == "transfers":
                if det_period is None or p.startswith(det_period):
                    detail_tx.append((d, p, row["text"], row["amount"]))
            n_skip += 1
            continue

        if eff_cat == "other-income":
            other_income[p] += row["amount"]
            if det_cat == "other-income":
                if det_period is None or p.startswith(det_period):
                    detail_tx.append((d, p, row["text"], row["amount"]))
            n_skip += 1
            continue

        if eff_cat == "skip":
            n_skip += 1
            continue

        totals[eff_cat][p] += -row["amount"]

        if eff_cat == "andet":
            andet_tx.append((d, p, row["text"], row["amount"]))

        if det_cat and eff_cat == det_cat:
            if det_period is None or p.startswith(det_period):
                detail_tx.append((d, p, row["text"], row["amount"]))

    if args.verbose:
        cats = n_total - n_skip
        print(f"Processed {n_total} rows; skipped {n_skip}; categorised {cats}",
              file=sys.stderr)

    # --- Output -----------------------------------------------------------------

    if args.s:
        rows = [(f"{d.year}-{d.month:02d}", text, f"{amt:.0f}", cat)
                for d, text, amt, cat in sorted(search_tx)]
        text_w = max((len(r[1]) for r in rows), default=0)
        amt_w  = max((len(r[2]) for r in rows), default=0)
        cat_w2 = max((len(r[3]) for r in rows), default=0)
        for period, text, amt_str, cat in rows:
            print(f"{period}  {text:<{text_w}}  {amt_str:>{amt_w}}  {cat:<{cat_w2}}")
        return

    if det_cat:
        rows = [(f"{d.year}-{d.month:02d}", text, f"{amt:.0f}")
                for d, p, text, amt in sorted(detail_tx)]
        text_w = max((len(r[1]) for r in rows), default=0)
        amt_w  = max((len(r[2]) for r in rows), default=0)
        for period, text, amt_str in rows:
            print(f"{period}  {text:<{text_w}}  {amt_str:>{amt_w}}")
        return

    if args.unrecognized:
        groups: dict[str, list[float]] = defaultdict(list)
        for _, _, text, amt in andet_tx:
            groups[text].append(amt)
        aggregated = sorted(
            ((text, len(amts), sum(amts)) for text, amts in groups.items()),
            key=lambda x: abs(x[2]),
        )
        text_w = max((len(r[0]) for r in aggregated), default=0)
        amt_w  = max((len(f"{r[2]:,.0f}") for r in aggregated), default=0)
        print(f"{len(andet_tx)} transactions in 'andet' ({len(aggregated)} unique):")
        for text, count, total in aggregated:
            print(f"  {count:>3}  {text:<{text_w}}  {total:{amt_w},.0f}")
        return

    if args.U:
        print(f"{len(andet_tx)} transactions in 'andet':")
        for d, p, text, amt in sorted(andet_tx, key=lambda x: abs(x[3])):
            print(f"  {d.year}-{d.month:02d}  {text:<55}  {amt:>10.2f}")
        return

    # --- Tabular output --------------------------------------------------------
    all_cats = sorted(totals)
    all_periods = sorted({p for cat_data in totals.values() for p in cat_data})
    cat_w = max(len(c) for c in all_cats) + 2

    MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if args.month:
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

        print("-" * len(hdr))
        for label, src in (("salary", salary), ("transfers", transfers), ("other-income", other_income)):
            print(f"{label}")
            for yr in years:
                vals = [src.get(f"{yr}-{m:02d}", 0.0) for m in range(1, 13)]
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

        print()
        total_exp_row = f"{'total-exp':>{cat_w}}"
        for p in cols:
            v = sum(totals[cat].get(p, 0.0) for cat in all_cats)
            total_exp_row += f"{v:{col_w},.0f}" if v else f"{'':>{col_w}}"
        print(total_exp_row)

        print()
        for label, src in (("salary", salary), ("transfers", transfers), ("other-income", other_income)):
            summary_row = f"{label:>{cat_w}}"
            for p in cols:
                v = src.get(p, 0.0)
                summary_row += f"{v:{col_w},.0f}" if v else f"{'':>{col_w}}"
            print(summary_row)

        print()
        total_income_row = f"{'total-income':>{cat_w}}"
        for p in cols:
            v = salary.get(p, 0.0) + transfers.get(p, 0.0) + other_income.get(p, 0.0)
            total_income_row += f"{v:{col_w},.0f}" if v else f"{'':>{col_w}}"
        print(total_income_row)


if __name__ == "__main__":
    main()
