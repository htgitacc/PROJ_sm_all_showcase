"""A bírálati keret számításának tesztjei.

A koncepció fél dokumentumon át arról szól, hogy a teszt nem opcionális, és hogy
a lefedettség nem elég. Egy tesztek nélküli prototípus aláásná a saját anyagát.
"""

from __future__ import annotations

import pytest

from modell import kapacitas
from modell.betoltes import betolt


@pytest.fixture(scope="module")
def adatok():
    return betolt()


def test_keplet_alapeset():
    """(R × 60 / t) × 2 / (1 + r) — a koncepció [00-mukodesi-modell.md] képlete."""
    k = kapacitas.szamol(R=3.0, t=60, r=0.5, napok=3)
    assert k.esemeny_per_szenior_nap == pytest.approx(3.0)
    assert k.esemeny_per_nap == pytest.approx(6.0)
    assert k.elem_per_nap == pytest.approx(4.0)
    assert k.elem_per_iteracio == pytest.approx(12.0)


def test_hosszabb_biralat_kevesebb_elem():
    """Ha a bírálat tovább tart, kevesebb elem fér a keretbe — ez a modell lényege."""
    gyors = kapacitas.szamol(R=3.0, t=60, r=0.5, napok=3)
    lassu = kapacitas.szamol(R=3.0, t=120, r=0.5, napok=3)
    assert lassu.elem_per_iteracio < gyors.elem_per_iteracio


def test_tobb_javitasi_kor_kevesebb_elem():
    keves = kapacitas.szamol(R=3.0, t=60, r=0.2, napok=3)
    sok = kapacitas.szamol(R=3.0, t=60, r=1.0, napok=3)
    assert sok.elem_per_iteracio < keves.elem_per_iteracio


def test_ervenytelen_parameter():
    with pytest.raises(ValueError):
        kapacitas.szamol(R=3.0, t=0, r=0.5, napok=3)
    with pytest.raises(ValueError):
        kapacitas.szamol(R=3.0, t=60, r=-0.1, napok=3)


# --- A példa adataira vonatkozó rögzített értékek --------------------------------
# Ezek a számok a koncepció [07-iteracios-pelda.md] dokumentumában is szerepelnek.
# Ha a példa adatai elmozdulnak, ezek a tesztek elbuknak, és a dokumentumot is
# frissíteni kell.


def test_elso_iteracio_mert_parameterei(adatok):
    m = kapacitas.mert_parameterek(adatok.esemenyek, adatok.iteracio(1))
    assert m["biralatok"] == 13
    assert m["beolvadt"] == 8
    assert m["t"] == pytest.approx(90.0)
    assert m["r"] == pytest.approx(0.625, abs=0.001)
    assert m["R"] == pytest.approx(3.25, abs=0.01)


def test_elso_iteracio_kapacitasa_nyolc_elem(adatok):
    """Az 1. iteráció mért értékeiből a 2. iteráció vállalása 8 elem lesz."""
    m = kapacitas.mert_parameterek(adatok.esemenyek, adatok.iteracio(1))
    k = kapacitas.szamol(m["R"], m["t"], m["r"], napok=3)
    assert k.elem_per_iteracio == pytest.approx(8.0, abs=0.1)
    assert adatok.iteracio(2)["vallalt"] == 8


def test_masodik_iteracio_mert_parameterei(adatok):
    m = kapacitas.mert_parameterek(adatok.esemenyek, adatok.iteracio(2))
    assert m["biralatok"] == 12
    assert m["beolvadt"] == 9
    assert m["t"] == pytest.approx(82.0)


def test_elso_koros_elfogadas(adatok):
    """37,5% majd 57% — a javuló irány, amelyből két iteráció alapján nem lehet trendet mondani."""
    elso = kapacitas.elso_koros_elfogadas(adatok.esemenyek, adatok.elemek, adatok.iteracio(1))
    masodik = kapacitas.elso_koros_elfogadas(adatok.esemenyek, adatok.elemek, adatok.iteracio(2))
    assert elso["arany"] == pytest.approx(0.375, abs=0.001)
    assert masodik["arany"] == pytest.approx(0.571, abs=0.001)


def test_terheles_kiegyensulyozott(adatok):
    """A két szenior között nincs tartós egyenetlenség egyik iterációban sem."""
    kuszob = adatok.konfig["terheles_egyenetlenseg_kuszob"]
    for it in adatok.iteraciok:
        eloszlas = kapacitas.terheles_eloszlas(adatok.esemenyek, it)
        assert max(eloszlas.values()) <= kuszob
