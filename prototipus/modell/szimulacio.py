"""A szimulációs motor — egy iteráció végigjátszása emberi jóváhagyással.

A motor eseményeket gyárt, **pontosan abban a sémában**, amelyben a példa
eseménynaplója van. Ettől működik rajta változtatás nélkül a teljes elemzőréteg:
az `allapot.pillanat()`, a `jelzesek.kiertekel()`, a `kapacitas.szamol()`, a
`tanulas.hibaosztaly_osszesites()` és az `animacio.forgatokonyv()` is.

A motor **soha nem ír a `prototipus/adatok/` alatti példaadatba** — arra a
koncepció 07. dokumentuma és a tesztek hivatkoznak. A szimuláció saját naplót
épít a memóriában.

A működés lényege, hogy a motor addig fut, amíg emberi döntésre nincs szükség.
Amikor van, megáll, és a hívó dolga a döntést visszaadni. Ez a human-in-the-loop:
a modell két emberi kapuja — a darabolás jóváhagyása és a beolvasztás — nem
automatizálható, mert ott keletkezik a felelősség.
"""

from __future__ import annotations

import pathlib
import random
from dataclasses import dataclass, field

import pandas as pd

from modell import allapot as allapot_modul
from modell import kapacitas
from modell.betoltes import ADATOK_MAPPA, Adatok
from modell.ugynok import SULYOS, SzimulaltUgynok, Ugynok

BACKLOG_FAJL = ADATOK_MAPPA / "szimulacio" / "backlog.csv"

MUNKA_KEZDET, MUNKA_VEGE = 9, 17          # a munkanap határai
TICK = pd.Timedelta(minutes=5)

ALAP_KONFIG = {
    "wip_korlatok": {"Kész a kezdésre": 3, "Megvalósítás alatt": 4, "Bírálatra vár": 4},
    "meretkorlat_sor": 200,
    "oregedesi_kuszob_ora": 8,
    "terheles_egyenetlenseg_kuszob": 0.65,
    "parameter_elteres_kuszob": 0.15,
    "gumibelyegzo_iteracio_kuszob": 3,
    "szeniorok": ["Kovács Kata", "Szabó Márton"],
}

# A koncepció kiinduló feltevései. Szándékosan itt, egy helyen és állíthatóan:
# ezek saját tervezési döntések bizonyíték nélkül, és a felületnek ezt látnia kell.
ALAP_PARAMETEREK = {"R": 3.0, "t": 70.0, "r": 0.5}

# Az `Allas`/`Dontes.tenyek` alakjának verziója. A Streamlit `session_state`
# egy folyamaton belül, kódfrissítés UTÁN is megtartja a régi objektumokat —
# ez élesben (a `sm-all-ui.service` folyamatosan fut) valódi hiba volt: egy
# fejlesztés közben nyitva hagyott böngészőlap egy régebbi sémájú `Dontes`-t
# tartott a kezében, az új kód pedig egy azóta bővült `tenyek` kulcsot
# (`sulyos`) olvasott róla — `KeyError`-ral. A verziószámot minden alkalommal
# emelni kell, amikor az `Allas` vagy a `Dontes.tenyek` alakja változik; az
# `allapot_ervenyes()` ez alapján dönti el, hogy a mentett állapot még
# megbízhatóan olvasható-e, vagy inkább újra kell kezdeni.
SEMA_VERZIO = 3

FELFEDEZES_ESELY = 0.75      # egy bírálat ekkora eséllyel találja meg a hibát
NAGY_CSOMAG_SZORZO = 0.55    # a méretkorlát fölötti csomagot felületesebben nézik (S-06)

# A két szakszó, amit a felület sokfelé használ. Egy helyen definiáljuk, mert
# korábban sehol nem volt kimondva, mit jelentenek — a felhasználó a szimuláció
# döntéskártyáján futott bele, hogy a „Súlyos találat van benne" mondatból nem
# derül ki sem az, hogy ez baj-e, sem az, hogy mit lehet vele kezdeni.
SULYOS_MAGYARAZAT = "hibás vagy adatot kiszivárogtató kód kerülne a termékbe"
ENYHE_MAGYARAZAT = "a folyamat, a tesztelés vagy a használhatóság minőségét rontja"


@dataclass
class SzimElem:
    elem_id: str
    cim: str
    tipus: str
    magas_kockazat: bool
    bonyolultsag: int
    # Melyik iterációban vállaltuk. Áthozott elemnél ez az EREDETI iteráció
    # marad: az elsőkörös elfogadási arány annak az iterációnak a vállalását
    # kéri számon, amelyik az elemet betette.
    iteracio: int = 0
    meret_sor: int = 0
    allapot: str = "Kész a kezdésre"
    rejtett_hibak: list[str] = field(default_factory=list)
    talalt_hibak: list[str] = field(default_factory=list)
    beolvadt_hibakkal: list[str] = field(default_factory=list)
    kapu_bukas: str = ""
    korok: int = 0
    biralo: str = ""
    szulo: str = ""
    vallalt: bool = True
    kesz_ekkor: pd.Timestamp | None = None


@dataclass
class Szenior:
    nev: str
    mai_perc: float = 0.0
    elem_id: str = ""
    biralat_vege: pd.Timestamp | None = None
    biralat_perc: float = 0.0
    osszes_perc: float = 0.0


@dataclass
class Valasztas:
    kod: str
    cimke: str
    kovetkezmeny: str


class _Tenyek:
    """A döntések tényeinek közös őse.

    A tényeket döntéstípusonként külön osztály tartja, kötelező mezőkkel: egy hiányzó
    vagy elgépelt mező már a `Dontes` létrehozásakor `TypeError`, nem egy távoli
    felületi olvasásnál `KeyError` (lásd a 2026-09-16-i incidenst és az ADR-0006-ot).
    A felület és a tesztek attribútumként olvassák (`d.tenyek.meret_sor`).
    """


@dataclass(frozen=True, kw_only=True)
class VallalasTenyek(_Tenyek):
    keret: int
    parameterek: dict
    parameter_forras: str
    athozott: int


@dataclass(frozen=True, kw_only=True)
class BeolvasztasTenyek(_Tenyek):
    talalt: list
    sulyos: list
    hibaosztalyok: list  # a felület ebből rajzolja a nevesített listát — a puszta kód nem elég
    meret_sor: int
    magas_kockazat: bool
    korok: int
    biralo: str
    perc: int


@dataclass(frozen=True, kw_only=True)
class TorlodasTenyek(_Tenyek):
    varakozok: int
    korlat: int


@dataclass(frozen=True, kw_only=True)
class MeretkorlatTenyek(_Tenyek):
    meret_sor: int
    korlat: int


@dataclass(frozen=True, kw_only=True)
class VisszatekintesTenyek(_Tenyek):
    hibaosztaly: str
    elofordulas: int
    van_szabaly: bool


# A döntés kódja és a hozzá tartozó tények típusa: ha a kettő nem egyezik, a `Dontes`
# létrehozása hibát ad, nem a felület olvasása.
TENYEK_TIPUSA: dict[str, type[_Tenyek]] = {
    "vallalas": VallalasTenyek,
    "beolvasztas": BeolvasztasTenyek,
    "torlodas": TorlodasTenyek,
    "meretkorlat": MeretkorlatTenyek,
    "visszatekintes": VisszatekintesTenyek,
}


