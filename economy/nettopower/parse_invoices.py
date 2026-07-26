"""Parse NettoPower invoice text files (pdftotext -layout output) into a CSV.

Extracts per invoice: period (month), electricity kWh + DKK, gas m3 + DKK.
Old format (2022-2023): "NettoPower-Faktura" emails; new format (2025-):
"Forbrugsopgørelse". Text files are Latin-1 encoded.
"""
import csv
import re
import sys
from pathlib import Path

MONTHS = {
    'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6,
    'juli': 7, 'august': 8, 'september': 9, 'oktober': 10, 'november': 11,
    'december': 12,
}

HEADINGS = ['El-forbrug', 'Gas-forbrug', 'Korrektioner', 'Indbetalinger',
            'Total for alle', 'Beskeder', 'Min NettoPower konto',
            'Din konto hos nettopower']

AMOUNT_RE = re.compile(r'(-?\d{1,3}(?:\.\d{3})*,\d{2})\s*kr')


def parse_amount(s):
    return float(s.replace('.', '').replace(',', '.'))


def parse_qty(s):
    return int(s.replace('.', ''))


def section(text, start_kw):
    i = text.find(start_kw)
    if i < 0:
        return ''
    rest = text[i + len(start_kw):]
    ends = [rest.find(kw) for kw in HEADINGS if kw != start_kw]
    ends = [e for e in ends if e > 0]
    return rest[:min(ends)] if ends else rest


def parse_file(path):
    text = path.read_text(encoding='latin-1')
    # pdftotext -layout can detach the value from the "Periode" label, so
    # take the first month-name + year token in the header instead.
    header = text[:max(text.find('Forbrugsoversigt'), 0) or 2000]
    m = re.search(r'\b(' + '|'.join(MONTHS) + r')\s+(\d{4})\b', header,
                  re.IGNORECASE)
    if not m:
        sys.exit(f'{path.name}: no Periode found')
    month = MONTHS[m.group(1).lower()]
    period = f'{m.group(2)}-{month:02d}'

    el = section(text, 'El-forbrug')
    gas = section(text, 'Gas-forbrug')

    el_kwh = el_dkk = gas_m3 = gas_dkk = None
    m = re.search(r'(\d{1,3}(?:\.\d{3})*)\s*kWh', el)
    if m:
        el_kwh = parse_qty(m.group(1))
    amounts = [parse_amount(a) for a in AMOUNT_RE.findall(el)]
    if amounts:
        el_dkk = max(amounts)  # total incl. VAT is the largest amount in the section
    m = re.search(r'(\d{1,3}(?:\.\d{3})*)\s*m\xb3', gas)
    if m:
        gas_m3 = parse_qty(m.group(1))
    amounts = [parse_amount(a) for a in AMOUNT_RE.findall(gas)]
    if amounts:
        gas_dkk = max(amounts)

    # Quarterly gas corrections (actual metered vs. aconto estimate)
    corr = section(text, 'Korrektioner')
    m = re.search(r'(-?\d{1,3}(?:\.\d{3})*)\s*m\xb3\s', corr)
    corr_m3 = None
    if corr:
        m = re.search(r'\s(-\d+|\d+)\s*m\xb3', corr)

    return {
        'period': period, 'el_kwh': el_kwh, 'el_dkk': el_dkk,
        'gas_m3': gas_m3, 'gas_dkk': gas_dkk, 'file': path.name,
    }


def main():
    txtdir = Path(__file__).parent / 'txt'
    rows = sorted((parse_file(p) for p in txtdir.glob('*.txt')),
                  key=lambda r: r['period'])
    out = Path(__file__).parent / 'consumption.csv'
    with out.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    fmt = '{:9} {:>7} {:>10} {:>7} {:>10}  {}'
    print(fmt.format('period', 'el_kWh', 'el_DKK', 'gas_m3', 'gas_DKK', 'file'))
    for r in rows:
        print(fmt.format(r['period'], r['el_kwh'] or '-', r['el_dkk'] or '-',
                         r['gas_m3'] or '-', r['gas_dkk'] or '-', r['file']))


if __name__ == '__main__':
    main()
