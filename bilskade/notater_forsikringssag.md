# Forsikringssag — totalskadet Ford Focus

## Sagens ramme

- **Bil:** Ford Focus III 1,0 EcoBoost **125 hk Titanium** stationcar, **reg.nr. JW 59 371**, 1. reg. juni 2012, 141.000 km, benzin, anhængertræk, 6-trins gearkasse (6 gear = 125 hk-varianten; 100 hk har 5 gear)
- **Skade:** Påkørt **29/7 2026** af Charlotte Kragelund, reg.nr. DX 24 572 (skadevolder; venstre bagdør + venstre bagskærm). Modpartens forsikringsselskab vil skrotte bilen (totalskade).
- **Modpartens selskab:** **Tryg** (ansvarsforsikring — det er modpartens forsikring, der skal betale)
- **Skadenummer hos Tryg:** **D258074**
- **Eget prisdokumentation:** bilbasen-analyse i denne mappe (`focus-vaerdi.html`, `focus_model.py`, `focus_listings.csv`) — estimeret genanskaffelsespris **ca. 52.300 kr** (bånd 47.000–57.000 kr) for 125 hk Titanium-varianten; bred model (alle benzin) ca. 55.000 kr. Modellen indeholder tillæg for 125 hk (+9.100 kr ift. 100 hk) og Titanium-trim (+3.200 kr); R² = 0,88. Udtrukket 26/8 2026.

## Juridisk grundlag (ansvarsskade — ikke egen kasko)

Da det er modpartens **ansvarsforsikring**, er grundlaget ikke forsikringsbetingelser/FAL § 37, men
**dansk rets almindelige erstatningsregler**:

- Færdselslovens § 101 (objektivt ansvar for motorkøretøjer) og § 108 (direkte krav mod
  modpartens forsikringsselskab).
- Ved totalskade af en løsøregenstand er erstatningen efter fast praksis
  **genanskaffelsesprisen for en tilsvarende genstand** (samme mærke, alder, stand) —
  samme målestok som i kaskosagerne nedenfor. Restværdi (skrotværdi) fratrækkes, hvis
  skadelidte beholder bilen; overtager selskabet bilen, udbetales det fulde beløb.
- **Vigtig konsekvens:** Ankenævnet for Forsikring behandler klager fra selskabets egne
  kunder — som skadelidt tredjemand hos Tryg kan man normalt **ikke** klage til nævnet.
  Eskalationsvejen er i stedet forhandling → evt. **småsagsprocessen** ved retten
  (krav under 50.000 kr; begrænsede omkostninger, ingen advokatpligt).
  Nævnspraksis er alligevel relevant som udtryk for branchens egen fortolkning af,
  hvad en tilsvarende bil "koster".

## Relevante afgørelser (fundet via Karnov, 26/8 2026)

