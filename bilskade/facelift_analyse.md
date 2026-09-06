# Focus III: facelift-generationer, ny bilbasen-søgning og kostmodel (6/9 2026)

Baggrund: Taksator (mail 2/9 2026) fastholder 45.000 kr og afviser sammenligning med
nyere årgange. Hypotese, der testes her: en nyere Focus III er kun mere værd, hvis den
er face-liftet — inden for samme karrosseri afgør km-tallet, ikke årgangen.

Filer: `focus_facelift_listings.csv` (30 annoncer, tagget pre/post facelift),
`focus_facelift_model.py` (modeller, kør med `python focus_facelift_model.py`).

## 1. Focus III-generationer (Titanium, stationcar)

| Generation | Produktion | 1. reg. i DK | Kendetegn |
|---|---|---|---|
| **Focus III (Mk3, "pre-facelift")** | 2011 – efterår 2014 | 3/2011 – ca. 10/2014 | Store "kattelygter", lille grill med Ford-oval i motorhjelmen, knapfyldt midterkonsol (Sony/SYNC 1), 1,0 EcoBoost 100/125 hk fra 2012. **Min bil (6/2012) er denne.** Sælges i DK typisk med "ECO"-suffix (1,0 SCTi 125 Titanium stc. ECO). |
| **Focus III.5 (Mk3.5, facelift)** | efterår 2014 – midt 2018 | ca. 11/2014 – 8/2018 | Vist Genève marts 2014; Ford DK pressemeddelelse 18/9 2014: "hos forhandlerne i november 2014". Ny smal trapez-grill (Aston/Mondeo-look), smallere forlygter, ny bagklap, nyt instrumentbord med få knapper og 8" touchskærm (SYNC 2, fra ca. 2016/17 SYNC 3), nyt 3-eget rat, justeret styretøj/undervogn, bedre lyddæmpning, flere assistentsystemer (Active City Stop 50 km/t, Cross Traffic Alert). Motorer 1,0 EcoBoost 100/125 uændret. |
| **Focus IV** | 2018 – | fra ca. 9/2018 | Ny generation ("EcoBoost"-badge på bilbasen i stedet for "SCTi"). Ikke Focus III — udeladt. |

Sen-facelift-varianter set i annoncerne: "Titanium Fun" (2017-18 specialudgave), "Titanium+" (2018).

**Skæringsdato verificeret på fotos:** alle biler med 1. reg. ≤ 9/2014 (6780078, 6985175)
har det gamle front; alle med 1. reg. ≥ 12/2014 (6971169, 6975560, 6987110, 6979886,
6864715) har facelift-fronten. Skæringen ligger altså mellem 10/2014 og 11/2014, som
pressemeddelelsen siger.

Kilder: Ford DK pressemeddelelse "Stærkt opdateret Ford Focus" (18/9 2014,
nyheder.ford.dk/pressreleases/staerkt-opdateret-ford-focus-1054328); Auto Express
"Ford Focus (2011-2018) review"; Wikipedia "Ford Focus (third generation)".

## 2. Ny bilbasen-søgning 6/9 2026

Søgning: Ford Focus, stationcar, benzin, modelår 2011-2018, med anhængertræk (alle
typer), inkl. engros/CVR → 52 annoncer, heraf **30 Titanium**, heraf **26 med 1,0
EcoBoost** (4 er 1,5/1,6 og udeladt).

Ændringer siden 1/9: solgt/fjernet 6883497, 6912059, 6927002, 6938187, 6542293, 6975476;
nye 6979886 (100 hk), 6986741 (**57.500 kr, 11/2016, 136.000 km, privat** — nu den
billigste med ≤ 141.000 km), 6987110.

### Pre-facelift (samme karrosseri som min bil) — 6 stk.

