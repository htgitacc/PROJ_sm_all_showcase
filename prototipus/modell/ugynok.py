"""Az ügynök viselkedése — interfész és determinisztikus megvalósítás.

Ez a modul a szimuláció **varrata**: a motor csak az `Ugynok` felületet ismeri,
tehát ide később be lehet kötni egy valódi modellre épülő megvalósítást anélkül,
hogy a folyamatlogikához hozzá kellene nyúlni. Amíg ez nem történik meg, a
`SzimulaltUgynok` dolgozik: forgatókönyv-számon (seed) alapuló, tehát ugyanaz a forgatókönyv-szám ugyanazt a
történetet adja, és a tesztek is számon kérhetők rajta.

Fontos, hogy ez a modul **nem tudja**, mi a Scrum-folyamat. Egy elemet kap, és
munkaeredményt ad vissza: mennyi ideig tartott, mekkora lett, és milyen hibákat
vitt bele. Hogy ebből mi következik, azt a `szimulacio.py` dönti el.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Protocol

# A hibaosztályok a példa katalógusából valók (adatok/hibaosztalyok.csv), hogy a
# Tanulás nézet és az eszkalációs létra változtatás nélkül működjön rajtuk.
HIBAOSZTALYOK = ["HO-01", "HO-02", "HO-03", "HO-04", "HO-05", "HO-06"]

# Melyik hibaosztály számít súlyosnak. A súlyos hiba beolvasztva valódi
# szökevény hiba lesz; az enyhe legfeljebb kellemetlenség.
SULYOS = {"HO-02", "HO-04", "HO-06"}


@dataclass
class Munkaeredmeny:
    """Amit az ügynök egy elemen végzett munkája után átad."""

    perc: int
    meret_sor: int
    hibak: list[str] = field(default_factory=list)
    kapu_bukott: str = ""  # üres, ha a verifikáló átengedte


class Ugynok(Protocol):
    """A motor ezt a felületet ismeri, semmi mást."""

    azonosito: str

    def dolgozik(self, elem, szabalyok: set[str], kapuk: set[str]) -> Munkaeredmeny:
        """Egy elem megvalósítása.

        A `szabalyok` a szabályfájlban már bent lévő hibaosztályok, a `kapuk` a
        gépi kapuval védettek. A kettő különbözően hat: a szabály puha korlát,
        a gépi kapu kemény — ezt a koncepció 06. dokumentuma mondja ki.
        """
        ...


@dataclass
class SzimulaltUgynok:
    """Determinisztikus, forgatókönyv-számon (seed) alapuló ügynök. Nem hív külső modellt."""

    azonosito: str = "implementalo-A"
    mag: int = 42

    # Egy elem megvalósításának ideje percben. Az ügynök nagyságrenddel gyorsabb
    # az emberi bírálatnál, és egyszerre négyen dolgoznak — ezért termelnek
    # gyorsabban, mint amennyit két szenior el tud bírálni. A modell egész
    # szerkezete ebből a különbségből következik, tehát ezek az értékek nem
    # díszítés: ha lassúra vennénk őket, a torlódás sosem állna elő.
    perc_tartomany: tuple[int, int] = (25, 110)

    # Az AI-val segített változtatások mérete a mérések szerint nagyobb a
    # szokásosnál (S-06), ezért a felső vége átlépi a 200 soros korlátot.
    sor_tartomany: tuple[int, int] = (70, 260)

    hiba_esely: float = 0.55          # esély legalább egy hibára
    masodik_hiba_esely: float = 0.25  # esély egy másodikra is
    szabaly_csillapitas: float = 0.35  # a szabály csökkenti, de nem szünteti meg
    kapu_bukas_esely: float = 0.12     # a verifikáló elkapja, még bírálat előtt

    def __post_init__(self) -> None:
        self._veletlen = random.Random(self.mag)

    def dolgozik(self, elem, szabalyok: set[str], kapuk: set[str]) -> Munkaeredmeny:
        v = self._veletlen
        bonyolultsag = getattr(elem, "bonyolultsag", 2)

        also, felso = self.perc_tartomany
        perc = int(v.uniform(also, felso) * (0.6 + 0.25 * bonyolultsag))

        s_also, s_felso = self.sor_tartomany
        meret = int(v.uniform(s_also, s_felso) * (0.55 + 0.2 * bonyolultsag))

        hibak = self._hibak(v, elem, szabalyok, kapuk)

        # A verifikáló kapu a bírálat ELŐTT fog meg dolgokat: ez gépi kapacitás,
        # nem emberi, tehát nem fogyaszt a bírálati keretből.
        kapu = ""
        if hibak and v.random() < self.kapu_bukas_esely:
            kapu = hibak.pop(0)

        return Munkaeredmeny(perc=perc, meret_sor=meret, hibak=hibak, kapu_bukott=kapu)

    def _hibak(self, v: random.Random, elem, szabalyok: set[str], kapuk: set[str]) -> list[str]:
        """Hibainjektálás, a tanulási hurok hatásával együtt.

        A gépi kapu teljesen kizárja az adott hibaosztályt, a szabály csak
        ritkítja — ez a koncepció állítása arról, hogy az utasításfájl puha
        korlát, a determinisztikus teszt pedig kemény.
        """
        eselyes = [h for h in HIBAOSZTALYOK if h not in kapuk]
        if not eselyes:
            return []

        # A magas kockázatú és a bonyolultabb elem többet hibázik.
        szorzo = 1.0 + (0.3 if getattr(elem, "magas_kockazat", False) else 0.0)
        szorzo *= 0.75 + 0.2 * getattr(elem, "bonyolultsag", 2)

        hibak: list[str] = []
        for esely in (self.hiba_esely, self.masodik_hiba_esely):
            jelolt = v.choice(eselyes)
            if jelolt in hibak:
                continue
            tenyleges = esely * szorzo
            if jelolt in szabalyok:
                tenyleges *= self.szabaly_csillapitas
            if v.random() < tenyleges:
                hibak.append(jelolt)
        return hibak