### FED2000.4586 (Ankenævnet for Forsikring, sag 53.099, 4/12 2000) — ⭐ vigtigst
Nævnet udtaler, at standardklausulen ("det beløb, en tilsvarende bil af samme alder og
stand vil kunne anskaffes for mod kontant betaling") **efter fast praksis fortolkes som
det beløb, en forhandler ville kunne opnå ved salg af bilen på normale vilkår** —
dvs. **forhandler-udsalgspris**, ikke privatsalgs- eller indbytningspris.
→ Bilbasen-analysen måler præcis forhandlerudbudspriser. Brug denne som hovedcitation.

### FED2011.364 (Ankenævnet, sag 78.323, 14/3 2011) — selskabernes egen metode
Tryg (netop Tryg!) fastsatte handelsværdien ud fra: Bilinfo-gennemsnitsvurdering,
**6 sammenlignelige bilbasen-annoncer**, og prisudsagn fra 2 forhandlere — og lagde
**3.000 kr i leveringsomkostninger oveni** ("incl. levering", salgsklar bil med
brugtvognsgaranti). Beskriver også syn- og skønsproceduren via DAF: klager betaler
(~6-7.000 kr i 2010), men selskabet betaler alt, hvis skønsmanden lander **over**
selskabets tilbud. NB: i sagen landede skønsmanden *under* (15.000 mod tilbudt 28.000).
Nævnet: bevisbyrden for højere værdi ligger hos klager. [Selskab medhold]
→ (1) Min metode = deres metode; (2) argumentér for leveringsomkostninger oveni;
(3) syn og skøn er en risiko — dokumentation først.

### FED1999.21 (Vestre Landsret, 12/2 1999) — dokumentation afgør
Ejer af totalskadet Mitsubishi krævede 65.000, fik tilbudt 50.000 — **tabte**, fordi hun
ikke kunne dokumentere, at en tilsvarende bil var dyrere end tilbuddet (én anekdotisk
bil + vag vidneforklaring; skønserklæringen støttede hende ikke). Tilsvarende
**FED1999.666 (VL)**: tilbudt erstatning ikke godtgjort urimelig.
→ Bevisbyrden ligger hos skadelidte. 26 annoncer + regression er langt stærkere
dokumentation, end hvad klagerne i disse sager havde.

### U.2016.3075V (Vestre Landsret, 11/5 2016) — standarden anvendt, men stand tæller
Erstatning for totalskadet bil = genanskaffelsesprisen (FAL § 37, stk. 1). Ejeren
krævede 219.800 kr ("billigste tilsvarende bil på nettet"); landsretten tilkendte
115.000 kr under hensyn til bilens faktiske stand (frikørt taxa, 300.000+ km,
motorskade).
→ Bilens konkrete stand justerer prisen. Min bils relativt lave km-tal (141.000 —
de fleste jævnaldrende i stikprøven har 170-250.000 km) trækker OP; nævn service-
historik og stand i argumentationen.

### FED1998.580 (Vestre Landsret, 20/4 1998) — ⭐ ansvarsskade: beløbet skal RÆKKE til køb
Ansvarsskade (færdselslovens § 108) — præcis min situation. Skadelidtes krav på fuld
erstatning omfatter *"et så stort kontantbeløb, at han på uheldstidspunktet kunne have
købt en bil svarende til den ødelagte"*. Retten fastslog, at dette beløb ligger **"en
del højere"** end den pris, en forhandler ville have KØBT bilen for (indbytningsværdi
163.000), og satte skønsmæssigt 180.000 (nypris var 186.000) — dvs. i den ØVRE ende af
spændet, ved hvad det faktisk koster at anskaffe. Også: underskrift på "fuld og endelig
afgørelse" over for egen kaskoforsikrer afskar IKKE yderligere krav mod ansvars-
forsikreren. Finansieringsomkostninger og senere prisstigninger dækkes ikke.
→ Argument: erstatningen skal kunne omsættes til en FAKTISK tilgængelig tilsvarende
bil — ikke et statistisk gennemsnit, man ikke kan handle til. Domstolene regner ikke
"middelværdi + usikkerhed", men fastsætter ét skønsmæssigt beløb — og lægger det dér,
hvor skadelidte reelt kan købe.

### FED1997.525 (Østre Landsret) — usikkerhed skabt af selskabet går ud over selskabet
Ved erstatningsfastsættelsen kom det selskabet til skade, at det trods opfordring
ikke havde foretaget taksering på skadetidspunktet. (Bådsag; princippet: den part,
der er skyld i bevisusikkerheden, bærer den.)

### FED1998.3558 (Ankenævnet, sag 47.120, 6/7 1998) — skriv ikke under
Klager underskrev erstatningsopgørelse dagen efter uheldet ("var i chok"), fortrød.
Nævnet: aftalen står ved magt. Samme mønster i FED2005.954.
→ **Underskriv ingen erstatningsopgørelse/accept, før beløbet er på plads.**

### 75 %-reglen (registreringsafgiftslovens § 7; refereret i FED2011.364)
Bilen SKAL erklæres totalskadet, når reparation (opgjort efter bruttopriser på nye
reservedele inkl. moms og lakering) overstiger 75 % af handelsværdien. Genopbygning
uden ny registreringsafgift er ulovlig.
→ Bemærk asymmetrien: jo lavere Tryg sætter bilens værdi, jo lettere bliver den
"totalskadet" — men den værdi, de bruger i 75 %-beregningen, skal være den samme
værdi, de udbetaler. Bed om taksatorrapporten og deres værdifastsættelse med
beregningsgrundlag (hvilke annoncer/kilder).

## Strategi

1. Bed Tryg om skriftligt erstatningstilbud **med beregningsgrundlag** (hvilke
   annoncer, Bilinfo-tal, stand-vurdering) + kopi af taksatorrapport, sagsnr. D258074.
