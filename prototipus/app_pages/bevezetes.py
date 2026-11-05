"""„Bevezetés" nézet — mi ez az egész, kinek készült és hogyan kell használni?

A szöveg a lezárt anyag (sm-all.md, koncepcio/, prototipus/README.md) összefoglalója,
új tartalmi állítást nem vezet be. A számok a példaadat konfigurációjából jönnek,
hogy ne csúszhassanak el a kódtól.
"""

from __future__ import annotations

import streamlit as st

from modell import arculat, bemutato, cimkek, fogalmak, hatter
from modell import jelzesek as jelzesek_modul

adatok = st.session_state.adatok
p = st.session_state.pillanat

konfig = adatok.konfig
terv = adatok.iteraciok[0]["parameterek_terv"]
R, t, r = terv["R"], terv["t"], terv["r"]
napi_kapacitas = (R * 60 / t) * 2 / (1 + r)
bir_korlat = konfig["wip_korlatok"]["Bírálatra vár"]
meretkorlat = konfig["meretkorlat_sor"]
napok = adatok.iteraciok[0]["napok"]
jelzesek = jelzesek_modul.kiertekel(adatok, p)


def _dok_gomb(cimke: str, azonosito: str) -> None:
    """Gomb, amely az „Amire épül” megfelelő nézetében megnyitja a megadott dokumentumot."""
    if st.button(cimke, key=f"dok_{azonosito}", icon=":material/menu_book:"):
        st.session_state[f"dok_valasztott_{hatter.nezet(azonosito).oldal}"] = azonosito
        st.switch_page(hatter.oldal_fajl(azonosito))


esemenyek_szama = len(adatok.esemenyek)
elemek_szama = len(adatok.elemek)
iteraciok = adatok.iteraciok

st.html(
    arculat.nyitosav_html(
        "Hogyan vezessünk egy Scrum-csapatot, amelyben AI-ügynökök is fejlesztenek?",
        "Kutatás, működési modell és egy működő prototípus a Scrum Master munkájának támogatására — "
        "egy kitalált, de valósághűen kezelt pilot két iterációján bemutatva.",
        [
            (len(iteraciok), "iteráció"),
            (elemek_szama, "backlog-elem"),
            (esemenyek_szama, "naplózott esemény"),
            (len(jelzesek), "beavatkozási jelzés"),
        ],
    )
)

g1, g2, _ = st.columns([1, 1, 1])
with g1:
    if st.button("Vezetett bemutató (kb. 5 perc)", type="primary", icon=":material/tour:", width="stretch",
                 key="hero_bemutato"):
        st.switch_page("app_pages/bemutato.py")
with g2:
    if st.button("Kipróbálom: Szimuláció", icon=":material/videogame_asset:", width="stretch", key="hero_szim"):
        st.switch_page("app_pages/szimulacio.py")

k1, k2 = st.columns(2)
with k1.container(border=True, key="kartya-1"):
    st.markdown("**:material/help: Mi ez?**")
    st.markdown(
        "Egy AI-first Scrum-csapat működési modellje. Az ügynökök órák alatt kódolnak, a két "
        "szenior bírálata viszont véges: **ez a szűk keresztmetszet**, és minden szabály ebből következik."
    )
with k2.container(border=True, key="kartya-2"):
    st.markdown("**:material/visibility: Mit mutat?**")
    st.markdown(
        "A Scrum Master beavatkozási felületét: mikor, hol és mit kell tennie. Két iteráció "
        f"{elemek_szama} backlog-elemének útja ({esemenyek_szama} naplózott esemény) visszajátszható, "
        "és egy szimulációban ki is próbálható."
    )

st.markdown(
    "**A munka útja** — egy backlog-elem útja a termékigénytől a beolvasztásig, hét lépésben; "
    "ebből kettőnél kötelezően ember áll:"
)
st.html(bemutato.munka_utja_html(bir_korlat))
st.caption(
    "**Az 1–4. lépés előkészít**, az iteráció tervezésekor: a termékigényből specifikáció, abból "
    "több backlog-elem lesz, és ezt a darabolást hagyja jóvá a PO és egy szenior. **Az 5–7. lépést "
    "minden elem külön járja végig**, az iteráció alatt egymással párhuzamosan; ha a bírálat javítást "
    "kér, az elem a 7. lépésből visszamegy az 5.-be. A lánc tehát nem az iteráció köre: egy "
    f"iterációban sok elem halad rajta egyszerre (a példa két iterációjában összesen {elemek_szama})."
)
with st.expander(fogalmak.GEPI_KAPU_CIM, icon=":material/gpp_good:"):
    st.markdown(hatter.linkek(fogalmak.GEPI_KAPU))

