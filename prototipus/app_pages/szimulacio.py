"""„Szimuláció" nézet — egy iteráció végigjátszása emberi jóváhagyással.

A négy táblázatos nézet megmutatja a modellt, az animáció megmutatja a
működését. Ez a nézet **gyakoroltatja**: a modell két emberi kapujánál megáll és
döntést kér, a következményeket pedig ugyanaz a kilenc jelzés és ugyanaz a
mérőszámkészlet mutatja meg, mint a valódi iterációnál.

Az iterációk láncolhatók. Ez nem kényelmi funkció: a visszatekintési döntés
következménye — hogy a hibaosztály eltűnik-e — egyetlen iterációból nem
figyelhető meg.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from modell import allapot as allapot_modul
from modell import cimkek
from modell import fogalmak, hatter
from modell import grafikonok, kapacitas
from modell import jelenet
from modell import jelzesek as jelzesek_modul
from modell import szimulacio as szim

KULCS = "szimulacio_allas"

# Védelem a `modell.szimulacio` élesben elavult, gyorsítótárazott verziója
# ellen: ez az oldal-szkript minden Streamlit-futtatáskor frissen fut le a
# lemezről, de az importált modult Python a folyamat indulása óta a
# memóriában tartja — kódfrissítés a lemezen ezt nem frissíti, csak egy
# teljes folyamat-újraindítás. A `getattr` alapértéke az eredeti, e
# munkamenet előtti viselkedést adja vissza, amíg az élesítés meg nem
# történik. Lásd `docs/HANDOFF.md` — 2026-09-16, AttributeError incidens.
_ALLAPOT_ERVENYES = getattr(szim, "allapot_ervenyes", lambda _allas: True)
_SULYOS_MAGYARAZAT = getattr(
    szim, "SULYOS_MAGYARAZAT", "hibás vagy adatot kiszivárogtató kód kerülne a termékbe"
)
_ENYHE_MAGYARAZAT = getattr(
    szim, "ENYHE_MAGYARAZAT", "a folyamat, a tesztelés vagy a használhatóság minőségét rontja"
)
_HIBAOSZTALY_LEIRO = getattr(
    szim, "hibaosztaly_leiro",
    lambda kod: {"kod": kod, "nev": "ismeretlen hibaosztály", "kategoria": "—", "sulyos": False},
)


def _indul() -> None:
    st.subheader("Új iteráció indítása")
    st.markdown(
        "A szimuláció a példa két iterációja **után** következő, harmadik iterációt "
        "játssza le. A tanulási hurok nem nulláról indul: a szabályfájlban (az ügynököknek "
        "szóló utasításfájlban) már benne van a példa első visszatekintésén született két "
        "szabály, egy-egy ismétlődő hibaosztályra:"
    )
    # Az örökölt szabályokat a motor indítása adja, hogy a szöveg ne csúszhasson el tőle.
    for sor in szim.indit(mag=1).szabaly_sorok:
        ho = _HIBAOSZTALY_LEIRO(sor["hibaosztaly"])
        st.markdown(f"- **{sor['kod']}** — {sor['cim']} _(hibaosztály: {ho['kod']} · {ho['nev']})_")
    st.markdown(
        "A szabály puha korlát: a hibaosztály ettől még visszatérhet. Az iteráció végén, a "
        "visszatekintésen te döntöd el, hogy egy ismétlődő hibára szabályt, gépi kaput vagy semmit "
        "nem hozol. Ennek a döntésnek a hatása csak a **következő** iterációban látszik meg, ezért "
        "a lezárás után érdemes a lánccal folytatni."
    )
    with st.expander(fogalmak.GEPI_KAPU_CIM, icon=":material/gpp_good:"):
        st.markdown(hatter.linkek(fogalmak.GEPI_KAPU))

    st.warning(
        "**Ezek a paraméterek feltevések, nem mérések.** A koncepció kifejezetten saját "
        "tervezési döntésként jelöli meg őket, bizonyíték nélkül. A szimuláció ezekkel "
        "számol, tehát az eredménye a modell feltevéseiről szól, nem a valóságról.",
        icon=":material/warning:",
    )

    bal, kozep, jobb = st.columns(3)
    with bal:
        R = st.number_input("Napi bírálati idő szeniorra (`R`, óra)", 0.5, 8.0,
                            szim.ALAP_PARAMETEREK["R"], 0.25)
    with kozep:
        t = st.number_input("Egy elem érdemi átnézése (`t`, perc)", 15.0, 240.0,
                            szim.ALAP_PARAMETEREK["t"], 5.0)
    with jobb:
        r = st.number_input("Átlagos plusz javítási körök (`r`)", 0.0, 3.0,
                            szim.ALAP_PARAMETEREK["r"], 0.05)

    bal2, jobb2 = st.columns(2)
    with bal2:
        napok = st.number_input("Az iteráció hossza (nap)", 1, 10, 3)
    with jobb2:
        mag = st.number_input(
            "Forgatókönyv-szám — ugyanaz a szám ugyanazt a sorsolást adja (angolul: seed)",
            1, 9999, 11,
            help=(
                "A véletlen részt rögzíti: a backlog sorrendjét és az ügynök szerencséjét, "
                "a te döntéseidet nem. Más szám más történet; ugyanaz a szám más döntésekkel attól "
                "a ponttól válik szét, ahol eltérsz. Ugyanaz a szám és ugyanazok a döntések "
                "ugyanazt a történetet adják."
            ),
        )

    if st.button("Iteráció indítása", type="primary", width="stretch"):
        st.session_state[KULCS] = szim.indit(
            mag=int(mag), napok=int(napok), parameterek={"R": R, "t": t, "r": r}
        )
        st.rerun()


def _dontes_kartya(allas: szim.Allas) -> None:
    d = allas.dontes
    assert d is not None

    # A döntés nem hiba: csak a szabályt érintő helyzet (torlódás, túl nagy csomag) figyelmeztet.
    fejlec = st.warning if d.kod in ("torlodas", "meretkorlat") else st.info
    fejlec(f"**Döntés: {d.cim}**", icon=":material/pan_tool:")
    with st.container(border=True):
        st.markdown(d.magyarazat)

        if d.kod == "beolvasztas":
            t = d.tenyek
            sulyos = t.sulyos
            hibaosztalyok = t.hibaosztalyok
            oszlopok = st.columns(4)
            oszlopok[0].metric("Méret", f"{t.meret_sor} sor")
            oszlopok[1].metric("Bírálat", f"{t.perc} perc")
            oszlopok[2].metric("Kör", t.korok + 1)
            # A darabszám önmagában nem mond semmit arról, hogy baj van-e.
            oszlopok[3].metric(
                "Megtalált hiba", len(t.talalt),
                delta=f"{len(sulyos)} súlyos" if sulyos else None,
                delta_color="inverse",
            )
            if hibaosztalyok:
                st.markdown("**A bírálat ezeket találta:**")
                for ho in hibaosztalyok:
                    jelzes = (":red-badge[súlyos]" if ho["sulyos"]
                              else ":gray-badge[enyhébb]")
                    st.markdown(
                        f"{jelzes} **{ho['kod']} — {ho['nev']}** · _{cimkek.kategoria(ho['kategoria'])}_"
                    )
                st.caption(
                    "Mind a hat hibaosztály katalógusa és az eszkalációs létra a "
                    "**Tanulás** nézetben van — ott a példa adatain, nem ezen a futamon."
                )

        st.divider()
        gombok = st.columns(len(d.valasztasok))
        for oszlop, v in zip(gombok, d.valasztasok):
            with oszlop:
                if st.button(v.cimke, key=f"v_{d.kod}_{d.elem_id}_{v.kod}", width="stretch"):
                    st.session_state[KULCS] = szim.dont(allas, v.kod)
                    st.rerun()
                st.caption(v.kovetkezmeny)


def _allapot_panel(allas: szim.Allas) -> None:
    adatok = szim.adatok(allas)
    if adatok.esemenyek.empty:
        return
    p = allapot_modul.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok,
                               len(adatok.esemenyek) - 1)

    nap = (allas.most.normalize() - allas.kezdet.normalize()).days + 1
    sajat = p.elemallapot[p.elemallapot["iteracio"] == allas.iteracio_id]
    beolvadt = int((sajat["allapot"] == "Beolvadt").sum())
    vallalt = max(int(allas.vallalas), 1)
    st.progress(
        min(beolvadt / vallalt, 1.0),
        text=(f"Szimulált idő: **{allas.most:%Y-%m-%d %H:%M}** · {min(nap, allas.napok)}. nap a "
              f"{allas.napok}-ból · beolvadt: **{beolvadt} / {allas.vallalas}** vállalt elem"),
    )

    korlatok = allas.konfig["wip_korlatok"]
    st.html(grafikonok.tabla_html(p.elemallapot, korlatok, allas.konfig["meretkorlat_sor"]))
    if allas.vallalas:
        pr = allas.parameterek
        keret = kapacitas.szamol(pr["R"], pr["t"], pr["r"], allas.napok).elem_per_iteracio
        st.html(grafikonok.keret_sav_html(allas.vallalas, keret, "elem vállalva", "bírálati keret"))

    aktivak = [j for j in jelzesek_modul.kiertekel(adatok, p) if j.aktiv]
    if aktivak:
        for j in aktivak:
            doboz = st.error if j.sulyossag == jelzesek_modul.KRITIKUS else st.warning
            doboz(f"**{j.cim}** — {j.uzenet}  \n:material/arrow_forward: {j.teendo}")


def _lanc_panel(allas: szim.Allas) -> None:
    """Az eddigi iterációk egymás mellett. Két iterációtól van értelme."""
    merlegek = allas.lezart_merlegek
    if len(merlegek) < 2:
        return

    st.markdown("#### Az iterációk egymás mellett")
    st.dataframe(
        [
            {
                "Iteráció": m["iteracio"],
                "Vállalt": m["vallalt"],
                "Áthozott": m["athozott"],
                "Beolvadt": m["beolvadt"],
                "Átcsúszott": m["atcsuszott"],
                "Súlyos szökevény": sum(len(h) for _, h in m["sulyos_szokevenyek"]),
                "Szabályszegés": len(m["szegesek"]),
                "Mért t (perc)": m["mert"]["t"],
                "Mért r": m["mert"]["r"],
            }
            for m in merlegek
        ],
        hide_index=True, width="stretch",
    )
    st.caption(
        "A következő iteráció kerete a **mért** paraméterekből számol, nem a kiinduló "
        "feltevésből — ez a modell visszacsatolása. A **súlyos szökevény** oszlop azt "
        f"számolja, hány olyan hiba maradt a beolvadt kódban, amelynél "
        f"{_SULYOS_MAGYARAZAT}."
    )


def _tanulasi_hurok_panel(allas: szim.Allas) -> None:
    """A lánc bizonyítéka: eltűnt-e a hibaosztály a beavatkozás után."""
    hurok = szim.tanulasi_hurok(allas)
    if not hurok:
        return

    st.markdown("#### A tanulási hurok")
    st.caption(
        hatter.linkek(
            "A koncepció szerint nem az ügynök ígérete a bizonyíték arra, hogy a hurok "
            "zárul, hanem az, hogy a hibaosztály **eltűnik** (S-26). Ezért nem elég egy "
            "iteráció: a beavatkozás hatása a következőben mérhető."
        )
    )

    iteraciok = sorted({azon for s in hurok for azon in s["iteraciok"]})
    sorok = []
    for s in hurok:
        sor = {"Hibaosztály": s["hibaosztaly"]}
        for azon in iteraciok:
            sor[f"{azon}. it."] = s["iteraciok"].get(azon, 0)
        sor["Beavatkozás"] = (
            f"{s['beavatkozas']} — {s['beavatkozas_kod']} "
            f"({s['beavatkozas_iteracio']}. it.)"
            if s["beavatkozas_kod"] else "—"
        )
        sor["Eredmény"] = (
            "eltűnt" if s["eltunt"] else "visszatért" if s["visszatert"] else "—"
        )
        sorok.append(sor)
    st.dataframe(sorok, hide_index=True, width="stretch")

    eltunt = [s["hibaosztaly"] for s in hurok if s["eltunt"]]
    visszatert = [s["hibaosztaly"] for s in hurok if s["visszatert"]]
    if eltunt:
        st.success(
            "A beavatkozás után eltűnt: " + ", ".join(f"`{h}`" for h in eltunt)
            + ". Ez a tanulási hurok bizonyítéka.",
            icon=":material/trending_down:",
        )
    if visszatert:
        st.warning(
            "A beavatkozás ellenére visszatért: " + ", ".join(f"`{h}`" for h in visszatert)
            + ". A szabályfájl puha korlát — a determinisztikus teszt a kemény.",
            icon=":material/replay:",
        )
    if len(allas.lezart_iteraciok) < 2:
        st.info(
            "Egyetlen lezárt iteráció után még nincs mihez viszonyítani. Indítsd el a "
            "következő iterációt, és itt fog látszani, hatott-e a döntésed.",
            icon=":material/info:",
        )


def _kovetkezo_iteracio_gomb(allas: szim.Allas) -> None:
    """A lánc folytatása. Akkor van értelme, ha van még mit vállalni."""
    van_munka = bool(allas.keszlet) or bool(
        [e for e in allas.elemek.values() if e.allapot == "Átcsúszott"]
    )
    if not van_munka:
        st.info(
            "A backlog elfogyott, és nem maradt átcsúszott elem — a lánc itt véget ér.",
            icon=":material/inventory:",
        )
        return

    bal, jobb = st.columns([2, 3])
    with bal:
        if st.button(f"A {allas.iteracio_id + 1}. iteráció indítása",
                     type="primary", width="stretch"):
            st.session_state[KULCS] = szim.kovetkezo_iteracio(allas)
            st.rerun()
    with jobb:
        st.caption(
            "Átmegy: a szabályfájl, a gépi kapuk, az eseménynapló és az át nem adott "
            "munka. A következő keretet már a mért paraméterek adják, nem a feltevés."
        )


def _szokeveny_lista(parok: list) -> None:
    """Elemenként, nevesítve: melyik hibaosztály maradt bent."""
    for eid, hibak in parok:
        nevek = ", ".join(f"`{h}` {_HIBAOSZTALY_LEIRO(h)['nev']}" for h in hibak)
        st.markdown(f"- **{eid}** — {nevek}")


def _szokeveny_magyarazat() -> None:
    """A „szökevény" szakszó feloldása.

    Nem elég annyi, hogy „átjutott a bírálaton": a beolvadt kódban az a hiba is
    bent marad, amit a bírálat **észre sem vett**. A kettő nem ugyanaz, és a
    modell mondanivalója éppen a különbségen áll.
    """
    st.caption(
        "**Szökevény hiba** = benne maradt a beolvadt kódban. Kétféleképpen "
        "kerülhetett oda: vagy a bírálat nem vette észre, vagy megtalálta, de "
        "mégis beolvasztottad — az utóbbi a fenti szabályszegések közt is "
        "szerepel. A szimulációban ez már nem javítható; a következő iteráció "
        "visszatekintésén lehet rá szabályt vagy gépi kaput építeni."
    )


def _merleg_panel(allas: szim.Allas) -> None:
    m = szim.merleg(allas)
    st.subheader(f"A(z) {m['iteracio']}. iteráció mérlege")

    van_beolvasztas = m["beolvadt"] > 0
    oszlopok = st.columns(5)
    oszlopok[0].metric("Vállalt", m["vallalt"])
    oszlopok[1].metric("Áthozott", m["athozott"])
    oszlopok[2].metric("Beolvadt", m["beolvadt"])
    oszlopok[3].metric("Átcsúszott", m["atcsuszott"])
    # Beolvasztás nélkül az arány nem nulla, hanem értelmezhetetlen — a kettő
    # összekeverése azt sugallná, hogy elmaradt az emberi felügyelet.
    oszlopok[4].metric(
        "Emberi bírálati arány",
        f"{m['emberi_biralati_arany']:.0%}" if van_beolvasztas else "—",
    )

    st.markdown("#### A paraméterek a mérés után")
    terv, mert = m["terv"], m["mert"]
    st.dataframe(
        [
            {"Paraméter": "Napi bírálati idő (R)", "Terv": terv["R"], "Mért": mert["R"]},
            {"Paraméter": "Validálási idő (t)", "Terv": terv["t"], "Mért": mert["t"]},
            {"Paraméter": "Javítási körök (r)", "Terv": terv["r"], "Mért": mert["r"]},
        ],
        hide_index=True, width="stretch",
    )
    if m["mert"]["biralatok"]:
        st.altair_chart(grafikonok.parameter_elteres_grafikon(terv, mert), width="stretch")
        st.caption(
            f"A mért értékekből a következő iteráció kerete **{m['kovetkezo_keret']} elem** volna. "
            f"Első körös elfogadási arány: {m['elso_koros_elfogadas']['arany']:.0%}."
        )
    else:
        st.caption("Nem zárult le bírálat, amiből mérni lehetne — a mért oszlop üres.")

    sulyos = m["sulyos_szokevenyek"]
    if not van_beolvasztas:
        st.info(
            "Nem olvadt be egyetlen elem sem, tehát nincs mit megvizsgálni "
            "szökevény hiba szempontjából.",
            icon=":material/info:",
        )
    elif sulyos:
        st.error(
            "**Súlyos szökevény hiba maradt a beolvadt kódban** — olyan, amelynél "
            f"{_SULYOS_MAGYARAZAT}:",
            icon=":material/bug_report:",
        )
        _szokeveny_lista(sulyos)
        _szokeveny_magyarazat()
    elif m["szokevenyek"]:
        st.warning(
            "**Enyhébb szökevény hibák maradtak a beolvadt kódban** — ezek nem a "
            f"terméket rontják el, hanem {_ENYHE_MAGYARAZAT}:"
        )
        _szokeveny_lista(m["szokevenyek"])
        _szokeveny_magyarazat()
    else:
        st.success("Nem maradt ismert hiba a beolvadt kódban.")

    if m["szegesek"]:
        st.markdown("#### Amit a saját szabályaidból átléptél")
        for s in m["szegesek"]:
            st.markdown(f"- {s}")
    else:
        st.success("A modell szabályait végig betartottad.")

    if m["megjegyzesek"]:
        st.markdown("#### Amit a számokról tudni kell")
        for mj in m["megjegyzesek"]:
            st.info(mj)

    with st.expander("A döntéseid sorrendben"):
        for sor in m["naplo"]:
            st.markdown(f"- {sor}")

    # Szándékosan kapcsoló és nem `st.expander`: az expander tartalma akkor is
    # felépül, ha csukva van. A forgatókönyv minden eseményindexre kiszámolja a
    # tábla állapotát, ezért a költsége az eseményszám négyzetével nő — egy
    # háromiterációs láncnál ez mérve 14 másodperc, és minden kattintás után
    # újra lefutna.
    if st.toggle("A lánc lejátszása animáción", key="szim_animacio"):
        st.caption(
            "Ugyanaz a színpad, mint az Animáció nézetben — a megjelenítő "
            "eseményfolyamot fogyaszt, tehát mindegy neki, hogy a példából vagy "
            "ebből a szimulációból jön. Hosszú láncnál a felépítése tíz másodperc "
            "fölött is lehet."
        )
        with st.spinner("A forgatókönyv felépítése…"):
            html = cimkek.animacio_cimkekkel(jelenet.oldal(szim.adatok(allas)))
        components.html(html, height=880, scrolling=True)


# --- Az oldal --------------------------------------------------------------------

allas: szim.Allas | None = st.session_state.get(KULCS)

if allas is not None and not _ALLAPOT_ERVENYES(allas):
    # A munkamenet egy korábbi kódverzióból származó `Allas`-t tart — ez élő,
    # folyamatosan futó szolgáltatás mellett valós helyzet: a felhasználó
    # böngészőlapja nyitva marad egy kódfrissítés alatt is. A régi állapot
    # olvasása helyenként hiányzó kulcshoz (`KeyError`) vezetne, ezért inkább
    # eldobjuk, és szólunk, ahelyett hogy elszállna az oldal.
    del st.session_state[KULCS]
    allas = None
    st.info(
        "A szimuláció belső formátuma frissült a munkameneted indulása óta, "
        "ezért a korábbi állását nem lehet folytatni. Indíthatsz egy újat.",
        icon=":material/info:",
    )

if allas is None:
    _indul()
else:
    fejlec, gomb = st.columns([4, 1])
    with fejlec:
        lezart = len(allas.lezart_iteraciok)
        st.caption(
            f"**{allas.iteracio_id}. iteráció**"
            + (f" · {lezart} lezárt iteráció a láncban" if lezart else "")
            + " — a modell két emberi kapuja nem automatizálható: a darabolás "
            "jóváhagyása és a beolvasztás. A felelősség ott keletkezik, ezért ott áll "
            "meg a szimuláció."
        )
    with gomb:
        if st.button("Újrakezdés", width="stretch"):
            del st.session_state[KULCS]
            st.rerun()

    if allas.dontes is not None:
        _dontes_kartya(allas)
        st.divider()
        _allapot_panel(allas)
    elif allas.kesz:
        _merleg_panel(allas)
        st.divider()
        _lanc_panel(allas)
        _tanulasi_hurok_panel(allas)
        st.divider()
        _kovetkezo_iteracio_gomb(allas)
    else:
        st.info("A szimuláció fut…")
