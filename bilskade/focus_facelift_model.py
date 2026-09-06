"""Facelift-aware price model for Ford Focus III 1.0 Titanium stationcars.

Sample: all Ford Focus stc., benzin, model year 2011-2018, with anhaengertraek
on bilbasen.dk, filtered to Titanium trim. Scraped 2026-09-06.
My car: 1.0 SCTi 125 Titanium stc, 1. reg 6/2012, 141,000 km  -> PRE-facelift.

Facelift split (Focus III "Mk3.5"): revealed Geneva Mar 2014, at Danish dealers
Nov 2014 (Ford DK press release 18/9 2014).  In the sample every car first
registered <= 9/2014 has the old front, every car >= 12/2014 the new front
(verified on listing photos for all 2014-2015 registrations).

Question: does a NEWER car of the SAME body (same facelift generation) fetch
more than an older one, once km is accounted for?  And how much is the
facelift itself worth?
"""
import csv, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
MY_KM = 141000.0
MY_AGE = 2026 + 8/12 - (2012 + 5.5/12)   # years since 1. reg, Sep 2026
NOW = 2026 + 8/12

rows = []
with open(os.path.join(HERE, "focus_facelift_listings.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        m, y = r["firstreg"].split("/")
        rows.append(dict(id=r["id"], variant=r["variant"], price=float(r["price"]),
                         pricetype=r["pricetype"], firstreg=r["firstreg"],
                         age=NOW - (int(y) + (int(m) - 0.5) / 12),
                         km=float(r["km"]), hk=int(r["hk"]), seller=r["seller"],
                         fl=int(r["facelift"])))

# ---------- tiny OLS ----------
def ols(X, y):
    """X: list of rows (with leading 1.0), y: list. Returns beta, se, r2, rmse."""
    n, k = len(X), len(X[0])
    # normal equations via Gaussian elimination
    A = [[sum(X[i][a]*X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    B = [sum(X[i][a]*y[i] for i in range(n)) for a in range(k)]
    # invert A
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(A)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        pv = M[c][c]; M[c] = [v / pv for v in M[c]]
        for r in range(k):
            if r != c:
                fct = M[r][c]; M[r] = [M[r][j] - fct * M[c][j] for j in range(2*k)]
    Ainv = [row[k:] for row in M]
    beta = [sum(Ainv[a][b]*B[b] for b in range(k)) for a in range(k)]
    yhat = [sum(X[i][a]*beta[a] for a in range(k)) for i in range(n)]
    ss_res = sum((y[i]-yhat[i])**2 for i in range(n))
    ybar = sum(y)/n; ss_tot = sum((v-ybar)**2 for v in y)
    dof = max(n - k, 1); s2 = ss_res / dof
    se = [math.sqrt(max(s2*Ainv[a][a], 0)) for a in range(k)]
    return beta, se, 1 - ss_res/ss_tot, math.sqrt(s2)

def show(label, names, beta, se, r2, rmse, n):
    print(f"\n{label}  (n={n}, R2={r2:.3f}, RMSE={rmse:,.0f} kr)")
    for nm, b, s in zip(names, beta, se):
        t = b/s if s else float('nan')
        print(f"   {nm:24s} {b:>10,.0f}   (se {s:,.0f}, t={t:+.1f})")

# ---------- sample ----------
f3 = [r for r in rows if r["variant"].startswith("1.0")]          # 1.0 EcoBoost only
retail = [r for r in f3 if r["pricetype"] == "Retail"]
pre = [r for r in retail if r["fl"] == 0]
post = [r for r in retail if r["fl"] == 1]
print(f"Titanium stc listings: {len(rows)} total, {len(f3)} with 1.0 EcoBoost, "
      f"{len(retail)} retail; pre-facelift {len(pre)}, facelift {len(post)}")

print("\n=== Group overview (1.0 Titanium, retail) ===")
for lbl, g in (("Pre-facelift (Focus III, 2011-9/2014)", pre), ("Facelift (Focus III.5, 12/2014-2018)", post)):
    kms = [r["km"] for r in g]; ps = [r["price"] for r in g]
    print(f"{lbl}: n={len(g)}, km {min(kms)/1e3:.0f}k-{max(kms)/1e3:.0f}k (mean {sum(kms)/len(g)/1e3:.0f}k), "
          f"price {min(ps):,.0f}-{max(ps):,.0f} (mean {sum(ps)/len(g):,.0f})")

# ---------- Model A: km + facelift dummy + 100hk dummy + private dummy ----------
names = ["const", "per 1.000 km", "facelift", "100 hk", "privatsalg"]
X = [[1, r["km"]/1e3, r["fl"], 1 if r["hk"] == 100 else 0, 1 if r["seller"] == "Privat" else 0] for r in retail]
y = [r["price"] for r in retail]
bA, seA, r2A, rmA = ols(X, y)
show("Model A: price ~ km + facelift + 100hk + privat", names, bA, seA, r2A, rmA, len(retail))
pre_pred = bA[0] + bA[1]*MY_KM/1e3
print(f"   => pre-facelift 125 hk dealer car at 141.000 km: {pre_pred:,.0f} kr")
print(f"   => facelift premium: {bA[2]:,.0f} kr; facelift car at 141.000 km: {pre_pred+bA[2]:,.0f} kr")

# ---------- Model B: add age; does age matter beyond facelift + km? ----------
names = ["const", "per 1.000 km", "facelift", "per year of age", "100 hk", "privatsalg"]
X = [[1, r["km"]/1e3, r["fl"], r["age"], 1 if r["hk"] == 100 else 0, 1 if r["seller"] == "Privat" else 0] for r in retail]
bB, seB, r2B, rmB = ols(X, y)
show("Model B: price ~ km + facelift + age + 100hk + privat", names, bB, seB, r2B, rmB, len(retail))

# ---------- Model C: WITHIN the facelift group only: km + age ----------
names = ["const", "per 1.000 km", "per year of age", "100 hk", "privatsalg"]
Xc = [[1, r["km"]/1e3, r["age"], 1 if r["hk"] == 100 else 0, 1 if r["seller"] == "Privat" else 0] for r in post]
yc = [r["price"] for r in post]
bC, seC, r2C, rmC = ols(Xc, yc)
show("Model C (facelift cars only): price ~ km + age + 100hk + privat", names, bC, seC, r2C, rmC, len(post))
names = ["const", "per 1.000 km", "100 hk", "privatsalg"]
Xd = [[1, r["km"]/1e3, 1 if r["hk"] == 100 else 0, 1 if r["seller"] == "Privat" else 0] for r in post]
bD, seD, r2D, rmD = ols(Xd, yc)
show("Model D (facelift cars only): price ~ km + 100hk + privat  [no age]", names, bD, seD, r2D, rmD, len(post))
print(f"   => age adds R2 {r2C - r2D:+.3f} on top of km within the same body.")

# ---------- Model E: pre-facelift group alone, km only ----------
Xe = [[1, r["km"]/1e3] for r in pre]; ye = [r["price"] for r in pre]
bE, seE, r2E, rmE = ols(Xe, ye)
show("Model E (pre-facelift cars only): price ~ km", ["const", "per 1.000 km"], bE, seE, r2E, rmE, len(pre))
print(f"   => extrapolated to 141.000 km: {bE[0] + bE[1]*MY_KM/1e3:,.0f} kr  (extrapolation! min km in group is {min(r['km'] for r in pre)/1e3:.0f}k)")

# ---------- Tryg's reference, km-corrected within the SAME body ----------
ref = next(r for r in rows if r["id"] == "6859693")
for lbl, slope in (("Model A slope", bA[1]), ("facelift-group slope", bD[1]), ("pre-facelift slope", bE[1])):
    corr = ref["price"] + (-slope) * (ref["km"] - MY_KM) / 1e3
    print(f"Tryg ref 6859693 ({ref['price']:,.0f} kr, {ref['km']/1e3:.0f}k km, pre-facelift) km-corrected to 141k "
          f"with {lbl} ({slope:+,.0f}/1.000 km): {corr:,.0f} kr")
print(f"Wear ratio Tryg ref / my car: {ref['km']/MY_KM:.2f}  (= {100*(ref['km']/MY_KM-1):.0f} % more km)")

# ---------- listing table sorted by group then km ----------
print("\n=== All 1.0 Titanium listings, grouped ===")
for lbl, g in (("PRE-FACELIFT (same body as my car)", [r for r in f3 if r["fl"] == 0]),
               ("FACELIFT (Focus III.5)", [r for r in f3 if r["fl"] == 1])):
    print(f"\n{lbl}")
    print(f"  {'id':8s} {'variant':30s} {'1.reg':>7s} {'km':>8s} {'pris':>8s}  sælger")
    for r in sorted(g, key=lambda r: r["km"]):
        tag = " (engros)" if r["pricetype"] == "Wholesale" else ""
        tag += "  <- Trygs reference" if r["id"] == "6859693" else ""
        print(f"  {r['id']:8s} {r['variant']:30s} {r['firstreg']:>7s} {r['km']/1e3:6.0f}k {r['price']:8,.0f}  {r['seller']}{tag}")

# ---------- Model F: log-price (proportional depreciation), all retail 1.0 ----------
print("\n=== Log-price models (percent effects; more appropriate for old, cheap cars) ===")
names = ["const", "per 1.000 km", "per year of age", "100 hk", "privatsalg"]
Xf = [[1, r["km"]/1e3, r["age"], 1 if r["hk"] == 100 else 0, 1 if r["seller"] == "Privat" else 0] for r in retail]
yf = [math.log(r["price"]) for r in retail]
bF, seF, r2F, rmF = ols(Xf, yf)
print(f"\nModel F: ln(price) ~ km + age + 100hk + privat  (n={len(retail)}, R2={r2F:.3f})")
for nm, b, s in zip(names, bF, seF):
    print(f"   {nm:24s} {100*b:+8.2f} %   (t={b/s:+.1f})")
predF = math.exp(bF[0] + bF[1]*MY_KM/1e3 + bF[2]*MY_AGE)
print(f"   => my car (141k km, {MY_AGE:.1f} yr, 125 hk, dealer): {predF:,.0f} kr")
print(f"   => 1 year of age is worth the same as {bF[2]/bF[1]*1e3/1e3:,.0f}k km")
# Tryg reference under model F
refF = math.exp(bF[0] + bF[1]*ref["km"]/1e3 + bF[2]*ref["age"])
print(f"   => Tryg ref 6859693 predicted {refF:,.0f} kr (listed {ref['price']:,.0f}); my car / ref ratio = {predF/refF:.3f} "
      f"-> ref price scaled: {ref['price']*predF/refF:,.0f} kr")
