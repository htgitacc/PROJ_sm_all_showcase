"""Az „Amire épül” menücsoport: a háttéranyag csoportonként külön nézetben.

A Dokumentumok nézet egyetlen legördülőben mutatta a brief, a kutatás, a koncepció és a
spike-ok minden dokumentumát, így nem látszott, mire épül a projekt. A csoportok most saját
nézetet kapnak; ez a modul mondja meg, melyik dokumentum melyik nézetben nyílik, és a belső
hivatkozásokat ehhez igazítja.

Szándékosan külön, új modul: az élő folyamat a már betöltött `modell/*.py` fájlokat nem frissíti
újraindításig, egy új fájl viszont az első importnál frissen töltődik be. A `dokumentumok` és a
`forrasok` modul változatlan; ez a modul az ő kimenetüket irányítja a megfelelő nézetre.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from modell import dokumentumok, forrasok


@dataclass(frozen=True)
class Nezet:
    oldal: str  # az app_pages/ alatti fájl neve kiterjesztés nélkül; ez az URL-útvonal is
    cim: str
    ikon: str
    csoportok: tuple[str, ...]
    alapertelmezett: str
    bevezeto: str


NEZETEK = [
    Nezet(
        "kiindulas",
        "Kiindulás",
        ":material/flag:",
        ("brief",),
        "brief",
        "Az eredeti feladatleírás (brief), amelyből a projekt indult: a cég helyzete, a csapat "
        "felállása és a kérdések, amelyekre a kutatás és a koncepció választ keres.",
    ),
    Nezet(
        "kutatas",
        "Kutatás",
        ":material/travel_explore:",
        ("kutatas",),
        "kutatas/00-osszefoglalo",
        "A bizonyíték: tematikus dokumentumok arról, mit tudunk ma az AI-ügynökös fejlesztőcsapatokról, "
        "vezetői összefoglaló, a forrásjegyzék (az `S-nn` hivatkozások feloldása) és a glossary.",
    ),
    Nezet(
        "koncepcio",
        "Koncepció",
        ":material/architecture:",
        ("koncepcio", "sablon"),
        "koncepcio/00-mukodesi-modell",
        "A kutatásból levezetett működési modell: hogyan darabolunk, bírálunk, mérünk, és ki felel. "
        "Minden döntésnél jelölve, hogy bizonyítékra vagy saját tervezési döntésre épül. A végén a "
        "használható sablonok.",
    ),
    Nezet(
        "spike",
        "Spike-ok",
        ":material/science:",
        ("spike",),
        "spike/01-ugynok-architektura/README",
        "A lezárt anyag mellé készült fejlesztési ötletek, friss célzott kutatással (`U-nn` források) "
        "és döntéssel arról, megéri-e belőlük bemutatható megoldást építeni.",
    ),
]

CSOPORTNEV = "Amire épül"

_CSOPORT_NEZETE = {cs: n for n in NEZETEK for cs in n.csoportok}


def nezet(azonosito: str) -> Nezet:
    """A dokumentum nézete az azonosítója alapján (`kutatas/forrasok` → Kutatás)."""
    return _CSOPORT_NEZETE[dokumentumok._csoport(_relativ(azonosito))]


def oldal_fajl(azonosito: str) -> str:
    """Az `st.switch_page` célja a dokumentumhoz."""
    return f"app_pages/{nezet(azonosito).oldal}.py"


def _relativ(azonosito: str) -> str:
    return "sm-all.md" if azonosito == "brief" else azonosito + ".md"


_BELSO = re.compile(r"\]\((?:dokumentumok)?\?dok=([^)&]+)")


def _iranyit(szoveg: str) -> str:
    return _BELSO.sub(lambda m: f"]({nezet(m.group(1)).oldal}?dok={m.group(1)}", szoveg)


def belso_hivatkozasok(szoveg: str, relativ_ut: str, ismert: dict[str, dokumentumok.Dokumentum]) -> str:
    """Mint `dokumentumok.belso_hivatkozasok`, de a hivatkozás a dokumentum saját nézetébe visz."""
    return _iranyit(dokumentumok.belso_hivatkozasok(szoveg, relativ_ut, ismert))


def linkek(szoveg: str) -> str:
    """Mint `forrasok.linkek`: az `S-nn` hivatkozás a Kutatás nézet forrásjegyzékébe visz."""
    return _iranyit(forrasok.linkek(szoveg))


FORRASJEGYZEK = "kutatas?dok=kutatas/forrasok"