| id | variant | 1. reg | km | pris | sælger |
|---|---|---|---|---|---|
| 6780078 | 1.0 SCTi 125 Titanium stc ECO | 9/2014 | 172.000 | 54.900 | forhandler |
| 6859693 | 1.0 SCTi 125 Titanium stc ECO | 7/2013 | 179.000 | 44.700 | forhandler ← Trygs reference |
| 6985175 | 1.0 SCTi 125 Titanium stc ECO | 6/2014 | 199.000 | 39.900 | forhandler |
| 6919484 | 1.0 SCTi 125 Titanium stc ECO | 11/2013 | 242.000 | 39.900 | forhandler |
| 6980626 | 1.0 SCTi 125 Titanium stc ECO | 11/2013 | 254.000 | 26.995 | forhandler (engros) |
| 6981634 | 1.0 SCTi 125 Titanium stc ECO | 4/2013 | 298.000 | 29.900 | forhandler |

Ingen pre-facelift-bil på markedet har under 172.000 km. Alle er 2013-14; ingen fra 2011-12.

### Facelift (Focus III.5) — 20 stk. (1,0 EcoBoost)

| id | variant | 1. reg | km | pris | sælger |
|---|---|---|---|---|---|
| 6864715 | 125 Titanium | 9/2015 | 109.000 | 71.900 | forhandler |
| 6952123 | 125 Titanium | 6/2017 | 109.500 | 72.000 | forhandler |
| 6938839 | 125 Titanium | 4/2018 | 115.000 | 89.900 | forhandler |
| 6982544 | 125 Titanium Fun | 7/2018 | 115.000 | 72.400 | privat |
| 6967276 | 125 Titanium Fun | 4/2017 | 117.000 | 75.900 | forhandler |
| 6986741 | 125 Titanium | 11/2016 | 136.000 | 57.500 | privat |
| 6977537 | 125 Titanium | 6/2017 | 141.000 | 74.900 | forhandler |
| 6984909 | 125 Titanium | 12/2016 | 141.000 | 59.000 | privat |
| 6955205 | 125 Titanium | 11/2017 | 144.000 | 69.900 | forhandler |
| 6968845 | 125 Titanium | 7/2017 | 147.000 | 69.900 | forhandler |
| 6982864 | 125 Titanium | 4/2018 | 164.000 | 84.900 | privat |
| 6913154 | 125 Titanium | 7/2018 | 169.000 | 74.900 | forhandler |
| 6960082 | 125 Titanium | 3/2017 | 176.000 | 64.800 | forhandler |
| 6655644 | 125 Titanium | 8/2018 | 177.000 | 89.900 | forhandler |
| 6975560 | 100 Titanium | 12/2014 | 190.000 | 52.400 | forhandler |
| 6965920 | 125 Titanium | 2/2018 | 194.000 | 64.800 | forhandler |
| 6953404 | 100 Titanium | 3/2016 | 209.000 | 39.900 | forhandler |
| 6987110 | 125 Titanium | 1/2015 | 209.000 | 39.990 | forhandler |
| 6979886 | 100 Titanium | 5/2015 | 210.000 | 37.990 | forhandler |
| 6971169 | 125 Titanium | 12/2014 | 226.000 | 49.900 | forhandler |

## 3. Kostmodel: hvad koster facelift-modellen ekstra?

25 retail-annoncer (1,0 Titanium; engros udeladt). OLS, pris i kr.

| Model | km-hældning | facelift | alder | R² | min bil (141k, pre-facelift, 14,2 år) |
|---|---|---|---|---|---|
| A: km + facelift (+100 hk, privat) | −184 kr/1.000 km | **+16.700 kr** (t=2,5) | — | 0,70 | **56.000 kr** |
| B: km + facelift + alder | −120 | −3.000 (t=−0,5, insignifikant) | **−7.250 kr/år** (t=−4,4) | 0,85 | ca. 39.500 kr (ekstrapoleret) |
| C: kun facelift-biler, km + alder | −131 | — | **−7.360 kr/år** (t=−4,0) | 0,79 | — |
| D: kun facelift-biler, kun km | −202 | — | — | 0,55 | — |
| E: kun pre-facelift-biler, kun km (n=5) | −153 | — | — | 0,78 | 53.600 kr (ekstrapoleret fra ≥172k km) |
| F: ln(pris) ~ km + alder | −0,26 %/1.000 km | — | **−10,9 %/år** (t=−5,8) | 0,88 | 42.300 kr |

