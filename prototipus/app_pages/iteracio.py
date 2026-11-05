"""„Iteráció" nézet — hol tartunk a ciklusban, és mi van hátra."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modell import cimkek, grafikonok, kapacitas

adatok = st.session_state.adatok
p = st.session_state.pillanat

it = adatok.iteracio(p.iteracio)
kezdet = pd.Timestamp(it["kezdet"])
veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
eddig = p.esemenyek_eddig
ablak = eddig[(eddig["idopont"] >= kezdet) & (eddig["idopont"] < veg)]

nap = (p.idopont.normalize() - kezdet).days + 1
nap = max(1, min(nap, it["napok"]))

st.subheader(f"{it['id']}. iteráció — {it['nev']}")
st.caption(f"{it['kezdet']} – {it['veg']} · **{nap}. nap** a {it['napok']}-ból")

# --- A tervezett keret -----------------------------------------------------------

terv = it["parameterek_terv"]
k = kapacitas.szamol(terv["R"], terv["t"], terv["r"], it["napok"])

with st.container(horizontal=True):
    st.metric("Vállalt elem", it["vallalt"], border=True)
    st.metric("Számított keret", f"{cimkek.szam(k.elem_per_iteracio)} elem", border=True)
    st.metric("Bírálati esemény / nap", cimkek.szam(k.esemeny_per_nap), border=True)
    st.metric(
        "Eddigi bírálatok",
        int(ablak["esemeny"].isin(kapacitas.BIRALAT_LEZARO).sum()),
        border=True,
    )
st.html(grafikonok.keret_sav_html(it["vallalt"], k.elem_per_iteracio, "elem vállalva", "számított keret"))
st.caption(
    f"A keret forrása: _{it['terv_forrasa']}_ — R = {terv['R']} óra, "
    f"t = {terv['t']} perc, r = {terv['r']}"
)
if it.get("megjegyzes"):
    st.info(it["megjegyzes"])

st.divider()


# --- Ellenőrzőlista --------------------------------------------------------------

def volt(esemeny: str) -> bool:
    return bool((ablak["esemeny"] == esemeny).any())


def jel(kesz: bool) -> str:
    return ":material/check_circle:" if kesz else ":material/radio_button_unchecked:"


st.subheader("Ellenőrzőlista")
st.caption("A modell minden szakaszhoz ellenőrizhető kimenetet rendel.")

beolvadt_ablak = ablak[ablak["esemeny"] == "biralat_jovahagyva"]
szeniorok = set(adatok.konfig["szeniorok"])
mind_jovahagyott = (
    not beolvadt_ablak.empty and beolvadt_ablak["szereplo"].isin(szeniorok).all()
)

szakaszok = {
    "Iteráció indulása": [
        ("Bírálati keret kiszámítva a legutóbb mért paraméterekkel", True),
        ("A vállalt elemszám nem lépi túl a keretet", it["vallalt"] <= k.elem_per_iteracio),
        ("A darabolás jóváhagyva", volt("darabolas_jovahagyva")),
        ("Technikai átnézés megtörtént", volt("darabolas_technikai_ok")),
        ("Minden elem specifikációja jóváhagyva", volt("spec_jovahagyva")),
    ],
    "Napi ritmus": [
        ("A bírálati sor a korláton belül van",
         p.darab("Bírálatra vár") < adatok.konfig["wip_korlatok"]["Bírálatra vár"]),
        ("Volt bírálat ebben az iterációban",
         bool(ablak["esemeny"].isin(kapacitas.BIRALAT_LEZARO).any())),
    ],
    "Iteráció zárása": [
        ("Minden beolvadt elemnek van megnevezett emberi jóváhagyója", mind_jovahagyott),
        ("Bemutató megtörtént, emberi felelősségvállalással", volt("bemutato")),
        ("Visszatekintés gépi rétege megtörtént, kimenettel", volt("retro_gepi")),
        ("Visszatekintés emberi rétege megtörtént (minden második iterációban)",
         volt("retro_emberi") or it["id"] % 2 == 0),
    ],
}

for szakasz, tetelek in szakaszok.items():
    with st.container(border=True):
        kesz = sum(1 for _, ok in tetelek if ok)
        st.markdown(f"**{szakasz}** — {kesz}/{len(tetelek)}")
        for szoveg, ok in tetelek:
            st.markdown(f"{jel(ok)} {szoveg}")

st.divider()

# --- Az iteráció elemei ----------------------------------------------------------

st.subheader("Az iteráció elemei")
elemek = p.elemallapot[p.elemallapot["iteracio"] == it["id"]]
if elemek.empty:
    st.info("Ebben az iterációban még nem indult el elem.")
else:
    st.html(grafikonok.tabla_html(elemek, adatok.konfig["wip_korlatok"], adatok.konfig["meretkorlat_sor"]))
    with st.expander("Ugyanez táblázatként"):
        st.dataframe(
            elemek[["elem_id", "cim", "allapot", "meret_sor", "magas_kockazat", "vallalt"]].rename(
                columns={
                    "elem_id": "Azonosító",
                    "cim": "Cím",
                    "allapot": "Állapot",
                    "meret_sor": "Méret (sor)",
                    "magas_kockazat": "Magas kockázatú",
                    "vallalt": "Vállalt",
                }
            ),
            hide_index=True,
            width="stretch",
        )
