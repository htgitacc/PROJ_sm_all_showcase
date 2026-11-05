"""„Backlog” nézet — hogyan lett darabolva a munka, és mit tudunk előre egy-egy elemről?"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modell import backlog as bl
from modell import cimkek
from modell import szimulacio as szim

adatok = st.session_state.adatok
meretkorlat = adatok.konfig["meretkorlat_sor"]
LEIRASOK = bl.leirasok()
KESZLET_MERETE = len(bl.szimulacios_keszlet())
PELDA_ELEMEI = len(adatok.elemek)
PELDA_ESEMENYEI = len(adatok.esemenyek)

st.caption(
    "A darabolás eredménye egy helyen: mi az elem célja, mikor tekinthető késznek, mi kell a "
    "kezdéséhez (DoR), és mi kell a lezárásához (DoD). "
    "**A célok és az elfogadási feltételek kitalált mintaszövegek**: a példaadat többi része "
    "(méretek, események) rögzített, a szöveg nem. A **[PO: …]** jelölésű számok és döntések "
    "feltevések: valódi pilotban a Product Owner (vagy a HR, a jogi funkció) adja meg őket."
)

JEL = {"igen": ":material/check_circle:", "nem": ":material/cancel:", "nyitott": ":material/help:"}


def _dor(pontok: list[bl.DorPont]) -> None:
    st.markdown("**Kész a kezdésre? (DoR)**")
    for p in pontok:
        extra = f" — _{p.megjegyzes}_" if p.megjegyzes else ""
        st.markdown(f"{JEL[p.allapot]} {p.szoveg}{extra}")
    st.caption(
        "A koncepciónak nincs külön DoR-dokumentuma: ezek a darabolás jóváhagyási kapujának "
        "szempontjai (01. dokumentum), elemenként kiértékelve."
    )


def _dod(magas: bool, refakt: bool) -> None:
    st.markdown("**Kész a lezáráshoz? (DoD)**")
    for blokk in bl.dod(magas, refakt):
        with st.expander(blokk.cim + ("  ·  erre az elemre vonatkozik" if blokk.feltetel else "")):
            for pont in blokk.pontok:
                st.markdown(f":material/check_box_outline_blank: {pont}")
    mit = []
    if magas:
        mit.append("magas kockázatú modult érint")
    if refakt:
        mit.append("refaktorálás")
    st.caption(
        "A Definition of Done a koncepció sablonjából jön."
        + (f" Ennél az elemnél a feltételes szakaszok is érvényesek: {', '.join(mit)}." if mit else "")
    )


def _fejlec(elem_id: str, cim: str, cel: str) -> None:
    st.markdown(f"### {elem_id + ' · ' if elem_id else ''}{cim}")
    st.write(cel)


def _ac(leiras: dict) -> None:
    st.markdown("**Elfogadási feltételek (AC)**")
    for sor in leiras["elfogadasi_feltetelek"]:
        st.markdown(f"- {sor}")
    if leiras.get("megjegyzes"):
        st.info(leiras["megjegyzes"], icon=":material/sticky_note_2:")


tab_szim, tab_pelda = st.tabs(["A szimuláció készlete", "A példa elemei"])

# --- A szimuláció készlete -------------------------------------------------------

with tab_szim:
    futo = st.session_state.get("szimulacio_allas")
    alap_mag = int(getattr(futo, "mag", 11)) if futo is not None else 11

    st.markdown(
        f"A szimuláció **{KESZLET_MERETE} elemes készletből** vállal. Ez a szimuláció saját készlete, nem "
        f"a példa elemei: a példa két iterációja {PELDA_ELEMEI} elemmel dolgozott (*A példa elemei* fül). "
        "A készlet sorrendjét a **forgatókönyv-szám** "
        "dönti el (ugyanaz a szám ugyanazt a sorrendet adja), ezért a vállaláskor már látszik, mi következik. "
        "Az elemek méretét viszont a szimuláció a megvalósításkor sorsolja a bonyolultságból, ezért az "
        "előre nem ismert."
    )
    with st.expander("Mi a forgatókönyv-szám, és hogyan lesz belőle több változat?"):
        st.markdown(
            """**A forgatókönyv-szám a véletlen részt rögzíti, a te döntéseidet nem.** Két dolgot dönt el:

