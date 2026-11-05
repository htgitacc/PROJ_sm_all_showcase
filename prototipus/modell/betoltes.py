"""Adatbetöltés és -ellenőrzés.

Ez a modul szándékosan nem függ a Streamlittől, hogy tesztelhető maradjon.
A gyorsítótárazás a beépülő oldalon (streamlit_app.py) történik.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass

import pandas as pd

ADATOK_MAPPA = pathlib.Path(__file__).resolve().parent.parent / "adatok"


@dataclass(frozen=True)
class Adatok:
    konfig: dict
    iteraciok: list[dict]
    elemek: pd.DataFrame
    esemenyek: pd.DataFrame
    hibaosztalyok: pd.DataFrame
    szabalyok: pd.DataFrame
    koltseg: pd.DataFrame

    def iteracio(self, azonosito: int) -> dict:
        for it in self.iteraciok:
            if it["id"] == azonosito:
                return it
        raise KeyError(f"Nincs ilyen iteráció: {azonosito}")


def betolt(mappa: pathlib.Path | str = ADATOK_MAPPA) -> Adatok:
    mappa = pathlib.Path(mappa)

    with open(mappa / "iteraciok.json", encoding="utf-8") as f:
        meta = json.load(f)

    esemenyek = pd.read_csv(mappa / "esemenyek.csv")
    esemenyek["idopont"] = pd.to_datetime(esemenyek["idopont"])
    esemenyek["elem_id"] = esemenyek["elem_id"].fillna("")
    esemenyek["hibaosztaly"] = esemenyek["hibaosztaly"].fillna("")
    esemenyek["reszlet"] = esemenyek["reszlet"].fillna("")
    esemenyek = esemenyek.sort_values("idopont", kind="stable").reset_index(drop=True)

    elemek = pd.read_csv(mappa / "elemek.csv")
    elemek["szulo"] = elemek["szulo"].fillna("")

    adatok = Adatok(
        konfig=meta["konfiguracio"],
        iteraciok=meta["iteraciok"],
        elemek=elemek,
        esemenyek=esemenyek,
        hibaosztalyok=pd.read_csv(mappa / "hibaosztalyok.csv"),
        szabalyok=pd.read_csv(mappa / "szabalyok.csv").fillna(""),
        koltseg=pd.read_csv(mappa / "koltseg.csv"),
    )
    ellenoriz(adatok)
    return adatok


def ellenoriz(adatok: Adatok) -> None:
    """Alapvető épségvizsgálat. Hibás adatnál azonnal megáll, nem csendben téved."""
    ismert_elemek = set(adatok.elemek["elem_id"])
    hasznalt = {e for e in adatok.esemenyek["elem_id"] if e}
    if hiany := hasznalt - ismert_elemek:
        raise ValueError(f"Az eseménynaplóban ismeretlen elem szerepel: {sorted(hiany)}")

    ismert_ho = set(adatok.hibaosztalyok["kod"])
    hasznalt_ho = {h for h in adatok.esemenyek["hibaosztaly"] if h}
    if hiany := hasznalt_ho - ismert_ho:
        raise ValueError(f"Ismeretlen hibaosztály az eseménynaplóban: {sorted(hiany)}")

    # Minden lezárt bírálathoz tartozzon megkezdett bírálat.
    kezdesek: dict[str, int] = {}
    for _, sor in adatok.esemenyek.iterrows():
        if sor["esemeny"] == "biralat_indult":
            kezdesek[sor["elem_id"]] = kezdesek.get(sor["elem_id"], 0) + 1
        elif sor["esemeny"] in ("biralat_jovahagyva", "biralat_visszakuldve"):
            if kezdesek.get(sor["elem_id"], 0) < 1:
                raise ValueError(
                    f"Bírálat lezárása megkezdés nélkül: {sor['elem_id']} @ {sor['idopont']}"
                )
            kezdesek[sor["elem_id"]] -= 1

    # A beolvasztásnak mindig van megnevezett emberi jóváhagyója — ez a modell alapszabálya.
    szeniorok = set(adatok.konfig["szeniorok"])
    beolvadt = adatok.esemenyek[adatok.esemenyek["esemeny"] == "biralat_jovahagyva"]
    nevtelen = beolvadt[~beolvadt["szereplo"].isin(szeniorok)]
    if not nevtelen.empty:
        raise ValueError(
            "Beolvasztás megnevezett emberi jóváhagyó nélkül: "
            f"{nevtelen['elem_id'].tolist()}"
        )
