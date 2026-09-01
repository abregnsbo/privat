"""Mileage-only price model for Ford Focus 1.0 Titanium stationcars.

Sample: all Ford Focus stc. 1.0 (SCTi/EcoBoost) Titanium listings on
bilbasen.dk, first reg. 2011+, petrol, with anhaengertraek (all mount types).
Scraped 2026-09-01. My car: 1.0 SCTi 125 Titanium stc, 6/2012, 141,000 km.

Deliberately models price ~ km ONLY (no age term), per claim argument:
Tryg's 45,000 kr valuation rests on comparables with 40-60,000 km more
than my car; mileage is the dimension in dispute.
"""
import csv, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
MY_KM = 141000.0

rows = []
with open(os.path.join(HERE, "focus_titanium_listings.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append(dict(id=r["id"], variant=r["variant"], price=float(r["price"]),
                         pricetype=r["pricetype"], firstreg=r["firstreg"],
                         km=float(r["km"]), seller=r["seller"]))

# Focus III only ("SCTi" badging; "EcoBoost"-badged listings are Focus IV,
# 2018+, a newer generation than my car — excluded per claim scope).
f3_all = [r for r in rows if "SCTi" in r["variant"]]
retail = [r for r in f3_all if r["pricetype"] == "Retail"]
print(f"Listings: {len(rows)} total, {len(f3_all)} Focus III (SCTi), "
      f"{len(retail)} retail (engros/CVR excluded)")


def fit_km(sample, label):
    n = len(sample)
    xs = [r["km"] / 1000 for r in sample]          # 1000 km
    ys = [r["price"] for r in sample]
    xbar, ybar = sum(xs) / n, sum(ys) / n
    sxx = sum((x - xbar) ** 2 for x in xs)
    sxy = sum((xs[i] - xbar) * (ys[i] - ybar) for i in range(n))
    b1 = sxy / sxx
    b0 = ybar - b1 * xbar
    yhat = [b0 + b1 * x for x in xs]
    ss_res = sum((ys[i] - yhat[i]) ** 2 for i in range(n))
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot
    rmse = math.sqrt(ss_res / (n - 2))
    pred = b0 + b1 * MY_KM / 1000
    print(f"\n{label}  (n={n})")
    print(f"  price = {b0:,.0f} {b1:+,.0f} kr per 1.000 km   R2={r2:.3f}  RMSE={rmse:,.0f} kr")
    print(f"  km range {min(xs):.0f}k-{max(xs):.0f}k, mean {xbar:.0f}k; price mean {ybar:,.0f} kr")
    print(f"  Prediction at 141.000 km: {pred:,.0f} kr   +/-1 sigma: {pred-rmse:,.0f} - {pred+rmse:,.0f}")
    return pred


fit_km(retail, "Model: price ~ km, Focus III 1.0 SCTi Titanium stc")

# Cheapest Focus III listings with km <= 141,000 (all, then dealer-retail only)
print("\nFocus III listings with km <= 141.000, sorted by price:")
le = sorted((r for r in f3_all if r["km"] <= MY_KM), key=lambda r: r["price"])
# Wet-belt (tandrem) rule for Focus III 1.0 EcoBoost: 10 years or 240,000 km,
# whichever first — for this sample age is always the binding limit.
NOW = 2026 + 8 / 12  # Sep 2026
for r in le[:12]:
    m, y = r["firstreg"].split("/")
    due_in = int(y) + (int(m) - 0.5) / 12 + 10 - NOW  # years until 10-yr belt deadline
    belt = "tandrem OVERSKREDET" if due_in < 0 else f"tandrem om {due_in*12:.0f} mdr"
    print(f"  {r['id']}  {r['variant']:32s} {r['firstreg']:>7s} {r['km']/1000:5.0f}k km "
          f"{r['price']:8,.0f} kr  {r['seller']:10s} {belt}"
          f"{' (engros)' if r['pricetype']=='Wholesale' else ''}")
cheap_dealer = next(r for r in le if r["seller"] == "Forhandler" and r["pricetype"] == "Retail")
print(f"\nCheapest overall <=141k km: {le[0]['id']} at {le[0]['price']:,.0f} kr ({le[0]['seller']})")
print(f"Cheapest dealer-retail <=141k km: {cheap_dealer['id']} at {cheap_dealer['price']:,.0f} kr")