@dataclass
class Dontes:
    kod: str
    cim: str
    magyarazat: str
    valasztasok: list[Valasztas]
    tenyek: _Tenyek
    elem_id: str = ""

    def __post_init__(self) -> None:
        elvart = TENYEK_TIPUSA.get(self.kod)
        if elvart is None:
            raise ValueError(f"ismeretlen döntéstípus: {self.kod!r}")
        if not isinstance(self.tenyek, elvart):
            raise TypeError(
                f"a(z) {self.kod!r} döntés tényei {elvart.__name__} típusúak, "
                f"nem {type(self.tenyek).__name__}"
            )


@dataclass
class Allas:
    """A szimuláció teljes állapota. A felület ezt tartja a munkamenetben."""

    konfig: dict
    parameterek: dict
    mag: int
    iteracio_id: int
    napok: int
    kezdet: pd.Timestamp
    most: pd.Timestamp
    ugynok: Ugynok
    veletlen: random.Random
    elemek: dict[str, SzimElem] = field(default_factory=dict)
    sorrend: list[str] = field(default_factory=list)
    keszlet: list[dict] = field(default_factory=list)  # a még ki nem osztott backlog
    szeniorok: list[Szenior] = field(default_factory=list)
    munkaban: dict[str, pd.Timestamp] = field(default_factory=dict)  # elem_id → mikor készül el
    esemenyek: list[dict] = field(default_factory=list)
    szabalyok: set[str] = field(default_factory=set)
    kapuk: set[str] = field(default_factory=set)
    szabaly_sorok: list[dict] = field(default_factory=list)
    dontes: Dontes | None = None
    vallalas: int = 0
    ugynokok_allnak: bool = True   # a torlódásnál a szabály szerint leállnak
    torlodas_kezelve: bool = False
    kesz: bool = False
    szegesek: list[str] = field(default_factory=list)
    naplo: list[str] = field(default_factory=list)
    lezart_iteraciok: list[dict] = field(default_factory=list)
    retro_kezelt: set[str] = field(default_factory=set)
    # A lezárt iterációk mérlege, az iteráció zárásakor készített pillanatképként.
    # Azért pillanatkép, mert a `szegesek` és a `naplo` iterációnként nullázódik:
    # utólag már nem volna miből újraszámolni.
    lezart_merlegek: list[dict] = field(default_factory=list)
    parameter_forras: str = "A szimuláció induló paraméterei"
    sema_verzio: int = SEMA_VERZIO


# --- Indítás ---------------------------------------------------------------------


def indit(mag: int = 42, napok: int = 3, parameterek: dict | None = None,
          kezdet: str = "2026-09-14") -> Allas:
    """Új szimuláció a harmadik iterációra, a példa két iterációja után."""
    hatter = pd.read_csv(BACKLOG_FAJL)
    veletlen = random.Random(mag)
    keszlet = hatter.to_dict("records")
    veletlen.shuffle(keszlet)

    konfig = {**ALAP_KONFIG, "wip_korlatok": dict(ALAP_KONFIG["wip_korlatok"])}
    allas = Allas(
        konfig=konfig,
        parameterek=dict(parameterek or ALAP_PARAMETEREK),
        mag=mag,
        iteracio_id=3,
        napok=napok,
        kezdet=pd.Timestamp(f"{kezdet} 09:00"),
        most=pd.Timestamp(f"{kezdet} 09:00"),
        ugynok=SzimulaltUgynok(mag=mag),
        veletlen=veletlen,
        keszlet=keszlet,
        szeniorok=[Szenior(nev) for nev in konfig["szeniorok"]],
    )
    # A példa két iterációjából örökölt szabályok: a tanulási hurok nem nulláról indul.
    allas.szabalyok = {"HO-01", "HO-02"}
    allas.szabaly_sorok = [
        {"kod": "SZ-06", "cim": "A verifikáló csak a teljes tesztkészlet igazolt lefutása után jelenthet sikert",
         "hibaosztaly": "HO-01", "letrehozva": "2026-09-04 17:20", "iteracio": 1,
         "kategoria": "verifikacio", "kivalto_elem": "", "tipus": "szabaly"},
        {"kod": "SZ-07", "cim": "Kontaktadatot visszaadó végpont kizárólag a láthatósági szűrőn keresztül szolgálhat ki",
         "hibaosztaly": "HO-02", "letrehozva": "2026-09-04 17:20", "iteracio": 1,
         "kategoria": "adatvedelem", "kivalto_elem": "", "tipus": "szabaly"},
    ]
    _vallalasi_dontes(allas)
    return allas


_HIBAOSZTALY_GYORSITOTAR: dict[str, dict] | None = None


def hibaosztaly_leiro(kod: str) -> dict:
    """Hibaosztály kódjából olvasható leíró: név, kategória, súlyosság.

    A kód önmagában (`HO-02`) semmit nem mond annak, aki nem ismeri a
    katalógust — a felületnek mindenhol a nevet is ki kell írnia mellé.
    A katalógus a példa statikus adata, ezért egyszer olvassuk be.
    """
    global _HIBAOSZTALY_GYORSITOTAR
    if _HIBAOSZTALY_GYORSITOTAR is None:
        tabla = pd.read_csv(ADATOK_MAPPA / "hibaosztalyok.csv")
        _HIBAOSZTALY_GYORSITOTAR = {
            str(sor["kod"]): {
                "kod": str(sor["kod"]),
                "nev": str(sor["nev"]),
                "kategoria": str(sor["kategoria"]),
                "sulyos": str(sor["kod"]) in SULYOS,
            }
            for _, sor in tabla.iterrows()
        }
    return _HIBAOSZTALY_GYORSITOTAR.get(
        kod, {"kod": kod, "nev": "ismeretlen hibaosztály", "kategoria": "—",
              "sulyos": kod in SULYOS}
    )


def hibaosztaly_cimke(kod: str) -> str:
    """Egysoros, olvasható címke: `HO-02 — Láthatósági szűrő megkerülése`."""
    leiro = hibaosztaly_leiro(kod)
    return f"{leiro['kod']} — {leiro['nev']}"


def allapot_ervenyes(allas: Allas | None) -> bool:
    """Biztonságosan olvasható-e a mentett `Allas` az aktuális kóddal.

    A `session_state`-ben élő objektum egy korábbi kódverzióból is
    származhat — kódfrissítés nem üríti ki, csak az oldal újratöltése vagy a
    folyamat újraindítása. Ha a séma közben bővült, a régi objektum
    hiányos `tenyek` szótárral rendelkezhet, amit az új felületi kód már új
    kulcsokkal olvas. Ezt a felület hívja, MIELŐTT bármit olvasna az
    állapotból — nem azután, hogy már elszállt egy `KeyError`-ral.
    """
    if allas is None:
        return True
    return getattr(allas, "sema_verzio", None) == SEMA_VERZIO


def _keret(allas: Allas) -> float:
    p = allas.parameterek
    k = kapacitas.szamol(p["R"], p["t"], p["r"], allas.napok)
    return round(k.elem_per_iteracio, 1)


