#!/usr/bin/env python3
"""
Analyse bank CSV exports from Jyske Bank (Budgetkonto + Lønkonto).
Categorises transactions and reports totals by period.

Usage:
  bank_analyse.py [-m|-y|--running N] [-u] [-d CAT[:PERIOD]] [--budget-only] [-v] FILE ...

Examples:
  bank_analyse.py -m Budgetkonto_*.csv Lønkonto_*.csv
  bank_analyse.py --running 1 Budgetkonto_*.csv Lønkonto_*.csv
  bank_analyse.py -u Budgetkonto_*.csv Lønkonto_*.csv
  bank_analyse.py -d mad:2025-06 Lønkonto_*.csv
  bank_analyse.py --budget-only -r Budgetkonto_*.csv
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

# GASTECH is a gas (heating) company — always el-varme regardless of bank category
GASTECH_RE = re.compile(r"GASTECH", re.IGNORECASE)

# Positive patterns for genuine travel expenses → ferie.
# Used both in TEXT_RULES and in the VDK block so that VDK transactions not matched
# here fall through to bank-category rules instead of defaulting to ferie.
TRAVEL_RE = re.compile(
    # Freeform travel notes (manually entered bank labels)
    r"^skiferie|^ferie:|\bferie\b|flybillet|flyrejse|\bRejser\b"
    # Airlines and flight booking
    r"|\bNORWEGIAN\s+A\b|\bRYANAIR\b|\bSAS\b|\bEASYJET\b|\bWIZZ\s+AIR\b|\bTRANSAVIA\b|\bFLIXBUS\b"
    r"|lastminute|Travellink|kiwi\.com|\bESKY\b"
    # Airport infrastructure: transport, food, shops
    r"|\bAIRPORT\b|\bLUFTHAVN\b|STANSTED"
    r"|\bFLYTOGET\b|HMSHost|DUTY.?FREE|\bDUFRITAL\b|AELIA\s+DUTY\s+FREE"
    r"|\bENTUR\b|BLQ\s+Schengen|FASTY\s+APT|RELAY\d{6}PV"
    # Hotels and accommodation
    r"|hotel|BKG\*|booking\.com|\bBOOKING\b|\bHOSTDOMUS\b"
    r"|\bPREMIER\s+INN\b|\bPREMIER\s+SUITES\b|\bComwell\b|\bSINATUR\b"
    r"|\bSONDER\b|\bMAEVA\b|\bBROHOLM\s+SLOT\b|LONDON\s+TOWER"
    # Car rental
    r"|ENTERPRISE\s+RENT.?A.?CAR|Cars\s+on\s+Booking"
    # Public transport while travelling
    r"|EDINBURGH\s+TRAMS|MTA\*METROCARD|NYC\s+FERRY|\bMEGABUS\b"
    r"|\bOMIO\b|ITALIARAIL|TPG\s+Transports\s+Publics|TFL\s+TRAVEL"
    r"|TPER\s+SPA|AUTOST\s+DIREZIONE|AUTOVIA\s+BERGAMO"
    r"|PAYPAL\s*\*STANSTED|LONDON.?TAXI"
    # Ferries
    r"|\bFERRYHOPPER\b|\bMOBY\b"
    # Ski and mountain
    r"|GOITSCHEL|\bSESTRIERE\b|LA\s+CIME|CARREFOUR\s+PECLET"
    r"|CHALET\s+DE\s+THORENS|\bSHERPA\b|\bLIFT\s+CLUB\b|\bALPETTE\b|\bV\s+T\s+S\b"
    # Tourist attractions and museum tickets
    r"|\bUFFIZI\b|MIDATICKET|ESERCIZIO\s+PROMOZIONE\s+TUR|PARCO\s+METRI\s+VILLASIMIUS"
    # Events and experiences (ticketed activities while travelling)
    r"|\bDICE\.FM\b|FEVER\*"
    # Travel admin
    r"|UKVI\s+ETAMOB",
    re.IGNORECASE
)

# --- Text-pattern rules: first match wins ---------------------------------------
TEXT_RULES = [
    ("salary", re.compile(
        r"L[øo]noverf[øo]rsel"
        r"|\bSalary\b"
        r"|FK-Feriepenge"
        r"|restskat|^skat \d{4}\b"
        r"|OVERSKYDENDE SKAT|SKATTEFORVALTNINGEN"
        r"|Overf\. Skattestyrels|Til Frivillig ind skat"
        r"|Danmarks Tekniske|NTG A/S",
        re.IGNORECASE)),
    ("transfers", re.compile(
        r"^L[øo]nkonto$|^Budgetkonto$|^Til L[øo]nkonto|^Fra Budgetkonto"
        r"|Larysa Lunar Bank"
        r"|^Til Opsparingskonto|^Fra Opsparingskonto"
        r"|Overf[øo]rsel",
        re.IGNORECASE)),
    ("other-income", re.compile(
        r"B[øo]rne- og Ungeydelse|^Rente$",
        re.IGNORECASE)),
    ("el-varme", re.compile(
        r"EVIDA|LYNGBY-TAARB[ÆAæa]K FORSYNING|NETTOPOWER|\bStr[øo]m\b",
        re.IGNORECASE)),
    ("forsikring", re.compile(
        r"ALM\.?\s*BRAND FORSIKR|NEXT\s+forsikring|Police\s+\d+|Velliv Foreningen",
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
    ("ferie", TRAVEL_RE),
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
        r"|GO.?ON|CARGLASS|bilsyn|TANK KAI DIGE|Skrotningsgodtg[øo]relse",
        re.IGNORECASE)),
    ("sundhed", re.compile(
        r"tandl[æa]ge|TANDLAGE"
        r"|FITNESS WORLD|\bSATS\b|\bfitness\b|first fitness"
        r"|loebeshop|HEALTHWELL|\bterapi\b|GODZHAEVA"
        r"|MASSAGE.TID|I care massage|MMSPORTSSTORE|SPORTSTIMING|PURE.?GYM|FitnessX|\biherb\b",
        re.IGNORECASE)),
    ("support", re.compile(
        r"JULIA GLINSKA|Svitli|Anton Sido[rt]ov|ANTONSIDORO|Kovsharev"
        r"|DUDIKOV|Klym Jevlanov|VLADISMELNIX|\bDeepStateUA\b|\bMonodirectFJ"
        r"|\bMONOBANK\b|STERNENKO",
        re.IGNORECASE)),
    ("abonnement", re.compile(
        r"Economist|Berlingske|\bB\.DK\b"
        r"|BOOKMATE|SAXO\.COM|GODADDY"
        r"|NETFLIX|HBO |DISNEY\+?|VIAPLAY|TV 2 PLAY|DPLAY"
        r"|YOUTUBE|SPOTIFY|APPLE.*MUSIC|SKY.?SHOWTIME",
        re.IGNORECASE)),
]


def classify(text: str, bank_main_cat: str, bank_cat: str, amount: float) -> str:
    """Return category name for this transaction."""
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

    # VDK prefix = physical card swipe; only route to ferie if TRAVEL_RE matches.
    # Everything else falls through to bank-category rules and the andet default.
    if text.startswith("VDK "):
        if re.search(r"Lygten Bazar|Mariam M Marked|MOB\.PAY\*(FOOD|CAFE)", text, re.IGNORECASE):
            return "mad"
        if re.search(r"Zara|\bHM\b|\bZalando\b|\bApotek\b|nogler og haele", text, re.IGNORECASE):
            return "andet"
        if TRAVEL_RE.search(text):
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
    """Yield transaction dicts from a Jyske Bank semicolon CSV export.

    CSV is sorted newest-first; line numbers start at 2 (row 1 is the header).
    """
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header row
        for lineno, row in enumerate(reader, start=2):
            if len(row) < 3 or not row[0].strip():
                continue
            try:
                yield {
                    "date":     _parse_date(row[0]),
                    "text":     row[1].strip(),
                    "amount":   _parse_amount(row[2]),
                    "balance":  _parse_amount(row[3]) if len(row) > 3 else 0.0,
                    "account":  row[6].strip() if len(row) > 6 else "",
                    "main_cat": row[7].strip() if len(row) > 7 else "",
                    "cat":      row[8].strip() if len(row) > 8 else "",
                    "lineno":   lineno,
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
    grp.add_argument("-a", "--avg", action="store_true",
                     help="Monthly average: like -y but each value divided by the number of"
                          " months spanned by data in that year")

    ap.add_argument("-u", "--unrecognized", action="store_true",
                    help="List 'andet' transactions aggregated by text (count + total)")
    ap.add_argument("-U", action="store_true",
                    help="List 'andet' transactions individually (one line per transaction)")
    ap.add_argument("-d", metavar="CAT[:PERIOD]",
                    help="Show individual transactions for category CAT;"
                         " optionally filter to PERIOD prefix, e.g. -d mad:2025-06")
    ap.add_argument("-s", metavar="PATTERN",
                    help="Regex search all transactions by text, showing assigned category")
    ap.add_argument("--budget-only", action="store_true",
                    help="Withdrawal report for the Budgetkonto account only: every debit"
                         " (incl. transfers out to Lønkonto) grouped by category, with a"
                         " total-withdrawal row and a per-month average. Honours -m/-y/-r.")
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

    totals:         dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    salary:         dict[str, float] = defaultdict(float)
    transfers:      dict[str, float] = defaultdict(float)
    other_income:   dict[str, float] = defaultdict(float)
    dates_per_year: dict[int, list[int]] = defaultdict(list)
    andet_tx:  list[tuple] = []
    detail_tx: list[tuple] = []
    search_tx: list[tuple] = []
    n_total = 0
    n_parsed = 0  # rows successfully parsed (before categorisation)

    files_txs = [list(read_csv(f)) for f in files]

    # Compute start/end balances across all accounts.
    # CSVs are sorted newest-first: first row = most recent (end), last row = oldest (start).
    # Using CSV order avoids ambiguity when multiple transactions share the same date.
    bal_start = bal_end = 0.0
    for file_txs in files_txs:
        if not file_txs:
            continue
        bal_end   += file_txs[0]["balance"]
        bal_start += file_txs[-1]["balance"] - file_txs[-1]["amount"]

    all_rows = [tx for txs in files_txs for tx in txs]
    n_parsed = len(all_rows)

    # --- Budgetkonto withdrawal report -----------------------------------------
    # Self-contained: every debit on the Budgetkonto account (including transfers
    # out to Lønkonto) counted as a withdrawal, grouped by category and period.
    if args.budget_only:
        wtotals: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        months_seen: dict[str, set] = defaultdict(set)
        for row in all_rows:
            if "budget" not in row["account"].lower():
                continue
            if row["amount"] >= 0:
                continue  # withdrawals (debits) only
            d = row["date"]
            p = period_key(d)
            # same hard-coded overrides as the main accounting loop
            if (re.search(r"Axel Bogdan Bregnsbo", row["text"], re.IGNORECASE)
                    and round(row["amount"]) == 38495):
                cat = "salary"
            elif (d.year == 2024 and d.month == 3
                  and re.search(r"Faktura", row["text"], re.IGNORECASE)
                  and round(abs(row["amount"])) == 12000):
                cat = "ferie"
            else:
                cat = classify(row["text"], row["main_cat"], row["cat"], row["amount"])
            wtotals[cat][p] += -row["amount"]
            months_seen[p].add((d.year, d.month))

        cats = sorted(wtotals, key=lambda c: -sum(wtotals[c].values()))
        periods = sorted({p for c in wtotals.values() for p in c})
        if args.running:
            cols = sorted(periods, key=lambda p: int(p.split()[0]))
        else:
            cols = periods

        # -a: divide every value by the number of months with data in that period,
        # turning the whole table into monthly averages (as in the normal -a view).
        def divisor(p: str) -> int:
            return (len(months_seen[p]) or 1) if args.avg else 1

        def col_hdr(p: str) -> str:
            return f"{p}({len(months_seen[p])}mo)" if args.avg else p

        labels = cats + ["total-withdrawal", "per month"]
        cat_w = max(len(c) for c in labels) + 2
        col_w = max(10, max((len(col_hdr(p)) for p in cols), default=0) + 2)
        hdr = f"{'':>{cat_w}}" + "".join(f"{col_hdr(p):>{col_w}}" for p in cols)
        print("Budgetkonto withdrawals (debits only)")
        print(hdr)
        print("-" * len(hdr))
        for cat in cats:
            line = f"{cat:>{cat_w}}"
            for p in cols:
                v = wtotals[cat].get(p, 0.0)
                line += f"{v / divisor(p):{col_w},.0f}" if v else f"{'':>{col_w}}"
            print(line)

        print("-" * len(hdr))
        tot_line = f"{'total-withdrawal':>{cat_w}}"
        for p in cols:
            v = sum(wtotals[c].get(p, 0.0) for c in cats)
            tot_line += f"{v / divisor(p):{col_w},.0f}" if v else f"{'':>{col_w}}"
        print(tot_line)
        # Redundant under -a (every row is already a monthly average).
        if not args.avg:
            avg_line = f"{'per month':>{cat_w}}"
            for p in cols:
                v = sum(wtotals[c].get(p, 0.0) for c in cats)
                n = len(months_seen[p]) or 1
                avg_line += f"{v / n:{col_w},.0f}" if v else f"{'':>{col_w}}"
            print(avg_line)
        return

    for row in all_rows:
        n_total += 1
        d = row["date"]
        p = period_key(d)
        dates_per_year[d.year].append(d.month)

        # Determine effective category once per transaction
        if (re.search(r"Axel Bogdan Bregnsbo", row["text"], re.IGNORECASE)
                and round(row["amount"]) == 38495):
            eff_cat = "salary"
        elif (d.year == 2024 and d.month == 3
              and re.search(r"Faktura", row["text"], re.IGNORECASE)
              and round(abs(row["amount"])) == 12000):
            eff_cat = "ferie"
        else:
            eff_cat = classify(row["text"], row["main_cat"], row["cat"], row["amount"])
            if eff_cat == "andet" and row["amount"] > 0:
                eff_cat = "other-income"

        if search_re and search_re.search(row["text"]):
            search_tx.append((d, row["text"], row["amount"], eff_cat))

        if eff_cat in ("salary", "transfers", "other-income"):
            {"salary": salary, "transfers": transfers, "other-income": other_income}[eff_cat][p] += row["amount"]
            if det_cat == eff_cat:
                dm = f"{d.year}-{d.month:02d}"
                if det_period is None or dm.startswith(det_period):
                    detail_tx.append((d, p, row["text"], row["amount"]))
            continue

        totals[eff_cat][p] += -row["amount"]

        if eff_cat == "andet":
            andet_tx.append((d, p, row["text"], row["amount"]))

        if det_cat and eff_cat == det_cat:
            dm = f"{d.year}-{d.month:02d}"
            if det_period is None or dm.startswith(det_period):
                detail_tx.append((d, p, row["text"], row["amount"]))

    total_exp = sum(sum(ps.values()) for ps in totals.values())
    total_inc = sum(salary.values()) + sum(transfers.values()) + sum(other_income.values())
    net_change  = bal_end - bal_start
    net_tracked = total_inc - total_exp
    discrepancy = net_change - net_tracked
    if abs(discrepancy) > 0.01:
        print(f"ERROR: balance and categories do not reconcile  (discrepancy: {discrepancy:,.4f})", file=sys.stderr)

    if args.verbose:
        print(f"Parsed {n_parsed} rows, categorised {n_total}", file=sys.stderr)
        print(f"Balance:     start {bal_start:>12,.0f}  end {bal_end:>12,.0f}  net change  {net_change:>12,.0f}", file=sys.stderr)
        print(f"Categories:    exp {total_exp:>12,.0f}  inc {total_inc:>12,.0f}  net tracked {net_tracked:>12,.0f}", file=sys.stderr)
        print(f"Discrepancy: {discrepancy:>16,.4f}  OK", file=sys.stderr)

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

    elif args.avg:
        # Monthly averages: like -y but divided by months spanned in each year.
        months_per_year = {yr: max(ms) - min(ms) + 1
                           for yr, ms in dates_per_year.items()}
        cols = all_periods  # sorted year strings

        def _hdr(p: str) -> str:
            return f"{p}({months_per_year.get(int(p), 12)}mo)"

        col_w = max(10, max(len(_hdr(p)) for p in cols) + 2)
        hdr = f"{'':>{cat_w}}" + "".join(f"{_hdr(p):>{col_w}}" for p in cols)
        sep = "-" * len(hdr)
        print(hdr)
        print(sep)
        for cat in all_cats:
            row = f"{cat:>{cat_w}}"
            for p in cols:
                v = totals[cat].get(p, 0.0)
                n = months_per_year.get(int(p), 12)
                row += f"{v / n:{col_w},.0f}" if v else f"{'':>{col_w}}"
            print(row)

        print()
        total_exp_row = f"{'total-exp':>{cat_w}}"
        for p in cols:
            v = sum(totals[cat].get(p, 0.0) for cat in all_cats)
            n = months_per_year.get(int(p), 12)
            total_exp_row += f"{v / n:{col_w},.0f}" if v else f"{'':>{col_w}}"
        print(total_exp_row)

        print()
        for label, src in (("salary", salary), ("transfers", transfers), ("other-income", other_income)):
            summary_row = f"{label:>{cat_w}}"
            for p in cols:
                v = src.get(p, 0.0)
                n = months_per_year.get(int(p), 12)
                summary_row += f"{v / n:{col_w},.0f}" if v else f"{'':>{col_w}}"
            print(summary_row)

        print()
        total_income_row = f"{'total-income':>{cat_w}}"
        for p in cols:
            v = salary.get(p, 0.0) + transfers.get(p, 0.0) + other_income.get(p, 0.0)
            n = months_per_year.get(int(p), 12)
            total_income_row += f"{v / n:{col_w},.0f}" if v else f"{'':>{col_w}}"
        print(total_income_row)

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
