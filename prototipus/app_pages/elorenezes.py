"""„Előretekintés" nézet — mi várható a következő iterációban."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modell import kapacitas, tanulas
from modell import cimkek

adatok = st.session_state.adatok


def _ugras_az_elso_iteracio_vegere() -> None:
    from modell import konyvjelzok

    st.session_state.kurzor = konyvjelzok.konyvjelzok(adatok.esemenyek)["Paramétereltérés (1. it. vége)"]

p = st.session_state.pillanat

st.caption(
    "Ez a nézet a **mért** paraméterekből számol, nem modellez. Azt mondja meg, "
    "mennyi fér bele — nem azt, hogy mi fog történni."
)

# --- Van-e már lezárt iteráció? --------------------------------------------------

lezart = []
for it in adatok.iteraciok:
    veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
    esemenyek_addig = adatok.esemenyek[adatok.esemenyek["idopont"] < veg]
    if not esemenyek_addig.empty and esemenyek_addig.index[-1] <= p.index:
        lezart.append(it)

if not lezart:
    st.info(
        "Még nincs lezárt iteráció, tehát nincs mért paraméter. "
        "Az első iteráció a feltevésekkel indul."
    )
    st.button(
        "Ugrás az 1. iteráció végére, ahol már van mért paraméter",
        icon=":material/fast_forward:",
        on_click=_ugras_az_elso_iteracio_vegere,
    )
    st.stop()

utolso = lezart[-1]
mert = kapacitas.mert_parameterek(adatok.esemenyek, utolso)
terv = utolso["parameterek_terv"]

# --- A következő iteráció kapacitása ---------------------------------------------

st.subheader("A következő iteráció kapacitása")

kovetkezo_napok = utolso["napok"]
elorejelzes = kapacitas.szamol(mert["R"], mert["t"], mert["r"], kovetkezo_napok)
tervezett = kapacitas.szamol(terv["R"], terv["t"], terv["r"], kovetkezo_napok)

with st.container(horizontal=True):
    st.metric(
        "Vállalható elem",
        cimkek.szam(elorejelzes.elem_per_iteracio),
        delta=f"{elorejelzes.elem_per_iteracio - tervezett.elem_per_iteracio:+.1f} a korábbi tervhez képest",
        border=True,
    )
    st.metric("Lezárható elem / nap", cimkek.szam(elorejelzes.elem_per_nap, 2), border=True)
    st.metric("Bírálati esemény / nap", cimkek.szam(elorejelzes.esemeny_per_nap), border=True)

with st.container(border=True):
    nevelo = "Az" if str(utolso["id"]).startswith(("1", "5")) else "A"
    st.markdown(f"**{nevelo} {utolso['id']}. iteráció mért paraméterei**")
    osszehas = pd.DataFrame(
        {
            "Paraméter": ["R — napi bírálati idő (óra)", "t — validálási idő (perc)", "r — javítási körök"],
            "Terv": [terv["R"], terv["t"], terv["r"]],
            "Mért": [mert["R"], mert["t"], mert["r"]],
            "Eltérés": [
                f"{(mert['R'] - terv['R']) / terv['R']:+.0%}",
                f"{(mert['t'] - terv['t']) / terv['t']:+.0%}",
                f"{(mert['r'] - terv['r']) / terv['r']:+.0%}" if terv["r"] else "—",
            ],
        }
    )
    st.dataframe(osszehas, hide_index=True, width="stretch")
    st.caption(
        f"Alap: {mert['biralatok']} lezárt bírálat, {mert['beolvadt']} beolvadt elem. "
        "A képlet: (R × 60 / t) × 2 szenior / (1 + r)."
    )

st.divider()

# --- Ami átgörgetődik ------------------------------------------------------------

st.subheader("Ami átgörgetődik")
st.caption("Ezek már lefoglalják a következő iteráció keretének egy részét.")

atgorgetodo = p.elemallapot[
    p.elemallapot["allapot"].isin(["Átcsúszott", "Javítás alatt", "Bírálatra vár", "Bírálat alatt"])
]
if atgorgetodo.empty:
    st.success("Nincs átgörgetődő elem.")
else:
    st.dataframe(
        atgorgetodo[["elem_id", "cim", "allapot", "iteracio"]].rename(
            columns={
                "elem_id": "Azonosító",
                "cim": "Cím",
                "allapot": "Állapot",
                "iteracio": "Iteráció",
            }
        ),
        hide_index=True,
        width="stretch",
    )
    szabad = elorejelzes.elem_per_iteracio - len(atgorgetodo)
    st.warning(
        f"A nyers keret {cimkek.szam(elorejelzes.elem_per_iteracio)} elem, ebből "
        f"{len(atgorgetodo)} már foglalt — **szabad kapacitás: {cimkek.szam(szabad)} elem**."
    )

st.divider()

# --- Visszamérendő szabályok -----------------------------------------------------

st.subheader("Visszamérendő szabályok")
st.caption(
    "A visszatekintéseken felvett szabályok, és az a hibaosztály, amelyet figyelni "
    "kell ahhoz, hogy eldőljön, fogtak-e."
)

vissza = tanulas.visszamerendo(adatok, p)
if vissza.empty:
    st.info("Még nincs visszamérendő szabály.")
else:
    megjelenit = vissza.rename(
        columns={
            "szabaly": "Szabály",
            "kod": "Hibaosztály",
            "nev": "Megnevezés",
            "szabaly_datuma": "Felvéve",
            "visszateres_szabaly_utan": "Visszatért",
            "letra_neve": "Létrafok",
        }
    )
    st.dataframe(megjelenit, hide_index=True, width="stretch")
    for _, sor in vissza.iterrows():
        if sor["visszateres_szabaly_utan"] > 0:
            st.error(
                f"**{sor['szabaly']}** nem fogott: a {sor['kod']} hibaosztály "
                f"{sor['visszateres_szabaly_utan']} alkalommal tért vissza a felvétele óta. "
                "A teendő nem a szabály átfogalmazása, hanem gépi kapu építése köré."
            )
