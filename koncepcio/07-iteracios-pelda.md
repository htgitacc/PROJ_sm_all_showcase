# 7. Két iteráció végigvezetve

> Ez a dokumentum a modell próbája. A célja nem az, hogy megmutassa, milyen szép, amikor minden jól megy, hanem az, hogy **minden kapu elsüljön benne**, és kiderüljön, mi történik, amikor valami elromlik. Ha egy kapu a példában soha nem lép működésbe, akkor vagy felesleges, vagy nem tesztelhető — a dokumentum végén erre külön kitérünk.
>
> A számok kitaláltak, de a modell szabályaival és a kutatási adatokkal konzisztensek. Ahol egy szám az irodalomból származik, ott `S-nn` hivatkozás jelzi.

## A kiinduló helyzet

A csapat egy Product Ownerből, egy Scrum Masterből és két szenior fejlesztőből áll, mellettük a [00-mukodesi-modell.md](00-mukodesi-modell.md) szerinti ügynökpark. A termék a vállalati intranet megújítása. Az első iteráció a munkatárs-keresőt építi meg, a második a távollét-igénylést, amely a szervezeti adatokra épül — és éppen ezért kényszeríti ki az első iteráció kódjának átalakítását.

A kapacitás kiinduló feltevése napi mintegy 3,4 lezárható elem, háromnapos iterációra tehát valamivel több mint tíz — ebből a specifikációk jóváhagyása és a biztonsági találatok mérlegelése is fogyaszt, így a csapat kilenc elemet vállal.

> A dokumentumban szereplő számok a [prototipus/adatok/](../prototipus/adatok/) eseménynaplójából származnak, és a prototípus tesztjei rögzítik őket. Ha az adatok elmozdulnak, a tesztek elbuknak, és ezt a dokumentumot is frissíteni kell.

---

## Első iteráció — Munkatárs-kereső

### Az iteráció előtt: specifikáció és darabolás

A Product Owner megfogalmazza az igényt: legyen kereshető munkatárs-adatlap és böngészhető szervezeti fa. A specifikációt egy ügynök írja meg a vázlatából, és ebbe egy olyan szabály is bekerül, amely később a példa gerince lesz: **az alapadatokat minden bejelentkezett munkatárs láthatja, a telefonszám és az irodahely viszont csak az azonos vagy a fölérendelt szervezeti egységben dolgozóknak jelenik meg.**

A darabolásnál a csapat elvégzi a [01-munka-utja.md](01-munka-utja.md) szerinti vak összehasonlítást. A daraboló ügynök tizenegy elemet állít elő, a Product Owner hetet. A szeniorok vakon értékelik a két változatot, és az eredmény tanulságos: az ügynöki darabolás lefedettsége jobb, mert kigondolt olyan eseteket is, amelyeket a Product Owner átugrott — viszont **a láthatósági szabályt három különböző elem közé osztotta szét.** Ez pontosan az a hiba, amelyre a jóváhagyási kapu való, és amely a modell szerint a legolcsóbb helyen derül ki.

A Product Owner visszaküldi a darabolást, az ügynök összevonja a szabályt egyetlen elembe, és így áll össze a végleges kilenc elem.

| # | Elem | Megjegyzés |
|---|---|---|
| 1 | Adatmodell és migráció | |
| 2 | Adatbetöltés a HR-rendszerből | |
| 3 | Szervezeti fa API | |
| 4 | Munkatárs-kereső API | |
| 5 | **Láthatósági szabály** | magas kockázatú modul |
| 6 | Keresőfelület | |
| 7 | Szervezetifa-felület | |
| 8 | Adatlap nézet | |
| 9 | Auditnapló a kontaktadat-lekérésekről | |

A tervezés és a jóváhagyás összesen három bírálati eseményt fogyaszt (egy elutasított és egy elfogadott darabolás, plusz a technikai átnézés).

### Első nap

Négy ügynök indul párhuzamosan — ez a megvalósítás alatti oszlop korlátja. A délutáni védett bírálati idősávban az első két elem érkezik meg. Az adatmodell beolvad; az adatbetöltő visszamegy javításra, mert nem kezeli a duplikált e-mail-címeket, amelyek a valós HR-adatban előfordulnak.

A nap mérlege egy beolvadt és egy javítás alatt lévő elem. Ez a modell szerint várható: az első napon az ügynököknek először be kell fejezniük valamit, tehát a bírálati kapacitás egy része kihasználatlan marad.

### Második nap

