# Koncepció — AI-first fejlesztőcsapat működési modellje

Ez a mappa a [kutatas/](../kutatas/) eredményeire épülő működési modellt tartalmazza. A kutatás azt vizsgálta, mit tudunk; ez a koncepció azt mondja meg, mit csinálunk.

## A modell egy mondatban

**A csapat kapacitása nem az ügynökök sebességéből, hanem abból következik, hogy mennyi munkát tudnak a szeniorok felelősséggel átvenni — és minden más szabály ebből vezethető le.**

## Olvasási sorrend

A dokumentumok egymásra épülnek, de nem mind kell mindenkinek.

| Ha ez érdekel | Ezt olvasd |
|---|---|
| A modell egésze, gyorsan | [00-mukodesi-modell.md](00-mukodesi-modell.md), majd [07-iteracios-pelda.md](07-iteracios-pelda.md) |
| Hogyan működik a gyakorlatban | [07-iteracios-pelda.md](07-iteracios-pelda.md) — a két iteráció végigvezetve |
| Mit kell a Scrum Masternek csinálnia | [05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md) és [08-sm-felulet-specifikacio.md](08-sm-felulet-specifikacio.md) |
| Mi buktathatja meg | [09-kockazatok-es-kilepes.md](09-kockazatok-es-kilepes.md) |

## A dokumentumok

| Fájl | Miről szól |
|---|---|
| [00-mukodesi-modell.md](00-mukodesi-modell.md) | **A modell magja.** Csapatfelállás, a bírálati keret számítása, iterációritmus, WIP-korlátok, méretkorlát |
| [01-munka-utja.md](01-munka-utja.md) | A backlogtól a beolvasztásig; ki darabol, és hogyan mérjük, hogy jobb-e |
| [02-minosegi-kapuk.md](02-minosegi-kapuk.md) | Definition of Done, tesztstratégia, a négylépcsős biztonsági lánc |
| [03-esemenyek-es-tanulas.md](03-esemenyek-es-tanulas.md) | Az események átalakítása és a tanulási hurok az ügynökökbe |
| [04-meres.md](04-meres.md) | Mit mérünk, mit engedünk el, ki mondja meg, hogy jó |
| [05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md) | Szerepváltozások, az eszkalációs létra, kétrétegű csapatmodell |
| [06-kormanyzas.md](06-kormanyzas.md) | Jogosultságok, felelősség, dokumentációs rend, átadás, hibaelhárítás |
| [07-iteracios-pelda.md](07-iteracios-pelda.md) | **A modell próbája:** két iteráció végigvezetve, hibákkal együtt |
| [08-sm-felulet-specifikacio.md](08-sm-felulet-specifikacio.md) | Az SM-támogató felület specifikációja — a 3. fázis bemenete |
| [09-kockazatok-es-kilepes.md](09-kockazatok-es-kilepes.md) | Tizenkét kockázat, sikerkritérium, kilépési feltétel |

### Sablonok

Ezek használatra kész dokumentumok, nem leírások:

- [sablonok/csapatindito-dokumentum.md](sablonok/csapatindito-dokumentum.md) — a csapatot életre hívó dokumentum
- [sablonok/definition-of-done.md](sablonok/definition-of-done.md)
- [sablonok/AGENTS.md](sablonok/AGENTS.md) — az ügynököknek szóló utasításfájl
- [sablonok/iteracio-ellenorzolista.md](sablonok/iteracio-ellenorzolista.md) — a Scrum Master iterációs listája

## Hol válaszolunk a brief kérdéseire

| A [sm-all.md](../sm-all.md) kérdésköre | Hol |
|---|---|
| **Backlog** — ki darabol, hogyan mérhető | [01](01-munka-utja.md) |
| **Sebesség** — hogyan ne készüljön 30 elem 5 átnézett mellett | [00](00-mukodesi-modell.md) *(fő)*, [07](07-iteracios-pelda.md) |
| **Biztonság** — egy ügynök és modell, vagy több | [02](02-minosegi-kapuk.md) |
| **Tesztek** — hogyan legyen inkrementális, ne csak iteratív | [02](02-minosegi-kapuk.md) |
| **Scrum események** — mi marad, mi új, bevonható-e az AI | [03](03-esemenyek-es-tanulas.md) |
| **Teljesítmény** — mit mérünk, van-e értelme story pontnak | [04](04-meres.md) |
| **Csapatpszichológia** — Tuckman helyett mi | [05](05-szerepek-es-dinamika.md) |
| **Jogi keretek, felelősség, átadás, hibaelhárítás** | [06](06-kormanyzas.md) |
| **Szerepkör-változások, hibázó ügynök kezelése** | [05](05-szerepek-es-dinamika.md) |
| **Dokumentáció, csapatindító dokumentum** | [06](06-kormanyzas.md) + [sablonok](sablonok/) |
| **SM-segítő felület** | [08](08-sm-felulet-specifikacio.md) |

---

## Mi mögött áll bizonyíték, és mi a saját döntésünk

