"""Az animációs nézet forgatókönyve.

A megjelenítő eseményfolyamot fogyaszt, nem CSV-t: ettől tudja majd ugyanez a
színpad egy élő szimuláció eseményeit is lejátszani, változtatás nélkül.

A tábla állapotát **nem** a JavaScript számolja, hanem ez a modul, a meglévő
`allapot.pillanat()` hívásával. Enélkül az állapotgép második, párhuzamos
megvalósítása keletkezne a böngészőben, ami némán elcsúszhatna a négy
táblázatos nézettől — márpedig a kettőnek ugyanazt kell mutatnia.

A modul szándékosan nem függ a Streamlittől, hogy tesztelhető maradjon.
"""

from __future__ import annotations

import re
from typing import Any

import pandas as pd

from modell import allapot as allapot_modul
from modell import kapacitas, konyvjelzok
from modell.betoltes import Adatok

# Az ügynökpark a koncepció [00-mukodesi-modell.md] táblázatából. A modellcsalád
# azért szerepel, mert a modell egyik sarokpontja, hogy a verifikáló és a cáfoló
# más családból való, mint az implementáló.
UGYNOKOK = {
    "implementalo-A": ("Implementáló", "A"),
    "verifikalo-B": ("Verifikáló", "B"),
    "biztonsagi-kereso-A": ("Biztonsági kereső", "A"),
    "cafolo-B": ("Biztonsági cáfoló", "B"),
    "kutato": ("Kutató", "—"),
}

# A sávok a modell saját oszlopnevei (allapot.ALLAPOT_ATMENET értékei). A
# koncepció 08. dokumentumának ellenőrzési feltétele, hogy a felület ne vezessen
# be új fogalmat, ezért itt nem születik új elnevezés.
SAVOK = [
    "Kész a kezdésre",
    "Megvalósítás alatt",
    "Bírálatra vár",
    "Bírálat alatt",
    "Javítás alatt",
    "Beolvadt",
]

# Ezek nem sávok, hanem kilépők: az elem elhagyja a folyamatot.
KILEPOK = ["Visszabontva", "Átcsúszott"]

# A verifikáló kapu nem oszlop, hanem két sáv közötti átjáró. A napló csak a
# bukásokat rögzíti (kapu_bukott), a sikeres átengedést nem — ezért vezetjük le.
LEVEZETETT_ESEMENY = "verifikalo_atengedte"


def _szereplo_tipus(nev: str, szeniorok: set[str]) -> tuple[str, str, str]:
    """Szereplő → (típus, szerep, modellcsalád). A típus 'ugynok' vagy 'ember'."""
    if nev in UGYNOKOK:
        szerep, csalad = UGYNOKOK[nev]
        return "ugynok", szerep, csalad
    if nev in szeniorok:
        return "ember", "Szenior fejlesztő", "—"
    # A név végén zárójelben áll a szerep, például „Nagy Réka (PO)".
    if talalat := re.search(r"\(([^)]+)\)\s*$", nev):
        return "ember", talalat.group(1), "—"
    return "ember", "Csapattag", "—"


def _talalat_szam(reszlet: str) -> int | None:
    """A biztonsági lánc darabszáma a részletszövegből („4 találat…" → 4).

    Szándékosan szűk minta: ha az adat elmozdul, inkább semmit ne mutassunk,
    mint rosszat. A jelenlegi négy előfordulást teszt rögzíti.
    """
    talalat = re.match(r"^(\d+)\s+találat", reszlet.strip())
    return int(talalat.group(1)) if talalat else None


def _szereplok(adatok: Adatok) -> list[dict[str, Any]]:
    szeniorok = set(adatok.konfig["szeniorok"])
    nevek = [n for n in adatok.esemenyek["szereplo"].unique() if n]
    # A levezetett kockák szereplője akkor is kell, ha a naplóban nem fordul elő.
    if "verifikalo-B" not in nevek:
        nevek.append("verifikalo-B")
    sorok = []
    for nev in sorted(nevek):
        tipus, szerep, csalad = _szereplo_tipus(nev, szeniorok)
        sorok.append(
            {"azonosito": nev, "tipus": tipus, "szerep": szerep, "modellcsalad": csalad}
        )
    return sorok


def _elemek(adatok: Adatok) -> dict[str, dict[str, Any]]:
    """Az elemek statikus adatai — a kockákban csak azonosító szerepel."""
    return {
        str(sor["elem_id"]): {
            "cim": str(sor["cim"]),
            "iteracio": int(sor["iteracio"]),
            "tipus": str(sor["tipus"]),
            "magas_kockazat": sor["magas_kockazat"] == "igen",
            "meret_sor": int(sor["meret_sor"]),
            "vallalt": sor["vallalt"] == "igen",
            "szulo": str(sor["szulo"]),
        }
        for _, sor in adatok.elemek.iterrows()
    }


