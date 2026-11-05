"""A Backlog nézet és adatainak tesztjei."""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from modell import backlog
from modell.betoltes import betolt

GYOKER = Path(__file__).resolve().parent.parent
# A szimulációs backlog típus–kockázat–bonyolultság oszlopainak ujjlenyomata (2026-10-17).
UJJLENYOMAT = "c27593fc6937ea68"


@pytest.fixture(scope="module")
def adatok():
    return betolt()


def test_minden_elemnek_van_leirasa_es_elfogadasi_felteteli(adatok):
    leir = backlog.leirasok()
    assert set(leir["pelda"]) == set(adatok.elemek["elem_id"])
    assert set(leir["szimulacio"]) == set(backlog.szimulacios_keszlet()["cim"])
    for csoport in ("pelda", "szimulacio"):
        for kulcs, d in leir[csoport].items():
            assert d["cel"].strip(), kulcs
            assert len(d["elfogadasi_feltetelek"]) >= 2, kulcs


def test_a_dod_a_sablonbol_jon_es_a_feltetelek_szerint_bovul():
    alap = backlog.dod(False, False)
    magas = backlog.dod(True, False)
    refakt = backlog.dod(False, True)
    assert [b.cim for b in alap] == ["Funkcionális megfelelés", "Tesztek", "Biztonság", "Méret és felelősség"]
    assert len(magas) == len(alap) + 1 and "magas kockázatú" in magas[-1].cim
    assert len(refakt) == len(alap) + 1 and "refaktorálás" in refakt[-1].cim
    assert all(b.pontok for b in alap)


def test_a_dor_a_meretet_az_elem_adatabol_ertekeli():
    ok = backlog.dor(3, 150, 200, True)
    assert [p.allapot for p in ok] == ["igen", "igen", "igen"]
    tul = backlog.dor(3, 310, 200, True)
    assert tul[1].allapot == "nem" and "bontani" in tul[1].megjegyzes
    kesz = backlog.dor(3, None, 200, None)
    assert kesz[1].allapot == "nyitott" and kesz[2].allapot == "nyitott"
    assert backlog.dor(0, 100, 200, True)[0].allapot == "nem"


def test_az_i2_6_a_dor_szerint_nem_volt_kesz_a_kezdesre(adatok):
    sor = adatok.elemek.set_index("elem_id").loc["I2-6"]
    dor = backlog.dor(3, int(sor["meret_sor"]), adatok.konfig["meretkorlat_sor"], True)
    assert dor[1].allapot == "nem"


def test_az_elem_tortenete_az_eseménynaplóból_jon(adatok):
    t = backlog.elem_tortenet(adatok.esemenyek, "I2-6")
    assert "visszabontva" in set(t["esemeny"])
    assert backlog.spec_jovahagyva(adatok.esemenyek, "I2-6")


def _nezet() -> AppTest:
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=60)
    at.switch_page("app_pages/backlog.py")
    at.run()
    return at


def test_a_backlog_nezet_hiba_nelkul_betolt_es_mutatja_az_ac_t_es_a_dod_t():
    at = _nezet()
    assert not at.exception
    szoveg = "\n".join(m.value for m in at.markdown)
    assert "Elfogadási feltételek (AC)" in szoveg
    assert "Kész a kezdésre? (DoR)" in szoveg
    assert "Kész a lezáráshoz? (DoD)" in szoveg


def test_a_pelda_elemenek_kivalasztasa_a_visszabontast_mutatja():
    at = _nezet()
    at.selectbox(key="backlog_pelda_elem").select("I2-6").run()
    assert not at.exception
    assert any("I2-6a" in i.value for i in at.info)


def test_a_szimulacios_backlog_viselkedest_meghatarozo_oszlopai_valtozatlanok():
    """Az AC-felülvizsgálat (2026-10-17) csak címeket írt át a szimulációs backlogban. A szimuláció
    a típusból, a kockázatból és a bonyolultságból dolgozik; ha ezek sorrendje változna, minden
    forgatókönyv-szám más történetet adna. Ez az ujjlenyomat azt őrzi, hogy ez ne történjen meg véletlenül."""
    import hashlib

    df = backlog.szimulacios_keszlet()
    ujjlenyomat = hashlib.sha256(
        df[["tipus", "magas_kockazat", "bonyolultsag"]].to_csv(index=False).encode()
    ).hexdigest()[:16]
    assert len(df) == 36
    assert ujjlenyomat == UJJLENYOMAT, ujjlenyomat


def test_a_megjegyzes_megjelenik_a_backlog_nezetben():
    at = _nezet()
    at.selectbox(key="backlog_pelda_elem").select("I1-3").run()
    assert not at.exception
    assert any("Szándékos hiány" in i.value for i in at.info)