2. Svar med bilbasen-dokumentationen: 26 forhandlerannoncer, model ⇒ **ca. 52.300 kr**
   for 125 hk Titanium (+ evt. leveringsomkostninger, jf. FED2011.364). Citer
   FED2000.4586 (forhandler-udsalgspris er målestokken) og fremhæv lavt km-tal ift.
   sammenlignelige biler. Hvis Trygs taksator bruger 100 hk/5-gears-annoncer som
   reference, skal de korrigeres op med ca. 9.000 kr.
3. Underskriv intet før enighed om beløb.
4. Ved fastlåst forhandling: overvej syn og skøn (hvis Tryg tilbyder det) eller
   småsagsproces. Kravets størrelse (differencen) afgør, om det kan betale sig.
5. Husk også sideomkostninger: nummerplader/omregistrering, evt. leje-/transportudgifter
   i rimelig periode kan kræves erstattet ved ansvarsskade.

## Udlevering af bil og registreringsattest (Bjarne Nielsen Birkerød / Tryg)

Status: Bilen har været til vurdering hos Bjarne Nielsen Birkerød (konkluderede
totalskade). De krævede registreringsattesten og ville beholde bilen — uden at
stille erstatningsbil. Attesten blev IKKE udleveret, og **bilen er fortsat i min
besiddelse**.

**Retsstillingen:**

- **FED1989.247 (Ankenævnet):** Vraget tilhører først selskabet **efter udbetaling af
  kontanterstatningen**. Indtil da er bilen MIN, og selskabet må ikke bortskaffe
  den, så længe værdien ikke er endeligt fastsat.
- Udlevering af bil + registreringsattest og betaling er **samtidige ydelser** —
  standardproceduren (jf. Trygs eget brev i FED2011.364): skriftligt tilbud →
  accept → udbetaling mod registreringsattest. **Der er ingen pligt til at aflevere
  attest eller bil, før erstatningsbeløbet er aftalt.** Værkstedets krav er en
  praktisk rutine, ikke et retskrav.
- Praktisk: Så længe bilen står indregistreret, løber vægtafgift og forsikring.
  Ved lang forhandling kan man selv afmelde bilen (nummerplader til Motorstyrelsen)
  uden at udlevere bilen til Tryg.
- Alternativ: Man kan vælge at beholde vraget mod fradrag af restværdien i
  erstatningen (sælge det selv til autoophug) — men bilen kan ikke genindregistreres
  uden ny registreringsafgift (75 %-reglen).

## Erstatningsbil / afsavnserstatning

- **F&P Responsum nr. 3296 (23/6 2000):** Skadelidte har krav på fuld erstatning,
  begrænset af tabsbegrænsningspligten. Ved totalskade ydes **normalt
  afsavnserstatning i 14 dage** — perioden hvor man med rimelighed kan skaffe en
  anden bil. (Rejseselskab, der krævede 104 dage frem til opgørelsen, fik afvist
  udgangspunktet — men F&P åbnede for mere, hvis 14 dage ikke praktisk rakte.)
- **FED2002.7 (Vestre Landsret — ansvarsskade):** Skadevolders ansvarsforsikring
  skulle dække **billeje i hele den rimelige taksations- og reparationsperiode**
  (45 af 68 dage tilkendt). Vigtigt: retten lagde til grund, at langsom taksation
  er **selskabets risiko**, ikke skadelidtes. Fradrag for sparet drift på egen bil
  (0,90 kr/km i sagen); perioden blev beskåret for ferie/fridage, og behovet var
  erhvervsmæssigt begrundet — ved rent privat behov kan dækningen være smallere
  (evt. takstmæssig afsavnserstatning i stedet for fuld lejebil).
- **Konklusion for min sag:** Bilen er kørbar, og jeg bruger den stadig — der er
  derfor intet afsavn fra skadedatoen. Afsavnsperioden begynder, når bilen
  udleveres til Tryg (mod betaling), og løber, indtil en tilsvarende bil er
  anskaffet (normalperiode ca. 14 dage, jf. F&P responsum 3296 — længere, hvis
  forsinkelsen skyldes Tryg). Krav: lejebil eller afsavnserstatning i denne
  periode. Kravet rejses over for Tryg (skadenr. D258074), ikke over for
  værkstedet — Bjarne Nielsen har ingen pligt til at stille bil, men Tryg har
  pligt til at erstatte tabet.
