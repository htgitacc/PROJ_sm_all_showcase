"""A magyar címkék és az üres állapotok tesztjei.

A felületen nem látszhat nyers gépi kód (`biralatra_kerult`, `helyesseg`), és ahol a kurzor
miatt nincs mit mutatni, ott legyen egy gomb, amely olyan pillanatra visz, ahol van.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from modell import cimkek, konyvjelzok
from modell.betoltes import betolt

GYOKER = Path(__file__).resolve().parent.parent
BELEPES = str(GYOKER / "streamlit_app.py")


def test_a_pelda_minden_esemenyenek_van_magyar_neve():
    hianyzik = set(betolt().esemenyek["esemeny"]) - set(cimkek.ESEMENYEK)
    assert not hianyzik, hianyzik


def test_a_szimulacio_minden_esemenyenek_van_magyar_neve():
    kodok = set(re.findall(r'_esemeny\(allas, "([a-z_]+)"', (GYOKER / "modell" / "szimulacio.py").read_text(encoding="utf-8")))
    assert kodok and not kodok - set(cimkek.ESEMENYEK), kodok - set(cimkek.ESEMENYEK)


def test_az_animacio_levezetett_esemenyenek_is_van_neve():
    assert "verifikalo_atengedte" in cimkek.ESEMENYEK


def test_minden_kategorianak_van_ekezetes_neve():
    import pandas as pd

    kat = set(pd.read_csv(GYOKER / "adatok" / "hibaosztalyok.csv")["kategoria"])
    assert not kat - set(cimkek.KATEGORIAK), kat - set(cimkek.KATEGORIAK)


def test_szamformatum_es_ora():
    assert cimkek.szam(10.33) == "10,3" and cimkek.szam(2.666, 2) == "2,67"
    assert cimkek.ora(0.0) == "most került be"
    assert cimkek.ora(3.8) == "4 órája" and cimkek.ora(21.2) == "21,2 órája"


def test_az_animacio_html_megkapja_a_cimketablat():
    h = cimkek.animacio_cimkekkel("<html><head><script>x()</script></head></html>")
    assert h.index("ESEMENY_CIMKE") < h.index("x()")
    assert "bírálatra került" in h


def _nezet(oldal: str, kurzor: int) -> AppTest:
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.run()
    at.session_state["kurzor"] = kurzor
    at.switch_page(f"app_pages/{oldal}")
    at.run()
    assert not at.exception, [e.value for e in at.exception]
    return at


KODOK = re.compile(r"\b(" + "|".join(map(re.escape, cimkek.ESEMENYEK)) + r"|" +
                   "|".join(map(re.escape, [k for k in cimkek.KATEGORIAK if k != "gepi"])) + r")\b")


@pytest.mark.parametrize("oldal", ["teendok.py", "iteracio.py", "tanulas.py", "elorenezes.py"])
@pytest.mark.parametrize("kurzor", [30, 67, 135])
def test_nyers_kod_nem_latszik_a_szovegben(oldal, kurzor):
    at = _nezet(oldal, kurzor)
    szoveg = "\n".join(e.value for e in [*at.markdown, *at.caption, *at.info, *at.warning, *at.error]
                       + list(at.sidebar.markdown) + list(at.sidebar.caption))
    talalat = KODOK.findall(szoveg)
    assert not talalat, (oldal, kurzor, talalat)


@pytest.mark.parametrize("oldal", ["elorenezes.py", "tanulas.py"])
def test_az_ures_allapot_gombja_olyan_pillanatra_visz_ahol_van_tartalom(oldal):
    at = _nezet(oldal, 0)
    gomb = next(b for b in at.button if "Ugrás az 1. iteráció végére" in b.label)
    gomb.click().run()
    assert not at.exception
    assert at.session_state["kurzor"] == konyvjelzok.konyvjelzok(betolt().esemenyek)["Paramétereltérés (1. it. vége)"]
    assert not any("Ugrás az 1. iteráció végére" in b.label for b in at.button), "a cél pillanat is üres"
