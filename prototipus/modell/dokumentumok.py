"""A felületen olvasható háttéranyag: a brief, a koncepció, a sablonok és a kutatás.

Csak olvassa a lezárt anyagot (`koncepcio/`, `kutatas/`, `sm-all.md`) és a mellé készült
spike-okat (`spike/`), nem módosítja őket.
A dokumentumok egymásra fájl-hivatkozásokkal mutatnak; ezeket a felületen kattintható
belső hivatkozássá alakítjuk (`?dok=<azonosító>`), a fájlrendszerre mutatókat, amelyeket
a felület nem tud megnyitni, pedig sima szöveggé, hogy ne maradjon halott link.
"""

from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass
from pathlib import Path

GYOKER = Path(__file__).resolve().parents[2]

CSOPORTOK = {
    "brief": "A kiindulás",
    "koncepcio": "Koncepció — a működési modell",
    "sablon": "Koncepció — használható sablonok",
    "kutatas": "Kutatás — a bizonyíték",
    "spike": "Spike — fejlesztési ötletek",
}

_HIVATKOZAS = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")


@dataclass(frozen=True)
class Dokumentum:
    azonosito: str
    csoport: str
    ut: str
    cim: str

    @property
    def fajl(self) -> Path:
        return GYOKER / self.ut


def _cim(fajl: Path) -> str:
    for sor in fajl.read_text(encoding="utf-8").splitlines():
        if sor.startswith("# "):
            return sor[2:].strip()
    return fajl.stem


def _azonosito(rel: str) -> str:
    if rel == "sm-all.md":
        return "brief"
    return rel.removesuffix(".md")


def _csoport(rel: str) -> str:
    if rel == "sm-all.md":
        return "brief"
    if rel.startswith("koncepcio/sablonok/"):
        return "sablon"
    return rel.split("/", 1)[0]


def katalogus() -> list[Dokumentum]:
    """Az olvasható dokumentumok, a felületen mutatott sorrendben."""
    relativ = ["sm-all.md"]
    relativ += sorted(p.relative_to(GYOKER).as_posix() for p in (GYOKER / "koncepcio").glob("*.md"))
    relativ += sorted(p.relative_to(GYOKER).as_posix() for p in (GYOKER / "koncepcio/sablonok").glob("*.md"))
    relativ += sorted(p.relative_to(GYOKER).as_posix() for p in (GYOKER / "kutatas").glob("*.md"))
    relativ += sorted(p.relative_to(GYOKER).as_posix() for p in (GYOKER / "spike").glob("*/*.md"))
    return [
        Dokumentum(_azonosito(rel), _csoport(rel), rel, _cim(GYOKER / rel))
        for rel in relativ
        if (GYOKER / rel).is_file()
    ]


def belso_hivatkozasok(szoveg: str, relativ_ut: str, ismert: dict[str, Dokumentum]) -> str:
    """A dokumentum fájl-hivatkozásait a felület belső hivatkozásaira cseréli.

    `ismert`: azonosító → dokumentum. Külső (`http…`) és horgony (`#…`) hivatkozás marad.
    Ami a katalógusban nincs benne (forráskód, docs/, mappák), az sima szöveg lesz.
    """
    utak = {d.ut: d.azonosito for d in ismert.values()}
    mappa = posixpath.dirname(relativ_ut)

    def csere(m: re.Match[str]) -> str:
        szoveg_, cel = m.group(1), m.group(2)
        if re.match(r"^[a-z][a-z0-9+.-]*:", cel) or cel.startswith("#"):
            return m.group(0)
        ut = posixpath.normpath(posixpath.join(mappa, cel.split("#", 1)[0]))
        azonosito = utak.get(ut)
        if azonosito is None:
            return szoveg_
        return f"[{szoveg_}](?dok={azonosito})"

    return _HIVATKOZAS.sub(csere, szoveg)
