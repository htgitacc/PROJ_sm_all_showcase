"""Képernyőképet készít az animáció kulcspillanatairól.

A zöld teszt felületnél nem elég: a jelzéslogika hibátlan lehet úgy is, hogy a
színpadon semmi nem látszik. Ez az eszköz az önálló HTML-exportot nyitja meg,
tehát szerver nélkül fut.

Használat:
    .venv/bin/python prototipus/eszkozok/kepernyokepek.py [kimeneti_konyvtar]
        [--szeles=N]

A --szeles az ablak szélessége: 390 (telefon) vagy 1440 (asztali, alapértelmezés).
A színpad egyetlen világos témában van (ADR 0008), ezért nincs sötét változat.
"""

from __future__ import annotations

import pathlib
import sys
import tempfile

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from modell import betoltes, jelenet  # noqa: E402  (a sys.path beállítása után)

# Kocka → fájlnév. Az indexek a forgatókönyv fejezeteivel egyeznek.
PILLANATOK = {
    0: "01-iteracio-eleje",
    37: "02-torlodas",
    121: "03-meretkorlat",
    151: "04-biztonsagi-lanc",
    161: "05-jelen-allapot",
}


def main() -> None:
    argumentumok = sys.argv[1:]
    szeles = next(
        (int(a.split("=")[1]) for a in argumentumok if a.startswith("--szeles=")), 1440
    )
    konyvtar = pathlib.Path(
        next((a for a in argumentumok if not a.startswith("--")), "kepernyokepek")
    )
    konyvtar.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as f:
        f.write(jelenet.oldal(betoltes.betolt()))
        forras = pathlib.Path(f.name)

    utotag = f"-{szeles}"
    hibak: list[str] = []

    with sync_playwright() as p:
        bongeszo = p.chromium.launch()
        oldal = bongeszo.new_page(
            viewport={"width": szeles, "height": 1000},
        )
        oldal.on("pageerror", lambda e: hibak.append(str(e)))
        oldal.goto(f"file://{forras}")
        oldal.wait_for_timeout(500)

        for idx, nev in PILLANATOK.items():
            oldal.evaluate(f"window.animacio.ugras({idx})")
            oldal.wait_for_timeout(600)  # a kártyák átmenete 420 ms
            cel = konyvtar / f"{nev}{utotag}.png"
            oldal.screenshot(path=str(cel), full_page=True)
            print(f"  {cel}")

        bongeszo.close()

    forras.unlink()
    if hibak:
        print("JS-hiba a lejátszóban:", *hibak, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