def _keret(adatok: Adatok, p: allapot_modul.Pillanat, iteracio_id: int) -> dict[str, float]:
    """A bírálati keret fogyása az adott iterációban.

    A keret bírálati eseményben mérődik, nem elemben: a modell szerint minden,
    ami emberi szemet igényel, ugyanabból a véges készletből fogyaszt.
    """
    it = adatok.iteracio(iteracio_id)
    terv = it["parameterek_terv"]
    k = kapacitas.szamol(terv["R"], terv["t"], terv["r"], int(it["napok"]))

    kezdet = pd.Timestamp(it["kezdet"])
    veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
    ablak = p.esemenyek_eddig[
        (p.esemenyek_eddig["idopont"] >= kezdet) & (p.esemenyek_eddig["idopont"] < veg)
    ]
    elhasznalt = int(ablak["esemeny"].isin(kapacitas.BIRALAT_LEZARO).sum())
    return {
        "elhasznalt": elhasznalt,
        "osszes": round(k.esemeny_per_nap * k.napok, 1),
    }


def _tabla(p: allapot_modul.Pillanat) -> dict[str, list[str]]:
    return {sav: p.oszlop(sav)["elem_id"].tolist() for sav in SAVOK + KILEPOK}


def _biralok(p: allapot_modul.Pillanat) -> dict[str, str]:
    alatt = p.oszlop("Bírálat alatt")
    return {str(r.elem_id): str(r.biralo) for r in alatt.itertuples()}


def forgatokonyv(adatok: Adatok) -> dict[str, Any]:
    """A teljes animációs forgatókönyv, JSON-szerializálható formában."""
    esemenyek = adatok.esemenyek
    korlatok = adatok.konfig["wip_korlatok"]
    biralati_korlat = korlatok["Bírálatra vár"]

    # A pillanatokat eseményindexenként egyszer számoljuk ki: a levezetett kockák
    # ugyanazokra hivatkoznak vissza, nincs értelme újra végigfuttatni.
    pillanatok = {
        i: allapot_modul.pillanat(esemenyek, adatok.elemek, adatok.iteraciok, i)
        for i in range(len(esemenyek))
    }

    kockak: list[dict[str, Any]] = []
    naplo_kocka: dict[int, int] = {}  # eseményindex → kockaindex

    def kocka_hozzaad(naplo_idx: int, esemeny_sor: pd.Series, forras: str) -> None:
        # Levezetett kocka a horgonyesemény ELŐTTI táblaállapotot mutatja, és
        # annak az időbélyegét veszi át — kitalált időadatot nem gyártunk.
        allapot_idx = naplo_idx if forras == "naplo" else naplo_idx - 1
        p = pillanatok[allapot_idx]
        varakozok = len(p.oszlop("Bírálatra vár"))
        reszlet = str(esemeny_sor["reszlet"])
        kockak.append(
            {
                "idx": len(kockak),
                "naplo_idx": naplo_idx if forras == "naplo" else None,
                "idopont": esemeny_sor["idopont"].isoformat(sep=" "),
                "iteracio": allapot_modul.iteracio_esemenyhez(
                    esemenyek, adatok.iteraciok, naplo_idx
                ),
                "elem_id": str(esemeny_sor["elem_id"]),
                "esemeny": LEVEZETETT_ESEMENY if forras == "levezetett" else str(
                    esemeny_sor["esemeny"]
                ),
                "szereplo": "verifikalo-B" if forras == "levezetett" else str(
                    esemeny_sor["szereplo"]
                ),
                "forras": forras,
                "reszlet": "" if forras == "levezetett" else reszlet,
                "hibaosztaly": "" if forras == "levezetett" else str(
                    esemeny_sor["hibaosztaly"]
                ),
                "talalat_szam": _talalat_szam(reszlet) if forras == "naplo" else None,
                "tabla": _tabla(p),
                "biralok": _biralok(p),
                "varakozok": varakozok,
                # A torlódás nem külön esemény, hanem a szabály állapota: ha a sor
                # eléri a korlátot, az ügynökök nem indíthatnak új feladatot.
                "torlodas": varakozok >= biralati_korlat,
                "keret": _keret(
                    adatok,
                    p,
                    allapot_modul.iteracio_esemenyhez(
                        esemenyek, adatok.iteraciok, naplo_idx
                    ),
                ),
            }
        )

    for i, sor in esemenyek.iterrows():
        # A modell szerint minden elem áthalad a verifikálón, de a napló csak a
        # bukást rögzíti. A sikeres átengedést ezért levezetett kockaként tesszük
        # láthatóvá, a felületen megkülönböztetve.
        if sor["esemeny"] == "biralatra_kerult":
            kocka_hozzaad(int(i), sor, "levezetett")
        naplo_kocka[int(i)] = len(kockak)
        kocka_hozzaad(int(i), sor, "naplo")

    return {
        "konfig": {
            "wip_korlatok": korlatok,
            "meretkorlat_sor": int(adatok.konfig["meretkorlat_sor"]),
            "szeniorok": list(adatok.konfig["szeniorok"]),
            "savok": SAVOK,
            "kilepok": KILEPOK,
        },
        "iteraciok": [
            {
                "id": int(it["id"]),
                "nev": str(it["nev"]),
                "kezdet": str(it["kezdet"]),
                "veg": str(it["veg"]),
                "napok": int(it["napok"]),
                "vallalt": int(it["vallalt"]),
            }
            for it in adatok.iteraciok
        ],
        "szereplok": _szereplok(adatok),
        "elemek": _elemek(adatok),
        "kockak": kockak,
        "fejezetek": [
            {"cimke": cimke, "idx": naplo_kocka[idx]}
            for cimke, idx in konyvjelzok.konyvjelzok(esemenyek).items()
        ],
    }
