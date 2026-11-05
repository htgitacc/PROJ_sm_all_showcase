"""Számlálók és léptetés: ami egymás alatt áll, ugyanúgy számoljon, és a szám mondja meg, mit számol.

A felhasználó jelezte: a csúszka 0-tól 135-ig ment, alatta „1. / 136”; az animáció 162 lépést
számolt a 136 esemény mellett; a Backlog 36 eleme és a 136 esemény viszonya nem derült ki; és
egérrel nehéz egyesével lépni. Ezek a tesztek ezt őrzik.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from modell import animacio, backlog, betoltes, cimkek, jelenet

GYOKER = Path(__file__).resolve().parent.parent
BELEPES = str(GYOKER / "streamlit_app.py")


@pytest.fixture(scope="module")
def adatok():
    return betoltes.betolt()


def _most(kurzor: int) -> AppTest:
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.run()
    at.session_state["kurzor"] = kurzor
    at.switch_page("app_pages/teendok.py")
    at.run()
    assert not at.exception
    return at


def test_a_csuszka_es_a_felirata_ugyanugy_szamol(adatok):
    n = len(adatok.esemenyek)
    at = _most(0)
    csuszka = at.sidebar.slider[0]
    assert (csuszka.min, csuszka.max, csuszka.value) == (1, n, 1)
    assert any(c.value.startswith(f"1\\. / {n} esemény") for c in at.sidebar.caption)


def test_a_csuszka_mozgatasa_a_kurzort_egy_eseménnyel_kisebb_indexre_allitja(adatok):
    at = _most(0)
    at.sidebar.slider[0].set_value(40).run()
    assert at.session_state["kurzor"] == 39
    assert any(c.value.startswith(f"40\\. / {len(adatok.esemenyek)} esemény") for c in at.sidebar.caption)


def test_a_leptetogombok_egyesevel_lepnek_es_a_szelen_tiltva_vannak(adatok):
    utolso = len(adatok.esemenyek) - 1
    at = _most(10)
    gomb = {b.key: b for b in at.sidebar.button}
    gomb["kurzor_elore"].click().run()
    assert at.session_state["kurzor"] == 11
    {b.key: b for b in at.sidebar.button}["kurzor_vissza"].click().run()
    {b.key: b for b in at.sidebar.button}["kurzor_vissza"].click().run()
    assert at.session_state["kurzor"] == 9
    assert at.sidebar.slider[0].value == 10

    eleje = {b.key: b for b in _most(0).sidebar.button}
    assert eleje["kurzor_vissza"].disabled and not eleje["kurzor_elore"].disabled
    vege = {b.key: b for b in _most(utolso).sidebar.button}
    assert vege["kurzor_elore"].disabled and not vege["kurzor_vissza"].disabled


def test_az_animacio_felirata_kimondja_a_levezetett_lepeseket(adatok):
    kockak = animacio.forgatokonyv(adatok)["kockak"]
    levezetett = sum(k["forras"] == "levezetett" for k in kockak)
    assert levezetett and len(kockak) == len(adatok.esemenyek) + levezetett
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.switch_page("app_pages/animacio.py")
    at.run()
    assert not at.exception
    felirat = next(c.value for c in at.caption if "naplózott eseménye" in c.value)
    assert f"{len(adatok.esemenyek)} naplózott eseménye" in felirat
    assert f"**{len(kockak)} lépést** számol" in felirat
    assert f"{levezetett} **levezetett lépést**" in felirat


def test_az_animacio_leptetheto_es_a_szamlalo_lepest_mond(adatok):
    html = cimkek.animacio_cimkekkel(jelenet.oldal(adatok))
    assert 'id="elozo"' in html and 'id="kovetkezo"' in html
    assert "ugras(mutato - 1)" in html and "ugras(mutato + 1)" in html
    assert '"ArrowLeft"' in html and '"ArrowRight"' in html
    assert "${kockak.length} lépés`" in html


def test_a_backlog_megkulonbozteti_a_keszletet_a_pelda_elemeitol_es_esemenyeitol(adatok):
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.switch_page("app_pages/backlog.py")
    at.run()
    assert not at.exception
    szoveg = "\n".join(m.value for m in at.markdown)
    assert f"**{len(backlog.szimulacios_keszlet())} elemes készletből**" in szoveg
    assert f"a példa két iterációja {len(adatok.elemek)} elemmel dolgozott" in szoveg
    felirat = "\n".join(c.value for c in at.caption)
    assert f"A {len(adatok.elemek)} elem útja során {len(adatok.esemenyek)} esemény" in felirat
    # „jellemzően öt eseményt ad”: a példa elemeinek mediánja
    e = adatok.esemenyek
    assert e[e["elem_id"] != ""].groupby("elem_id").size().median() == 5
    assert "jellemzően öt eseményt ad" in felirat