A reggeli eltéréskezelésen az első valódi probléma kerül elő. A verifikáló ügynök az ötös elemnél — a láthatósági szabálynál — sikert jelentett, a tesztfuttató nyers kimenetéből viszont látszik, hogy a tizenegy tesztből csak kettő futott le. Ez a MAST-taxonómia korai lezárási hibamódja, amely a mért kudarcok 6,2 százalékát adja (S-10), és amelyre a gyártói útmutató is külön figyelmeztet „korai győzelem" néven (S-08).

A modell ezt azért fogta meg, mert a Definition of Done a nyers gépi kimenetből követeli meg a teljes tesztkészlet lefutását, nem az ügynök összefoglalójából ([02-minosegi-kapuk.md](02-minosegi-kapuk.md)). Ha az összefoglalóra hagyatkoztunk volna, az elem átment volna.

A délutáni bírálati sávban három elem kerül elbírálásra, és ekkor következik be az iteráció legkellemetlenebb pillanata: **öt elem várna bírálatra, a korlát négy.** A szabály szerint az ügynökök nem kapnak új feladatot, amíg a sor nem apad. A csapatnak ez rosszul esik, mert szabad gépi kapacitás áll kihasználatlanul — pontosan ez az az ösztön, amely ellen a korlát szól (S-28).

Ugyanezen a napon fut le a biztonsági lánc az ötös elemre. A kereső ügynök négy találatot jelez, a másik modellcsaládra épülő cáfoló ügynök hármat kiejt: kettő fejlesztői alapértelmezésre vonatkozott, amely éles környezetben nem áll fenn, egy pedig félreértette az adatfolyam irányát. **Egy találat marad, és az valódi:** a szűrés a kereső API-n megtörténik, de a szervezetifa-végpont szűretlenül adja vissza a telefonszámot. Az ember dönt: javítjuk még ebben az iterációban.

Ez a négyből egy arány jól illeszkedik ahhoz, amit a cáfoló architektúráról tudunk — a hivatkozott mérésben a jelöltek 79 százaléka esett ki a cáfolási szakaszban (S-15). A lényeg nem a szám, hanem az, hogy a három téves riasztás nem fogyasztott emberi figyelmet.

### Harmadik nap

Az elemek befejeződnek. Nyolc elem olvad be, az auditnapló átcsúszik a következő iterációba. A bemutatón az egyik szenior fejlesztő mutatja be az eredményt, és ő az, akinek a neve a beolvasztási nyomvonalon szerepel — a felelősségvállalás tehát nem szónoklat, hanem visszakereshető adat ([06-kormanyzas.md](06-kormanyzas.md)).

### A visszatekintés és ami belőle lett

A gépi réteg két ismétlődő hibaosztályt azonosít, mindkettő kétszer fordult elő, tehát az eszkalációs létra második fokára kerül ([05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md)).

Az elsőnél a verifikáló ügynök részleges tesztfuttatás után jelentett sikert. A másodiknál az implementáló ügynök nem alkalmazta a láthatósági szűrést az újonnan bevezetett végpontokon. Mindkettőből szabály lesz a szabályfájlban, azonosítóval és visszamutatással arra a bírálati eseményre, amelyből született (S-26):

> **SZ-06** — A verifikáló nem jelenthet sikert, amíg a tesztfuttató nyers kimenete nem igazolja a teljes tesztkészlet lefutását; a lefutott és az összes teszt számát a kimenetből kell kiolvasni.
> *Kiváltó esemény: 5. elem, 2. nap. Kategória: verifikáció.*
>
> **SZ-07** — Minden végpont, amely munkatárs kontaktadatot ad vissza, kötelezően a láthatósági szűrőn keresztül szolgál ki. Új végpont nem vezethető be a szűrő alkalmazása nélkül.
> *Kiváltó esemény: 5. elem, biztonsági találat. Kategória: adatvédelem.*

Az emberi réteg fő témája a WIP-korlát miatti leállás. A csapat rossz érzésként éli meg, hogy az ügynökök álltak — a Scrum Master feladata itt az, hogy ezt ne szabályszegéssel oldják meg, hanem lássák, hogy a leállás a rendszer helyes működése.

### Mérés az iteráció végén

A legfontosabb hozadék a paraméterek kalibrálása.

| Paraméter | Feltevés | Mért | Következmény |
|---|---|---|---|
| Napi bírálati idő szeniorra (`R`) | 3 óra | 3,25 óra | a bírálat valamivel többet vitt el |
| Elemenkénti validálási idő (`t`) | 70 perc | 90 perc | **az elemek érdemben nehezebbek voltak a vártnál** |
| Javítási körök átlaga (`r`) | 0,5 | 0,625 | több visszaadás |

