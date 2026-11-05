# Definition of Done

> **Használat.** Ez a lista akkor jó, ha minden pontja eldönthető: vagy gépi kimenet felel meg neki, vagy egy megnevezett ember mondja ki. Ha egy pontról vitatkozni kell, hogy teljesült-e, akkor a pont rosszul van megfogalmazva.
>
> A döntések indoklása a [koncepcio/02-minosegi-kapuk.md](../02-minosegi-kapuk.md) dokumentumban található. A DoD módosítása csak a visszatekintésen, a teljes csapat egyetértésével történhet.

---

## Minden elemre

### Funkcionális megfelelés
- [ ] Az elem elfogadási feltételei teljesülnek, és ez a specifikációra visszavezethetően igazolható.
- [ ] A teljes meglévő tesztsorozat lefutott. **A megállapítás forrása a tesztfuttató nyers kimenete, nem az ügynök szöveges összefoglalója.**

### Tesztek
- [ ] Az elem rendelkezik új tesztekkel ott, ahol új viselkedést vezetett be.
- [ ] A teszteket **külön elbírálták** abból a szempontból, hogy mit állítanak, és mikor buknának el. *(Egy teszt, amely az implementáció kimenetét önmagához hasonlítja, nem teszt.)*

### Biztonság
- [ ] A determinisztikus biztonsági kapuk lefutottak: statikus elemzés, függőségi sebezhetőségvizsgálat, titokkeresés, licencellenőrzés.
- [ ] A cáfoló lépcsőt túlélő biztonsági találatok vagy javítva lettek, vagy megnevezett emberi döntéssel elfogadva.

### Méret és felelősség
- [ ] A változtatás mérete nem lépi túl a 200 nettó sort, **vagy** az eltérést külön jóváhagyták.
- [ ] A beolvasztásnak van megnevezett emberi jóváhagyója, és ez a nyom a verziókezelőben marad.

---

## Ha az elem magas kockázatú modult érint

*(hitelesítés, jogosultságkezelés, üzleti szabály, pénzügyi számítás)*

- [ ] A modul mutációs pontszáma nem csökkent a változtatás hatására.
- [ ] Ha a modul most készült el először: az elfogadás után felvettük róla a mutációs alapmérést, és rögzítettük a küszöböt.

> **Fontos megkülönböztetés.** A mutációs pontszám **nem** minőségi kapu az új kódon: ha a kód maga is tartalmazhat hibát, a pontszám nem megbízható jelző, mert a tesztek a hibás viselkedést is védhetik. Regressziós védőhálóként viszont működik — vagyis a már elfogadott modul viselkedésének megőrzésére.

---

## Ha az elem refaktorálás

- [ ] A munka megkezdése **előtt** elkészült a karakterizációs tesztréteg, amely a jelenlegi viselkedést rögzíti.
- [ ] A tesztréteget szenior fejlesztő hagyta jóvá — itt dől el, mit tekintünk megőrzendő viselkedésnek.
- [ ] A karakterizációs tesztek a refaktorálás után változatlanul futnak.

---

## Ha az elem dokumentációt is érint

- [ ] A gépi ellenőrzések lefutottak: séma, kötelező mezők, hivatkozások épsége, a futtatható példák tényleges lefutása.
- [ ] Az ügynök által generált szöveget ember bírálta el. *(A hihetően hangzó, de pontatlan mondatot nehezebb kiszúrni, mint a hibás kódot.)*

---

## Amit ez a lista szándékosan nem tartalmaz

**Nincs lefedettségi küszöb.** A kódlefedettség AI-generált tesztnél nem alkalmas kapunak: vizsgáltak olyan tesztsorozatokat, amelyek 100%-os lefedettség mellett 4%-os mutációs pontszámot értek el. A lefedettséget továbbra is mérjük, de tájékoztató mutatóként, nem célként — mert amit céllá teszünk, azt az ügynök nagyon hatékonyan fogja teljesíteni.

Ha a mérés azt mutatja, hogy a lefedettség a küszöb hiányában érdemben esik, a helyes válasz nem kapu, hanem riasztás.

---

## Az iteráció végi ellenőrző kérdés

A formális lista mellett érdemes minden iterációban lefuttatni egy néhány perces próbát: egy eldobható másolaton elrontunk néhány dolgot az iterációban érintett kódban, és megnézzük, elbukik-e valamelyik teszt.

**„Ha most elrontanánk ezt a modult, észrevennénk?"**

Ha a válasz nem egyértelmű igen, akkor az iteráció nem volt inkrementális, csak iteratív.