- **A backlog sorrendjét.** Ez a szimuláció legelején dől el, még a te döntéseid előtt.
- **A szerencsét.** Mennyi ideig dolgozik az ügynök, mekkora lesz a változtatás, milyen rejtett hibák kerülnek bele, és észreveszi-e őket a bírálat.

**Hogyan lesz több változat?**

1. *Más számot adsz meg:* más sorrend és más szerencse, tehát egészen más történet.
2. *Ugyanazt a számot adod meg, de máshogy döntesz:* a sorrend és az első elemek ugyanazok, de a véletlen sorban fogy, ezért attól a ponttól, ahol eltérsz, a történet szétválik.

Ugyanaz a szám és ugyanazok a döntések mindig ugyanazt a történetet adják. A láncban a következő iteráció ugyanazon a számon megy tovább."""
        )
    mag = st.number_input(
        "Forgatókönyv-szám",
        1,
        9999,
        alap_mag,
        help=(
            "A szimuláció indításánál megadott szám (angolul: seed, véletlenmag). Futó szimulációnál "
            "annak száma az alapértelmezés."
        ),
    )

    kiosztott_sorrend = [str(r["cim"]) for r in szim.indit(mag=int(mag)).keszlet]
    meg_varo = None
    if futo is not None and int(getattr(futo, "mag", -1)) == int(mag):
        meg_varo = {str(r["cim"]) for r in getattr(futo, "keszlet", [])}

    keszlet = bl.szimulacios_keszlet().set_index("cim")
    leir = LEIRASOK["szimulacio"]
    sorok = []
    for i, cim in enumerate(kiosztott_sorrend, start=1):
        r = keszlet.loc[cim]
        allapot = "" if meg_varo is None else ("vár" if cim in meg_varo else "kiosztva")
        sorok.append(
            {
                "Sorrend": i,
                "Elem": cim,
                "Magas kockázat": r["magas_kockazat"],
                "Bonyolultság": int(r["bonyolultsag"]),
                "AC": len(leir[cim]["elfogadasi_feltetelek"]),
                **({"Állapot": allapot} if meg_varo is not None else {}),
            }
        )
    tabla = pd.DataFrame(sorok)

    c1, c2, c3 = st.columns(3)
    c1.metric("Elemek a készletben", len(tabla))
    c2.metric("Magas kockázatú", int((tabla["Magas kockázat"] == "igen").sum()))
    c3.metric("Átlagos bonyolultság", cimkek.szam(tabla["Bonyolultság"].mean()))
    st.dataframe(tabla, hide_index=True, width="stretch")
    if meg_varo is not None:
        st.caption("Az Állapot oszlop a futó szimulációból jön.")

    valasztott = st.selectbox(
        "Elem részletei",
        kiosztott_sorrend,
        format_func=lambda c: f"{kiosztott_sorrend.index(c) + 1}. {c}",
        key="backlog_szim_elem",
    )
    r = keszlet.loc[valasztott]
    magas = r["magas_kockazat"] == "igen"
    refakt = bl.refaktoralas_e(valasztott)
    d = leir[valasztott]

    st.divider()
    bal, jobb = st.columns(2)
    with bal:
        _fejlec("", valasztott, d["cel"])
        _ac(d)
        st.markdown("**Becslés**")
        st.markdown(
            f"Bonyolultság: **{int(r['bonyolultsag'])}** (1–3). Ez a szimuláció nehézségi paramétere, "
            "**nem story point**: ebből sorsolódik a megvalósítás ideje, a változtatás mérete és a "
            "hibaesély. A koncepció az ügynöki munkára elveti a story pontot."
        )
        st.markdown(f"Várható méret: **nem ismert előre** (a korlát {meretkorlat} sor).")
    with jobb:
        _dor(bl.dor(len(d["elfogadasi_feltetelek"]), None, meretkorlat, None))
        _dod(magas, refakt)

# --- A példa elemei --------------------------------------------------------------

with tab_pelda:
    st.markdown(
        f"A példa két lezárt iterációjának **{PELDA_ELEMEI} eleme**, a rögzített mérettel és az eseménynaplóból "
        "visszaolvasott történetükkel. Itt látszik, mi lett a darabolásból a gyakorlatban: mi csúszott át, "
        "mit kellett visszabontani."
    )
    st.caption(
        f"**Elem és esemény nem ugyanaz.** A backlog-elem egy elvégzendő munkadarab; az esemény egy "
        f"naplóbejegyzés arról, hogy valami történt. A {PELDA_ELEMEI} elem útja során {PELDA_ESEMENYEI} esemény "
        "keletkezett: egy elem útja jellemzően öt eseményt ad (specifikáció jóváhagyva → ügynök indult → "
        "bírálatra került → bírálat indult → jóváhagyva), a javításra visszaküldött elemé többet, és "
        "vannak elemhez nem kötött események is (a darabolás jóváhagyása, az ügynökök leállítása, a "
        "visszatekintés). "
        "Az eseménynapló hossza ezért nem a backlog mérete."
    )
    elemek = adatok.elemek.copy()
    leir = LEIRASOK["pelda"]
    esem = adatok.esemenyek
    tabla = pd.DataFrame(
        {
            "Elem": elemek["elem_id"],
            "Iteráció": elemek["iteracio"],
            "Cím": elemek["cim"],
            "Magas kockázat": elemek["magas_kockazat"],
            "Méret (sor)": elemek["meret_sor"],
            "Vállalt": elemek["vallalt"],
            "Szülő": elemek["szulo"],
            "AC": [len(leir[e]["elfogadasi_feltetelek"]) for e in elemek["elem_id"]],
        }
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Elemek", len(tabla))
    c2.metric("Magas kockázatú", int((tabla["Magas kockázat"] == "igen").sum()))
    c3.metric(f"A {meretkorlat} soros korlát fölött", int((tabla["Méret (sor)"] > meretkorlat).sum()))
    c4.metric("Visszabontott elem", int(elemek.loc[elemek["szulo"] != "", "szulo"].nunique()))
    st.dataframe(tabla, hide_index=True, width="stretch")

    ids = list(elemek["elem_id"])
    valasztott = st.selectbox(
        "Elem részletei",
        ids,
        format_func=lambda e: f"{e} · {elemek.set_index('elem_id').loc[e, 'cim']}",
        key="backlog_pelda_elem",
    )
    sor = elemek.set_index("elem_id").loc[valasztott]
    magas = sor["magas_kockazat"] == "igen"
    refakt = bl.refaktoralas_e(sor["cim"])
    d = leir[valasztott]

    st.divider()
    bal, jobb = st.columns(2)
    with bal:
        _fejlec(valasztott, sor["cim"], d["cel"])
        kapcsolat = []
        if sor["szulo"]:
            kapcsolat.append(f"Az **{sor['szulo']}** elemből bontva")
        gyerekek = list(elemek.loc[elemek["szulo"] == valasztott, "elem_id"])
        if gyerekek:
            kapcsolat.append("Szétbontva: " + ", ".join(f"**{g}**" for g in gyerekek))
        if kapcsolat:
            st.info(" · ".join(kapcsolat), icon=":material/call_split:")
        _ac(d)
        st.markdown("**Becslés**")
        st.markdown(
            f"Előzetes becslés nincs: a modell nem használ story pontot. A **mért méret "
            f"{int(sor['meret_sor'])} sor** (korlát: {meretkorlat}), {int(sor['iteracio'])}. iteráció, "
            f"{'vállalt' if sor['vallalt'] == 'igen' else 'nem vállalt, előfeltétel vagy bontás'}."
        )
    with jobb:
        _dor(
            bl.dor(
                len(d["elfogadasi_feltetelek"]),
                int(sor["meret_sor"]),
                meretkorlat,
                bl.spec_jovahagyva(esem, valasztott),
            )
        )
        _dod(magas, refakt)

    tortenet = bl.elem_tortenet(esem, valasztott).assign(
        esemeny=lambda d: d["esemeny"].map(cimkek.esemeny)
    )
    st.markdown("**Az elem története az eseménynaplóban**")
    st.dataframe(
        tortenet.rename(
            columns={"idopont": "Időpont", "esemeny": "Esemény", "szereplo": "Szereplő", "reszlet": "Részlet"}
        ),
        hide_index=True,
        width="stretch",
    )