- Gem dokumentation: kvitteringer for lejebil/offentlig transport, datoer for
  Trygs sagsskridt (besigtigelse, tilbud), egne rykkere.

## Trygs tilbud 1/9 2026 og km-baseret modsvar

**Trygs tilbud (mail 1/9 2026 fra taksator Thomas Dyrendal Nielsen, `tryg_taksator_vurdering.eml`):
45.000 kr.** Dokumentation: 3 annoncer — bilbasen 6859693 (44.700 kr, **179.000 km** = 38.000 km
mere end min), bilbasen 6964634 (29.800 kr, 100 hk Trend, 185.000 km), biltorvet 3068448
(ca. 60.000 km mere). **Alle tre referencebiler har kørt 40-60.000 km mere end min bil (141.000 km).**

**Km-analyse 1/9 2026** (`focus_titanium_listings.csv`, `focus_km_model.py`): alle 54 annoncer
på bilbasen for Ford Focus stc. 1,0 Titanium, 1. reg. 2011+, benzin, med anhængertræk;
heraf 29 Focus III (SCTi — samme generation som min; Focus IV/"EcoBoost"-badge 2018+ frasorteret).
Prismodel med **kun km som parameter** (ikke alder), 28 retail-annoncer:

> pris = 112.285 − 284 kr pr. 1.000 km, R² = 0,61 ⇒ **72.200 kr ved 141.000 km** (±10.400)

Billigste Focus III med km ≤ 141.000 (jf. FED1998.580: beløbet skal RÆKKE til faktisk køb):
- **59.000 kr** — 6984909, 1,0 SCTi 125 Titanium stc, 12/2016, præcis 141.000 km (privatsalg)
- **71.900 kr** — 6864715, 1,0 SCTi 125 Titanium stc, 9/2015, 109.000 km (billigste **forhandler**,
  jf. FED2000.4586: forhandler-udsalgspris er målestokken)

Krydstjek: korrigeres Trygs egen referencebil 6859693 (44.700 kr, 179.000 km) for
km-forskellen på 38.000 km med Focus III-hældningen (−284 kr/1.000 km) fås 44.700 + 10.800 ≈
**55.500 kr** — dvs. selv Trygs egen metode giver mere end 45.000, når der korrigeres for km.
Ingen bil i hele stikprøven med ≤ 141.000 km udbydes under 59.000 kr.

### Tandrem (våd rem / "wet belt") — 1,0 EcoBoost

Fords officielle interval for Focus III 1,0 EcoBoost: **10 år eller 240.000 km — det, der
kommer først** (150.000 miles; bekræftet af flere kilder, bl.a. autodoc.dk-servicedata og
danske Ford-værksteder; skift koster ca. 10-15.000 kr, fx bilhusetTHYBO tilbyder 9.995 kr).
Værksteder anbefaler ofte tidligere skift (5-6 år / 100-120.000 km), fordi den oliebadede
rem er kendt for at nedbrydes før tid, men **det officielle krav er 10 år/240.000 km**.
I hele stikprøven (max 291.000 km) er **alderen altid det bindende krav**, ikke km.

**Min rem ER skiftet i 2022, og faktura haves** (bilen er fra 6/2012 — remmen forfaldt
aldersmæssigt juni 2022). Det giver et stærkt standargument: de billigste
sammenligningsbiler har ikke dokumenteret remskift og står lige foran/over fristen:
6984909 (59.000 kr, 12/2016) forfalder om ca. 3 mdr; 6864715 (71.900 kr, 9/2015) er
**overskredet**; 6952123/6977537 (72-74.900 kr, 2017) forfalder om ca. 9 mdr. En
"tilsvarende bil i samme stand" skal derfor have frisk rem ⇒ ca. 15.000 kr lægges til
genanskaffelsesprisen (jf. U.2016.3075V: konkret stand justerer prisen — begge veje).
**Fakturaen vedlægges svaret til Tryg.**

### Svar til taksator (udkast 1/9 2026: `svar_taksator_udkast.txt`)

Krav baseret på den billigste faktisk tilgængelige bil med ≤ 141.000 km (59.000 kr,
privatsalg 6984909) — bevidst konservativt valgt frem for modellens 72.200 kr og
billigste forhandler 71.900 kr (forhandler-udsalgspris er ellers målestokken, jf.
FED2000.4586 — det er forhandlingsmæssigt "gratis" opside):

