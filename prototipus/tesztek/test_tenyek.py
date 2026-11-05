"""A döntések tényeinek típusai.

A cél az, hogy egy hiányzó vagy elgépelt mező a `Dontes` LÉTREHOZÁSAKOR derüljön ki,
ne a felület egy távoli olvasásánál (2026-09-16: `KeyError: 'sulyos'`).
"""

from __future__ import annotations

import dataclasses

import pytest

from modell import szimulacio as szim


def _dontes(kod: str, tenyek) -> szim.Dontes:
    return szim.Dontes(kod=kod, cim="c", magyarazat="m", valasztasok=[], tenyek=tenyek)


def test_minden_dontestipushoz_tartozik_tenyek_osztaly():
    assert set(szim.TENYEK_TIPUSA) == {"vallalas", "beolvasztas", "torlodas", "meretkorlat", "visszatekintes"}


def test_hianyzo_mezo_a_letrehozaskor_hibat_ad():
    with pytest.raises(TypeError):
        szim.TorlodasTenyek(varakozok=3)  # a `korlat` hiányzik


def test_elgepelt_mezo_a_letrehozaskor_hibat_ad():
    with pytest.raises(TypeError):
        szim.TorlodasTenyek(varakozok=3, korlatt=4)


def test_a_dontes_tipusa_es_a_tenyek_tipusa_egyezni_kell():
    ok = szim.TorlodasTenyek(varakozok=3, korlat=4)
    _dontes("torlodas", ok)
    with pytest.raises(TypeError):
        _dontes("meretkorlat", ok)


def test_ismeretlen_dontestipus_hibat_ad():
    with pytest.raises(ValueError):
        _dontes("nincs_ilyen", szim.TorlodasTenyek(varakozok=1, korlat=1))


def test_a_tenyek_attributumkent_olvashatok_a_szotar_alak_megszunt():
    t = szim.MeretkorlatTenyek(meret_sor=310, korlat=200)
    assert t.meret_sor == 310 and t.korlat == 200
    with pytest.raises(TypeError):
        t["meret_sor"]
    with pytest.raises(AttributeError):
        t.nincs_ilyen


def test_a_tenyek_valtoztathatatlanok():
    t = szim.TorlodasTenyek(varakozok=1, korlat=1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        t.korlat = 9


def test_a_szimulacio_minden_dontese_tipusos_tenyeket_hordoz():
    """Végigjátszott futamon minden keletkezett döntés a saját típusát hordozza."""
    allas = szim.indit(mag=11)
    latott: set[str] = set()
    for _ in range(80):
        d = allas.dontes
        if d is None:
            break
        assert isinstance(d.tenyek, szim.TENYEK_TIPUSA[d.kod])
        latott.add(d.kod)
        allas = szim.dont(allas, d.valasztasok[0].kod)
    assert len(latott) >= 3