Az újraszámolt kapacitás így alakul: szeniononként `3,25 × 60 / 90 ≈ 2,17` bírálati esemény naponta, két szeniorral 4,33, ebből `4,33 / 1,625 ≈ 2,67` lezárható elem naponta, háromnapos iterációra **pontosan nyolc**. Ez kevesebb, mint a feltételezett tíz, tehát **a következő iterációra kilenc helyett nyolc elemet vállalunk** — és az iteráció valóban nyolc elemet zárt le, tehát a modell a mért paraméterekkel önmagával konzisztens.

A három közül a `t` eltérése a legfontosabb: húsz százalékkal hosszabb bírálatot mértünk, mint amit feltételeztünk, és mivel ez a szám a nevezőben van, egymagában húzza le a kapacitást. Ez a pilot legértékesebb egyetlen adata.

A többi mutató közül kettő érdemel figyelmet. Az emberi bírálati arány száz százalék: mind a nyolc beolvadt elemet ember nézte át — ez a modell legfontosabb egészségjelzője (S-05). Az első körös elfogadási arány viszont csak 37,5 százalék, vagyis nyolcból három elem ment át javítás nélkül. Ez elsőre rossznak tűnik, de illeszkedik ahhoz, amit az iparági mérés az AI-generált munka elfogadási arányáról mutat (S-06), és az igazi kérdés nem az abszolút érték, hanem az, hogy a következő iterációkban javul-e.

---

## Második iteráció — Távollét-igénylés

### Amit a modell másképp csinál a második körben

A kapacitás nyolc elem. A specifikáció szabadságkeret-számítást, jóváhagyási láncot és ütközésvizsgálatot ír elő. A jóváhagyó személyét a szervezeti fából kell meghatározni — és itt jön a példa fordulópontja: **az első iterációban épített szervezetifa-szolgáltatás csak lefelé tud járni, most viszont felfelé is kell.** Vagyis hozzá kell nyúlni a már beolvadt, működő kódhoz.

| # | Elem | Megjegyzés |
|---|---|---|
| 1 | Auditnapló | átcsúszott az előző iterációból |
| 2 | Távollét-adatmodell | |
| 3 | **Szabadságkeret-számítás** | magas kockázatú modul |
| 4 | **Jóváhagyó meghatározása** | refaktorálást igényel |
| 5 | Ütközésvizsgálat | |
| 6 | Igénylőfelület | |
| 7 | Jóváhagyói nézet | |
| 8 | Értesítés | |

### A refaktorálás szála

A négyes elem a modell szerint nem indulhat el karakterizációs tesztréteg nélkül, mert refaktorálást igényel. A szenior fejlesztő ezért először azt kéri, hogy egy ügynök rögzítse a szervezetifa-szolgáltatás **jelenlegi** viselkedését.

Az ügynök tizennégy tesztet ír. A szenior a tesztek külön bírálatánál ötöt visszadob, mert tautologikusak: a szolgáltatás kimenetét hasonlítják önmagához, tehát soha nem bukhatnának el, hacsak a kód nem dob kivételt. Ez pontosan az a jelenség, amely miatt a tesztek elbírálását elkülönítjük a kódétól ([02-minosegi-kapuk.md](02-minosegi-kapuk.md), S-17). A második körben az ügynök kézzel megadott, rögzített szervezeti struktúrára írja meg a teszteket, és így már használhatók.

Ezután fut le a refaktorálás — és **a karakterizációs teszt elbukik.** A felfelé járás bevezetése mellékhatásként megváltoztatta a gyermeklista rendezését: eddig név szerint jött, most beszúrási sorrendben. A távollét-igénylés szempontjából ez teljesen közömbös, a munkatárs-keresőben viszont felborítja a szervezeti fa megjelenítését.

Ez a példa legfontosabb pillanata, mert **ez a brief eredeti aggálya élesben**: az AI javított és rontott egyszerre. A hiba nem is abban az elemben jelent volna meg, amelyen dolgoztunk, hanem egy másikban, amelyhez látszólag nem nyúlt senki. A védőháló azért fogta meg, mert előre megépítettük.

### A magas kockázatú modul kezelése

A hármas elem, a szabadságkeret-számítás, üzleti szabályokat tartalmaz, tehát magas kockázatú. Itt érdemes pontosan követni, mit csinál a modell — mert nem azt, amit elsőre gondolnánk.