def _athozott_elemek(allas: Allas) -> list[SzimElem]:
    """Az előző iterációból áthozott, még le nem zárt elemek."""
    return [
        e for e in allas.elemek.values()
        if e.iteracio < allas.iteracio_id and e.allapot in allapot_modul.AKTIV_ALLAPOTOK
    ]


def _vallalasi_dontes(allas: Allas) -> None:
    keret = _keret(allas)
    athozott = len(_athozott_elemek(allas))
    # A specifikációk jóváhagyása is fogyaszt a keretből, az áthozott elem pedig
    # ugyanúgy bírálatot fog kérni, mint az új — tehát mindkettő levonás.
    javasolt = max(1, int(keret) - 1 - athozott)
    allas.dontes = Dontes(
        kod="vallalas",
        cim=f"Mennyit vállalsz a(z) {allas.iteracio_id}. iterációra?",
        magyarazat=(
            f"A bírálati keret **{keret} elem** {allas.napok} napra. Forrás: "
            f"_{allas.parameter_forras.lower()}_. "
            + (f"Az előző iterációból **{athozott} elem** csúszott át, ezek is bírálatot "
               "kérnek majd, tehát a keretből előre elmennek. "
               if athozott else "")
            + "Ebből a specifikációk jóváhagyása és a biztonsági találatok mérlegelése is "
            "fogyaszt, tehát a kódelemekre valamivel kevesebb marad. A modell szerint nem "
            "az a kérdés, mennyit tudnak az ügynökök megírni, hanem mennyit tudtok "
            "felelősséggel átvenni."
        ),
        valasztasok=[
            Valasztas(str(javasolt), f"{javasolt} elem — a keret szerint", "A modell ajánlása."),
            Valasztas(str(javasolt + 3), f"{javasolt + 3} elem", "Az ügynökök gyorsak, kihasználjuk."),
            Valasztas(str(max(1, javasolt - 2)), f"{max(1, javasolt - 2)} elem", "Óvatosabb vállalás."),
        ],
        tenyek=VallalasTenyek(
            keret=keret,
            parameterek=dict(allas.parameterek),
            parameter_forras=allas.parameter_forras,
            athozott=athozott,
        ),
    )


# --- Eseménynapló ----------------------------------------------------------------


def _esemeny(allas: Allas, esemeny: str, elem_id: str = "", szereplo: str = "",
             biralati_perc: float = 0, hibaosztaly: str = "", reszlet: str = "") -> None:
    allas.esemenyek.append({
        "idopont": allas.most,
        "elem_id": elem_id,
        "esemeny": esemeny,
        "szereplo": szereplo,
        "biralati_perc": round(biralati_perc),
        "hibaosztaly": hibaosztaly,
        "reszlet": reszlet,
    })


# --- Idő -------------------------------------------------------------------------


def _munkaidobe(t: pd.Timestamp) -> pd.Timestamp:
    """A munkanapon kívüli időt a következő munkanap kezdetére tolja."""
    if t.hour < MUNKA_KEZDET:
        return t.normalize() + pd.Timedelta(hours=MUNKA_KEZDET)
    if t.hour >= MUNKA_VEGE:
        return t.normalize() + pd.Timedelta(days=1, hours=MUNKA_KEZDET)
    return t


def _iteracio_vege(allas: Allas) -> pd.Timestamp:
    return allas.kezdet.normalize() + pd.Timedelta(days=allas.napok - 1, hours=MUNKA_VEGE)


# --- A fő ciklus -----------------------------------------------------------------


def lep(allas: Allas) -> Allas:
    """Addig futtatja a szimulációt, amíg emberi döntés nem kell (vagy vége)."""
    orzo = 0
    while allas.dontes is None and not allas.kesz:
        orzo += 1
        if orzo > 5000:  # a szimulált óra sosem áll meg, de a ciklus mégse fusson el
            allas.kesz = True
            break
        _tick(allas)
    return allas


def _tick(allas: Allas) -> None:
    elozo_nap = allas.most.date()
    allas.most = _munkaidobe(allas.most + TICK)
    if allas.most.date() != elozo_nap:
        for sz in allas.szeniorok:
            sz.mai_perc = 0.0  # új nap, új bírálati keret

    if allas.most >= _iteracio_vege(allas):
        # A zárás az iteráció utolsó munkaórájára kerül, nem az utána következő
        # reggelre — különben a bemutató és a visszatekintés kiesne abból az
        # időablakból, amelyre a mérőszámok számolnak.
        allas.most = _iteracio_vege(allas)
        _iteraciot_zar(allas)
        return

    _ugynoki_munka_befejezese(allas)
    if allas.dontes:
        return
    _biralatok_befejezese(allas)
    if allas.dontes:
        return
    _biralatok_inditasa(allas)
    _ugynoki_munka_inditasa(allas)


def _sorban(allas: Allas) -> list[SzimElem]:
    return [e for e in allas.elemek.values() if e.allapot == "Bírálatra vár"]


def felfedezes_esely(meret_sor: int, korlat: int) -> float:
    """Mekkora eséllyel veszi észre a bírálat az elemben lévő hibát.

    A méretkorlát fölötti csomagot felületesebben nézik át (S-06) — a modellben
    éppen ezért van méretkorlát. Külön függvény, hogy önmagában is számon
    kérhető legyen: ha ez a büntetés eltűnne, a méretkorlát értelmét vesztené.
    """
    return FELFEDEZES_ESELY * (NAGY_CSOMAG_SZORZO if meret_sor > korlat else 1.0)


# --- Ügynöki oldal ---------------------------------------------------------------


def _ugynoki_munka_inditasa(allas: Allas) -> None:
    korlat = allas.konfig["wip_korlatok"]["Megvalósítás alatt"]
    biralati_korlat = allas.konfig["wip_korlatok"]["Bírálatra vár"]

    while len(allas.munkaban) < korlat:
        # A modell alapszabálya: ha a bírálati sor betelt, az ügynökök nem
        # kezdenek új feladatot. Ezt a játékos felül tudja írni — és a mérleg
        # ezt szabályszegésként fogja számon kérni.
        if len(_sorban(allas)) >= biralati_korlat and allas.ugynokok_allnak:
            return
        elem = _kovetkezo_elem(allas)
        if elem is None:
            return
        eredmeny = allas.ugynok.dolgozik(elem, allas.szabalyok, allas.kapuk)
        elem.meret_sor = eredmeny.meret_sor
        elem.rejtett_hibak = list(eredmeny.hibak)
        elem.allapot = "Megvalósítás alatt"
        elem.kapu_bukas = eredmeny.kapu_bukott
        allas.munkaban[elem.elem_id] = allas.most + pd.Timedelta(minutes=eredmeny.perc)
        _esemeny(allas, "ugynok_indult", elem.elem_id, allas.ugynok.azonosito)


def _kovetkezo_elem(allas: Allas) -> SzimElem | None:
    """A következő kiadható elem: előbb a javításra váró, aztán az új."""
    for elem in allas.elemek.values():
        if elem.allapot == "Javítás alatt":
            return elem
    for elem in allas.elemek.values():
        if elem.allapot == "Kész a kezdésre":
            return elem
    return None