st.divider()
st.caption(
    "Részletesen: a fülek sorban válaszolnak a kérdésekre. Ha csak egyet olvasol el, a **Mi a "
    "projekt?** legyen az."
)

projekt, miert, kinek, csapat, modell, mer, hasznalat, hatar = st.tabs(
    [
        "Mi a projekt?",
        "Miért készült?",
        "Kinek szól?",
        "Kik vannak a csapatban?",
        "A modell lényege",
        "Mit mér és mit jelez?",
        "Hogyan használd?",
        "Mi ez, és mi nem",
    ]
)

with projekt:
    st.markdown(
        f"""
A projektnek **két rétege** van, és a félreértések többnyire abból jönnek, hogy a kettőt
összekeverjük.

**1. A kitalált termék: egy vállalati intranet megújítása.** Ezt építené a csapat. Úgy kell
kezelni, mintha külső cég számára készülne, bár ha nem sikerül, nem sérül ügyfél. A példában
két darabot látsz belőle: az első iterációban a **{iteraciok[0]["nev"]}** készül (kereshető
munkatárs-adatlap és szervezeti fa), a másodikban a **{iteraciok[1]["nev"]}**, amely az első
kódjára épül, és ezért át is kell alakítania azt.

**2. A valódi kérdés: hogyan kell egy ilyen csapatot agilisan vezetni?** Ez a projekt tárgya.
A termék csak ürügy: azért kell, hogy a módszert valami konkrét munkán lehessen kipróbálni.
"""
    )

    st.markdown("#### Mit szeretnénk agilisan megvalósítani?")
    st.markdown(
        """
Egy **AI-first Scrum-csapat** működési modelljét: olyan csapatét, amelyben az ügynökök órák
alatt elkészülnek a munkával, az emberek viszont nem. A hagyományos Scrum két pontja nem
marad így:

- **Az iteráció.** Két hét helyett néhány napos kör kell, mert az ügynök gyorsan ír, az
  ember lassabban néz át és javíttat. Az iterációhossz nem előre adott, hanem abból
  vezetjük le, hogy egy teljes kör (feladat → ügynök → bírálat → javítás → beolvasztás)
  beleférjen.
- **A tervezés alapja.** A story pont helyett az számít, mennyit tud a csapat
  *felelősséggel átvenni*, nem mennyit tud megírni.

Az agilitás itt azt jelenti, hogy a modell **feltevésekkel indul, és az első iterációkban
megmérjük**, mi igaz belőlük. Ahol a mérés mást mutat, a modellt módosítjuk, nem a mérést.
"""
    )

    st.markdown("#### Mi a cél?")
    st.markdown(
        """
- **Válaszolni** a briefben feltett kérdésekre: ki darabol (ember vagy ügynök), hogyan
  ne fusson el a sebesség, hogyan legyen biztonságos és tesztelt a kód, mi lesz a Scrum
  eseményeivel, mit mérünk, ki felel, mit kell dokumentálni.
- **Kialakítani egy kipróbálható keretet** ott, ahol a cégvezetés szerint még nincs.
- **Eszközt adni a Scrum Masternek**, amellyel gyorsan látja, hol tart az iteráció és mikor
  kell beavatkoznia (ez a felület).
- **Megmondani, mikor nem működik.** A negatív eredmény is eredmény, ezért előre rögzítettük,
  mikor állítjuk le a pilotot.
"""
    )

    st.markdown("#### Honnan indulunk?")
    st.markdown(
        """
Nincs kész recept. A kutatás szerint az AI-ügynökökkel dolgozó fejlesztőcsapat ma már
létező gyakorlat, de **a keretrendszere nincs kidolgozva**. Amit biztosan tudunk:

- A szűk keresztmetszet az **emberi bírálat**, nem az ügynök sebessége. Az ügynöki
  pull requestek jelentős részét a nyílt forrású világban senki sem nézi át emberként.
- A gépi munka **gyorsabb, de instabilabb**, és a csapat saját önértékelése nem bizonyíték.
- A karbantarthatóság **csendben romlik**, és ez hónapokkal később jelentkezik.
- Három szám, amelyre a modell épül (`R`, `t`, `r`), **nem ismert az irodalomból**, ezeket
  meg kell mérni.
"""
    )

    st.markdown("#### Hova érkezünk?")
    st.markdown(
        f"""
**Ami kész (ez a projekt eddigi eredménye):**

- Lezárt **kutatás**: tematikus dokumentumok, vezetői összefoglaló, forrásjegyzék, glossary.
- Lezárt **koncepció**: kilenc dokumentum és négy használható sablon (csapatindító
  dokumentum, Definition of Done, `AGENTS.md`, iterációs ellenőrzőlista).
- Ez a **prototípus**: két végigvezetett iteráció ({elemek_szama} backlog-elem, {esemenyek_szama}
  naplózott esemény),
  amely azt mutatja meg, hogyan nézne ki a modell a gyakorlatban, és egy szimuláció, ahol
  te vezetsz egy iterációt.

**Ami még nincs kész, és szándékosan nem is ennek a projektnek a dolga:** egy valódi pilot
valódi csapattal. Ott dől el, hogy a feltevések (a bírálati idő, a háromnapos iteráció, a
méretkorlát) valóban igazak-e.

**Mi lenne a siker egy pilotban?** Három iteráció után értékeljük először. Az élesen vizsgált
alapfeltételek: az emberi bírálati arány legalább 95%, nulla beolvadt elem emberi jóváhagyó
nélkül, és nulla éles biztonsági incidens, amit a védelmi lánc átengedett. A többi mutató
(beolvadt elemek száma, első körös elfogadás, visszatérő hibák, szeniorok terhelése, költség)
irányt jelez, és beszélgetést indít, mert három iterációból trendet megállapítani nem lehet.

**Mikor állítjuk le?** Ha az emberi bírálati arány két iteráción át 80% alatt marad, ha éles
biztonsági incidens történik, ha a szeniorok terhelése nő úgy, hogy az átbocsátás nem, ha hat
iteráció után sem stabilizálódnak a paraméterek, vagy ha a költség túllépi a keretet.
"""
    )
    st.markdown("**Részletesen, a felületen olvasva:**")
    _dok_gomb("Sikerkritérium és kilépési feltétel (9. dokumentum)", "koncepcio/09-kockazatok-es-kilepes")
    _dok_gomb("A modell magja (0. dokumentum)", "koncepcio/00-mukodesi-modell")
    _dok_gomb("A kutatás vezetői összefoglalója", "kutatas/00-osszefoglalo")

