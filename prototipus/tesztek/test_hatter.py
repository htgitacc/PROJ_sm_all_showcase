"""Az „Amire épül” menücsoport: a háttéranyag csoportonként külön nézetben.

A Dokumentumok nézet egyetlen legördülője helyett a brief, a kutatás, a koncepció és a spike-ok
saját nézetet kapnak. Ezek a tesztek azt őrzik, hogy minden dokumentum pontosan egy nézetben
nyílik meg, és hogy a dokumentumok közti hivatkozások a cél saját nézetébe visznek — a megszűnt
Dokumentumok nézetre semmi nem mutat.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from modell import dokumentumok, hatter

GYOKER = Path(__file__).resolve().parent.parent
KATALOGUS = {d.azonosito: d for d in dokumentumok.katalogus()}
LINK = re.compile(r"\]\(([a-z]+)\?dok=([^)&]+)")


def test_minden_dokumentumcsoport_pontosan_egy_nezetben_van():
    csoportok = [cs for n in hatter.NEZETEK for cs in n.csoportok]
    assert sorted(csoportok) == sorted(dokumentumok.CSOPORTOK)


def test_minden_nezetnek_van_oldala_es_letezo_alapertelmezett_dokumentuma():
    for n in hatter.NEZETEK:
        assert (GYOKER / "app_pages" / f"{n.oldal}.py").is_file(), n.oldal
        assert n.alapertelmezett in KATALOGUS, n.alapertelmezett
        assert hatter.nezet(n.alapertelmezett) == n


def test_a_csoportok_a_megfelelo_nezetbe_kerulnek():
    assert hatter.nezet("brief").oldal == "kiindulas"
    assert hatter.nezet("kutatas/forrasok").oldal == "kutatas"
    assert hatter.nezet("koncepcio/02-minosegi-kapuk").oldal == "koncepcio"
    assert hatter.nezet("koncepcio/sablonok/AGENTS").oldal == "koncepcio"
    assert hatter.nezet("spike/01-ugynok-architektura/README").oldal == "spike"


@pytest.mark.parametrize("azonosito", sorted(KATALOGUS))
def test_a_belso_hivatkozas_a_cel_sajat_nezetebe_visz(azonosito):
    dok = KATALOGUS[azonosito]
    ki = hatter.linkek(hatter.belso_hivatkozasok(dok.fajl.read_text(encoding="utf-8"), dok.ut, KATALOGUS))
    assert "dokumentumok?" not in ki and "](?dok=" not in ki
    for oldal, cel in LINK.findall(ki):
        assert cel in KATALOGUS, (azonosito, cel)
        assert oldal == hatter.nezet(cel).oldal, (azonosito, oldal, cel)


def test_a_forrashivatkozas_a_kutatas_nezet_forrasjegyzekebe_visz():
    assert hatter.linkek("lásd S-26") == "lásd [S-26](kutatas?dok=kutatas/forrasok&forras=S-26)"
    assert hatter.FORRASJEGYZEK == "kutatas?dok=kutatas/forrasok"


def test_a_menu_a_regi_hatter_csoport_helyett_a_nezeteket_mutatja():
    assert not (GYOKER / "app_pages" / "dokumentumok.py").exists()
    forras = (GYOKER / "streamlit_app.py").read_text(encoding="utf-8")
    assert "hatter.CSOPORTNEV" in forras and '"Háttér"' not in forras
    # Telefonon a menü az oldalsávba kerül; kibontva nem bújik nézet „View more” mögé.
    assert "expanded=True" in forras


@pytest.mark.parametrize("nezet", hatter.NEZETEK, ids=lambda n: n.oldal)
def test_minden_nezet_hiba_nelkul_megnyitja_az_alapertelmezett_dokumentumot(nezet):
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=30)
    at.switch_page(f"app_pages/{nezet.oldal}.py")
    at.run()
    assert not at.exception
    cim = KATALOGUS[nezet.alapertelmezett].cim
    assert any(f"# {cim}" in m.value for m in at.markdown), cim
    # Egydokumentumos nézetben (Kiindulás) nincs választó, a többiben csak a saját csoport.
    if nezet.oldal == "kiindulas":
        assert not at.selectbox
    else:
        sajat = [a for a, d in KATALOGUS.items() if d.csoport in nezet.csoportok]
        assert len(at.selectbox[0].options) == len(sajat)
        assert at.selectbox[0].value == nezet.alapertelmezett


def test_a_bevezetes_gombja_a_kutatas_nezetben_nyitja_a_forrasjegyzeket():
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=30)
    at.run()
    next(b for b in at.button if b.key == "dok_kutatas/forrasok").click().run()
    assert not at.exception
    assert at.selectbox[0].value == "kutatas/forrasok"
    assert any("### S-26 — " in m.value for m in at.markdown)
