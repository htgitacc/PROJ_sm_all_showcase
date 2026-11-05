"""A forgatókönyv beágyazása a színpad HTML-sablonjába.

Külön modul, mert a rétegek nem tudhatnak egymásról: az `animacio.py` adatot
állít elő, ez pedig megjelenítést. Ugyanezt a kimenetet használja a Streamlit
oldal és az önálló fájlt kiíró exportáló is — egy forrás, két út.
"""

from __future__ import annotations

import json
import pathlib

from modell import animacio
from modell.betoltes import Adatok

ANIMACIO_MAPPA = pathlib.Path(__file__).resolve().parent.parent / "animacio"


def oldal(adatok: Adatok) -> str:
    """Önálló, működő HTML-dokumentum: a CSS, a JS és az adat beágyazva."""
    forgatokonyv = animacio.forgatokonyv(adatok)

    # A `<` escape-elése azért kell, mert a JSON egy <script> blokkba kerül: egy
    # `</script>` részlet bármely szövegmezőben kitörne a blokkból. A JSON-elemző
    # a < alakot ugyanúgy olvassa.
    adat_json = json.dumps(forgatokonyv, ensure_ascii=False).replace("<", "\\u003c")

    return (
        (ANIMACIO_MAPPA / "jelenet.html")
        .read_text(encoding="utf-8")
        .replace("/*__CSS__*/", (ANIMACIO_MAPPA / "jelenet.css").read_text(encoding="utf-8"))
        .replace("/*__JS__*/", (ANIMACIO_MAPPA / "jelenet.js").read_text(encoding="utf-8"))
        .replace("__FORGATOKONYV__", adat_json)
    )