with miert:
    st.markdown(
        """
Egy közepes méretű magyar vállalat pilot projektet indít: a cég belső weboldalát, az
intranetet kell megújítani, de úgy, mintha külső ügyfélnek készülne. A különlegesség, hogy a
csapat **AI-first**: két szenior fejlesztő dolgozik együtt AI-ügynökökkel, amelyeket ők maguk
írnak meg és hangolnak, és amelyek úgy viselkednek, mint egy junior-medior fejlesztő.

A cégvezetés azt szeretné, hogy a csapat gyorsan és hatékonyan dolgozzon, megelőzve a
versenytársakat, de **ilyen felállásnak még nincs kialakult kerete**. A kérdés tehát nem az,
hogy az ügynökök tudnak-e kódot írni, hanem az, hogy hogyan kell egy csapatot úgy vezetni,
hogy a gyors gép mellett a minőség és a felelősség ne vesszen el.

A munka három lépésben készült, egymásra építve:

1. **Kutatás** — létezik-e már hasonló csapat, milyen mérések és milyen kudarcok ismertek.
2. **Koncepció** — a kutatásból levezetett működési modell: hogyan darabolunk, hogyan
   bírálunk, mit mérünk, ki felel.
3. **Ez a prototípus** — a modell egy működő mintája, hogy lássuk, 1–2 iteráción át hogyan
   nézne ki a gyakorlatban.
"""
    )