def _ugynoki_munka_befejezese(allas: Allas) -> None:
    kesz = [eid for eid, vege in allas.munkaban.items() if vege <= allas.most]
    for eid in kesz:
        if allas.dontes:
            return  # egyszerre egy döntést kérünk; a többi elem a következő tickben jön
        elem = allas.elemek[eid]
        del allas.munkaban[eid]

        if elem.kapu_bukas:
            # A verifikáló gépi kapu: még a bírálat előtt visszaadja. Ez gépi
            # kapacitás, nem fogyaszt a bírálati keretből.
            elem.rejtett_hibak = [h for h in elem.rejtett_hibak if h != elem.kapu_bukas]
            elem.allapot = "Javítás alatt"
            elem.korok += 1
            _esemeny(allas, "kapu_bukott", eid, "verifikalo-B", hibaosztaly=elem.kapu_bukas,
                     reszlet="A verifikáló elbuktatta, bírálat elé nem került")
            elem.kapu_bukas = ""
            continue

        if elem.meret_sor > allas.konfig["meretkorlat_sor"]:
            _meretkorlat_dontes(allas, elem)
            return

        _sorba_all(allas, elem)


def _sorba_all(allas: Allas, elem: SzimElem) -> None:
    elem.allapot = "Bírálatra vár"
    elem.kesz_ekkor = allas.most
    _esemeny(allas, "biralatra_kerult", elem.elem_id, allas.ugynok.azonosito)

    korlat = allas.konfig["wip_korlatok"]["Bírálatra vár"]
    if len(_sorban(allas)) >= korlat and not allas.torlodas_kezelve:
        _torlodas_dontes(allas)


# --- Bírálati oldal --------------------------------------------------------------


def _biralatok_inditasa(allas: Allas) -> None:
    napi_keret = allas.parameterek["R"] * 60
    for sz in allas.szeniorok:
        if sz.elem_id or sz.mai_perc >= napi_keret:
            continue
        sor = sorted(_sorban(allas), key=lambda e: e.kesz_ekkor or allas.most)
        if not sor:
            continue
        elem = sor[0]
        # A bírálati idő a mért `t` körül szór; a méretkorlát fölötti csomag tovább tart.
        perc = allas.veletlen.gauss(allas.parameterek["t"], allas.parameterek["t"] * 0.18)
        if elem.meret_sor > allas.konfig["meretkorlat_sor"]:
            perc *= 1.4
        perc = max(20.0, perc)

        elem.allapot = "Bírálat alatt"
        elem.biralo = sz.nev
        sz.elem_id = elem.elem_id
        sz.biralat_perc = perc
        sz.biralat_vege = allas.most + pd.Timedelta(minutes=perc)
        _esemeny(allas, "biralat_indult", elem.elem_id, sz.nev)


def _biralatok_befejezese(allas: Allas) -> None:
    for sz in allas.szeniorok:
        if not sz.elem_id or sz.biralat_vege is None or sz.biralat_vege > allas.most:
            continue
        elem = allas.elemek[sz.elem_id]
        sz.mai_perc += sz.biralat_perc
        sz.osszes_perc += sz.biralat_perc

        esely = felfedezes_esely(elem.meret_sor, allas.konfig["meretkorlat_sor"])
        talalt = [h for h in elem.rejtett_hibak if allas.veletlen.random() < esely]
        elem.talalt_hibak = talalt

        _beolvasztasi_dontes(allas, elem, sz)
        return  # egyszerre egy döntést kérünk


# --- Döntések --------------------------------------------------------------------


def _beolvasztasi_dontes(allas: Allas, elem: SzimElem, sz: Szenior) -> None:
    talalt = elem.talalt_hibak
    sulyos = [h for h in talalt if h in SULYOS]

    # A „{n}. bírálati kör" alak azért kell, mert a „ez a 1. kör" magyarul
    # hibás: az 1-et „első"-nek mondjuk ki, tehát „az" névelő járna hozzá, a
    # 2-höz viszont „a". Névelő nélkül a mondat minden körszámra jó marad.
    jellemzok = f"A csomag {elem.meret_sor} sor"
    if elem.meret_sor > allas.konfig["meretkorlat_sor"]:
        jellemzok += " (a méretkorlát fölött)"
    if elem.magas_kockazat:
        jellemzok += ", magas kockázatú modul"
    jellemzok += f", **{elem.korok + 1}. bírálati kör**."

    zaras = ("A beolvasztásnak megnevezett emberi jóváhagyója lesz — "
             "a felelősség itt keletkezik.")

    if not talalt:
        magyarazat = f"A bírálat **nem talált kifogást**. {jellemzok} {zaras}"
    else:
        magyarazat = (
            f"A bírálat **{len(talalt)} hibát talált** az elemben"
            + (f", ebből **{len(sulyos)} súlyos**" if sulyos else "")
            + ". Nevesítve, súlyosság szerint jelölve alább.\n\n"
            + (
                f"**Mit jelent a súlyos?** Azt, hogy {SULYOS_MAGYARAZAT}, "
                "ha az elem így, javítás nélkül olvad be. Az enyhébb hibaosztály "
                f"ezzel szemben {ENYHE_MAGYARAZAT}.\n\n"
                if sulyos else ""
            )
            + "**Hol lehet javítani?** Itt, a **Visszaküldöm javításra** gombbal: "
            "az ügynök kijavítja a megtalált hibákat, és új bírálati kör indul. "
            "Ha megtalált hibával olvasztod be, a hiba bent marad a termékben — "
            "a zárómérleg ezt szabályszegésként veszi számba"
            + (", a súlyosat ráadásul „szökevény hibaként” is" if sulyos else "")
            + f".\n\n{jellemzok} {zaras}"
        )

    allas.dontes = Dontes(
        kod="beolvasztas",
        cim=f"{sz.nev} elbírálta: {elem.elem_id} — {elem.cim}",
        magyarazat=magyarazat,
        elem_id=elem.elem_id,
        valasztasok=[
            Valasztas("beolvaszt", "Beolvasztom", "Lezárul, és a nevem kerül a nyomvonalra."),
            Valasztas("visszakuld", "Visszaküldöm javításra", "Új kör, újabb bírálati esemény."),
        ],
        tenyek=BeolvasztasTenyek(
            talalt=talalt,
            sulyos=sulyos,
            hibaosztalyok=[hibaosztaly_leiro(h) for h in talalt],
            meret_sor=elem.meret_sor,
            magas_kockazat=elem.magas_kockazat,
            korok=elem.korok,
            biralo=sz.nev,
            perc=round(sz.biralat_perc),
        ),
    )


def _torlodas_dontes(allas: Allas) -> None:
    korlat = allas.konfig["wip_korlatok"]["Bírálatra vár"]
    allas.dontes = Dontes(
        kod="torlodas",
        cim="Betelt a bírálati sor",
        magyarazat=(
            f"{len(_sorban(allas))} elem vár bírálatra, a korlát {korlat}. A modell szerint "
            "ilyenkor az ügynökök nem kezdenek új feladatot, amíg a sor nem apad. "
            "Ezt a döntést nem könnyű meghozni, mert kifelé az látszik, hogy szabad gépi "
            "kapacitás áll üresen. Az általános reflex az lenne, hogy mindenkinek dolgoznia "
            "kell — ez a korlát ezt akadályozza meg, ez ellen véd."
        ),
        valasztasok=[
            Valasztas("leallit", "Leállítom az ügynököket", "A modell szabálya szerint."),
            Valasztas("tovabb", "Hadd dolgozzanak tovább", "A szabad gépi kapacitást kihasználjuk."),
        ],
        tenyek=TorlodasTenyek(varakozok=len(_sorban(allas)), korlat=korlat),
    )


