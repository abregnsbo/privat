#!/usr/bin/env python3
"""
Jyske Fast 1% — annuity mortgage model.

Reproduces the bank's payment schedule and is designed for scenario analysis
(e.g. refinancing, rate changes, extra payments).

Usage:
  python mortgage.py           # yearly schedule from Q2 2026 (matches bank tab)
  python mortgage.py -q        # quarterly schedule from Q2 2026
  python mortgage.py --full    # full schedule from loan origination (2019)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date


@dataclass
class Mortgage:
    """
    Fixed-rate annuity mortgage with quarterly payments.

    `pmt` (fixed annuity component = interest + instalment) is derived from
    `principal` and `term_quarters`.  The admin margin is calculated separately
    on the outstanding balance each period, so the total payment decreases over
    time as the debt shrinks.

    For mid-loan scenarios (e.g. refinancing from the current balance):
      - Set `principal` to the current outstanding balance.
      - Set `term_quarters` to the desired new term.
      - Set `first_payment` to the first payment date.

    For reproducing the existing loan from a mid-point while keeping the
    original fixed PMT:
      - Keep `principal` and `term_quarters` at their original values.
      - Set `start_balance` to the actual balance at `first_payment`.
      - Set `start_quarter` to the payment number corresponding to `first_payment`.
    """

    principal: float          # Original loan amount — drives pmt calculation
    interest_rate: float      # Annual interest rate (e.g. 0.01 for 1.00%)
    admin_rate: float         # Annual admin/bidrag rate (e.g. 0.00325 for 0.3250%)
    term_quarters: int        # Total quarterly payments over the full loan life
    first_payment: date       # Date of the first payment in this schedule
    tax_rate: float           # Marginal tax rate on interest + admin (e.g. 0.256)
    start_balance: float | None = None   # Balance just before first_payment (default: principal)
    start_quarter: int = 1               # Sequence number of first_payment (1-based)
    pmt_override: float | None = None    # Override the formula-computed annuity payment

    @property
    def r(self) -> float:
        """Quarterly interest rate."""
        return self.interest_rate / 4

    @property
    def a(self) -> float:
        """Quarterly admin rate."""
        return self.admin_rate / 4

    @property
    def pmt(self) -> float:
        """Fixed quarterly annuity payment (interest + instalment, excl. admin)."""
        if self.pmt_override is not None:
            return self.pmt_override
        r, n = self.r, self.term_quarters
        return self.principal * r / (1 - (1 + r) ** -n)

    def balance_after(self, k: int) -> float:
        """Outstanding balance after k payments from loan origination.

        Uses the closed-form amortization formula; does not accumulate rounding.
        """
        r, pmt, pv = self.r, self.pmt, self.principal
        factor = (1 + r) ** k
        return pv * factor - pmt * (factor - 1) / r

    def quarterly_schedule(self) -> list[dict]:
        """Quarterly amortization rows from first_payment to end of loan."""
        r, a, pmt = self.r, self.a, self.pmt
        balance = self.start_balance if self.start_balance is not None else self.principal
        pdate = self.first_payment
        n_remaining = self.term_quarters - self.start_quarter + 1
        rows = []

        for i in range(n_remaining):
            is_last = (i == n_remaining - 1)
            interest = balance * r
            admin = balance * a
            # Last quarter: pay off the remaining balance exactly to avoid float drift
            instalment = balance if is_last else (pmt - interest)
            before_tax = interest + instalment + admin
            after_tax = before_tax - (interest + admin) * self.tax_rate
            balance = max(0.0, balance - instalment)

            rows.append({
                'quarter': self.start_quarter + i,
                'date': pdate,
                'year': pdate.year,
                'interest': interest,
                'admin': admin,
                'instalment': instalment,
                'before_tax': before_tax,
                'after_tax': after_tax,
                'balance': balance,
            })
            pdate = _next_quarter(pdate)

        return rows

    def yearly_summary(self) -> list[dict]:
        """Aggregate quarterly schedule into yearly totals."""
        years: dict[int, dict] = {}
        for q in self.quarterly_schedule():
            y = q['year']
            if y not in years:
                years[y] = {
                    'year': y, 'before_tax': 0.0, 'after_tax': 0.0,
                    'instalment': 0.0, 'interest': 0.0, 'admin': 0.0,
                    'int_admin': 0.0, 'balance': 0.0, 'quarters': 0,
                }
            d = years[y]
            d['before_tax'] += q['before_tax']
            d['after_tax'] += q['after_tax']
            d['instalment'] += q['instalment']
            d['interest'] += q['interest']
            d['admin'] += q['admin']
            d['int_admin'] += q['interest'] + q['admin']
            d['balance'] = q['balance']  # end-of-year balance
            d['quarters'] += 1
        for d in years.values():
            d['months'] = d['quarters'] * 3
        return list(years.values())

    def pv_of_payments(self, discount_rate: float) -> float:
        """Present value of all future after-tax payments at the given annual discount rate."""
        r = discount_rate / 4   # quarterly discount rate
        return sum(
            q['after_tax'] / (1 + r) ** i
            for i, q in enumerate(self.quarterly_schedule(), start=1)
        )

    def print_yearly(self, discount_rates: list[float] = (0.04, 0.03, 0.02)) -> None:
        pvs = [(r, self.pv_of_payments(r)) for r in discount_rates]
        _print_yearly(self.yearly_summary(), pvs)

    def print_quarterly(self) -> None:
        _print_quarterly(self.quarterly_schedule())


def _next_quarter(d: date) -> date:
    """Return the next quarter-end date (Mar 31, Jun 30, Sep 30, Dec 31)."""
    ends = [(3, 31), (6, 30), (9, 30), (12, 31)]
    for i, (m, day) in enumerate(ends):
        if (d.month, d.day) == (m, day):
            j = (i + 1) % 4
            ny = d.year + (1 if j == 0 else 0)
            return date(ny, ends[j][0], ends[j][1])
    raise ValueError(f"Not a quarter-end date: {d}")


def _print_yearly(rows: list[dict], pvs: list[tuple[float, float]]) -> None:
    year_w = 6
    col_w = 10
    header = f"{'Year':>{year_w}}  {'Current':>{col_w}}"
    sep = '-' * len(header)
    print(header)
    print(sep)
    for rate, pv in pvs:
        label = f"PV({rate:.0%})"
        print(f"{label:>{year_w}}  {pv:>{col_w},.0f}")
    print(sep)
    for r in rows:
        monthly = r['after_tax'] / r['months']
        print(f"{r['year']:>{year_w}}  {monthly:>{col_w},.0f}")


def _print_quarterly(rows: list[dict]) -> None:
    cols = ['No', 'Date', 'Before tax', 'After tax', 'Instalment', 'Interest', 'Admin', 'Balance']
    widths = [3, 10, 10, 10, 10, 9, 9, 12]
    header = '  '.join(c.rjust(w) for c, w in zip(cols, widths))
    sep = '-' * len(header)
    print(header)
    print(sep)
    for r in rows:
        vals = [
            str(r['quarter']),
            r['date'].isoformat(),
            f"{r['before_tax']:,.2f}",
            f"{r['after_tax']:,.2f}",
            f"{r['instalment']:,.2f}",
            f"{r['interest']:,.2f}",
            f"{r['admin']:,.2f}",
            f"{r['balance']:,.2f}",
        ]
        print('  '.join(v.rjust(w) for v, w in zip(vals, widths)))


# ─── Loan definition ──────────────────────────────────────────────────────────
#
# Jyske Fast Rente 1%, loan no. 41064296
# Principal: 3,026,000 DKK | Interest: 1.00% p.a. | Admin: 0.3250% p.a.
# Disbursed: ~2019-07-01 | First payment: 2019-09-30 | Term: 20 years (80 qtrs)
# Final payment: 2039-06-30
#
# Bank snapshot (taken before Q2 2026 payment = 2026-06-30, payment no. 28):
#   Q2 2026 interest:   5,160.72 DKK  → balance before Q2 = 5160.72 / 0.0025
#   Q2 2026 instalment: 36,620.17 DKK → PMT = 5160.72 + 36620.17 = 41,780.89
#   Outstanding after Q2 2026: 2,027,669.42 DKK (shown in bank UI as at 01.07.2026)
#
# Why balance_after(27) from the formula doesn't match:
#   The bank rounds each payment to the nearest øre from loan origination (2019),
#   so rounding drift makes the formula-computed balance deviate by ~7,200 DKK
#   after 27 quarterly payments.  We anchor to the observed Q2 2026 data instead.
#
# Note on admin margin (bidragssats) in 2038-2039:
#   The bank's projected schedule shows higher admin than 0.3250% implies for the
#   final two years, likely due to a tiered bidragssats applied at low LTV ratios.
#   Interest and instalment (core amortization) match throughout.

_Q2_2026_INTEREST   = 5_160.72
_Q2_2026_INSTALMENT = 36_620.17
_Q2_2026_PMT        = _Q2_2026_INTEREST + _Q2_2026_INSTALMENT      # 41,780.89
_BAL_BEFORE_Q2_2026 = _Q2_2026_INSTALMENT + 2_027_669.42           # 2,064,289.59

_ORIGIN = Mortgage(
    principal=3_026_000,
    interest_rate=0.01,
    admin_rate=0.00325,
    term_quarters=80,
    first_payment=date(2019, 9, 30),
    tax_rate=0.256,
)

# Schedule from Q2 2026 onwards — matches the bank's "Payment schedule" tab.
# 2026 shows 3 quarters (Q2/Q3/Q4), 2039 shows 2 quarters (Q1/Q2).
CURRENT_LOAN = Mortgage(
    principal=3_026_000,
    interest_rate=0.01,
    admin_rate=0.00325,
    term_quarters=80,
    first_payment=date(2026, 6, 30),
    tax_rate=0.256,
    start_balance=_BAL_BEFORE_Q2_2026,
    start_quarter=28,
    pmt_override=_Q2_2026_PMT,
)


def main() -> None:
    ap = argparse.ArgumentParser(description='Jyske Fast 1% mortgage payment schedule')
    ap.add_argument('-q', '--quarterly', action='store_true',
                    help='show quarterly detail (default: yearly)')
    ap.add_argument('--full', action='store_true',
                    help='show full schedule from origination in 2019')
    ap.add_argument('--discount', type=float, nargs='+', default=[0.04, 0.03, 0.02],
                    metavar='RATE', help='discount rate(s) for PV rows (default: 0.04 0.03 0.02)')
    args = ap.parse_args()

    loan = _ORIGIN if args.full else CURRENT_LOAN
    period = '2019-2039 (full)' if args.full else '2026-2039 (from next payment)'

    print(f'\n=== Jyske Fast 1%  Monthly after-tax cost  {period} ===')
    print(f'    Quarterly PMT:  {loan.pmt:>12,.2f} DKK')
    print()

    if args.quarterly:
        loan.print_quarterly()
    else:
        loan.print_yearly(discount_rates=args.discount)


if __name__ == '__main__':
    main()
