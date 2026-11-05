# Iterációs ellenőrzőlista — Scrum Master

> **Használat.** Iterációnként egy példány. Ez a lista a [koncepcio/08-sm-felulet-specifikacio.md](../08-sm-felulet-specifikacio.md) szerinti felület papíralapú megfelelője: ugyanazokat a beavatkozási pontokat követi. Amíg a felület nem készül el, ez helyettesíti.
>
> **Iteráció:** [sorszám] · **Dátum:** [-tól -ig] · **Scrum Master:** [név]

---

## Az iteráció indulása

### Kapacitás
- [ ] A bírálati keret kiszámítva a **legutóbb mért** paraméterekkel, nem a feltevésekkel
  - `R` = [ ] óra · `t` = [ ] perc · `r` = [ ]
  - Napi kapacitás `(R/t) × 2 / (1+r)` = [ ] elem
  - Iterációs keret = [ ] bírálati esemény
- [ ] A keretből elkülönítve a specifikációs jóváhagyás költsége: [ ] esemény
- [ ] A keretből elkülönítve a biztonsági találatok mérlegelése: [ ] esemény
- [ ] Az előző iterációból átgörgetett elemek betervezve: [ ] elem
- [ ] **A vállalt elemszám nem lépi túl a maradék keretet**

### Készenlét
- [ ] Minden vállalt elem specifikációja jóváhagyva
- [ ] Minden elemhez megvan az ügynök technikai kontextusa *(enélkül az elem nem „Ready")*
- [ ] A visszamérendő szabályok listája összeállítva: mely szabályok kerültek be az előző visszatekintéseken, és melyik hibaosztályt figyeljük

| Szabály | Mikor került be | Melyik hibaosztályt figyeljük |
|---|---|---|
| | | |

---

## Naponta

*(Másold ezt a blokkot az iteráció minden napjára.)*

### [n]. nap

**Eltéréskezelés**
- [ ] Megtörtént, vagy indokoltan elmaradt *(nincs eltérés)*
- [ ] Bukott minőségi kapuk átnézve
- [ ] Döntés megszületett: mit állítunk le, mit engedünk tovább

**Beavatkozási jelzések**

| Jelzés | Fennáll? | Teendő, ha igen |
|---|---|---|
| Torlódás: a bírálati sor eléri a 4-es korlátot | | ügynökök nem indítanak új feladatot |
| Öregedő elem: valami a küszöbnél régebben vár | | soron kívüli bírálat vagy tudatos elengedés |
| **Felügyeleti rés:** beolvadt elem jóváhagyó nélkül | | **azonnali kivizsgálás** |
| Egyenetlen terhelés a két szenior között | | terheléskiegyenlítés |
| Méretkorlát-túllépés | | visszabontás, nem hosszabb bírálat |

**Védett bírálati idősáv**
- [ ] Megtartva, megszakítás nélkül
- [ ] A bírálati sor apadt

---

## Az iteráció zárása

### Az inkrementum
- [ ] **Minden beolvadt elemnek van megnevezett emberi jóváhagyója** *(ha nem, ez a modell alapszabályának sérülése)*
- [ ] Bemutató megtörtént, emberi felelősségvállalással
- [ ] Az iteráció végi ellenőrző próba lefutott: *„Ha most elrontanánk ezt a modult, észrevennénk?"*

### Visszatekintés — gépi réteg *(minden iterációban)*
- [ ] Ismétlődő hibaosztályok összegyűjtve

| Hibaosztály | Előfordulás | Létra foka | Teendő |
|---|---|---|---|
| | | | |

- [ ] **Kötelező kimenet megvan:** legalább egy szabályváltozás, vagy annak leírt indoklása, miért nem kellett
- [ ] A visszamérendő szabályok kiértékelve: melyik fogott, melyik nem

| Szabály | Visszatért a hibaosztály? | Következmény |
|---|---|---|
| | | |

> **Emlékeztető:** ha egy hibaosztály a szabály felvétele után is visszatér, az a létra **3. foka**. Ilyenkor nem a szabályt kell átfogalmazni, hanem **gépi kaput** kell építeni köré. Az utasításfájl puha korlát, a teszt kemény.

### Visszatekintés — emberi réteg *(minden második iterációban)*
- [ ] Megtörtént
- [ ] Kötelező téma: a bírálati terhelés eloszlása és a kimerülés
- [ ] Kötelező téma: a bizalom kalibráltsága — nem lett-e felületesebb a bírálat, mert az ügynökök „általában jók"

### Kalibráció
- [ ] Paraméterek újramérve

| Paraméter | Előző | Mostani | Eltérés |
|---|---|---|---|
| `R` | | | |
| `t` | | | |
| `r` | | | |

- [ ] A következő iteráció vállalása ehhez igazítva
- [ ] Ha az eltérés jelentős: az iterációhossz és a WIP-korlátok felülvizsgálva

---

## Havi vagy háromiterációnkénti ellenőrzés

*(Nem minden iterációban, de rendszeresen.)*

- [ ] **Gumibélyegző-vizsgálat:** volt-e olyan kapu, ahol tartósan nulla az elutasítási arány? *(Ez nem siker, hanem gyanús.)*
- [ ] **Szabályfájl-higiénia:** van-e szabály, amely régóta nem sült el? Törlendő vagy gépi kapuvá alakítandó?
- [ ] **Lazulásgyanú:** csökken a validálási idő **és** nő az elfogadási arány **és** nő a hibaarány? *(Külön-külön egyik sem rossz hír, a három együtt igen.)*
- [ ] **Szerkezeti mutatók:** a duplikációs arány nő, a refaktorálási arány csökken?
- [ ] **Költség:** a keretben vagyunk?
- [ ] **Sikerkritérium és kilépési feltétel** átnézve a csapatindító dokumentumban

---

## Az iteráció egymondatos értékelése

*(A Scrum Master írja, az iteráció zárásakor. Ez a mondat kerül a következő iteráció tervezésének elejére.)*

> [ ]