A mutációs pontszámot **nem** használjuk kapuként az új kódon. Ennek oka a replikációs vizsgálat eredménye: a mutációs pontszám akkor ad megbízható jelzést, ha a vizsgált kódot hibátlannak feltételezzük, viszont ha a kód maga is tartalmazhat hibát — márpedig egy frissen írt modul ilyen —, akkor nem megbízható jelző (S-35). Egy hibás implementációhoz tökéletesen illeszkedő tesztsorozat magas mutációs pontszámot érhet el, miközben a hibás viselkedést védi.

A modul tehát a szokásos módon megy át: elfogadási feltételek, emberi bírálat, tesztek külön elbírálása. **Amikor viszont elfogadtuk és beolvadt, felvesszük róla a mutációs alapmérést**, amely 71 százalék lesz. Ez a szám innentől regressziós védelemként működik: a következő iterációkban, ha bárki hozzányúl ehhez a modulhoz, a pontszám nem csökkenhet alá.

Ez a megkülönböztetés — hogy a mutációs teszt nem minőségi kapu az új kódon, hanem regressziós védőháló a már elfogadotton — a modell egyik legfinomabb pontja, és a példa nélkül nehéz lenne megérteni.

### A méretkorlát

A hatos elem, az igénylőfelület, 310 nettó sorral érkezik, ami túllépi a kétszáz soros határt. A modell szerint ilyenkor nem a bírálatot hosszabbítjuk meg, hanem az elemet bontjuk vissza: külön lesz belőle az űrlap és a naptárnézet. Ez a döntés a mérésekből következik, amelyek szerint az AI-val segített változtatások két és félszer nagyobbak a szokásosnál, és a nagyobb csomag rosszabb elbírálást vált ki (S-06).

A visszabontás egy plusz bírálati eseménybe kerül, tehát a nyolc elemből az egyik átcsúszik a következő iterációba.

### A visszatérő hibaosztály és az eszkaláció

Az iteráció végén a Scrum Master összeveti a hibaosztályokat az előző iterációval, és két különböző eredményt kap.

A verifikáció korai lezárása (SZ-06) **nem tért vissza**. A szabály fogott, a hurok működött — ez a bizonyíték arra, hogy a visszajelzés beépült (S-26).

A láthatósági szűrő megkerülése (SZ-07) viszont **visszatért**: az új távollét-végpont szűretlenül adta vissza a kérelmező telefonszámát. Ezzel az eszkalációs létra harmadik fokára lépünk, ahol a kérdés már nem az, hogy „miért hibázik az ügynök", hanem az, hogy mit kell a rendszeren változtatni.

A szenior fejlesztő megvizsgálja, és kiderül, hogy a szabály szövege végpontokról szólt, az új kód viszont egy lekérdezési mezőn keresztül szolgálta ki az adatot — a szabály betűje szerint nem is sérült. A csábító megoldás az volna, hogy átfogalmazzuk a szabályt. A csapat viszont mást dönt, és ez a példa második legfontosabb tanulsága:

**A visszatérő hibaosztályt nem szabállyal, hanem géppel kell megfogni.** Az utasításfájl puha korlát, mert az utasítás követendő szöveg, nem kikényszerített megkötés; a determinisztikus teszt kemény korlát ([06-kormanyzas.md](06-kormanyzas.md)). A megoldás ezért egy architektúrateszt, amely elbukik, ha bármely kontaktadatot visszaadó útvonal megkerüli a szűrőt — függetlenül attól, hogy végpontról, mezőről vagy bármi másról van szó. Az SZ-07 szabály megmarad, de már csak magyarázatként; a védelmet a teszt adja.

### Mérés a második iteráció végén

| Mutató | 1. iteráció | 2. iteráció |
|---|---|---|
| Vállalt / beolvadt elem | 9 / 8 | 8 / 7 |
| Emberi bírálati arány | 100% | 100% |
| Első körös elfogadási arány | 37,5% | 57,1% |
| Napi bírálati idő (`R`) | 3,25 óra | 2,73 óra |
| Validálási idő (`t`) | 90 perc | 82 perc |
| Javítási körök (`r`) | 0,625 | 0,33 |
| Ismétlődő hibaosztályok | 2 | 1 (ebből 1 visszatérő) |
| Új szabályok | 2 | 1 szabály + 1 architektúrateszt |