def _meretkorlat_dontes(allas: Allas, elem: SzimElem) -> None:
    korlat = allas.konfig["meretkorlat_sor"]
    _esemeny(allas, "meretkorlat_tullepes", elem.elem_id, "Tóth Bence (SM)",
             reszlet=f"{elem.meret_sor} nettó sor a {korlat}-as korlát ellenében")
    allas.dontes = Dontes(
        kod="meretkorlat",
        cim=f"Túl nagy csomag: {elem.elem_id} — {elem.cim}",
        magyarazat=(
            f"{elem.meret_sor} sor érkezett a {korlat} soros korlát ellenében. A mérések "
            "szerint a nagyobb csomag felületesebb elbírálást vált ki, ezért a modell szerint "
            "ilyenkor nem a bírálatot hosszabbítjuk meg, hanem az elemet bontjuk vissza."
        ),
        elem_id=elem.elem_id,
        valasztasok=[
            Valasztas("visszabont", "Visszabontom két elemre", "Egy plusz bírálati esemény, de átnézhető méret."),
            Valasztas("igy_hagy", "Így nézzük át", "Hosszabb bírálat, nagyobb eséllyel marad benne hiba."),
        ],
        tenyek=MeretkorlatTenyek(meret_sor=elem.meret_sor, korlat=korlat),
    )


# --- A döntés alkalmazása --------------------------------------------------------

def dont(allas: Allas, valasztas: str) -> Allas:
    """A játékos döntésének alkalmazása, majd továbbfutás a következőig."""
    d = allas.dontes
    if d is None:
        return allas
    allas.dontes = None

    if d.kod == "vallalas":
        _vallalas_alkalmaz(allas, int(valasztas))
    elif d.kod == "torlodas":
        _torlodas_alkalmaz(allas, valasztas)
    elif d.kod == "meretkorlat":
        _meretkorlat_alkalmaz(allas, allas.elemek[d.elem_id], valasztas)
    elif d.kod == "beolvasztas":
        _beolvasztas_alkalmaz(allas, allas.elemek[d.elem_id], valasztas)
    elif d.kod == "visszatekintes":
        _visszatekintes_alkalmaz(allas, d.tenyek.hibaosztaly, valasztas)

    return lep(allas)


def _vallalas_alkalmaz(allas: Allas, darab: int) -> None:
    keret = _keret(allas)
    allas.vallalas = darab
    allas.naplo.append(
        f"{allas.iteracio_id}. iteráció — vállalás: {darab} elem (a keret {keret}, "
        f"{allas.parameter_forras.lower()} alapján)."
    )
    if darab > keret:
        allas.szegesek.append(
            f"Túlvállalás: {darab} elemet vállaltál, a bírálati keret {keret} volt."
        )

    if darab > len(allas.keszlet):
        # A backlog véges: a láncban ez előbb-utóbb bekövetkezik, és a mérlegnek
        # látszania kell rajta, különben a kisebb vállalás önfegyelemnek tűnne.
        allas.naplo.append(
            f"A backlogból csak {len(allas.keszlet)} elem maradt, ennyit vettünk be."
        )

    for i in range(darab):
        if not allas.keszlet:
            break
        nyers = allas.keszlet.pop(0)
        eid = f"I{allas.iteracio_id}-{i + 1}"
        allas.elemek[eid] = SzimElem(
            elem_id=eid,
            cim=str(nyers["cim"]),
            tipus=str(nyers["tipus"]),
            magas_kockazat=nyers["magas_kockazat"] == "igen",
            bonyolultsag=int(nyers["bonyolultsag"]),
            iteracio=allas.iteracio_id,
        )
        _esemeny(allas, "spec_jovahagyva", eid, "Nagy Réka (PO)")

    _esemeny(allas, "darabolas_jovahagyva", "", "Nagy Réka (PO)",
             reszlet=f"{darab} elem a {keret} elemes keret mellett")


def _torlodas_alkalmaz(allas: Allas, valasztas: str) -> None:
    allas.torlodas_kezelve = True
    if valasztas == "leallit":
        allas.ugynokok_allnak = True
        allas.naplo.append("Torlódásnál leállítottad az ügynököket — a modell szabálya szerint.")
        _esemeny(allas, "ugynok_leallitva", "", "Tóth Bence (SM)",
                 reszlet="A bírálati sor a korlát fölé ment — új feladat nem indul")
    else:
        allas.ugynokok_allnak = False
        allas.naplo.append("Torlódásnál továbbengedted az ügynököket.")
        allas.szegesek.append(
            "Átlépted a saját WIP-korlátodat: a bírálati sor betelt, de az ügynökök tovább dolgoztak."
        )


def _meretkorlat_alkalmaz(allas: Allas, elem: SzimElem, valasztas: str) -> None:
    if valasztas == "visszabont":
        _esemeny(allas, "visszabontva", elem.elem_id, "Tóth Bence (SM)",
                 reszlet="Szétbontva két kisebb elemre")
        elem.allapot = "Visszabontva"
        fele = elem.meret_sor // 2
        for jel, hibak in (("a", elem.rejtett_hibak[:1]), ("b", elem.rejtett_hibak[1:])):
            uj_id = f"{elem.elem_id}{jel}"
            allas.elemek[uj_id] = SzimElem(
                elem_id=uj_id,
                cim=f"{elem.cim} ({'első' if jel == 'a' else 'második'} rész)",
                tipus=elem.tipus,
                magas_kockazat=elem.magas_kockazat,
                bonyolultsag=max(1, elem.bonyolultsag - 1),
                iteracio=elem.iteracio,
                meret_sor=fele,
                allapot="Bírálatra vár",
                rejtett_hibak=list(hibak),
                szulo=elem.elem_id,
                vallalt=False,
                kesz_ekkor=allas.most,
            )
            _esemeny(allas, "biralatra_kerult", uj_id, allas.ugynok.azonosito)
        allas.naplo.append(f"{elem.elem_id}: visszabontottad a méretkorlát miatt.")
    else:
        allas.naplo.append(f"{elem.elem_id}: a méretkorlát fölött is egyben bíráltattad el.")
        allas.szegesek.append(
            f"{elem.elem_id}: {elem.meret_sor} sort engedtél bírálatra a "
            f"{allas.konfig['meretkorlat_sor']} soros korlát ellenében."
        )
        _sorba_all(allas, elem)


