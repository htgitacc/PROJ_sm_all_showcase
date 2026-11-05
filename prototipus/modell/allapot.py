"""Az elemek állapotának kiszámítása egy adott időpontra.

Az állapotot mindig az eseménynaplóból származtatjuk, nem tárolt mezőkből.
Ettől működik az időkurzor: bármely korábbi pillanat visszajátszható,
és a demót nem lehet egyetlen szép állapotra „beállítani".
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

ALLAPOT_ATMENET = {
    "spec_jovahagyva": "Kész a kezdésre",
    "ugynok_indult": "Megvalósítás alatt",
    "biralatra_kerult": "Bírálatra vár",
    "biralat_indult": "Bírálat alatt",
    "biralat_visszakuldve": "Javítás alatt",
    "biralat_jovahagyva": "Beolvadt",
    "visszabontva": "Visszabontva",
    "atcsuszott": "Átcsúszott",
    # Az átcsúszott elem a következő iteráció elején visszakerül a táblára. Ez
    # nem új fogalom, hanem visszatérés a folyamat első oszlopába: a félkész
    # munka nem hordozható át, az ügynök újrakezdi.
    "athozva": "Kész a kezdésre",
}

# A folyamat oszlopai, ahogy a WIP-korlátok vonatkoznak rájuk.
WIP_OSZLOPOK = ["Kész a kezdésre", "Megvalósítás alatt", "Bírálatra vár"]

AKTIV_ALLAPOTOK = [
    "Kész a kezdésre",
    "Megvalósítás alatt",
    "Bírálatra vár",
    "Bírálat alatt",
    "Javítás alatt",
]


@dataclass(frozen=True)
class Pillanat:
    """Az adatok állapota egy adott eseményindexnél."""

    index: int
    idopont: pd.Timestamp
    iteracio: int
    esemenyek_eddig: pd.DataFrame
    elemallapot: pd.DataFrame

    def oszlop(self, nev: str) -> pd.DataFrame:
        return self.elemallapot[self.elemallapot["allapot"] == nev]

    def darab(self, nev: str) -> int:
        return int((self.elemallapot["allapot"] == nev).sum())


def iteracio_esemenyhez(esemenyek: pd.DataFrame, iteraciok: list[dict], index: int) -> int:
    """Melyik iterációhoz tartozik az adott indexű esemény."""
    idopont = esemenyek.loc[index, "idopont"]
    for it in iteraciok:
        veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
        if pd.Timestamp(it["kezdet"]) <= idopont < veg:
            return int(it["id"])
    return int(iteraciok[-1]["id"])


def pillanat(
    esemenyek: pd.DataFrame,
    elemek: pd.DataFrame,
    iteraciok: list[dict],
    index: int,
) -> Pillanat:
    """Az `index`-edik esemény lefutása utáni állapot (0-alapú, befoglaló)."""
    eddig = esemenyek.iloc[: index + 1]
    most = esemenyek.loc[index, "idopont"]

    sorok = []
    for _, elem in elemek.iterrows():
        sajat = eddig[eddig["elem_id"] == elem["elem_id"]]
        allapot = None
        allapot_ota = None
        biralo = ""
        for _, e in sajat.iterrows():
            uj = ALLAPOT_ATMENET.get(e["esemeny"])
            if uj is not None:
                allapot = uj
                allapot_ota = e["idopont"]
                biralo = e["szereplo"] if uj in ("Bírálat alatt",) else biralo
        if allapot is None:
            continue
        sorok.append(
            {
                "elem_id": elem["elem_id"],
                "cim": elem["cim"],
                "iteracio": elem["iteracio"],
                "tipus": elem["tipus"],
                "magas_kockazat": elem["magas_kockazat"],
                "meret_sor": elem["meret_sor"],
                "vallalt": elem["vallalt"],
                "allapot": allapot,
                "allapot_ota": allapot_ota,
                "varakozas_ora": round((most - allapot_ota).total_seconds() / 3600, 1),
                "biralo": biralo,
            }
        )

    allapotok = pd.DataFrame(sorok)
    if allapotok.empty:
        allapotok = pd.DataFrame(
            columns=[
                "elem_id", "cim", "iteracio", "tipus", "magas_kockazat", "meret_sor",
                "vallalt", "allapot", "allapot_ota", "varakozas_ora", "biralo",
            ]
        )

    return Pillanat(
        index=index,
        idopont=most,
        iteracio=iteracio_esemenyhez(esemenyek, iteraciok, index),
        esemenyek_eddig=eddig,
        elemallapot=allapotok,
    )


def esemeny_cimke(sor: pd.Series) -> str:
    """Rövid, olvasható címke egy eseményhez — az időkurzor felirata."""
    elem = f"{sor['elem_id']} · " if sor["elem_id"] else ""
    return f"{sor['idopont']:%m-%d %H:%M} — {elem}{sor['esemeny']}"