with kinek:
    st.markdown(
        """
**Elsősorban a Scrum Masternek.** A hagyományos Scrumban az SM-nek volt ideje mindenre.
Itt az ügynökök órák alatt elkészülnek, ezért gyorsan kell látni, **mikor, hol és mit kell
tenni** — és nagyjából egy iterációval előre is látszania kell, mi következik. Ez a felület
erre való: nem irányítópult tele számokkal, hanem *beavatkozási felület*, amely alapállapotban
azt mondja, hogy nincs teendő, és csak akkor szólal meg, ha konkrét döntést kér.

**Másodsorban annak, aki kívülről nézi.** A táblázatos nézeteket csak az érti, aki a
folyamatban dolgozik. Az Animáció és a Szimuláció azért van, hogy a modell annak is érthető
legyen, aki először látja.

Őszintén: a projekt egyelőre **személyes használatra, kutatási prototípusként** készült, nem
kész termék és nem éles csapat eszköze.
"""
    )

with csapat:
    st.markdown(
        """
**Az emberek:** egy Product Owner (PO), egy Scrum Master (SM) és két szenior fejlesztő.

**Az ügynökök** nem újabb „csapattagok", hanem a két szenior fejlesztő munkaeszközei — ők
írják, hangolják és korlátozzák őket. Ez azért fontos, mert ha az ügynököt csapattagként
számolnánk, a kapacitást is hozzáadnánk, pedig a kapacitás továbbra is két emberé marad.
"""
    )
    st.table(
        {
            "Ügynök": ["Implementáló", "Verifikáló", "Biztonsági kereső", "Biztonsági cáfoló", "Kutató"],
            "Mit csinál": [
                "egy backlog-elemet valósít meg, egyszálúan",
                "futtatja a teszteket, és eldönti, teljesül-e a kilépési feltétel",
                "az iteráció változásait vizsgálja biztonsági szempontból",
                "megtámadja a kereső találatait; csak a túlélő megy ember elé",
                "könyvtárakat, mintákat, dokumentációt keres a specifikációhoz",
            ],
        }
    )
    st.caption(
        "A verifikáló és a cáfoló szándékosan más gyártó modelljére épül, mint az "
        "implementáló: az azonos családon belüli ellenőrzés ugyanazokat a hibákat nézi el."
    )

with modell:
    st.markdown(
        f"""
**Az alapgondolat:** ha a kódírás olcsó, a szűk keresztmetszet átkerül az **emberi
bírálatra**. Ezért a csapat kapacitását nem az határozza meg, mennyit tudnak az ügynökök
megírni, hanem az, hogy a szeniorok mennyit tudnak **felelősséggel átvenni**. Ezt a mennyiséget
*bírálati keretnek* hívjuk, és ez váltja fel a story pontot.

Három számból áll ki: a szenior napi bírálati ideje (`R` = {R:g} óra), egy elem érdemi
átnézésének ideje (`t` = {t:g} perc) és az átlagos plusz javítási körök (`r` = {r:g}). Ezekkel a
csapat naponta nagyjából **{cimkek.szam(napi_kapacitas)} elemet** tud lezárni — ebből következik minden
más szabály:

- **Kemény korlát a bírálati soron:** legfeljebb {bir_korlat} elem várhat bírálatra. Ha betelt,
  az ügynökök nem kezdenek újat, a csapat a meglévők lezárására áll rá.
- **Méretkorlát:** egy bírálatra beadott változtatás legfeljebb {meretkorlat} sor. Ami nagyobb,
  azt szét kell bontani, nem hosszabban nézni.
- **Rövid iteráció:** kiinduló hipotézis a {napok} napos iteráció.
- **Mindennek van emberi felelőse:** nincs beolvasztás megnevezett emberi jóváhagyó nélkül.
"""
    )
    st.warning(
        "A fenti számok **saját feltevések**, nem bizonyított tények: a kutatás nem talált "
        "mérést sem a bírálati kapacitásra, sem az iterációhosszra. A pilot első két "
        "iterációja arra való, hogy ezeket megmérje.",
        icon=":material/science:",
    )

with mer:
    st.markdown(
        """
**Amit a felület figyel:** kilenc beavatkozási jelzés. Mindegyikhez tartozik egy teendő, de
a teendőt **ember hajtja végre** — a felület nem állítja le az ügynököket, csak megmondja,
hogy le kell állítani. Ez tudatos: a pilot egyik célja megfigyelni, mikor lépné át a csapat a
saját szabályait.
"""
    )
    for j in jelzesek:
        st.markdown(f"- **{j.kod} · {j.cim}**")
    st.markdown(
        """
**Amit megtartunk** a hagyományos mérésből: a szállítási teljesítmény mutatói (DORA).
**Amit elengedünk:** a story pontot és a velocityt (ügynöki munkára félrevezetők), valamint a
lefedettségi küszöböt. **Amit nem mérünk:** az egyes emberek teljesítményét — a bírálók
megjelenítése csak a terheléseloszlás követésére szolgál.
"""
    )

