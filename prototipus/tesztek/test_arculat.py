"""Az arculat: egy világos téma, jáde kiemelés, csoportszínű oldalfejléc (ADR 0008).

A kontrasztot számoljuk (WCAG 2.1), nem becsüljük; a téma a `config.toml`-ban és a modulban
ugyanazokkal a színekkel áll; minden nézet fejléce a saját menücsoportja színét kapja.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from modell import arculat, hatter

GYOKER = Path(__file__).resolve().parent.parent
BELEPES = str(GYOKER / "streamlit_app.py")
CONFIG = tomllib.loads((GYOKER.parent / ".streamlit" / "config.toml").read_text(encoding="utf-8"))
TEMA = CONFIG["theme"]


def _fenyesseg(szin: str) -> float:
    csatornak = [int(szin[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in csatornak]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def kontraszt(a: str, b: str) -> float:
    vilagos, sotet = sorted([_fenyesseg(a), _fenyesseg(b)], reverse=True)
    return (vilagos + 0.05) / (sotet + 0.05)


def test_a_kontraszt_szamitas_helyes():
    assert round(kontraszt("#000000", "#ffffff"), 1) == 21.0
    assert round(kontraszt("#777777", "#ffffff"), 2) == 4.48


@pytest.mark.parametrize("csoport", list(arculat.CSOPORTOK))
def test_a_csoportszinek_olvashatok_feher_szoveggel_es_a_hatteren(csoport):
    szin = arculat.CSOPORTOK[csoport]
    assert kontraszt(szin, "#ffffff") >= 4.5
    assert kontraszt(szin, arculat.HATTER) >= 4.5


def test_a_szoveg_a_kiemeles_es_a_dobozok_olvashatok():
    assert kontraszt(arculat.SZOVEG, arculat.HATTER) >= 7
    assert kontraszt(arculat.SZOVEG, TEMA["secondaryBackgroundColor"]) >= 7
    assert kontraszt(arculat.SZOVEG, CONFIG["theme"]["sidebar"]["backgroundColor"]) >= 7
    assert kontraszt(arculat.SZOVEG, arculat.HALVANY) >= 7
    assert kontraszt(arculat.SZOVEG, arculat.KARTYA) >= 7
    assert kontraszt(arculat.KIEMELES, arculat.HATTER) >= 4.5
    assert kontraszt(TEMA["blueTextColor"], TEMA["blueBackgroundColor"]) >= 4.5
    assert all(kontraszt(sz, "#ffffff") >= 4.5 for sz in arculat.NYITOSAV)


def test_egy_vilagos_tema_a_modul_szineivel():
    assert TEMA["base"] == "light"
    assert "light" not in TEMA and "dark" not in TEMA, "sötét mód nincs: egyetlen téma"
    assert TEMA["primaryColor"] == TEMA["linkColor"] == arculat.KIEMELES
    assert TEMA["textColor"] == arculat.SZOVEG
    assert TEMA["backgroundColor"] == arculat.HATTER


def test_az_animacio_sem_valt_sotet_modra():
    css = (GYOKER / "animacio" / "jelenet.css").read_text(encoding="utf-8")
    assert "prefers-color-scheme" not in css
    assert f"--hatter: {arculat.HATTER};" in css


def test_a_menu_csoportjai_mind_kapnak_szint():
    forras = (GYOKER / "streamlit_app.py").read_text(encoding="utf-8")
    nevek = set(re.findall(r'^        "([^"]+)": \[', forras, flags=re.MULTILINE)) | {hatter.CSOPORTNEV}
    assert nevek == set(arculat.CSOPORTOK)


def test_a_css_minden_csoport_fejlecet_szinezi():
    css = arculat.css()
    for i, szin in enumerate(arculat.CSOPORTOK.values()):
        assert f".st-key-fejlec-{i} {{ background: {szin}; }}" in css
    assert "opacity: 1" in css  # a Streamlit 0,6-ra halványítja az idézetet


def test_a_nyitosav_escapeli_a_szoveget():
    sav = arculat.nyitosav_html("<b>Cím</b>", "a & b", [(3, "<x>")])
    assert "&lt;b&gt;Cím&lt;/b&gt;" in sav and "a &amp; b" in sav and "&lt;x&gt;" in sav


def _cimkek_es_kulcsok(at: AppTest) -> tuple[list[str], list[str]]:
    kulcsok = []

    def bejar(cs) -> None:
        azon = getattr(getattr(cs, "proto", None), "id", "") or ""
        if "fejlec-" in azon:
            kulcsok.append(azon.rsplit("-", 1)[-1])
        for gy in getattr(cs, "children", {}).values():
            bejar(gy)

    bejar(at._tree)
    return [c.value for c in at.caption], kulcsok


@pytest.mark.parametrize(
    ("fajl", "csoport"),
    [
        ("bemutato.py", "Kezdés"),
        ("teendok.py", "A példa — két iteráció"),
        ("backlog.py", "A példa — két iteráció"),
        ("szimulacio.py", "Lejátszás és gyakorlás"),
        ("kutatas.py", "Amire épül"),
    ],
)
def test_az_oldalfejlec_a_menucsoport_szinet_kapja(fajl, csoport):
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.switch_page(f"app_pages/{fajl}")
    at.run()
    assert not at.exception
    cimkek, kulcsok = _cimkek_es_kulcsok(at)
    assert cimkek[0] == csoport
    assert kulcsok == [str(list(arculat.CSOPORTOK).index(csoport))]
