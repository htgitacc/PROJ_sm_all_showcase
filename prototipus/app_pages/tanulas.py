"""„Tanulás" nézet — az ügynökpark állapota és a visszacsatolási hurok."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modell import fogalmak, hatter
from modell import cimkek, grafikonok
from modell import tanulas as tanulas_modul

# Ugyanaz a védelem, mint `app_pages/szimulacio.py`-ban: a `HIBAOSZTALY_MAGYARAZAT`
# 2026-09-16 11:15 után került a kódba, az élő szolgáltatás pedig 09:31 óta
# fut — az importált modul emiatt hiányozhat ilyet, amíg nem indul újra.
_HIBAOSZTALY_MAGYARAZAT = getattr(tanulas_modul, "HIBAOSZTALY_MAGYARAZAT", {})

adatok = st.session_state.adatok


def _ugras_az_elso_iteracio_vegere() -> None:
    from modell import konyvjelzok

    st.session_state.kurzor = konyvjelzok.konyvjelzok(adatok.esemenyek)["Paramétereltérés (1. it. vége)"]

p = st.session_state.pillanat

st.caption(
    "A visszajelzés akkor épült be, ha az adott hibaosztály többé nem fordul elő. "
    "A bizonyíték nem az ügynök ígérete, hanem a hiba eltűnése."
)

# --- Hibaosztályok ---------------------------------------------------------------

st.subheader("Hibaosztályok és az eszkalációs létra")

osszes = tanulas_modul.hibaosztaly_osszesites(adatok, p)
if osszes.empty:
    st.info("Ebben a pillanatban még nincs rögzített hibaosztály — az első bírálati találatok a 2. napon születnek.")
    st.button(
        "Ugrás az 1. iteráció végére, a visszatekintéshez",
        icon=":material/fast_forward:",
        on_click=_ugras_az_elso_iteracio_vegere,
    )
    st.stop()

st.caption(
    "Minél többször tér vissza egy hibaosztály, annál feljebb lép a létrán, és annál erősebb a "
    "válasz: a bíráló javíttatja → szabály a szabályfájlba → gépi kapu → architektúra- vagy "
    "modellváltás → a folyamat felülvizsgálata."
)
st.html(grafikonok.letra_html(tanulas_modul.LETRA, osszes["letrafok"].value_counts().to_dict()))
with st.expander(fogalmak.GEPI_KAPU_CIM, icon=":material/gpp_good:"):
    st.markdown(hatter.linkek(fogalmak.GEPI_KAPU))

for _, sor in osszes.iterrows():
    with st.container(border=True):
        fejlec, jobb = st.columns([3, 1])
        with fejlec:
            st.markdown(f"**{sor['kod']} · {sor['nev']}**")
            st.caption(f"Kategória: {cimkek.kategoria(sor['kategoria'])}")
        with jobb:
            szin = {1: "gray", 2: "orange", 3: "red"}.get(sor["letrafok"], "gray")
            st.markdown(
                f":{szin}-badge[{sor['letrafok']}. fok — {sor['letra_neve']}]"
            )

        reszek = [f"Előfordulás: **{sor['elofordulas']}**"]
        if sor["szabaly"]:
            reszek.append(f"Szabály: **{sor['szabaly']}** ({sor['szabaly_datuma']})")
            reszek.append(f"Azóta visszatért: **{sor['visszateres_szabaly_utan']}×**")
        else:
            reszek.append("Szabály: _még nincs_")
        if sor["gepi_kapu"]:
            kapu = adatok.szabalyok.loc[adatok.szabalyok["kod"] == sor["gepi_kapu"], "cim"]
            reszek.append(
                f"Gépi kapu: **{sor['gepi_kapu']}**" + (f" — {kapu.iloc[0]}" if not kapu.empty else "")
            )
        st.markdown(" · ".join(reszek))

        st.markdown(f":material/arrow_forward: {sor['teendo']}")

        magyarazat = _HIBAOSZTALY_MAGYARAZAT.get(sor["kod"])
        if magyarazat:
            st.caption(f"Mit jelent ez a gyakorlatban? {magyarazat}")

        if sor["szabaly"] and sor["visszateres_szabaly_utan"] > 0 and not sor["gepi_kapu"]:
            st.error(
                "A szabály nem fogott. Az utasításfájl **puha korlát** — "
                "az utasítás követendő szöveg, nem kikényszerített megkötés. "
                "A visszatérő hibaosztályt géppel kell megfogni."
            )

st.divider()

# --- Szabályfájl -----------------------------------------------------------------

st.subheader("A szabályfájl állapota")

ervenyes = tanulas_modul.ervenyes_szabalyok(adatok, p)
szabalyok = ervenyes[ervenyes["tipus"] == "szabaly"]
kapuk = ervenyes[ervenyes["tipus"] == "gepi_kapu"]

with st.container(horizontal=True):
    st.metric("Érvényes szabály", len(szabalyok), border=True)
    st.metric("Gépi kapu", len(kapuk), border=True)
    st.metric(
        "Bírálatból született szabály",
        int((szabalyok["kivalto_elem"] != "").sum()),
        border=True,
    )

st.dataframe(
    ervenyes[["kod", "cim", "hibaosztaly", "letrehozva", "iteracio", "kategoria", "tipus"]].rename(
        columns={
            "kod": "Azonosító",
            "cim": "Megszorítás",
            "hibaosztaly": "Hibaosztály",
            "letrehozva": "Felvéve",
            "iteracio": "Iteráció",
            "kategoria": "Kategória",
            "tipus": "Típus",
        }
    ),
    hide_index=True,
    width="stretch",
)

# --- A növekedés kétértelmű olvasata ---------------------------------------------

novekedes = (
    ervenyes.groupby("iteracio").size().rename("uj_szabaly").reset_index()
    if not ervenyes.empty
    else pd.DataFrame()
)
if not novekedes.empty and len(novekedes) > 1:
    with st.container(border=True):
        st.markdown("**A szabályfájl növekedése iterációnként**")
        st.bar_chart(novekedes, x="iteracio", y="uj_szabaly", height=200)
        st.warning(
            "**Ennek a görbének két olvasata van.** Ha az új szabályok száma csökken, "
            "*miközben a hibaosztályok is fogynak*, az érettség. Ha az új szabályok "
            "száma csökken, de a hibaosztályok nem, akkor a csapat valószínűleg "
            "kihagyja a visszatekintés gépi rétegét."
        )

st.divider()

# --- Költség ---------------------------------------------------------------------

st.subheader("Az ügynökpark költsége")
st.caption(
    hatter.linkek(
        "A többügynökös működés a mérések szerint 3–10-szeres tokenhasználatot jelent "
        "az együgynökössel szemben (S-08). A cáfoló lépcső minden találatot kétszer dolgoztat fel."
    )
)

lathato_iteraciok = [it["id"] for it in adatok.iteraciok if pd.Timestamp(it["kezdet"]) <= p.idopont]
koltseg = adatok.koltseg[adatok.koltseg["iteracio"].isin(lathato_iteraciok)]
if koltseg.empty:
    st.info("Még nincs költségadat.")
else:
    osszesitve = koltseg.groupby("iteracio")[["token_ezer", "koltseg_ft"]].sum().reset_index()
    with st.container(horizontal=True):
        for _, sor in osszesitve.iterrows():
            st.metric(
                f"{int(sor['iteracio'])}. iteráció",
                f"{int(sor['koltseg_ft']):,} Ft".replace(",", " "),
                delta=f"{int(sor['token_ezer']):,} e token".replace(",", " "),
                delta_color="off",
                border=True,
            )
    st.dataframe(
        koltseg.rename(
            columns={
                "iteracio": "Iteráció",
                "kategoria": "Ügynökszerep",
                "token_ezer": "Token (ezer)",
                "koltseg_ft": "Költség (Ft)",
            }
        ),
        hide_index=True,
        width="stretch",
    )
