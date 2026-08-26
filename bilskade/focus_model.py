"""Estimate market value of a Ford Focus III 1.0 EcoBoost stationcar,
1st reg 6/2012, 141,000 km, petrol, with anhaengertraek — from bilbasen.dk
listings of Ford Focus stationcars 2010-2016 with towbar (scraped 2026-08-26).
"""
import csv, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
NOW = 2026 + 8 / 12  # Aug 2026

rows = []
with open(os.path.join(HERE, "focus_listings.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        m, y = r["firstreg"].split("/")
        regdec = int(y) + (int(m) - 0.5) / 12
        rows.append(dict(
            id=r["id"], variant=r["variant"], price=float(r["price"]),
            pricetype=r["pricetype"], regdec=regdec, age=NOW - regdec,
            km=float(r["km"]), fuel=r["fuel"], seller=r["seller"]))

petrol = [r for r in rows if r["fuel"] == "Benzin" and r["pricetype"] != "Wholesale"]
print(f"Total listings: {len(rows)}  petrol retail (engros excluded): {len(petrol)}")

# Wholesale (Engros/CVR) prices exclude registration/prep — keep flag
for r in petrol:
    r["wholesale"] = 1.0 if r["pricetype"] == "Wholesale" else 0.0


def ols(X, y):
    """Plain OLS via normal equations, X list of feature lists (incl. const)."""
    n, k = len(X), len(X[0])
    XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    Xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
    # gaussian elimination
    M = [row[:] + [Xty[a]] for a, row in enumerate(XtX)]
    for c in range(k):
        p = max(range(c, k), key=lambda r_: abs(M[r_][c]))
        M[c], M[p] = M[p], M[c]
        for r_ in range(k):
            if r_ != c and M[c][c]:
                f = M[r_][c] / M[c][c]
                for cc in range(c, k + 1):
                    M[r_][cc] -= f * M[c][cc]
    beta = [M[i][k] / M[i][i] for i in range(k)]
    yhat = [sum(X[i][a] * beta[a] for a in range(k)) for i in range(n)]
    ybar = sum(y) / n
    ss_res = sum((y[i] - yhat[i]) ** 2 for i in range(n))
    ss_tot = sum((yi - ybar) ** 2 for yi in y)
    r2 = 1 - ss_res / ss_tot
    rmse = math.sqrt(ss_res / (n - k))
    return beta, r2, rmse, yhat


MY_AGE = NOW - (2012 + 5.5 / 12)   # 1st reg June 2012
MY_KM = 141.0                      # in 1000 km

# ---------- Model A: log-linear  ln(P) = b0 + b1*age + b2*km
X = [[1, r["age"], r["km"] / 1000] for r in petrol]
y = [math.log(r["price"]) for r in petrol]
bA, r2A, rmseA, _ = ols(X, y)
predA = math.exp(bA[0] + bA[1] * MY_AGE + bA[2] * MY_KM)  # retail
smearing = sum(math.exp(y[i] - sum(X[i][a] * bA[a] for a in range(3))) for i in range(len(y))) / len(y)
predA_sm = predA * smearing
print("\nModel A: ln(price) ~ age + km   (all retail petrol)")
print(f"  b: const={bA[0]:.3f} age={bA[1]*100:+.1f}%/yr km={bA[2]*100:+.2f}%/1000km "
      f"  R2={r2A:.3f} RMSE(log)={rmseA:.3f}")
print(f"  Prediction (retail, smearing-corrected): {predA_sm:,.0f} kr")
lo, hi = predA_sm * math.exp(-rmseA), predA_sm * math.exp(rmseA)
print(f"  +/-1 sigma band: {lo:,.0f} - {hi:,.0f} kr")

# ---------- Model B: linear  P = b0 + b1*age + b2*km
yl = [r["price"] for r in petrol]
bB, r2B, rmseB, _ = ols(X, yl)
predB = bB[0] + bB[1] * MY_AGE + bB[2] * MY_KM
print("\nModel B: price ~ age + km   (all retail petrol)")
print(f"  b: const={bB[0]:,.0f} age={bB[1]:,.0f} kr/yr km={bB[2]:,.0f} kr/1000km "
      f"  R2={r2B:.3f} RMSE={rmseB:,.0f} kr")
print(f"  Prediction (retail): {predB:,.0f} kr   +/-1 sigma: {predB-rmseB:,.0f} - {predB+rmseB:,.0f}")

# ---------- Nearest comparables: petrol, reg 2012-2014 or km 120-200k
print("\nClosest comparables (petrol; reg <= 2014 or km within 110-200k):")
sel = sorted(petrol, key=lambda r: abs(r["age"] - MY_AGE) + abs(r["km"] / 1000 - MY_KM) / 50)
for r in sel[:10]:
    print(f"  {r['id']}  {r['variant']:34s} {r['regdec']:.1f}  {r['km']/1000:5.0f}k km  "
          f"{r['price']:8,.0f} kr {'(engros)' if r['wholesale'] else ''}")

# ---------- Model C: only 1.0 EcoBoost (SCTi) petrol, retail prices
eco = [r for r in petrol if r["variant"].startswith("1.0") and not r["wholesale"]]
print(f"\n1.0 EcoBoost retail-only sample: {len(eco)}")
Xc = [[1, r["age"], r["km"] / 1000] for r in eco]
yc = [math.log(r["price"]) for r in eco]
bC, r2C, rmseC, _ = ols(Xc, yc)
predC = math.exp(bC[0] + bC[1] * MY_AGE + bC[2] * MY_KM)
smearC = sum(math.exp(yc[i] - sum(Xc[i][a] * bC[a] for a in range(3))) for i in range(len(yc))) / len(yc)
predC_sm = predC * smearC
print("Model C: ln(price) ~ age + km   (1.0 EcoBoost, retail)")
print(f"  b: const={bC[0]:.3f} age={bC[1]*100:+.1f}%/yr km={bC[2]*100:+.2f}%/1000km  R2={r2C:.3f} RMSE(log)={rmseC:.3f}")
print(f"  Prediction: {predC_sm:,.0f} kr  band {predC_sm*math.exp(-rmseC):,.0f} - {predC_sm*math.exp(rmseC):,.0f}")

Xd = [[1, r["age"], r["km"] / 1000] for r in eco]
yd = [r["price"] for r in eco]
bD, r2D, rmseD, _ = ols(Xd, yd)
predD = bD[0] + bD[1] * MY_AGE + bD[2] * MY_KM
print("Model D: price ~ age + km   (1.0 EcoBoost, retail)")
print(f"  b: const={bD[0]:,.0f} age={bD[1]:,.0f} kr/yr km={bD[2]:,.0f} kr/1000km  R2={r2D:.3f} RMSE={rmseD:,.0f}")
print(f"  Prediction: {predD:,.0f} kr  band {predD-rmseD:,.0f} - {predD+rmseD:,.0f}")

ages = sorted(r["age"] for r in eco)
kms = sorted(r["km"]/1000 for r in eco)
print(f"  age range in sample: {ages[0]:.1f} - {ages[-1]:.1f} yr (my car: {MY_AGE:.1f})")
print(f"  km range in sample: {kms[0]:.0f}k - {kms[-1]:.0f}k (my car: {MY_KM:.0f}k)")

# ---------- Model E: age + km + 125hp dummy + Titanium dummy (final model)
# My car: 1.0 EcoBoost 125 hk Titanium (6-speed manual; the 100 hk variant has 5 speeds)
for r in eco:
    r["hp125"] = 1.0 if " 125 " in r["variant"] else 0.0
    r["tit"] = 1.0 if "Titanium" in r["variant"] else 0.0
Xe = [[1, r["age"], r["km"] / 1000, r["hp125"], r["tit"]] for r in eco]
ye = [r["price"] for r in eco]
bE, r2E, rmseE, _ = ols(Xe, ye)
predE = bE[0] + bE[1] * MY_AGE + bE[2] * MY_KM + bE[3] + bE[4]
print(f"\nModel E: price ~ age + km + hp125 + titanium   (n={len(eco)})")
print(f"  b: const={bE[0]:,.0f} age={bE[1]:,.0f} kr/yr km={bE[2]:,.0f} kr/1000km "
      f"hp125={bE[3]:+,.0f} titanium={bE[4]:+,.0f}  R2={r2E:.3f} RMSE={rmseE:,.0f}")
print(f"  Prediction (125 hk Titanium): {predE:,.0f} kr  band {predE-rmseE:,.0f} - {predE+rmseE:,.0f}")