def _beolvasztas_alkalmaz(allas: Allas, elem: SzimElem, valasztas: str) -> None:
    sz = next(s for s in allas.szeniorok if s.elem_id == elem.elem_id)
    perc = sz.biralat_perc
    sz.elem_id = ""
    sz.biralat_vege = None

    if valasztas == "beolvaszt":
        maradt = list(elem.rejtett_hibak)
        elem.beolvadt_hibakkal = maradt
        elem.allapot = "Beolvadt"
        _esemeny(allas, "biralat_jovahagyva", elem.elem_id, sz.nev, biralati_perc=perc,
                 hibaosztaly=maradt[0] if maradt else "",
                 reszlet="Beolvasztva" + (f" — bent maradt: {', '.join(maradt)}" if maradt else ""))
        if elem.talalt_hibak:
            allas.szegesek.append(
                f"{elem.elem_id}: megtalált hibával olvasztottad be "
                f"({', '.join(elem.talalt_hibak)})."
            )
    else:
        # A megtalált hibát a javítás kiveszi; amit a bírálat nem vett észre, bent marad.
        elem.rejtett_hibak = [h for h in elem.rejtett_hibak if h not in elem.talalt_hibak]
        elem.allapot = "Javítás alatt"
        elem.korok += 1
        _esemeny(allas, "biralat_visszakuldve", elem.elem_id, sz.nev, biralati_perc=perc,
                 hibaosztaly=elem.talalt_hibak[0] if elem.talalt_hibak else "",
                 reszlet="Visszaküldve javításra")
        if not elem.talalt_hibak:
            allas.naplo.append(f"{elem.elem_id}: kifogás nélkül küldted vissza — egy kör keret elment rá.")
    elem.talalt_hibak = []


# --- Iterációzárás és visszatekintés ---------------------------------------------


def _iteraciot_zar(allas: Allas) -> None:
    if not any(e["esemeny"] == "bemutato" for e in allas.esemenyek):
        for elem in allas.elemek.values():
            if elem.allapot in ("Kész a kezdésre", "Megvalósítás alatt", "Bírálatra vár",
                                "Bírálat alatt", "Javítás alatt"):
                _esemeny(allas, "atcsuszott", elem.elem_id, "Tóth Bence (SM)",
                         reszlet="Nem készült el az iterációban")
                elem.allapot = "Átcsúszott"
        _esemeny(allas, "bemutato", "", allas.szeniorok[0].nev,
                 reszlet="Az iteráció eredményének bemutatása")
        _esemeny(allas, "retro_gepi", "", "Tóth Bence (SM)",
                 reszlet="A visszatekintés gépi rétege: hibaosztályok áttekintése")

    _visszatekintes_folytatasa(allas)


def _visszatekintes_folytatasa(allas: Allas) -> None:
    """A gépi réteg végigmegy az ismétlődő hibaosztályokon, egyesével."""
    ismetlodo = _ismetlodo_hibaosztalyok(allas)
    nyitott = [h for h in ismetlodo if h not in allas.retro_kezelt]
    if nyitott:
        _visszatekintes_dontes(allas, nyitott[0], ismetlodo[nyitott[0]])
        return

    _esemeny(allas, "retro_emberi", "", "Tóth Bence (SM)", reszlet="Emberi visszatekintés")
    allas.lezart_iteraciok.append(_iteracio_leiro(allas))
    # A mérleget MOST kell kiszámolni, nem a felület kérésére: a `szegesek` és a
    # `naplo` a következő iteráció indulásakor nullázódik.
    allas.lezart_merlegek.append(merleg(allas))
    allas.kesz = True


def _ismetlodo_hibaosztalyok(allas: Allas) -> dict[str, int]:
    """Az EBBEN az iterációban legalább kétszer előfordult hibaosztályok.

    Szándékosan csak a saját időablak: a teljes láncra számolva minden
    visszatekintés újratárgyalná a korábbi iterációk hibaosztályait is, és egy
    már bezárt kapu mögötti osztály örökre napirenden maradna.
    """
    szamlalo: dict[str, int] = {}
    for e in _iteracio_esemenyei(allas, _aktualis_leiro(allas)):
        if e["hibaosztaly"]:
            szamlalo[e["hibaosztaly"]] = szamlalo.get(e["hibaosztaly"], 0) + 1
    return {h: n for h, n in szamlalo.items() if n >= 2}


def _visszatekintes_dontes(allas: Allas, hibaosztaly: str, elofordulas: int) -> None:
    van_szabaly = hibaosztaly in allas.szabalyok
    allas.dontes = Dontes(
        kod="visszatekintes",
        cim=f"Visszatekintés: {hibaosztaly} — {elofordulas} előfordulás",
        magyarazat=(
            ("Erre a hibaosztályra **már van szabály**, mégis visszatért. A modell szerint "
             "ilyenkor nem a szabályt kell átfogalmazni: az utasításfájl puha korlát, a "
             "determinisztikus teszt kemény. "
             if van_szabaly else
             "Ez a hibaosztály ismétlődik, tehát az eszkalációs létra második fokára került. ")
            + "A bizonyíték nem az ügynök ígérete lesz, hanem az, hogy a hibaosztály eltűnik."
        ),
        valasztasok=(
            [Valasztas("kapu", "Gépi kaput építünk köré", "Kemény korlát: a hibaosztály eltűnik."),
             Valasztas("szabaly", "Átfogalmazzuk a szabályt", "Puha korlát — lehet, hogy megint nem fog."),
             Valasztas("semmi", "Most nem lépünk", "Marad, ahogy van.")]
            if van_szabaly else
            [Valasztas("szabaly", "Szabály a szabályfájlba", "Puha korlát, de ritkítja a hibát."),
             Valasztas("kapu", "Rögtön gépi kapu", "Erősebb, de drágább lépés."),
             Valasztas("semmi", "Most nem lépünk", "Marad, ahogy van.")]
        ),
        tenyek=VisszatekintesTenyek(
            hibaosztaly=hibaosztaly, elofordulas=elofordulas, van_szabaly=van_szabaly
        ),
    )


def _mar_van_beavatkozas(allas: Allas, hibaosztaly: str, tipus: str) -> bool:
    """Van-e már ilyen típusú sor a szabályfájlban erre a hibaosztályra.

    A láncban ugyanaz a hibaosztály több visszatekintésre is felkerülhet. A
    szabályfájl viszont nem naplófájl: ugyanaz a szabály ne szerepeljen kétszer,
    különben a Tanulás nézet és a hurokösszesítő is duplán számolná.
    """
    return any(
        str(sor["hibaosztaly"]) == hibaosztaly and str(sor["tipus"]) == tipus
        for sor in allas.szabaly_sorok
    )


