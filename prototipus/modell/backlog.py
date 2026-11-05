"""A backlog nézet adatai: mit tudunk előre egy-egy elemről?

Két backlog van: a *példa* két lezárt iterációjának elemei (`adatok/elemek.csv`, az
eseménynaplóval), és a *szimuláció* kiosztatlan készlete (`adatok/szimulacio/backlog.csv`).
A célt és az elfogadási feltételeket kitalált mintaszöveg adja (`adatok/backlog_leirasok.json`),
mert a darabolás kimenete a koncepció szerint tartalmazná, a példaadat viszont nem rögzíti.

A Definition of Done a koncepció sablonjából jön (`koncepcio/sablonok/definition-of-done.md`),
nem másolat: ha a sablon változik, a nézet vele változik.
A Definition of Ready-nek nincs külön dokumentuma; a koncepció 01. dokumentumának
jóváhagyási kapuja adja (értelmezhető-lezárható egység, ellenőrizhető elfogadási feltétel,
méretkorlát), elemenként kiértékelve.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

ADATOK = Path(__file__).resolve().parents[1] / "adatok"
DOD_SABLON = Path(__file__).resolve().parents[2] / "koncepcio" / "sablonok" / "definition-of-done.md"


def leirasok() -> dict:
    """Cél és elfogadási feltételek: {'pelda': {elem_id: …}, 'szimulacio': {cím: …}}."""
    return json.loads((ADATOK / "backlog_leirasok.json").read_text(encoding="utf-8"))


def szimulacios_keszlet() -> pd.DataFrame:
    return pd.read_csv(ADATOK / "szimulacio" / "backlog.csv")


# --- Definition of Done ----------------------------------------------------------


@dataclass(frozen=True)
class DodBlokk:
    cim: str
    pontok: list[str]
    feltetel: str = ""  # üres: minden elemre vonatkozik


def _dod_blokkok() -> list[DodBlokk]:
    """A sablon szakaszai: a „Minden elemre” alszakaszai, majd a feltételes szakaszok."""
    szoveg = DOD_SABLON.read_text(encoding="utf-8")
    blokkok: list[DodBlokk] = []
    szakasz = alszakasz = ""
    for sor in szoveg.splitlines():
        if sor.startswith("## "):
            szakasz, alszakasz = sor[3:].strip(), ""
        elif sor.startswith("### "):
            alszakasz = sor[4:].strip()
        elif sor.startswith("- [ ] "):
            pont = re.sub(r"\*\*|\*", "", sor[6:]).strip()
            if szakasz == "Minden elemre":
                cim, feltetel = alszakasz, ""
            elif szakasz.startswith("Ha az elem"):
                cim, feltetel = szakasz, szakasz
            else:
                continue
            if blokkok and blokkok[-1].cim == cim:
                blokkok[-1].pontok.append(pont)
            else:
                blokkok.append(DodBlokk(cim, [pont], feltetel))
    return blokkok


def dod(magas_kockazat: bool, refaktoralas: bool) -> list[DodBlokk]:
    """Az elemre vonatkozó DoD-blokkok: az általános, majd a feltételes szakaszok."""
    ki = []
    for blokk in _dod_blokkok():
        if not blokk.feltetel:
            ki.append(blokk)
        elif "magas kockázatú" in blokk.feltetel and magas_kockazat:
            ki.append(blokk)
        elif "refaktorálás" in blokk.feltetel and refaktoralas:
            ki.append(blokk)
    return ki


def refaktoralas_e(cim: str) -> bool:
    return "refaktorálás" in cim.lower()


# --- Definition of Ready ---------------------------------------------------------


@dataclass(frozen=True)
class DorPont:
    allapot: str  # "igen" | "nem" | "nyitott"
    szoveg: str
    megjegyzes: str = ""


def dor(
    ac_darab: int,
    meret_sor: int | None,
    meretkorlat: int,
    spec_jovahagyva: bool | None,
) -> list[DorPont]:
    """A „kész a kezdésre” feltételei; ami még nem dönthető el, az „nyitott”."""
    if spec_jovahagyva is None:
        spec = DorPont("nyitott", "A specifikációt ember jóváhagyta", "a vállaláskor dől el")
    elif spec_jovahagyva:
        spec = DorPont("igen", "A specifikációt ember jóváhagyta", "az eseménynapló rögzíti")
    else:
        spec = DorPont("nem", "A specifikációt ember jóváhagyta")

    if not meret_sor:
        meret = DorPont(
            "nyitott",
            f"A változtatás mérete belefér a {meretkorlat} sorba",
            "a méret a megvalósításkor derül ki",
        )
    elif meret_sor <= meretkorlat:
        meret = DorPont("igen", f"A változtatás mérete belefér a {meretkorlat} sorba", f"{meret_sor} sor")
    else:
        meret = DorPont(
            "nem", f"A változtatás mérete belefér a {meretkorlat} sorba", f"{meret_sor} sor, bontani kell"
        )

    return [
        DorPont(
            "igen" if ac_darab else "nem",
            "Az elfogadási feltételek ellenőrizhetők és le vannak írva",
            f"{ac_darab} feltétel" if ac_darab else "nincs rögzítve",
        ),
        meret,
        spec,
    ]


# --- A példa elemei --------------------------------------------------------------


def elem_tortenet(esemenyek: pd.DataFrame, elem_id: str) -> pd.DataFrame:
    return esemenyek[esemenyek["elem_id"] == elem_id][["idopont", "esemeny", "szereplo", "reszlet"]]


def spec_jovahagyva(esemenyek: pd.DataFrame, elem_id: str) -> bool:
    mask = (esemenyek["elem_id"] == elem_id) & (esemenyek["esemeny"] == "spec_jovahagyva")
    return bool(mask.any())
