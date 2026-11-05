"""A kilenc beavatkozási jelzés.

Minden jelzés a koncepció [08-sm-felulet-specifikacio.md] táblázatából származik,
és mindegyikhez a modell adja a teendőt. A felület jelez, de nem avatkozik be:
a döntést ember hozza meg.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from modell import kapacitas
from modell.allapot import Pillanat
from modell.betoltes import Adatok

def _ora(ertek: float) -> str:
    # Ugyanaz a formátum, mint a `cimkek.ora`; itt helyben, hogy a jelzések modulja ne
    # függjön a felületi címkéktől.
    if ertek < 0.5:
        return "most került be"
    if ertek < 10:
        return f"{ertek:.0f} órája"
    return f"{ertek:.1f} órája".replace(".", ",")


KRITIKUS, FIGYELEM, INFO = "kritikus", "figyelem", "info"


@dataclass
class Jelzes:
    kod: str
    cim: str
    aktiv: bool
    sulyossag: str
    uzenet: str
    teendo: str
    forras: str
    reszletek: list[str] = field(default_factory=list)


def _lezart_iteraciok(adatok: Adatok, p: Pillanat) -> list[dict]:
    """Azok az iterációk, amelyek utolsó eseménye már a kurzor előtt van."""
    kesz = []
    for it in adatok.iteraciok:
        veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
        utolso = adatok.esemenyek[adatok.esemenyek["idopont"] < veg]
        if not utolso.empty and utolso.index[-1] <= p.index:
            kesz.append(it)
    return kesz


def torlodas(adatok: Adatok, p: Pillanat) -> Jelzes:
    korlat = adatok.konfig["wip_korlatok"]["Bírálatra vár"]
    varakozok = p.oszlop("Bírálatra vár")
    n = len(varakozok)
    return Jelzes(
        kod="J1",
        cim="Torlódás a bírálati soron",
        aktiv=n >= korlat,
        sulyossag=FIGYELEM,
        uzenet=f"{n} elem vár bírálatra, a korlát {korlat}.",
        teendo="Az ügynökök nem indíthatnak új feladatot, amíg a sor nem apad.",
        forras="S-28",
        reszletek=[f"{r.elem_id} — {r.cim} ({_ora(r.varakozas_ora)})" for r in varakozok.itertuples()],
    )


def oregedo_elem(adatok: Adatok, p: Pillanat) -> Jelzes:
    kuszob = adatok.konfig["oregedesi_kuszob_ora"]
    varakozok = p.oszlop("Bírálatra vár")
    oregek = varakozok[varakozok["varakozas_ora"] > kuszob]
    return Jelzes(
        kod="J2",
        cim="Öregedő elem a sorban",
        aktiv=not oregek.empty,
        sulyossag=FIGYELEM,
        uzenet=f"{len(oregek)} elem vár {kuszob} óránál régebben.",
        teendo="Soron kívüli bírálat, vagy tudatos döntés az elengedésről.",
        forras="S-06",
        reszletek=[f"{r.elem_id} — {_ora(r.varakozas_ora)}" for r in oregek.itertuples()],
    )


def felugyeleti_res(adatok: Adatok, p: Pillanat) -> Jelzes:
    """Beolvadt elem megnevezett emberi jóváhagyó nélkül — a modell alapszabálya."""
    szeniorok = set(adatok.konfig["szeniorok"])
    beolvasztasok = p.esemenyek_eddig[p.esemenyek_eddig["esemeny"] == "biralat_jovahagyva"]
    nevtelen = beolvasztasok[~beolvasztasok["szereplo"].isin(szeniorok)]
    return Jelzes(
        kod="J3",
        cim="Felügyeleti rés",
        aktiv=not nevtelen.empty,
        sulyossag=KRITIKUS,
        uzenet=(
            f"{len(nevtelen)} elem olvadt be megnevezett emberi jóváhagyó nélkül."
            if not nevtelen.empty
            else f"Mind a {len(beolvasztasok)} beolvasztásnak van megnevezett emberi jóváhagyója."
        ),
        teendo="Azonnali kivizsgálás: ez a modell alapszabályának sérülése.",
        forras="S-05",
        reszletek=nevtelen["elem_id"].tolist(),
    )


def gumibelyegzo(adatok: Adatok, p: Pillanat) -> Jelzes:
    kuszob = adatok.konfig["gumibelyegzo_iteracio_kuszob"]
    sorozat = 0
    for it in _lezart_iteraciok(adatok, p):
        kezdet = pd.Timestamp(it["kezdet"])
        veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
        ablak = adatok.esemenyek[
            (adatok.esemenyek["idopont"] >= kezdet) & (adatok.esemenyek["idopont"] < veg)
        ]
        elutasitas = (ablak["esemeny"] == "darabolas_elutasitva").sum()
        sorozat = 0 if elutasitas else sorozat + 1
    return Jelzes(
        kod="J4",
        cim="Formálissá vált jóváhagyási kapu",
        aktiv=sorozat >= kuszob,
        sulyossag=FIGYELEM,
        uzenet=f"{sorozat} egymást követő iteráció elutasítás nélkül (küszöb: {kuszob}).",
        teendo=(
            "Napirendre a visszatekintésen: ha a kapu tartósan nem utasít el semmit, "
            "elvesztette a funkcióját — formálissá vált, és csak azt a látszatot "
            "kelti, mintha valóban működne. Ez nem siker, hanem gyanús."
        ),
        forras="saját döntés",
        reszletek=["Kevés adat: a jelzéshez legalább három lezárt iteráció kell."]
        if sorozat < kuszob
        else [],
    )


def egyenetlen_terheles(adatok: Adatok, p: Pillanat) -> Jelzes:
    kuszob = adatok.konfig["terheles_egyenetlenseg_kuszob"]
    lezart = _lezart_iteraciok(adatok, p)
    if not lezart:
        return Jelzes("J5", "Egyenetlen bírálati terhelés", False, INFO,
                      "Még nincs lezárt iteráció.", "—", "S-02, S-11")
    eloszlas = kapacitas.terheles_eloszlas(adatok.esemenyek, lezart[-1])
    legnagyobb = max(eloszlas.values()) if eloszlas else 0.0
    return Jelzes(
        kod="J5",
        cim="Egyenetlen bírálati terhelés",
        aktiv=legnagyobb > kuszob,
        sulyossag=FIGYELEM,
        uzenet=f"A legnagyobb részarány {legnagyobb:.0%} (küszöb: {kuszob:.0%}).",
        teendo="Terheléskiegyenlítés. Ez kapacitás- és kiégési kockázat is.",
        forras="S-02, S-11",
        reszletek=[f"{k}: {v:.0%}" for k, v in sorted(eloszlas.items())],
    )


def visszatero_hibaosztaly(adatok: Adatok, p: Pillanat) -> Jelzes:
    talalatok = []
    szabalyok = adatok.szabalyok[adatok.szabalyok["hibaosztaly"] != ""]
    for _, szab in szabalyok.iterrows():
        if szab["tipus"] != "szabaly":
            continue
        letrehozva = pd.Timestamp(szab["letrehozva"])
        utana = p.esemenyek_eddig[
            (p.esemenyek_eddig["hibaosztaly"] == szab["hibaosztaly"])
            & (p.esemenyek_eddig["idopont"] > letrehozva)
        ]
        if not utana.empty:
            nev = adatok.hibaosztalyok.set_index("kod").loc[szab["hibaosztaly"], "nev"]
            talalatok.append(
                f"{szab['hibaosztaly']} ({nev}) — {szab['kod']} felvétele óta "
                f"{len(utana)} alkalommal tért vissza"
            )
    return Jelzes(
        kod="J6",
        cim="Visszatérő hibaosztály",
        aktiv=bool(talalatok),
        sulyossag=KRITIKUS,
        uzenet="A szabály felvétele után is előfordult." if talalatok else "Nincs visszatérő hibaosztály.",
        teendo=(
            "Eszkaláció a 3. fokra: nem a szabályt kell átfogalmazni, hanem gépi kaput "
            "kell építeni köré. Az utasításfájl puha korlát, a teszt kemény."
        ),
        forras="S-26",
        reszletek=talalatok,
    )


def parameter_elteres(adatok: Adatok, p: Pillanat) -> Jelzes:
    kuszob = adatok.konfig["parameter_elteres_kuszob"]
    lezart = _lezart_iteraciok(adatok, p)
    if not lezart:
        return Jelzes("J7", "Paramétereltérés", False, INFO,
                      "Még nincs lezárt iteráció.", "—", "saját döntés")
    it = lezart[-1]
    mert = kapacitas.mert_parameterek(adatok.esemenyek, it)
    if not mert["biralatok"]:
        # Folyamatban lévő iteráció, amelyben még egyetlen bírálat sem zárult le:
        # nincs mit a tervhez hasonlítani, és a nulla validálási idővel a
        # kapacitásképlet sem értelmezhető.
        return Jelzes("J7", "Paramétereltérés", False, INFO,
                      "Még nincs lezárt bírálat, amiből mérni lehetne.", "—", "saját döntés")
    terv = it["parameterek_terv"]
    elteresek = []
    for kulcs in ("R", "t", "r"):
        if terv[kulcs] == 0:
            continue
        d = (mert[kulcs] - terv[kulcs]) / terv[kulcs]
        if abs(d) > kuszob:
            elteresek.append(f"{kulcs}: terv {terv[kulcs]} → mért {mert[kulcs]} ({d:+.0%})")
    uj = kapacitas.szamol(mert["R"], mert["t"], mert["r"], it["napok"])
    return Jelzes(
        kod="J7",
        cim="Paramétereltérés a tervhez képest",
        aktiv=bool(elteresek),
        sulyossag=FIGYELEM,
        uzenet=f"{it['id']}. iteráció: {len(elteresek)} paraméter tért el a küszöbnél jobban.",
        teendo=(
            f"A következő iteráció vállalását a mért értékekre kell igazítani: "
            f"{uj.elem_per_iteracio:.1f} elem.".replace(".", ",", 1)
        ),
        forras="saját döntés",
        reszletek=elteresek,
    )


def meretkorlat(adatok: Adatok, p: Pillanat) -> Jelzes:
    korlat = adatok.konfig["meretkorlat_sor"]
    biralatban = p.elemallapot[p.elemallapot["allapot"].isin(["Bírálatra vár", "Bírálat alatt"])]
    tullepok = biralatban[biralatban["meret_sor"] > korlat]
    return Jelzes(
        kod="J8",
        cim="Méretkorlát-túllépés",
        aktiv=not tullepok.empty,
        sulyossag=FIGYELEM,
        uzenet=f"{len(tullepok)} elem lépi túl a {korlat} soros korlátot.",
        teendo="Visszabontás, nem hosszabb bírálat. A nagy csomag rontja az elbírálás minőségét.",
        forras="S-06",
        reszletek=[f"{r.elem_id} — {r.meret_sor} sor" for r in tullepok.itertuples()],
    )


def lazulasgyanu(adatok: Adatok, p: Pillanat) -> Jelzes:
    """Összetett jelzés: külön-külön egyik komponens sem rossz hír, a három együtt igen."""
    lezart = _lezart_iteraciok(adatok, p)
    if len(lezart) < 2:
        return Jelzes("J9", "Bírálat felületessé válása", False, INFO,
                      "Legalább két lezárt iteráció kell az összehasonlításhoz.",
                      "—", "saját döntés, S-20 alapján")

    elozo, mostani = lezart[-2], lezart[-1]
    m_e = kapacitas.mert_parameterek(adatok.esemenyek, elozo)
    m_m = kapacitas.mert_parameterek(adatok.esemenyek, mostani)
    f_e = kapacitas.elso_koros_elfogadas(adatok.esemenyek, adatok.elemek, elozo)
    f_m = kapacitas.elso_koros_elfogadas(adatok.esemenyek, adatok.elemek, mostani)
    h_e = _hibaarany(adatok, elozo)
    h_m = _hibaarany(adatok, mostani)

    komponensek = {
        "a validálási idő csökken": m_m["t"] < m_e["t"],
        "az elfogadási arány nő": f_m["arany"] > f_e["arany"],
        "a hibaarány nő": h_m > h_e,
    }
    return Jelzes(
        kod="J9",
        cim="Bírálat felületessé válása",
        aktiv=all(komponensek.values()),
        sulyossag=FIGYELEM,
        uzenet=(
            "Mindhárom komponens egyszerre teljesül."
            if all(komponensek.values())
            else "Nem teljesül mindhárom komponens — a jelzés nem szólal meg."
        ),
        teendo="A bírálat felületessé válhatott; a visszatekintésen ki kell mondani.",
        forras="saját döntés, S-20 alapján",
        reszletek=[
            f"{'✓' if ertek else '✗'} {nev}"
            for nev, ertek in komponensek.items()
        ]
        + [
            f"t: {m_e['t']} → {m_m['t']} perc",
            f"első körös elfogadás: {f_e['arany']:.0%} → {f_m['arany']:.0%}",
            f"hibaarány: {h_e:.2f} → {h_m:.2f} hiba/beolvadt elem",
        ],
    )


def _hibaarany(adatok: Adatok, iteracio: dict) -> float:
    kezdet = pd.Timestamp(iteracio["kezdet"])
    veg = pd.Timestamp(iteracio["veg"]) + pd.Timedelta(days=1)
    ablak = adatok.esemenyek[
        (adatok.esemenyek["idopont"] >= kezdet) & (adatok.esemenyek["idopont"] < veg)
    ]
    hibak = (ablak["hibaosztaly"] != "").sum()
    beolvadt = (ablak["esemeny"] == "biralat_jovahagyva").sum()
    return round(hibak / beolvadt, 3) if beolvadt else 0.0


MIND = [
    torlodas,
    oregedo_elem,
    felugyeleti_res,
    gumibelyegzo,
    egyenetlen_terheles,
    visszatero_hibaosztaly,
    parameter_elteres,
    meretkorlat,
    lazulasgyanu,
]


def kiertekel(adatok: Adatok, p: Pillanat) -> list[Jelzes]:
    return [f(adatok, p) for f in MIND]