| Post | Beløb |
|---|---|
| Billigste tilsvarende bil (141.000 km) | 59.000 kr |
| Tandremsskift (min er skiftet 2022, faktura vedlagt) | 15.000 kr |
| Nummerplader | 1.780 kr |
| **I alt** | **75.780 kr** |

Svaret indeholder ascii-tabel over alle 29 Focus III-annoncer sorteret efter km
(gør km-gradienten synlig; Trygs egen referencebil markeret), links til de to
billigste biler (begge verificeret aktive 1/9 2026), kontooplysninger (udfyld
placeholders før afsendelse) samt forbehold: udbetaling af et ikke-aftalt beløb
er ikke fuld og endelig afgørelse; attest og nøgler udleveres, når beløbet er aftalt.

## Taksators svar 2/9 2026 og facelift-analyse 6/9 2026

Taksator (`tryg_taksator_vurdering2.eml`) fastholder 45.000 kr: ingen af mine 28 biler er
fra samme aargang (aeldste 4/2013), en 1-6 aar nyere bil kan ikke sammenlignes ud over km;
hans reference 6859693 er "1 aar nyere, 40.000 km mere" og udligner. Vedligehold (tandrem)
oeger ikke vaerdien, men bevarer den. Beder om dokumentation ud fra aargang, motor, udstyr, km.

Analyse i `facelift_analyse.md` (+ `focus_facelift_listings.csv`, `focus_facelift_model.py`):
- Focus III pre-facelift = 1. reg. <= 10/2014 (min bil); facelift Mk3.5 fra 11/2014 (Ford DK
  pressemeddelelse 18/9 2014); skaering verificeret paa annoncefotos.
- Ny soegning 6/9: 26 stk. 1,0 Titanium stc m. traek, heraf kun 6 pre-facelift (alle 2013-14,
  >=172k km). Trygs reference er pre-facelift som min.
- Facelift-tillaeg ved samme km (model A): ca. 16.700 kr. MEN med alder i modellen forsvinder
  facelift-effekten; alder taeller ca. 7.250 kr/aar (lineaer) / 10,9 %/aar (log), ogsaa inden for
  facelift-gruppen. 1 aar ~ 42.000 km - taksators paastand bekraeftes af markedet.
  Aldersmodeller giver min bil 39-42k. **Facelift-argumentet boer ikke bruges.**
- Holdbart: same-body-gruppen foelger km (R2 0,78) -> 53.600 kr ved 141k; Trygs reference
  km-korrigeret 50.500-52.400 kr; billigste tilgaengelige same-body-bil 54.900 kr (172k km).
  Ny billigste facelift-bil <=141k km: 6986741, 57.500 kr, 11/2016, 136k, privat.
- Anbefalet krav ca. 65-70k (54.900 + tandrem 10-15k + plader 1.780); forligsniveau 50-55k.
- Tjek 6/9: bilbasen Focus aargang 2011-2012, alle karrosserier/braendstof = 20 biler, 9 Titanium,
  kun 2 fra 2012 (1,6 Ti-VCT hatchback, 2,0 TDCi stc), INGEN 1,0 EcoBoost. Derfor er alle
  sammenligningsbiler noedvendigvis nyere - skrevet ind i svarudkast 2.
- Tandrem i de 6 same-body-annoncer (tjekket 6/9): dokumenteret skift i 6859693 (132k), 6985175
  (160k; 39.900 kr, 199k km, synet 7/2026) og 6980626 (206k, engros). IKKE i 6780078, 6919484, 6981634.
- **Svarudkast 2 (7/9 2026): `svar_taksator_udkast2.txt`** - krav 52.180 kr = Trygs egen
  reference 6859693 (44.700, 179k km, tandrem skiftet ved 132k som min) + km-kompensation
  38.000 km x 150 = 5.700 + plader 1.780. Rent km-argument; ingen tandremspost, ingen
  retspraksis. Forkastede versioner: 76.330 (6780078 54.900 + km + rem + plader, dobbelt
  kompensation), 71.680 (uden km-komp.).

*Noter udarbejdet 26/8 2026 på baggrund af Karnov-søgninger ("genanskaffelsespris
totalskade bil", 35 praksis-dokumenter; "afsavnserstatning bil totalskade",
19 dokumenter) og bilbasen-analyse i denne mappe.*
