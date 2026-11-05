"""„Teendők" nézet — mi az, ami a kurzor pillanatában beavatkozást igényel, és mi a teendő?"""

from __future__ import annotations

import streamlit as st

from modell import allapot as allapot_modul
from modell import fogalmak, hatter
from modell import grafikonok
from modell import jelzesek as jelzesek_modul

adatok = st.session_state.adatok
p = st.session_state.pillanat

jelzesek = jelzesek_modul.kiertekel(adatok, p)
aktivak = [j for j in jelzesek if j.aktiv]
csendben = [j for j in jelzesek if not j.aktiv]

# --- Beavatkozási jelzések -------------------------------------------------------

if not aktivak:
    st.success(
        ":material/check_circle: **Nincs teendő.** Mind a kilenc beavatkozási jelzés csendben van.",
        icon=":material/check_circle:",
    )
else:
    for j in aktivak:
        doboz = st.error if j.sulyossag == jelzesek_modul.KRITIKUS else st.warning
        doboz(f"**{j.cim}** — {j.uzenet}")
        with st.container(border=True):
            st.markdown(f":material/arrow_forward: **Teendő:** {j.teendo}")
            if j.kod == "J6":  # visszatérő hibaosztály: a teendő gépi kapu
                with st.expander(fogalmak.GEPI_KAPU_CIM, icon=":material/gpp_good:"):
                    st.markdown(hatter.linkek(fogalmak.GEPI_KAPU))
            if j.reszletek:
                for r in j.reszletek:
                    st.caption(f"· {hatter.linkek(r)}")
            st.caption(f"Forrás: {hatter.linkek(j.forras)} · [forrásjegyzék]({hatter.FORRASJEGYZEK})")

with st.expander(f"Csendben lévő jelzések ({len(csendben)})"):
    for j in csendben:
        st.markdown(f"**{j.kod} · {j.cim}** — {j.uzenet}")
        for r in j.reszletek:
            st.caption(f"· {hatter.linkek(r)}")

st.divider()

# --- Az áramlás állapota ---------------------------------------------------------

st.subheader("Az áramlás állapota")

korlatok = adatok.konfig["wip_korlatok"]
st.html(grafikonok.tabla_html(p.elemallapot, korlatok, adatok.konfig["meretkorlat_sor"]))

st.markdown("**A bírálati sor hossza az időben**")
st.altair_chart(
    grafikonok.sor_grafikon(
        st.session_state.sor_idosor, korlatok["Bírálatra vár"], p.index, st.session_state.konyvjelzok
    ),
    width="stretch",
)
st.caption(
    "Narancs vonal: a kurzor pillanata. Piros pont: a sor a korlát fölött. Szürke szaggatott "
    "vonalak: a példa kulcspillanatai (rámutatva látszik a nevük)."
)

# --- A bírálati sor --------------------------------------------------------------

st.subheader("Bírálati sor")
st.caption(
    "Ez a modell szűk keresztmetszete. A torlódás a sorban állásból ered, "
    "nem a bírálat lassúságából."
)

sor = p.oszlop("Bírálatra vár").sort_values("allapot_ota")
if sor.empty:
    st.info("A bírálati sor üres.")
else:
    st.dataframe(
        sor[["elem_id", "cim", "meret_sor", "varakozas_ora", "magas_kockazat"]].rename(
            columns={
                "elem_id": "Azonosító",
                "cim": "Cím",
                "meret_sor": "Méret (sor)",
                "varakozas_ora": "Vár (óra)",
                "magas_kockazat": "Magas kockázatú",
            }
        ),
        hide_index=True,
        width="stretch",
    )

# --- Éppen bírálat alatt ---------------------------------------------------------

folyamatban = p.oszlop("Bírálat alatt")
if not folyamatban.empty:
    st.subheader("Bírálat alatt")
    st.dataframe(
        folyamatban[["elem_id", "cim", "biralo", "varakozas_ora"]].rename(
            columns={
                "elem_id": "Azonosító",
                "cim": "Cím",
                "biralo": "Bíráló",
                "varakozas_ora": "Bírálat kezdete óta (óra)",
            }
        ),
        hide_index=True,
        width="stretch",
    )

# --- Az utolsó események ---------------------------------------------------------

with st.expander("Az utolsó tíz esemény"):
    utolsok = p.esemenyek_eddig.tail(10).iloc[::-1]
    st.dataframe(
        utolsok[["idopont", "elem_id", "esemeny", "szereplo", "reszlet"]].rename(
            columns={
                "idopont": "Időpont",
                "elem_id": "Elem",
                "esemeny": "Esemény",
                "szereplo": "Szereplő",
                "reszlet": "Részlet",
            }
        ),
        hide_index=True,
        width="stretch",
    )
