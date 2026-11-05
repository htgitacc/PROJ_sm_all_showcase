# AGENTS.md — [projekt neve]

> **Ez a fájl az ügynököknek szól.** Minden munkamenet elején be kell töltődnie. A formátum nyílt szabvány, a Linux Foundation alá tartozó Agentic AI Foundation gondozza.
>
> **Fontos korlát:** ez a fájl **puha korlát**. Az utasítás követendő szöveg, nem kikényszerített megkötés. A kemény korlátot a jogosultságkezelés, a hálózati elzárás, a determinisztikus tesztek és a beolvasztási védelem adja. Ha egy szabály másodszor is sérül, akkor nem a szöveget kell átfogalmazni, hanem gépi kaput kell építeni köré.
>
> **A fájl módosítása emberi jóváhagyáshoz kötött.**

---

## A projekt

[Egy bekezdés arról, mit csinál a rendszer és kinek. Ne architektúraleírás legyen, hanem az, amiből egy új belépő megérti a célt.]

**Fő technológiák:** [ ]
**Belépési pont:** [ ]

---

## Parancsok

```bash
# Függőségek telepítése
[parancs]

# Fejlesztői kiszolgáló indítása
[parancs]

# Teljes tesztsorozat
[parancs]

# Egyetlen teszt futtatása
[parancs]

# Linter és formázó
[parancs]

# Mutációs teszt (csak a magas kockázatú modulokra)
[parancs]
```

---

## Viselkedési szabályok

> Minden szabály egy elfogadott bírálati észrevételből született. A `Kiváltó` mező arra az eseményre mutat vissza, amelyből a szabály keletkezett — így később eldönthető, hogy a szabály még indokolt-e.

### SZ-01 — [rövid cím]
**Megszorítás:** [mit kell vagy nem szabad tenni]
**Indoklás:** [miért]
**Hatókör:** [hol érvényes]
**Kiváltó:** [iteráció, elem, bírálati esemény]
**Kategória:** [helyesség / adatvédelem / teljesítmény / verifikáció / stílus]

### SZ-02 — [rövid cím]
*(ugyanez a szerkezet)*

---

## Kódolási sztenderdek

[Nyelvenként vagy rétegenként. Ide az kerül, ami a bírálaton visszatérően előjött, nem az, ami a linterből amúgy is látszik.]

---

## Önellenőrzési lista

> Ezt a listát minden munka befejezése után, a pull request megnyitása **előtt** végig kell futtatni. A lista pontjai a szabályokból származnak.

- [ ] [pont, amely az SZ-01-hez tartozik]
- [ ] [pont, amely az SZ-02-höz tartozik]
- [ ] A változtatás nem lépi túl a 200 nettó sort. Ha túllépi, jelezd, és javasolj bontást — ne nyiss nagyobb pull requestet.
- [ ] Minden új teszt megmondható módon állít valamit: leírtam, mikor bukna el.
- [ ] Nem vezettem be új függőséget jóváhagyás nélkül.
- [ ] A dokumentációt is frissítettem ott, ahol a viselkedés megváltozott.

---

## Antiminták

> Amit már láttunk elromlani. Ezek nem elméleti hibák.

- **Teszt, amely az implementációt önmagához méri.** `assertEquals(service.foo(x), service.foo(x))` alakú vagy azzal egyenértékű állítás nem teszt. A várt értéket függetlenül kell megadni.
- **Részleges tesztfuttatásra alapozott sikerjelentés.** Sikert csak akkor jelenthetsz, ha a nyers kimenet igazolja a teljes tesztkészlet lefutását.
- **Új végpont vagy lekérdezési mező bevezetése a meglévő szűrők megkerülésével.** Ha adatot szolgálsz ki, keresd meg, milyen szűrőn keresztül szolgálja ki ugyanazt a meglévő kód.
- **Másolás refaktorálás helyett.** Ha egy meglévő logikát kell máshol is használni, emeld ki, ne másold.
- **Refaktorálás karakterizációs tesztréteg nélkül.** Ha meglévő, működő kódot alakítasz át, előbb rögzítsd a jelenlegi viselkedést.

---

## Amit nem tehetsz meg

- Nem férhetsz hozzá éles adathoz és titkokhoz.
- Nem írhatsz külső szolgáltatásba.
- Nem módosíthatsz jogosultsági és biztonsági beállítást.
- Nem kapcsolhatod ki a naplózást, és nem kerülheted meg a beolvasztási védelmeket.
- Nem módosíthatod ezt a fájlt jóváhagyás nélkül.

Az alábbiakhoz emberi jóváhagyás kell, tehát javasold, de ne hajtsd végre: új függőség behozatala, sémamódosítás, konfiguráció- és környezetiváltozó-módosítás, a build- és telepítési folyamat módosítása.

---

## Ha elakadsz

Ne találgass, és ne kerüld meg a korlátot. Írd le, mi hiányzik, és állj meg. Egy megállított feladat olcsóbb, mint egy rossz irányba elvitt.