A számok iránya biztató, de két dolgot érdemes kimondani róluk. Az első az, hogy két iteráció alapján **semmilyen trendet nem lehet megállapítani** — a javulás lehet a feladatok könnyebbségéből is. A második az, hogy a validálási idő csökkenése nem feltétlenül jó hír: jelentheti azt, hogy a bírálók gyakorlottabbak lettek, de azt is, hogy felületesebbek. Ezt csak a hibaarány későbbi alakulása fogja eldönteni, és a Scrum Masternek addig gyanakvónak kell maradnia ([05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md)).

---

## A modell próbája: mi sült el, és mi nem

A dokumentum elején rögzített feltétel az volt, hogy minden kapunak működésbe kell lépnie. Az alábbi számvetés őszintén megmutatja, hol állunk.

| Kapu vagy szabály | Elsült? | Hol |
|---|---|---|
| Specifikációs jóváhagyási kapu | igen | 1. it., a láthatósági szabály szétszórása |
| Determinisztikus kapu | igen | folyamatosan |
| Ügynöki kapu | igen | biztonsági keresés |
| Cáfoló kapu | igen | 1. it., négy találatból három kiesett |
| Emberi beolvasztási kapu | igen | mindkét iterációban, minden elemnél |
| Nyers gépi kimenet követelménye | igen | 1. it., korai lezárás elfogása |
| WIP-korlát a bírálati soron | igen | 1. it., 2. nap, ügynökök leállítása |
| Méretkorlát | igen | 2. it., 310 soros elem visszabontása |
| Karakterizációs tesztréteg | igen | 2. it., a rendezési regresszió elfogása |
| Tesztek külön bírálata | igen | 2. it., öt tautologikus teszt visszadobása |
| Mutációs alapmérés | igen | 2. it., a szabadságkeret-modulon |
| Kapacitás-újraszámítás | igen | 1. it. végén, 9-ről 8 elemre |
| Eszkalációs létra 2. foka | igen | 1. it., két új szabály |
| Eszkalációs létra 3. foka | igen | 2. it., architektúratesztté alakítás |
| **Tiltott jogosultsági szint** | **nem** | egyetlen ügynök sem próbált éles adathoz nyúlni |
| **Eszkalációs létra 4–5. foka** | **nem** | nem volt rá ok |

A két nem elsült elemről érdemes külön szólni. A tiltott jogosultsági szint **megelőző kontroll**, nem felderítő: az a dolga, hogy ne történjen meg valami, tehát az, hogy nem lépett működésbe, nem hiba, hanem a rendeltetése. Ellenőrizni viszont kell, hogy tényleg zár-e — ezt nem a napi működés fogja megmutatni, hanem egy célzott próba, amelyet a pilot elején egyszer érdemes lefuttatni.

Az eszkalációs létra felső fokai azért nem sültek el, mert két iteráció alatt nem volt olyan probléma, amely idáig eljutott volna. Ezt nem tudjuk a példával igazolni, tehát a létra felső része **kipróbálatlan marad** — ezt a [09-kockazatok-es-kilepes.md](09-kockazatok-es-kilepes.md) kockázatként kezeli.

## Amit a példa a felületről elárul

A két iteráció végigvezetése azt is megmutatja, mit kellett volna a Scrum Masternek egy pillantással látnia, és mikor. A második nap délelőttjén azt, hogy a bírálati sor öt elemnél tart a négyes korláttal szemben. A második iteráció elején azt, hogy az SZ-07 szabály felvétele óta hány alkalommal fordult elő újra az érintett hibaosztály. Az első iteráció végén azt, hogy a mért paraméterek eltérnek a feltevéstől, tehát a következő iteráció vállalását csökkenteni kell.

Ezek adják a következő dokumentum, a [08-sm-felulet-specifikacio.md](08-sm-felulet-specifikacio.md) bemenetét — és a modell egyik ellenőrzési feltétele éppen az, hogy a felülethez **ne kelljen új fogalmat bevezetni** azon túl, ami ebben a példában szerepel.

## Nyitott kérdések

A példa két iterációt mutat, márpedig a kapacitásparaméterek stabilizálódásához valószínűleg több kell. Nem tudjuk, hogy a második iteráció javuló számai valódi tanulást tükröznek-e, vagy csak azt, hogy a feladatok könnyebbek voltak. És nem tudjuk, mi történik akkor, ha a szervezeti fához hasonló alapmodulhoz nem két, hanem öt iterációval később nyúlunk hozzá — vagyis amikor a karakterizációs tesztréteg megírója már nem emlékszik arra, mit is akartunk megőrizni.