**Facelift-tillægget isoleret (model A) er ca. 16.700 kr** ved samme km-tal. Det er
den "rå" forskel mellem grupperne, når man kun korrigerer for km.

### Det ærlige resultat: hypotesen holder ikke i data

- Når alder tages med (model B), forsvinder facelift-effekten helt, og alder alene
  forklarer forskellen. Facelift og alder er ikke til at adskille i dette marked.
- **Inden for facelift-gruppen** (samme karrosseri, 2014-2018, model C vs. D) løfter alder
  R² fra 0,55 til 0,79 og er stærkt signifikant: en 2018-bil med 170-190k km koster
  65-90k, en 2015-bil med 209k km koster 40k. Årgang tæller altså, også uden facelift.
- Model F giver, at **1 års alder svarer til ca. 42.000 km**. Det er præcis
  taksators påstand ("1 år nyere udligner 40.000 km") — markedet støtter ham på det punkt.
- Alders-modellerne (B, F) forudsiger min bil til **39-42.000 kr**, dvs. *under* 45.000.
  Argumentet "nyere er kun mere værd ved facelift" bør derfor **ikke** sendes til Tryg:
  det inviterer til en aldersmodel, som ligger under tilbuddet.

Forbehold: der er kun 5-6 pre-facelift-biler til salg, alle 2013-14 og alle med ≥172k km;
ingen bil i hele stikprøven er så gammel som min (2012). Aldersmodellerne ekstrapolerer
derfor. En lineær aldersafskrivning på 7.250 kr/år er urealistisk i bunden af markedet
(model F's procent-afskrivning er mere retvisende, men lander samme sted).

### Det, der stadig holder: samme-karrosseri-gruppen og km-korrektion

- I pre-facelift-gruppen (2013-14, aldersspredning kun 17 mdr.) følger prisen km-tallet
  tæt (model E, R² 0,78): 172k → 54.900, 179k → 44.700, 199k → 39.900, 242k → 39.900,
  298k → 29.900. Ekstrapoleret til 141k: **ca. 53.600 kr**.
- Trygs egen reference 6859693 (44.700 kr, 179k) km-korrigeret til 141k med de tre
  hældninger (−153/−184/−202 kr pr. 1.000 km): **50.500 – 52.400 kr**. Referencen har
  kørt **27 % længere** end min bil.
- Billigste faktisk tilgængelige bil med samme karrosseri: **54.900 kr** (6780078,
  9/2014, 172.000 km = 31.000 km *mere* end min, forhandler). Jf. FED1998.580 skal
  beløbet række til et faktisk køb.
- Tandrem: alle pre-facelift-biler er ≥ 12 år og dermed over Fords 10-års-frist; min er
  skiftet 2022 med faktura. Alderseffekten i markedet dækker bl.a. den risiko —
  argumentet er derfor konsistent med data, ikke i modstrid.

### Anbefaling til næste svar

Drop facelift-/"kun km"-argumentet. Byg i stedet på (1) Trygs eget referencebil
km-korrigeret → 50-52k, (2) den billigste tilgængelige same-body-bil 54.900 kr med
31k km mere end min, (3) tandrem skiftet 2022 (faktura) → +10-15k, (4) nummerplader
1.780 kr. Realistisk krav ca. **65-70.000 kr**; realistisk forlig **50-55.000 kr**.
Kravet på 75.780 kr byggede på en facelift-bil (12/2016), og data viser, at den ikke er
"tilsvarende" — det er den svaghed, taksator allerede har ramt.
