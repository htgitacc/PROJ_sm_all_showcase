"""A kutatás forrásai (`S-nn`) kattinthatóan.

A felület több helyen hivatkozik forrásra (`S-26`), de a jelölés önmagában semmit nem mond annak,
aki nem ismeri a jegyzéket. Ez a modul az `S-nn` hivatkozást a Dokumentumok nézet megfelelő
bejegyzésére mutató linkké alakítja, és a bejegyzést ki tudja emelni a forrásjegyzékből.

Szándékosan külön, új modul: az élő folyamat a már betöltött `modell/*.py` fájlokat nem frissíti
újraindításig, egy új fájl viszont az első importnál frissen töltődik be.
"""

from __future__ import annotations

import re
from pathlib import Path

JEGYZEK = Path(__file__).resolve().parents[2] / "kutatas" / "forrasok.md"
KOD = re.compile(r"(?<![\w\[`/-])S-(\d{2})(?![\w\]`-])")
_FEJLEC = re.compile(r"^### (S-\d{2}) — (.+)$")


def link(kod: str) -> str:
    return f"dokumentumok?dok=kutatas/forrasok&forras={kod}"


def linkek(szoveg: str) -> str:
    """Az `S-nn` hivatkozásokat linkké alakítja.

    Nem nyúl a fejléc-sorokhoz, a kódrészletekhez (`` `S-26` ``) és a már linkké alakított
    szövegekhez.
    """
    ki = []
    for sor in szoveg.splitlines(keepends=True):
        if sor.lstrip().startswith("#"):
            ki.append(sor)
        else:
            ki.append(KOD.sub(lambda m: f"[S-{m.group(1)}]({link('S-' + m.group(1))})", sor))
    return "".join(ki)


def bejegyzesek() -> dict[str, tuple[str, str]]:
    """{kód: (cím, teljes szöveg)} a forrásjegyzék `### S-nn — …` szakaszaiból."""
    szakaszok: dict[str, tuple[str, list[str]]] = {}
    aktualis = None
    for sor in JEGYZEK.read_text(encoding="utf-8").splitlines():
        m = _FEJLEC.match(sor)
        if m:
            aktualis = m.group(1)
            szakaszok[aktualis] = (m.group(2), [])
        elif sor.startswith("#"):
            aktualis = None
        elif aktualis:
            szakaszok[aktualis][1].append(sor)
    return {k: (cim, "\n".join(sorok).strip()) for k, (cim, sorok) in szakaszok.items()}


def bejegyzes(kod: str) -> tuple[str, str] | None:
    return bejegyzesek().get(kod)
