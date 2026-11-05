# Csapatindító dokumentum — AI-first fejlesztőcsapat pilot

> **Használat.** Ez kitöltendő sablon, a szögletes zárójeles helyek a csapat döntéseit várják. Az indoklásokat a [koncepcio/06-kormanyzas.md](../06-kormanyzas.md) tartalmazza. A dokumentumot a pilot indulása előtt véglegesíteni kell, és minden iteráció végén felül kell vizsgálni, hogy még érvényes-e.
>
> **Verzió:** [x.y] · **Utolsó módosítás:** [dátum] · **Jóváhagyta:** [név]

---

## 1. Miért létezik ez a csapat

**A pilot célja.** [Egy bekezdés arról, mit akarunk megtudni. Nem a terméket írja le, hanem a kérdést: működtethető-e AI-ügynökökkel dolgozó fejlesztőcsapat úgy, hogy a minőségi kontroll ne csússzon el.]

**A termék.** [Mit építünk, és miért ez a választás.]

**Amit a pilot nem vizsgál.** [Amit tudatosan kihagyunk, hogy a kérdés élesen maradjon.]

**A pilot időtartama.** [X] iteráció, első értékelés a 3. iteráció után.

---

## 2. A siker kritériuma

### Alapfeltételek — mind teljesülnie kell

| Kritérium | Küszöb | Teljesült? |
|---|---|---|
| Emberi bírálati arány | ≥ 95% | |
| Beolvadt elem megnevezett emberi jóváhagyó nélkül | 0 | |
| A biztonsági lánc által átengedett éles incidens | 0 | |

### Értékteremtés

| Kritérium | Elvárás | Teljesült? |
|---|---|---|
| Iterációnként beolvadt elemek száma | nem csökken | |
| Első körös elfogadási arány | javuló irány | |
| Visszatérő hibaosztályok száma | csökkenő irány | |
| Innovációs arány | nem romlik | |

### Fenntarthatóság

| Kritérium | Elvárás | Teljesült? |
|---|---|---|
| Szeniorok önbevallásos terhelése | nem nő tartósan | |
| Bírálati terhelés eloszlása | nem tartósan egyenetlen | |
| Duplikációs arány | nem romlik érdemben | |
| Iterációnkénti költség | a keretben marad | |

---

## 3. Kilépési feltétel

A pilotot leállítjuk, ha az alábbiak **bármelyike** bekövetkezik:

- [ ] Az emberi bírálati arány két egymást követő iterációban 80% alá esik, és a WIP-korlát szigorításával sem hozható vissza.
- [ ] Éles biztonsági incidens történik, amelyet a négylépcsős lánc átengedett.
- [ ] A szeniorok terhelése tartósan nő, miközben az átbocsátás nem.
- [ ] Hat iteráció után a kapacitásparaméterek nem stabilizálódnak.
- [ ] A költség meghaladja a keretet anélkül, hogy az értékteremtési kritériumok teljesülnének.

**A leállítás nem kudarc.** Azt jelenti, hogy ez a modell, ebben a csapatban, ezekkel az eszközökkel nem működött — a negatív eredmény is eredmény, ha a mérés megbízható volt.

---

## 4. Ki miért felel

| Szerep | Név | Felelősség | Amit kiad a kezéből |
|---|---|---|---|
| Product Owner | [név] | sorrend, elfogadhatóság, a darabolás jóváhagyása | szövegezés, technikai bontás, háttérkutatás |
| Scrum Master | [név] | a kapuk épsége, a tanulási hurok fenntartása, terheléseloszlás, AI-jártasság | adatgyűjtés, státuszriportolás |
| Szenior fejlesztő | [név] | bírálat, ügynökök hangolása, architekturális felügyelet | mechanikus kódírás |
| Szenior fejlesztő | [név] | ugyanaz | ugyanaz |

**Alapszabály:** minden beolvasztásnak van megnevezett emberi jóváhagyója, és ez a nyom a verziókezelőben marad.

### Döntési jogkörök

| Kérdés | Ki dönt |
|---|---|
| Mi kerüljön a backlogba, milyen sorrendben | Product Owner |
| Egy elem kész-e | a bíráló szenior, a Definition of Done alapján |
| Architektúra és eszközválasztás | szeniorok közösen |
| A folyamat szabályainak módosítása | a csapat együtt, a visszatekintésen |
| Az iteráció leállítása torlódás miatt | Scrum Master |
| A pilot leállítása | Product Owner, a kilépési feltétel alapján |

---

## 5. Az ügynökök jogosultsági szintjei

### Szabad, jóváhagyás nélkül
- A repozitórium olvasása és elemzése
- Tesztfuttatás elkülönített környezetben
- Ág létrehozása, javaslat és pull request készítése
- Dokumentáció írása

### Emberi jóváhagyással
- Új függőség behozatala
- Adatbázis-sémamódosítás
- Konfiguráció és környezeti változó módosítása
- Build- és telepítési folyamat módosítása
- **A szabályfájl módosítása**