Ez a koncepció legfontosabb táblázata. A modell minden érdemi döntése vagy kutatási forrásra épül, vagy saját tervezési döntés bizonyíték nélkül — és a kettő nem ugyanannyit ér. Egy vitában vagy interjún az a mondat a legvédhetőbb, amelyik tudja magáról, melyik kategóriába tartozik.

### Bizonyítékra épülő döntések

| Döntés | Forrás |
|---|---|
| A kapacitás alapja az emberi bírálat, nem az ügynökök sebessége | S-05, S-06, S-24, S-28 |
| Kemény WIP-korlát a bírálati soron, szeniononként 2 elem | S-28 |
| A specifikáció jóváhagyása emberi kapu, a darabolás előtt | S-06, S-30 |
| Az implementáló ügynök egyszálú; egy feladatot nem osztunk szét | S-07, S-08, S-09, S-10 |
| A verifikáló és a cáfoló más modellcsaládból való, mint az implementáló | S-14, S-15 |
| A biztonsági lánc cáfoló, nem konszenzusos | S-15 |
| A kilépési feltételt nem az ügynök állapítja meg | S-08, S-10 |
| Nincs lefedettségi küszöb a Definition of Done-ban | S-16, S-17 |
| A mutációs teszt regressziós védőháló, nem új kód kapuja | S-35 |
| Karakterizációs tesztréteg minden refaktorálás előtt | S-04, S-06 |
| A tesztek elbírálása elkülönül a kódétól | S-17 |
| Minden beolvasztásnak van megnevezett emberi jóváhagyója | S-24, S-33 |
| Az emberi és a gépi bírálatot külön mérjük | S-05 |
| A story pontot elhagyjuk ügynöki munkára | S-11 |
| A DORA-mutatókat megtartjuk | S-02 |
| Kétrétegű csapatmodell: emberi réteg + T⁴ a szociotechnikain | S-18 |
| Az AI generálhat ötletet, de nem rangsorol | S-19, S-20 |
| Szabályfájl-alapú tanulási hurok, a hibaosztály eltűnése a bizonyíték | S-26 |
| `AGENTS.md` formátum a gépnek szóló dokumentációra | S-25, S-31 |
| A jogosultság szűkítése az elsődleges védelem | S-13 |
| Dokumentált AI-jártassági terv | S-22 (jogi kötelezettség) |

### Saját tervezési döntések — bizonyíték nélkül

Ezek azok, amelyeket **elsőként kell elhagyni vagy módosítani**, ha a modell túl bonyolultnak bizonyul.

| Döntés | Mivel dől el |
|---|---|
| A 200 soros méretkorlát konkrét értéke | mérés: átnézhető-e nagyobb csomag a becsült időn belül |
| A háromnapos iterációhossz | mérés: befér-e egy teljes kör |
| Az `R = 3 óra`, `t = 70 perc`, `r = 0,5` kiinduló értékek | mérés az első két iterációban; a `t` első becslése (35 perc) már a modell kidolgozása közben megdőlt |
| A védett bírálati idősáv mint önálló esemény | apad-e tőle a sor |
| Az emberi visszatekintés kétiterációnkénti ritmusa | elég gyors visszacsatolás-e |
| A „gumibélyegző-gyanú" figyelése | ad-e valaha valódi jelzést |
| Az eszkalációs létra öt foka | eljutunk-e valaha a felső fokokra |
| A háromszintű jogosultsági besorolás konkrét tételei | célzott próba a pilot elején |
| A csapatérettségi mutatótábla | értelmezhető-e egyáltalán |
| A „lazulásgyanú" összetett jelzése | túl sok téves riasztást ad-e |
| Vak összehasonlítás a darabolásnál | ad-e értékelhető jelzést két iteráció alatt |
| Vak rangsorolás a bemutatón | semlegesíti-e a torzítást |
| A felület jelez, de nem avatkozik be automatikusan | átlépi-e a csapat a saját szabályait |
| A sikerkritérium és a kilépési feltétel küszöbei | nincs viszonyítási alap |
| Külső szállításnak megfelelő nyomonkövetés belső terméknél | megéri-e a többletköltséget |
| Az átvevő csapat bíráljon az utolsó iterációban | csökkenti-e az átadási szakadékot |

---

## Amit ez a koncepció nem tartalmaz

Nem tartalmazza magát a Streamlit prototípust: annak specifikációja a [08](08-sm-felulet-specifikacio.md) dokumentumban van, a megvalósítás pedig a [prototipus/](../prototipus/) mappában.

Nem tartalmaz platformspecifikus leképezést. A modell szándékosan platformfüggetlen, hogy a későbbi, API-alapú irányba való elmozdulás ne jelentsen újraírást; a Claude Code és Cursor konkrét mechanizmusaira való leképezés külön függelék lesz.

És nem tartalmaz jogi tanácsadást. A [06](06-kormanyzas.md) dokumentum kutatási összefoglaló; a pilot éles indítása előtt a benne foglaltakat a szervezet jogi funkciójával kell egyeztetni.
