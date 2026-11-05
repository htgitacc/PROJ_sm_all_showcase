"""„Vezetett bemutató” — a példa két iterációja fejezetekben, annak, aki kívülről érkezik."""

from __future__ import annotations

import streamlit as st

from modell import allapot, bemutato, fogalmak, grafikonok, hatter, konyvjelzok
from modell import jelzesek as jelzesek_modul

adatok = st.session_state.adatok
esemenyek = adatok.esemenyek
KONYVJELZOK = konyvjelzok.konyvjelzok(esemenyek)
FEJEZETEK = bemutato.FEJEZETEK
KULCS = "bemutato_fejezet"

UTOLSO = "bemutato_utolso"

# A fejezetválasztó kulcsa maga a választott fejezet. Ha a látogató a kijelölt fejezetre
# kattintva törli a kijelölést, az utoljára látott fejezet marad.
if st.session_state.get(KULCS) not in range(len(FEJEZETEK)):
    st.session_state[KULCS] = st.session_state.get(UTOLSO, 0)


def _lep(cel: int) -> None:
    st.session_state[KULCS] = max(0, min(len(FEJEZETEK) - 1, cel))


st.caption(
    "A példa két iterációja hat rövid fejezetben: mi történik, mit lát a Scrum Master, és "
    "miért úgy dönt, ahogy. Minden fejezetből egy gombbal átléphetsz a részletes nézetre, "
    "ugyanarra a pillanatra."
)

st.pills(
    "Fejezet",
    options=list(range(len(FEJEZETEK))),
    format_func=lambda i: f"{i}. {FEJEZETEK[i].cim}",
    key=KULCS,
    label_visibility="collapsed",
)

i = st.session_state[KULCS] if st.session_state[KULCS] is not None else st.session_state.get(UTOLSO, 0)
st.session_state[UTOLSO] = i
f = FEJEZETEK[i]
st.progress((i + 1) / len(FEJEZETEK), text=f"{i + 1}. / {len(FEJEZETEK)} fejezet")

st.subheader(f"{i}. {f.cim}")
st.caption(f.alcim.replace(". ", "\\. ", 1))  # „1. iteráció” ne legyen számozott lista

if f.konyvjelzo is None:
    st.html(bemutato.munka_utja_html(adatok.konfig["wip_korlatok"]["Bírálatra vár"]))

for bekezdes in f.narracio:
    st.markdown(bekezdes)

if f.konyvjelzo is not None:
    index = KONYVJELZOK[f.konyvjelzo]
    p = allapot.pillanat(esemenyek, adatok.elemek, adatok.iteraciok, index)
    esemeny = esemenyek.loc[index]
    st.altair_chart(
        grafikonok.sor_grafikon(
            st.session_state.sor_idosor, adatok.konfig["wip_korlatok"]["Bírálatra vár"], index
        ),
        width="stretch",
    )
    st.caption(f"A pillanat: **{esemeny['idopont']:%Y-%m-%d %H:%M}** · {index + 1}. / {len(esemenyek)} esemény")

    if f.jelzesek:
        aktiv = [j for j in jelzesek_modul.kiertekel(adatok, p) if j.aktiv and j.kod in f.jelzesek]
        for j in aktiv:
            doboz = st.error if j.sulyossag == jelzesek_modul.KRITIKUS else st.warning
            doboz(f"**A felület jelez: {j.cim}** — {j.uzenet}", icon=":material/notifications_active:")
            st.markdown(f":material/arrow_forward: **Teendő:** {j.teendo}")
else:
    index = None

if f.tanulsag:
    st.info(f"**Tanulság:** {f.tanulsag}", icon=":material/lightbulb:")
    if "J6" in f.jelzesek:
        with st.expander(fogalmak.GEPI_KAPU_CIM, icon=":material/gpp_good:"):
            st.markdown(hatter.linkek(fogalmak.GEPI_KAPU))

if st.button(f"Nézd meg részletesen: {f.nezet_cim}", icon=":material/open_in_new:", key=f"bemutato_nezet_{i}"):
    if index is not None:
        st.session_state.kurzor = index
    st.switch_page(f.nezet)

st.divider()
bal, kozep, jobb = st.columns([1, 2, 1])
with bal:
    st.button("← Előző", on_click=_lep, args=(i - 1,), disabled=i == 0, width="stretch", key="bemutato_elozo")
with jobb:
    st.button("Következő →", on_click=_lep, args=(i + 1,), disabled=i == len(FEJEZETEK) - 1,
              width="stretch", type="primary", key="bemutato_kovetkezo")

if i == len(FEJEZETEK) - 1:
    st.success(
        "**Most te jössz.** A Szimulációban te vezetsz egy iterációt: te döntöd el, mennyit "
        "vállalsz, beolvasztasz vagy visszaküldesz, és leállítod-e az ügynököket.",
        icon=":material/videogame_asset:",
    )
    if st.button("Kipróbálom: Szimuláció", type="primary", key="bemutato_szim"):
        st.switch_page("app_pages/szimulacio.py")
