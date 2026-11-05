"""Hibaosztályok, szabályok és az eszkalációs létra.

A létra a koncepció [05-szerepek-es-dinamika.md] dokumentumából származik.
A lényege, hogy az ügynök hibája nem teljesítménykérdés, hanem konfigurációs
kérdés — ezért a Scrum Master nem az egyes hibákat továbbítja, hanem a
mintázatot teszi láthatóvá.
"""

from __future__ import annotations

import pandas as pd

# Egy hibaosztály neve (a katalógusban: `nev`) önmagában sokszor nem mondja meg,
# mi történik a gyakorlatban — ez itt kiegészítés csak azokhoz a kódokhoz,
# amelyeknél ez felmerült. Szándékosan nem minden hibaosztályra van bejegyzés:
# a hiányzó nem hiba, csak azt jelenti, hogy még nem volt rá visszajelzés.
HIBAOSZTALY_MAGYARAZAT = {
    "HO-03": (
        "A teszt a saját implementációjához méri magát, nem egy attól "
        "független forráshoz — például ugyanazt a képletet írja le a "
        "kódban és a tesztben. Egy ilyen teszt akkor sem bukik el, ha a "
        "kód hibás, mert a hibát megismétli."
    ),
}

LETRA = {
    1: ("Egyedi hiba", "A bíráló javíttatja. Nincs teendő."),
    2: ("Ismétlődő hibaosztály", "Napirend a visszatekintés gépi rétegén — szabály születik."),
    3: ("A szabály nem fog", "Eszkaláció a szeniorok felé: gépi kaput kell építeni köré."),
    4: ("A konfiguráció sem segít", "Architektúra- vagy modellváltás. A PO-t is be kell vonni."),
    5: ("Több ügynöknél ugyanaz", "Nem az ügynökökkel van baj, hanem a folyamattal vagy a kódbázissal."),
}


def hibaosztaly_osszesites(adatok, p) -> pd.DataFrame:
    """Hibaosztályonként: előfordulások, szabály, visszatérés, létrafok."""
    eddig = p.esemenyek_eddig
    szabalyok = adatok.szabalyok
    sorok = []

    for _, ho in adatok.hibaosztalyok.iterrows():
        elofordulasok = eddig[eddig["hibaosztaly"] == ho["kod"]]
        if elofordulasok.empty:
            continue

        sajat_szabaly = szabalyok[
            (szabalyok["hibaosztaly"] == ho["kod"]) & (szabalyok["tipus"] == "szabaly")
        ]
        sajat_kapu = szabalyok[
            (szabalyok["hibaosztaly"] == ho["kod"]) & (szabalyok["tipus"] == "gepi_kapu")
        ]

        szabaly_kod, szabaly_datum, utana = "", "", 0
        if not sajat_szabaly.empty:
            szab = sajat_szabaly.iloc[0]
            letrehozva = pd.Timestamp(szab["letrehozva"])
            # A szabály a visszatekintésen születik: csak azután létezik.
            if p.idopont >= letrehozva:
                szabaly_kod = szab["kod"]
                szabaly_datum = f"{letrehozva:%Y-%m-%d}"
                utana = int((elofordulasok["idopont"] > letrehozva).sum())

        van_kapu = not sajat_kapu.empty and p.idopont >= pd.Timestamp(
            sajat_kapu.iloc[0]["letrehozva"]
        )

        n = len(elofordulasok)
        if van_kapu:
            fok = 3
        elif szabaly_kod and utana > 0:
            fok = 3
        elif n >= 2:
            fok = 2
        else:
            fok = 1

        sorok.append(
            {
                "kod": ho["kod"],
                "nev": ho["nev"],
                "kategoria": ho["kategoria"],
                "elofordulas": n,
                "elso": elofordulasok["idopont"].min(),
                "utolso": elofordulasok["idopont"].max(),
                "szabaly": szabaly_kod,
                "szabaly_datuma": szabaly_datum,
                "visszateres_szabaly_utan": utana,
                "gepi_kapu": sajat_kapu.iloc[0]["kod"] if van_kapu else "",
                "letrafok": fok,
                "letra_neve": LETRA[fok][0],
                "teendo": LETRA[fok][1],
            }
        )

    if not sorok:
        return pd.DataFrame(
            columns=[
                "kod", "nev", "kategoria", "elofordulas", "elso", "utolso", "szabaly",
                "szabaly_datuma", "visszateres_szabaly_utan", "gepi_kapu", "letrafok",
                "letra_neve", "teendo",
            ]
        )
    return pd.DataFrame(sorok).sort_values(["letrafok", "elofordulas"], ascending=False)


def ervenyes_szabalyok(adatok, p) -> pd.DataFrame:
    """A kurzor időpontjában már létező szabályok és gépi kapuk."""
    szab = adatok.szabalyok.copy()
    szab["letrehozva_ts"] = pd.to_datetime(szab["letrehozva"])
    return szab[szab["letrehozva_ts"] <= p.idopont].drop(columns=["letrehozva_ts"])


def visszamerendo(adatok, p) -> pd.DataFrame:
    """Mely szabályokat kell a következő iterációban visszamérni."""
    osszes = hibaosztaly_osszesites(adatok, p)
    if osszes.empty:
        return osszes
    return osszes[osszes["szabaly"] != ""][
        ["szabaly", "kod", "nev", "szabaly_datuma", "visszateres_szabaly_utan", "letra_neve"]
    ]
