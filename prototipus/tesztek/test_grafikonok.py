"""Az ábrák tesztjei: ugyanazt mutatják-e, mint az állapot, amelyből rajzolnak.

Egy ábra akkor félrevezető, ha más számot mutat, mint a táblázat mellette. Ezek a tesztek
a példa kulcspillanataiban vetik össze az ábrák adatait az `allapot.pillanat()`-tal.
"""

from __future__ import annotations

import pytest

from modell import allapot, grafikonok, konyvjelzok, tanulas
from modell.betoltes import betolt


@pytest.fixture(scope="module")
def adatok():
    return betolt()


@pytest.fixture(scope="module")
def idosor(adatok):
    return grafikonok.sor_idosor(adatok)


@pytest.fixture(scope="module")
def kj(adatok):
    return konyvjelzok.konyvjelzok(adatok.esemenyek)


def _p(adatok, i):
    return allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, i)


def test_az_idosor_minden_eseményre_van_es_egyezik_az_allapottal(adatok, idosor, kj):
    assert len(idosor) == len(adatok.esemenyek)
    for i in kj.values():
        assert idosor.loc[i, "varakozo"] == len(_p(adatok, i).oszlop("Bírálatra vár"))


def test_a_torlodas_pillanataban_a_sor_a_korlat_folott_van(adatok, idosor, kj):
    korlat = adatok.konfig["wip_korlatok"]["Bírálatra vár"]
    assert idosor.loc[kj["Torlódás (1. it., 2. nap)"], "varakozo"] > korlat
    assert idosor["varakozo"].max() > korlat


def test_a_grafikon_felepul_kurzorral_es_jelolokkel(adatok, idosor, kj):
    ch = grafikonok.sor_grafikon(idosor, 4, kurzor=30, jelolok=kj)
    spec = ch.to_dict()
    assert len(spec["layer"]) >= 6


def test_a_tabla_a_torlodasnal_jelzi_a_korlat_folotti_oszlopot(adatok, kj):
    p = _p(adatok, kj["Torlódás (1. it., 2. nap)"])
    h = grafikonok.tabla_html(p.elemallapot, adatok.konfig["wip_korlatok"], adatok.konfig["meretkorlat_sor"])
    assert "osz tul" in h and "korlát felett" in h
    for eid in p.oszlop("Bírálatra vár")["elem_id"]:
        assert f">{eid}<" in h


def test_a_tabla_pirossal_jeloli_a_meretkorlat_feletti_elemet(adatok, kj):
    p = _p(adatok, kj["Méretkorlát (2. it., 2. nap)"])
    h = grafikonok.tabla_html(p.elemallapot, adatok.konfig["wip_korlatok"], adatok.konfig["meretkorlat_sor"])
    assert 'class="k nagy"' in h and ">I2-6<" in h


def test_a_tabla_a_korlaton_belul_nem_jelez(adatok, kj):
    p = _p(adatok, kj["Iteráció eleje"])
    h = grafikonok.tabla_html(p.elemallapot, adatok.konfig["wip_korlatok"], adatok.konfig["meretkorlat_sor"])
    assert "osz tul" not in h


def test_a_letra_minden_fokot_mutat_es_a_foglaltakat_kiemeli():
    h = grafikonok.letra_html(tanulas.LETRA, {3: 1, 1: 2})
    for fok in tanulas.LETRA:
        assert f"{fok}. fok" in h
    assert "1 hibaosztály" in h and "2 hibaosztály" in h


def test_a_keret_sav_jelzi_a_tulvallalast():
    assert "túlvállalás" in grafikonok.keret_sav_html(12, 10.3)
    assert "túlvállalás" not in grafikonok.keret_sav_html(9, 10.3)


def test_a_parameter_elteres_a_t_novekedeset_szukitokent_mutatja():
    ch = grafikonok.parameter_elteres_grafikon({"R": 3.0, "t": 70, "r": 0.5}, {"R": 3.25, "t": 90, "r": 0.625})
    sorok = {s["Paraméter"]: s for s in ch.to_dict()["datasets"][next(iter(ch.to_dict()["datasets"]))]}
    t = sorok["Egy elem átnézése (t)"]
    assert t["Eltérés (%)"] == pytest.approx(28.6, abs=0.1) and t["Hatás"] == "szűkíti a keretet"
    assert sorok["Napi bírálati idő (R)"]["Hatás"] == "bővíti vagy semleges"
