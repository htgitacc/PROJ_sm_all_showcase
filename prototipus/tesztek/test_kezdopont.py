"""A példa az elejéről indul, és a „Most” helyett „Teendők” a nézet neve.

A felhasználó jelezte: a kurzor a 136. eseménynél, a végén állt, pedig aki először jár itt, az
elejéről játszaná le a folyamatot; a „Most” név pedig azt sugallta, hogy a végét mutatja.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

GYOKER = Path(__file__).resolve().parent.parent
BELEPES = str(GYOKER / "streamlit_app.py")
PILLANAT = ["teendok.py", "iteracio.py", "elorenezes.py", "tanulas.py"]
UTMUTATO = "Az időkurzor a példa **elején** áll"


def _oldal(fajl: str) -> AppTest:
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.switch_page(f"app_pages/{fajl}")
    at.run()
    assert not at.exception
    return at


@pytest.mark.parametrize("fajl", PILLANAT)
def test_a_pillanatnezetek_az_elejerol_indulnak_utmutatoval(fajl):
    at = _oldal(fajl)
    assert at.session_state["kurzor"] == 0
    assert at.sidebar.slider[0].value == 1
    assert any(UTMUTATO in i.value for i in at.info)


def test_az_utmutato_eltunik_ha_elore_lepunk():
    at = _oldal("teendok.py")
    next(b for b in at.sidebar.button if b.key == "kurzor_elore").click().run()
    assert at.session_state["kurzor"] == 1
    assert not any(UTMUTATO in i.value for i in at.info)


def test_kurzor_nelkuli_nezeten_nincs_utmutato():
    assert not any(UTMUTATO in i.value for i in _oldal("backlog.py").info)


def test_a_nezet_neve_teendok():
    assert not (GYOKER / "app_pages" / "most.py").exists()
    at = _oldal("teendok.py")
    assert at.title[0].value.endswith("Teendők")
    forras = (GYOKER / "streamlit_app.py").read_text(encoding="utf-8")
    assert 'title="Most"' not in forras


def test_az_abra_is_1_tol_szamoz_es_a_kurzort_nem_most_nak_hivja():
    from modell import betoltes, grafikonok

    adatok = betoltes.betolt()
    korlat = adatok.konfig["wip_korlatok"]["Bírálatra vár"]
    spec = grafikonok.sor_grafikon(grafikonok.sor_idosor(adatok), korlat, kurzor=0).to_dict()
    szoveg = str(spec)
    assert "'zero': False" in szoveg
    assert "'kurzor'" in szoveg and "'most'" not in szoveg


def test_a_kartyas_tabla_jelmagyarazata_a_csik_valodi_szinet_mondja():
    from modell import grafikonok

    forras = (GYOKER / "modell" / "grafikonok.py").read_text(encoding="utf-8")
    assert "Kék csík" not in forras and "Zöld csík" in forras
    assert grafikonok.KEK != "#2563eb"  # a csík a jáde kiemelőszín, nem a régi kék