### Tiltott
- Hozzáférés éles adathoz és titkokhoz
- Írás külső szolgáltatásba
- Jogosultsági és biztonsági beállítások módosítása
- A naplózás kikapcsolása vagy a beolvasztási védelmek megkerülése

**Incidens alatt a jogosultsági szintek nem lazulnak.**

A jogosultságok tényleges zárását a pilot elején egyszer célzott próbával ellenőrizni kell — a napi működés ezt nem fogja megmutatni.

---

## 6. Az iteráció ritmusa és a korlátok

**Iterációhossz:** [3] nap — *levezetett érték, a mért ciklusidőből újraszámítandó.*

**Kapacitásparaméterek** (a legutóbbi mérés alapján):

| Paraméter | Feltevés | Legutóbb mért | Mikor |
|---|---|---|---|
| Napi bírálati idő szeniorra (`R`) | 3 óra | [ ] | [ ] |
| Elemenkénti validálási idő (`t`) | 70 perc | [ ] | [ ] |
| Javítási körök átlaga (`r`) | 0,5 | [ ] | [ ] |

**Számított napi kapacitás:** `(R × 60 / t) × 2 / (1 + r)` = [ ] elem/nap
**Iterációs bírálati keret:** [ ] esemény, ebből kódra [ ]

**WIP-korlátok:**

| Szakasz | Korlát |
|---|---|
| Finomítás alatt álló specifikáció | 3 |
| Ügynöki megvalósítás alatt | 4 |
| **Bírálatra vár** | **4** (szeniononként 2) |
| Javítás alatt | nincs |

**Méretkorlát:** 200 nettó megváltoztatott kódsor elemenként, generált és triviálisan ismétlődő részek nélkül.

**Védett bírálati idősáv:** naponta [időpont]–[időpont], megszakíthatatlan.

---

## 7. Események

| Esemény | Gyakoriság | Kötelező kimenet |
|---|---|---|
| Iterációtervezés | minden iteráció | kiosztott elemek, a bírálati keret elosztása |
| Napi eltéréskezelés | naponta, ha van eltérés | mit állítunk le, mit engedünk tovább |
| Védett bírálati idősáv | naponta | a bírálati sor apadása |
| Iterációs bemutató | minden iteráció | megnevezett emberi felelős az inkrementumért |
| Visszatekintés — gépi réteg | minden iteráció | legalább egy szabályváltozás, vagy annak indoklása, miért nem kellett |
| Visszatekintés — emberi réteg | minden második iteráció | — |

---

## 8. Definition of Done

Lásd: [sablonok/definition-of-done.md](definition-of-done.md). A DoD módosítása csak a visszatekintésen, a teljes csapat egyetértésével történhet.

---

## 9. AI-jártassági terv

> Az EU mesterségesintelligencia-rendeletének 4. cikke 2025. február 2. óta alkalmazandó, és megköveteli, hogy a szervezet gondoskodjon a személyzete megfelelő szintű AI-jártasságáról. Ez a szakasz nem jó gyakorlat, hanem jogi kötelezettség dokumentálása.

| Szerep | Mit kell értenie | Hogyan biztosítjuk | Mikor |
|---|---|---|---|
| Product Owner | mit tud és mit nem tud egy ügynök; miért nem delegálható az elfogadhatóság | [ ] | [ ] |
| Scrum Master | a hibaosztályok értelmezése; az eszkalációs létra; a mérőszámok korlátai | [ ] | [ ] |
| Szenior fejlesztők | prompt- és kontextustervezés; a fenyegetési modell; a modellcsaládok keverésének oka | [ ] | [ ] |
| Mindenki | mit tilos ügynöknek megmutatni és megadni | [ ] | [ ] |

---

## 10. Mérési terv

**Alapelv:** az adatgyűjtés csapatszinten aggregált, egyéni bontás nélkül. A mérőszámok nem alkalmasak egyéni teljesítményértékelésre, és ezt a csapatnak írásban garantáljuk.

| Mérőszám | Forrás | Gyakoriság |
|---|---|---|
| Emberi bírálati arány | verziókezelő | folyamatos |
| Bírálati sor hossza és kora | folyamatkezelő | folyamatos |
| `R`, `t`, `r` | kézi rögzítés | naponta |
| Első körös elfogadási arány | verziókezelő | iterációnként |
| Változtatás mérete | verziókezelő | folyamatos |
| Duplikációs és refaktorálási arány | kódelemző | iterációnként |
| Mutációs pontszám (magas kockázatú modulok) | tesztfuttatás | iterációnként |
| Hibaosztály-eloszlás | kézi besorolás | iterációnként |
| Szabályfájl növekedése és visszaesések | verziókezelő | iterációnként |
| Token- és pénzköltség | ügynöknaplók | iterációnként |

**Amit nem mérünk:** kódsort, commitszámot és pull request-darabszámot teljesítménymutatóként; ügynökök közötti teljesítménysorrendet; önbevallásos sebességet.

---

## 11. Aláírás

A csapat tagjai elolvasták és elfogadták a fentieket.

| Név | Szerep | Dátum |
|---|---|---|
| | | |
| | | |
| | | |
| | | |