def _visszatekintes_alkalmaz(allas: Allas, hibaosztaly: str, valasztas: str) -> None:
    sorszam = len(allas.szabaly_sorok) + 1
    if valasztas in ("kapu", "szabaly") and _mar_van_beavatkozas(
        allas, hibaosztaly, "gepi_kapu" if valasztas == "kapu" else "szabaly"
    ):
        allas.naplo.append(
            f"{hibaosztaly}: ugyanezt a lépést már megtetted egy korábbi iterációban."
        )
        (allas.kapuk if valasztas == "kapu" else allas.szabalyok).add(hibaosztaly)
        allas.retro_kezelt.add(hibaosztaly)
        _visszatekintes_folytatasa(allas)
        return
    if valasztas == "kapu":
        allas.kapuk.add(hibaosztaly)
        allas.szabaly_sorok.append({
            "kod": f"AT-{sorszam:02d}", "cim": f"Architektúrateszt a(z) {hibaosztaly} hibaosztályra",
            "hibaosztaly": hibaosztaly, "letrehozva": str(allas.most), "iteracio": allas.iteracio_id,
            "kategoria": "gepi", "kivalto_elem": "", "tipus": "gepi_kapu",
        })
        allas.naplo.append(f"{hibaosztaly}: gépi kaput építettél köré.")
    elif valasztas == "szabaly":
        allas.szabalyok.add(hibaosztaly)
        allas.szabaly_sorok.append({
            "kod": f"SZ-{sorszam:02d}", "cim": f"Szabály a(z) {hibaosztaly} hibaosztályra",
            "hibaosztaly": hibaosztaly, "letrehozva": str(allas.most), "iteracio": allas.iteracio_id,
            "kategoria": "altalanos", "kivalto_elem": "", "tipus": "szabaly",
        })
        allas.naplo.append(f"{hibaosztaly}: szabályt vettél fel rá.")
    else:
        allas.naplo.append(f"{hibaosztaly}: nem léptél rá.")
        allas.szegesek.append(
            f"{hibaosztaly}: ismétlődő hibaosztály maradt lépés nélkül — a tanulási hurok itt szakad meg."
        )
    allas.retro_kezelt.add(hibaosztaly)
    _visszatekintes_folytatasa(allas)


def _iteracio_leiro(allas: Allas) -> dict:
    return {
        "id": allas.iteracio_id,
        "nev": "Szimulált iteráció",
        "kezdet": str(allas.kezdet.date()),
        "veg": str((allas.kezdet + pd.Timedelta(days=allas.napok - 1)).date()),
        "napok": allas.napok,
        "vallalt": allas.vallalas,
        "parameterek_terv": dict(allas.parameterek),
        "terv_forrasa": allas.parameter_forras,
        "megjegyzes": "Szimulált iteráció, nem mérés.",
    }


def _aktualis_leiro(allas: Allas) -> dict:
    """A most futó — vagy épp lezárt — iteráció leírója."""
    for it in allas.lezart_iteraciok:
        if int(it["id"]) == allas.iteracio_id:
            return it
    return _iteracio_leiro(allas)


def _iteracio_esemenyei(allas: Allas, it: dict) -> list[dict]:
    """Egy iteráció időablakába eső események.

    Ugyanaz az ablak, amellyel a `kapacitas` modul dolgozik, tehát a mérleg és a
    mért paraméterek biztosan ugyanazt a halmazt látják.
    """
    kezdet = pd.Timestamp(it["kezdet"])
    veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
    return [e for e in allas.esemenyek if kezdet <= e["idopont"] < veg]


# --- A lánc: a következő iteráció ------------------------------------------------


def kovetkezo_iteracio(allas: Allas) -> Allas:
    """A lezárt iteráció után a következő indítása — ez zárja be a tanulási hurkot.

    Ami átmegy: a szabályfájl, a gépi kapuk, a teljes eseménynapló, az át nem
    adott munka és a mért paraméterek. Ami nem megy át: a napi bírálati keret, a
    WIP-állapot és az előző iteráció szabályszegései — azok az iterációval együtt
    lezárulnak, különben a mérleg két iteráció hibáit mosná össze.
    """
    if not allas.kesz:
        return allas

    elozo = allas.iteracio_id
    allas.iteracio_id += 1

    # A keret innentől a MÉRT paraméterekből számol. Ez a modell visszacsatolása:
    # a következő vállalást nem a feltevés korlátozza, hanem az, ami tényleg
    # megtörtént. Ha nem zárult le mérhető bírálat, marad az előző terv — nulla
    # validálási idővel a kapacitásképlet nem értelmezhető.
    mert = allas.lezart_merlegek[-1]["mert"]
    if mert["biralatok"] and mert["t"]:
        allas.parameterek = {
            "R": mert["R"] or allas.parameterek["R"],
            "t": mert["t"],
            "r": mert["r"],
        }
        allas.parameter_forras = f"A(z) {elozo}. iteráció mért paraméterei"
    else:
        allas.parameter_forras = (
            f"A(z) {elozo}. iteráció terve — mérhető bírálat nem zárult le"
        )

    # Az új iteráció az előző utáni első munkanap reggelén indul. Az ablakok így
    # nem érnek össze: minden esemény pontosan egy iterációhoz tartozik.
    allas.kezdet = (allas.kezdet.normalize() + pd.Timedelta(days=allas.napok)
                    + pd.Timedelta(hours=MUNKA_KEZDET))
    allas.most = allas.kezdet

    for sz in allas.szeniorok:
        sz.mai_perc, sz.elem_id, sz.biralat_vege, sz.biralat_perc = 0.0, "", None, 0.0
    allas.munkaban.clear()

    allas.torlodas_kezelve = False
    allas.ugynokok_allnak = True
    allas.retro_kezelt = set()
    allas.szegesek = []
    allas.naplo = []
    allas.vallalas = 0
    allas.kesz = False

    # Az átcsúszott elem visszakerül a tábla első oszlopába, és az ügynök
    # újrakezdi. A félkész munkát a motor szándékosan nem viszi tovább: ez a
    # túlvállalás ára, és így a hibák is már az ÚJ szabályokkal keletkeznek —
    # enélkül egy áthozott elem a régi hibaosztályt hozná be a gépi kapu mögé.
    for elem in allas.elemek.values():
        if elem.allapot != "Átcsúszott":
            continue
        elem.allapot = "Kész a kezdésre"
        elem.rejtett_hibak, elem.talalt_hibak = [], []
        elem.kapu_bukas, elem.biralo = "", ""
        elem.kesz_ekkor = None
        _esemeny(allas, "athozva", elem.elem_id, "Nagy Réka (PO)",
                 reszlet=f"Áthozva a(z) {elozo}. iterációból")

    _vallalasi_dontes(allas)
    return allas


def tanulasi_hurok(allas: Allas) -> list[dict]:
    """Hibaosztályonként: hány előfordulás melyik iterációban, és mit léptél rá.

    Ez a lánc bizonyítéka. A koncepció szerint nem az ügynök ígérete mutatja meg,
    hogy a tanulási hurok zárul, hanem az, hogy a hibaosztály **eltűnik**
    (S-26, `koncepcio/03-esemenyek-es-tanulas.md`). Egyetlen iterációból ez nem
    látszik — pontosan ezért maradt üres pont a szimulációban a láncolás előtt.
    """
    leirok = [it for it in allas.lezart_iteraciok if int(it["id"]) != allas.iteracio_id]
    leirok.append(_aktualis_leiro(allas))

    # Hibaosztályonként a legerősebb beavatkozás: a gépi kapu üti a szabályt.
    beavatkozas: dict[str, dict] = {}
    for sor in allas.szabaly_sorok:
        ho = str(sor["hibaosztaly"])
        elozo = beavatkozas.get(ho)
        # A gépi kapu üti a szabályt; azonos típusból a korábbi számít, mert az
        # a kérdés, mikortól kellett volna hatnia.
        if elozo is None or (sor["tipus"] == "gepi_kapu" and elozo["tipus"] != "gepi_kapu"):
            beavatkozas[ho] = sor

    ablakok = {int(it["id"]): _iteracio_esemenyei(allas, it) for it in leirok}

    sorok = []
    for ho in sorted({str(e["hibaosztaly"]) for e in allas.esemenyek if e["hibaosztaly"]}):
        per_iteracio = {
            azon: sum(1 for e in ablak if e["hibaosztaly"] == ho)
            for azon, ablak in ablakok.items()
        }
        b = beavatkozas.get(ho)
        b_iteracio = int(b["iteracio"]) if b else None
        kesobbiek = (
            [n for azon, n in per_iteracio.items() if azon > b_iteracio]
            if b_iteracio is not None else []
        )
        sorok.append({
            "hibaosztaly": ho,
            "iteraciok": per_iteracio,
            "beavatkozas": (
                {"gepi_kapu": "gépi kapu", "szabaly": "szabály"}.get(str(b["tipus"]), "—")
                if b else "—"
            ),
            "beavatkozas_kod": str(b["kod"]) if b else "",
            "beavatkozas_iteracio": b_iteracio,
            "eltunt": bool(kesobbiek) and sum(kesobbiek) == 0,
            "visszatert": bool(kesobbiek) and sum(kesobbiek) > 0,
        })
    return sorok


