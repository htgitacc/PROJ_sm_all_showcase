"""A példa kulcspillanatai — az időkurzor és az animáció közös ugrópontjai.

Azért külön modulban él, mert három helyről kell ugyanaz a lista: az
időkurzor oldalsávjából, az animáció fejezeteiből és az exportálóból.
Két külön másolat némán elcsúszna egymástól.
"""

from __future__ import annotations

import pandas as pd


def esemeny_index(
    esemenyek: pd.DataFrame,
    esemeny: str,
    elem: str = "",
    idopont: str = "",
) -> int:
    """Az első olyan esemény sorszáma, amely illeszkedik a megadott szűrőre."""
    maszk = esemenyek["esemeny"] == esemeny
    if elem:
        maszk &= esemenyek["elem_id"] == elem
    if idopont:
        maszk &= esemenyek["idopont"] == pd.Timestamp(idopont)
    talalat = esemenyek[maszk]
    return int(talalat.index[0]) if not talalat.empty else 0


def _pelda_naplo(esemenyek: pd.DataFrame) -> bool:
    """A koncepció 07. dokumentumának naplója-e, vagy egy szimulált iteráció.

    A példa kulcspillanatai konkrét elemekhez és időpontokhoz kötődnek; egy
    szimulált naplóban ezek nem léteznek, ott általános fejezetek kellenek.
    """
    maszk = (
        (esemenyek["esemeny"] == "biralatra_kerult")
        & (esemenyek["elem_id"] == "I1-7")
        & (esemenyek["idopont"] == pd.Timestamp("2026-09-03 13:20"))
    )
    return bool(maszk.any())


def _altalanos_fejezetek(esemenyek: pd.DataFrame) -> dict[str, int]:
    """Eseménytípusból levezetett fejezetek tetszőleges naplóhoz."""
    fejezetek = {"Iteráció eleje": 0}
    keresendo = [
        ("Első beolvasztás", "biralat_jovahagyva"),
        ("Ügynökök leállítva", "ugynok_leallitva"),
        ("Méretkorlát", "meretkorlat_tullepes"),
        ("Visszatekintés", "retro_gepi"),
    ]
    for cimke, esemeny in keresendo:
        talalat = esemenyek[esemenyek["esemeny"] == esemeny]
        if not talalat.empty:
            fejezetek[cimke] = int(talalat.index[0])
    fejezetek["Jelen állapot"] = len(esemenyek) - 1
    return fejezetek


def konyvjelzok(esemenyek: pd.DataFrame) -> dict[str, int]:
    """Címke → eseményindex. A pillanatok a koncepció 07. dokumentumából valók."""
    if not _pelda_naplo(esemenyek):
        return _altalanos_fejezetek(esemenyek)

    utolso = len(esemenyek) - 1
    return {
        "Iteráció eleje": 0,
        "Torlódás (1. it., 2. nap)": esemeny_index(
            esemenyek, "biralatra_kerult", "I1-7", "2026-09-03 13:20"
        ),
        "Paramétereltérés (1. it. vége)": esemeny_index(esemenyek, "retro_emberi"),
        "Méretkorlát (2. it., 2. nap)": esemeny_index(
            esemenyek, "meretkorlat_tullepes", "I2-6"
        ),
        "Visszatérő hibaosztály (2. it.)": esemeny_index(
            esemenyek, "talalat_elfogadva", "I2-7"
        ),
        "Jelen állapot": utolso,
    }
