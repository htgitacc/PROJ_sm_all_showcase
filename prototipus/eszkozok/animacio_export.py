"""Önálló HTML-fájlba írja az animációt.

A kimenet szerver nélkül, dupla kattintással megnyitható — ez a lényege: a
modellt meg lehessen mutatni annak is, aki nem fog Streamlitet indítani.

Használat:
    .venv/bin/python prototipus/eszkozok/animacio_export.py [kimenet.html]
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from modell import betoltes, cimkek, jelenet  # noqa: E402  (a sys.path beállítása után)

ALAPERTELMEZETT = pathlib.Path("animacio-munkatarskereso.html")


def main() -> None:
    cel = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ALAPERTELMEZETT
    cel.write_text(cimkek.animacio_cimkekkel(jelenet.oldal(betoltes.betolt())), encoding="utf-8")
    meret = cel.stat().st_size / 1024
    print(f"Kész: {cel} ({meret:.0f} KB)")
    print("Megnyitás: böngészőben, szerver nélkül. Egy adott pillanatra: #kocka=37")


if __name__ == "__main__":
    main()