# --- Kimenet az elemzőrétegnek ---------------------------------------------------


def adatok(allas: Allas) -> Adatok:
    """A szimuláció állapota `Adatok` alakban, hogy minden meglévő nézet működjön rajta."""
    esemenyek = pd.DataFrame(allas.esemenyek or [{
        "idopont": allas.kezdet, "elem_id": "", "esemeny": "spec_jovahagyva",
        "szereplo": "Nagy Réka (PO)", "biralati_perc": 0, "hibaosztaly": "", "reszlet": "",
    }])
    esemenyek = esemenyek.sort_values("idopont", kind="stable").reset_index(drop=True)

    elemek = pd.DataFrame([{
        "elem_id": e.elem_id, "iteracio": e.iteracio or allas.iteracio_id,
        "cim": e.cim, "tipus": e.tipus,
        "magas_kockazat": "igen" if e.magas_kockazat else "nem", "meret_sor": e.meret_sor,
        "vallalt": "igen" if e.vallalt else "nem", "szulo": e.szulo,
    } for e in allas.elemek.values()] or [{
        "elem_id": "", "iteracio": allas.iteracio_id, "cim": "", "tipus": "kod",
        "magas_kockazat": "nem", "meret_sor": 0, "vallalt": "nem", "szulo": "",
    }])

    return Adatok(
        konfig=allas.konfig,
        iteraciok=allas.lezart_iteraciok or [_iteracio_leiro(allas)],
        elemek=elemek,
        esemenyek=esemenyek,
        hibaosztalyok=pd.read_csv(ADATOK_MAPPA / "hibaosztalyok.csv"),
        szabalyok=pd.DataFrame(allas.szabaly_sorok),
        koltseg=pd.DataFrame(columns=["iteracio", "kategoria", "token_ezer", "koltseg_ft"]),
    )


# --- A mérleg --------------------------------------------------------------------


def merleg(allas: Allas) -> dict:
    """Az iteráció zárómérlege: mit mondanak a számok a döntéseidről.

    Mindig az **aktuális** iterációra számol. A láncban a korábbi iterációk
    mérlege az `allas.lezart_merlegek` listában van, a zárás pillanatában
    készített pillanatképként.
    """
    ad = adatok(allas)
    it = _aktualis_leiro(allas)
    ablak = _iteracio_esemenyei(allas, it)
    mert = kapacitas.mert_parameterek(ad.esemenyek, it)
    elso_kor = kapacitas.elso_koros_elfogadas(ad.esemenyek, ad.elemek, it)

    # Az iteráció terméke az, ami EBBEN az időablakban olvadt be — akkor is, ha
    # az elemet egy korábbi iteráció vállalta, és csak most zárult le.
    beolvadt = [allas.elemek[e["elem_id"]] for e in ablak
                if e["esemeny"] == "biralat_jovahagyva"]
    szokevenyek = [(e.elem_id, e.beolvadt_hibakkal) for e in beolvadt if e.beolvadt_hibakkal]
    sulyos = [(eid, [h for h in hibak if h in SULYOS]) for eid, hibak in szokevenyek]
    sulyos = [(eid, hibak) for eid, hibak in sulyos if hibak]

    uj = kapacitas.szamol(mert["R"] or allas.parameterek["R"],
                          mert["t"] or allas.parameterek["t"],
                          mert["r"], allas.napok)

    megjegyzesek = []
    if mert["R"] and mert["R"] < allas.parameterek["R"] * 0.9:
        megjegyzesek.append(
            f"A mért napi bírálati idő ({mert['R']} óra) elmarad a tervezettől "
            f"({allas.parameterek['R']} óra). Ez nem azt jelenti, hogy gyorsabb lett a "
            "bírálat, hanem hogy a bírálók egy részét nem kötötte le munka — a "
            "következő iteráció keretét ezért óvatosan olvasd."
        )
    if elso_kor["arany"] >= 0.9 and sulyos:
        megjegyzesek.append(
            "Magas az első körös elfogadási arány, miközben **súlyos hiba jutott át** "
            f"a bírálaton — vagyis {SULYOS_MAGYARAZAT}, és ez meg is történt. "
            "Ez a kettő együtt nem siker, hanem a felületessé vált bírálat képe — a "
            "mennyiségi mutató itt éppen az ellenkezőjét mutatja a valóságnak."
        )
    if not allas.szegesek and sulyos:
        megjegyzesek.append(
            "A szabályokat végig betartottad, mégis átment **súlyos hiba** — olyan, "
            f"amelynél {SULYOS_MAGYARAZAT}. Ez nem szabályszegés: a bírálat nem vette "
            "észre, a modell kapui pedig valószínűségi szűrők, nem garanciák."
        )
    if not beolvadt:
        megjegyzesek.append(
            "Egyetlen elem sem olvadt be: minden bírálatot visszaküldéssel zártál. "
            "A bírálati keret teljes egészében újramunkára ment el, az iteráció pedig "
            "nem állított elő inkrementumot. A mért paraméterek ezért nem "
            "értelmezhetők — nincs mihez viszonyítani."
        )

    beolvasztasok = [e for e in ablak if e["esemeny"] == "biralat_jovahagyva"]
    szeniorok = set(allas.konfig["szeniorok"])
    emberi = (
        sum(1 for e in beolvasztasok if e["szereplo"] in szeniorok) / len(beolvasztasok)
        if beolvasztasok else 0.0
    )

    return {
        "iteracio": allas.iteracio_id,
        "vallalt": allas.vallalas,
        "beolvadt": len(beolvadt),
        "atcsuszott": sum(1 for e in ablak if e["esemeny"] == "atcsuszott"),
        "athozott": sum(1 for e in ablak if e["esemeny"] == "athozva"),
        "terv": dict(allas.parameterek),
        "mert": mert,
        "kovetkezo_keret": round(uj.elem_per_iteracio, 1),
        "elso_koros_elfogadas": elso_kor,
        "emberi_biralati_arany": float(emberi),
        "szokevenyek": szokevenyek,
        "sulyos_szokevenyek": sulyos,
        "szegesek": allas.szegesek,
        "megjegyzesek": megjegyzesek,
        "naplo": allas.naplo,
    }
