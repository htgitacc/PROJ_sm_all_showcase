"""A bírálati keret számítása.

A koncepció [00-mukodesi-modell.md] képlete:

    bírálati esemény / szenior / nap = R * 60 / t
    bírálati esemény / nap           = ez * 2 (két szenior)
    lezárható elem / nap             = ez / (1 + r)

ahol R a napi bírálati idő órában, t az elemenkénti validálási idő percben,
r pedig az átlagos plusz javítási körök száma.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

BIRALAT_LEZARO = ("biralat_jovahagyva", "biralat_visszakuldve")


@dataclass(frozen=True)
class Kapacitas:
    R: float
    t: float
    r: float
    napok: int
    szeniorok: int
    esemeny_per_szenior_nap: float
    esemeny_per_nap: float
    elem_per_nap: float
    elem_per_iteracio: float


def szamol(R: float, t: float, r: float, napok: int, szeniorok: int = 2) -> Kapacitas:
    if t <= 0:
        raise ValueError("A validálási idő (t) csak pozitív lehet.")
    if r < 0:
        raise ValueError("A javítási körök átlaga (r) nem lehet negatív.")
    per_szenior = R * 60 / t
    per_nap = per_szenior * szeniorok
    elem_per_nap = per_nap / (1 + r)
    return Kapacitas(
        R=R,
        t=t,
        r=r,
        napok=napok,
        szeniorok=szeniorok,
        esemeny_per_szenior_nap=per_szenior,
        esemeny_per_nap=per_nap,
        elem_per_nap=elem_per_nap,
        elem_per_iteracio=elem_per_nap * napok,
    )


def mert_parameterek(
    esemenyek: pd.DataFrame,
    iteracio: dict,
    szeniorok: int = 2,
) -> dict[str, float]:
    """A tényleges paraméterek kiolvasása az eseménynaplóból.

    Csak a lezárt bírálatok számítanak: ezekhez tartozik mért időtartam.
    """
    kezdet = pd.Timestamp(iteracio["kezdet"])
    veg = pd.Timestamp(iteracio["veg"]) + pd.Timedelta(days=1)
    ablak = esemenyek[(esemenyek["idopont"] >= kezdet) & (esemenyek["idopont"] < veg)]

    biralatok = ablak[ablak["esemeny"].isin(BIRALAT_LEZARO)]
    beolvadt = ablak[ablak["esemeny"] == "biralat_jovahagyva"]

    n_biralat = len(biralatok)
    n_beolvadt = len(beolvadt)
    if n_biralat == 0 or n_beolvadt == 0:
        return {"R": 0.0, "t": 0.0, "r": 0.0, "biralatok": 0, "beolvadt": 0}

    ossz_perc = float(biralatok["biralati_perc"].sum())
    napok = int(iteracio["napok"])

    return {
        "R": round(ossz_perc / (szeniorok * napok) / 60, 2),
        "t": round(ossz_perc / n_biralat, 1),
        "r": round(n_biralat / n_beolvadt - 1, 3),
        "biralatok": n_biralat,
        "beolvadt": n_beolvadt,
    }


def terheles_eloszlas(esemenyek: pd.DataFrame, iteracio: dict) -> dict[str, float]:
    """Melyik szenior mennyi bírálati időt vitt el. Terheléskövetés, nem értékelés."""
    kezdet = pd.Timestamp(iteracio["kezdet"])
    veg = pd.Timestamp(iteracio["veg"]) + pd.Timedelta(days=1)
    ablak = esemenyek[(esemenyek["idopont"] >= kezdet) & (esemenyek["idopont"] < veg)]
    biralatok = ablak[ablak["esemeny"].isin(BIRALAT_LEZARO)]
    if biralatok.empty:
        return {}
    ossz = biralatok.groupby("szereplo")["biralati_perc"].sum()
    return (ossz / ossz.sum()).round(3).to_dict()


def elso_koros_elfogadas(esemenyek: pd.DataFrame, elemek: pd.DataFrame, iteracio: dict) -> dict:
    """Hány vállalt elem ment át javítás nélkül."""
    kezdet = pd.Timestamp(iteracio["kezdet"])
    veg = pd.Timestamp(iteracio["veg"]) + pd.Timedelta(days=1)
    ablak = esemenyek[(esemenyek["idopont"] >= kezdet) & (esemenyek["idopont"] < veg)]

    vallalt = set(
        elemek[(elemek["iteracio"] == iteracio["id"]) & (elemek["vallalt"] == "igen")]["elem_id"]
    )
    # A visszabontott elem gyermekei a szülő nevében szerepelnek.
    szulo = dict(zip(elemek["elem_id"], elemek["szulo"]))

    def gyoker(elem_id: str) -> str:
        return szulo.get(elem_id) or elem_id

    beolvadt = {gyoker(e) for e in ablak[ablak["esemeny"] == "biralat_jovahagyva"]["elem_id"]}
    javitott = {gyoker(e) for e in ablak[ablak["esemeny"] == "biralat_visszakuldve"]["elem_id"]}
    visszabontott = {gyoker(e) for e in ablak[ablak["esemeny"] == "visszabontva"]["elem_id"]}

    lezart = beolvadt & vallalt
    elso_korben = lezart - javitott - visszabontott
    return {
        "lezart": len(lezart),
        "elso_korben": len(elso_korben),
        "arany": round(len(elso_korben) / len(lezart), 3) if lezart else 0.0,
    }
