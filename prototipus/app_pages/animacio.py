"""„Animáció" nézet — a két iteráció lejátszva.

A négy táblázatos nézet annak szól, aki a folyamatban dolgozik. Ez a nézet annak,
aki kívülről nézi: a modell központi állítása — hogy nem az ügynökök sebessége a
szűk keresztmetszet, hanem az emberi bírálat — időbeli és mennyiségi állítás,
amit egy mozgó ábra jobban ad át, mint egy táblázat.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from modell import animacio, betoltes, cimkek, jelenet


@st.cache_data
def szinpad_html() -> str:
    """A forgatókönyv felépítése drága, a kimenete viszont állandó — egyszer fut le."""
    return jelenet.oldal(betoltes.betolt())


@st.cache_data
def lepesek() -> tuple[int, int]:
    """(naplózott, levezetett) lépések száma: a lejátszó számlálója a kettő összegét mutatja."""
    kockak = animacio.forgatokonyv(betoltes.betolt())["kockak"]
    levezetett = sum(k["forras"] == "levezetett" for k in kockak)
    return len(kockak) - levezetett, levezetett


naplozott, levezetett = lepesek()
st.caption(
    f"A példa két iterációjának {naplozott} naplózott eseménye, lejátszva. A lejátszó "
    f"**{naplozott + levezetett} lépést** számol: a naplózott események mellett {levezetett} "
    "**levezetett lépést** is mutat — a verifikáló sikeres átengedését, amely a modell szerint "
    "minden bírálatra kerülés előtt megtörténik, de a napló csak a bukást rögzíti. Léptetni "
    "egyesével a ‹ › gombokkal vagy a nyilakkal lehet. A színpad ugyanazt az állapotot mutatja, "
    "mint a táblázatos nézetek — az elemek helyét mindkettő az eseménynaplóból számolja."
)

components.html(cimkek.animacio_cimkekkel(szinpad_html()), height=880, scrolling=True)

with st.expander("Mit érdemes megnézni rajta"):
    st.markdown(
        """
Az **1. iteráció 2. napján** öt elem vár a négyes korláttal szemben: az ötödik
kártya kilóg az oszlopból, mert nincs hova betenni. Néhány másodperccel később a
Scrum Master leállítja az ügynököket. Ez a modell legfontosabb pillanata — a
gépi kapacitás azért áll, mert az emberi bírálat betelt.

A **2. iterációban** az igénylőfelület 310 sorral érkezik a 200-as korlát
ellenében, és pirosan jelenik meg: a teendő visszabontás, nem hosszabb bírálat.

A **biztonsági láncnál** látszik, hogy a kereső ügynök négy találatából a másik
modellcsaládra épülő cáfoló hármat kiejt, és csak egy jut emberi döntésre.

A szaggatott keretű lépések **levezetettek**: a modell szerint minden elem
áthalad a verifikálón, de a napló csak a bukást rögzíti. Ezeket a felület
szándékosan megkülönbözteti, hogy ne keveredjen a megfigyelt a következtetettel.
        """
    )
