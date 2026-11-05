"""Az „Amire épül” nézetek közös megjelenítője — a háttéranyag közvetlenül a felületen olvasható.

A brief, a kutatás, a koncepció és a spike-ok mind saját nézetet kapnak (`modell/hatter.py`), de
ugyanígy jelennek meg. A lezárt anyagot csak megjelenítjük; a dokumentumok egymásra mutató
hivatkozásai belső hivatkozássá alakulnak (`<nézet>?dok=<azonosító>`).
"""

from __future__ import annotations

import streamlit as st

from modell import dokumentumok, forrasok, hatter

KULCS = "dok_valasztott"


def megjelenit(nev: str) -> None:
    nezet = next(n for n in hatter.NEZETEK if n.oldal == nev)
    osszes = {d.azonosito: d for d in dokumentumok.katalogus()}
    sajat = {a: d for a, d in osszes.items() if d.csoport in nezet.csoportok}
    if not sajat:
        st.error("A háttéranyag nem található a telepítésben.")
        st.stop()

    kulcs = f"{KULCS}_{nev}"

    def _valasztas_valtozott() -> None:
        st.query_params["dok"] = st.session_state[kulcs]

    kert = st.query_params.get("dok")
    if kert in sajat:
        st.session_state[kulcs] = kert
    elif st.session_state.get(kulcs) not in sajat:
        st.session_state[kulcs] = nezet.alapertelmezett if nezet.alapertelmezett in sajat else next(iter(sajat))

    st.caption(
        nezet.bevezeto
        + " Ugyanazt olvasod itt, ami a projekt mappájában is megtalálható — a szövegen nem változtattunk."
    )

    if len(sajat) > 1:
        tobb_csoport = len(nezet.csoportok) > 1
        st.selectbox(
            "Dokumentum",
            options=list(sajat),
            key=kulcs,
            format_func=lambda a: (
                f"{dokumentumok.CSOPORTOK[sajat[a].csoport]} · {sajat[a].cim}" if tobb_csoport else sajat[a].cim
            ),
            on_change=_valasztas_valtozott,
        )
    st.query_params["dok"] = st.session_state[kulcs]

    dok = sajat[st.session_state[kulcs]]
    szoveg = dok.fajl.read_text(encoding="utf-8")

    kert_forras = st.query_params.get("forras")
    if kert_forras and dok.azonosito == "kutatas/forrasok":
        talalat = forrasok.bejegyzes(kert_forras)
        if talalat:
            with st.container(border=True):
                st.markdown(f"**{kert_forras} — {talalat[0]}**")
                st.markdown(talalat[1].replace("\n", "  \n"))  # a jegyzék sortörései megmaradnak
            st.caption("Lent a teljes forrásjegyzék.")
        else:
            st.warning(f"A(z) {kert_forras} forrás nincs a jegyzékben.")

    st.divider()
    st.markdown(hatter.linkek(hatter.belso_hivatkozasok(szoveg, dok.ut, osszes)))