with hasznalat:
    st.markdown(
        """
A menü négy csoportból áll. Ajánlott útvonal, ha először jársz itt:

1. **Kezdés → Vezetett bemutató** — a példa két iterációja hat rövid fejezetben: darabolás,
   torlódás, paramétereltérés, méretkorlát, visszatérő hibaosztály. Minden fejezetből egy
   gombbal átléphetsz a részletes nézetre, ugyanarra a pillanatra.
2. **Lejátszás és gyakorlás → Animáció** — ugyanez mozgó ábrán: látszik, hogy az ügynökök
   gyorsan termelnek, az emberi bírálat lassan fogyaszt, és a sor korlátos.
3. **A példa — két iteráció** — a Scrum Master munkafelülete:
   - **Teendők**: mi igényel beavatkozást a kurzor pillanatában, konkrét teendővel;
   - **Iteráció**: a keret, a vállalás és az ellenőrzőlista;
   - **Előretekintés**: a mért paraméterekből számolt következő keret;
   - **Tanulás**: a hibaosztályok, a szabályfájl és az eszkalációs létra;
   - **Backlog**: hogyan lett a munka darabolva — elemenként cél, elfogadási feltételek (AC),
     becslés, kész-a-kezdésre (DoR) és kész-a-lezáráshoz (DoD).

   A Teendők, az Iteráció, az Előretekintés és a Tanulás egy pillanat állapotát mutatja: a bal oldali
   **Időkurzor** a példa elejéről indul: léptesd előre eseményenként, vagy ugorj bármely
   pillanatra; a **könyvjelzők** a tanulságos pillanatokra visznek. A Backlog elemgyűjtő, ezért ott nincs idővonal: mindig a teljes
   darabolást mutatja.
4. **Lejátszás és gyakorlás → Szimuláció** — itt te vezetsz egy iterációt: te döntöd el, mennyit
   vállalsz, beolvasztasz vagy visszaküldesz, leállítod-e az ügynököket. A végén a mérleg
   szembesít: a felületes bírálat szebb mérőszámokat termel, miközben több súlyos hiba megy át.
   Az iterációk láncolhatók, így a visszatekintési döntésed következménye is látszik.
5. **Amire épül** — a projekt alapjai, csoportonként külön: a **Kiindulás** (az eredeti brief), a
   **Kutatás** (a bizonyíték, a forrásjegyzék és a glossary), a **Koncepció** (a működési modell és
   a sablonok) és a **Spike-ok** (a lezárt anyag mellé készült fejlesztési ötletek).
"""
    )

with hatar:
    st.markdown(
        """
- **Kitalált példa.** Az adatok egy kétiterációs, kézzel szerkeszthető minta, nem valódi csapat
  mérései. A Szimuláció a modell feltevéseivel számol, nem a valósággal.
- **Olvasható demó.** Nincs bejelentkezés, adatbázis, szerkesztés vagy integráció.
- **Nem avatkozik be.** Jelez, de a döntés mindig emberé.
- **A háttéranyag** az **Amire épül** menü nézeteiben végig olvasható: az eredeti brief, a
  kutatás, a forrásjegyzék, a glossary, a koncepció, a sablonok és a spike-ok. A számok mögötti
  bizonyítékokat és a „saját döntés, bizonyíték nélkül" tételeket a koncepció áttekintője
  különíti el.
"""
    )
    _dok_gomb("A koncepció áttekintője", "koncepcio/README")
    _dok_gomb("Forrásjegyzék (az S-nn hivatkozások feloldása)", "kutatas/forrasok")
    _dok_gomb("Glossary — az idegen kifejezések magyarázata", "kutatas/glossary")
    st.markdown(
        "**Fejlesztési ötletek (spike-ok).** A lezárt anyag mellé készült, friss kutatásra épülő "
        "összehasonlítások — például hogy mit hozna egy ügynök, egy orkesztrátor, vagy skillek és MCP-toolok "
        "a mostani ügynökpark helyett."
    )
    _dok_gomb("Spike 01 — Ügynök-architektúra: egy ügynök, orkesztrátor, skillek, MCP",
              "spike/01-ugynok-architektura/README")
