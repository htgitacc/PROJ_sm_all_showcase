"""A showcase-README képernyőképeinek gyártása — egységes méretben, egy paranccsal.

A felületet saját szerveren indítja egy szabad porton (127.0.0.1), Playwrighttal lépked, és a végén leállítja.
A képek 1440×1000 pixelesek, a menü az éles megjelenés szerint; a pillanatnézeteknél az oldalsáv
könyvjelzőjével ugrik a példa kulcspillanatára (az időkurzor különben a példa elején áll, ahol még semmi sem
történt).

Használat a repó gyökeréből (a Chromium egyszeri telepítése: `.venv/bin/playwright install chromium`):

    .venv/bin/python prototipus/eszkozok/showcase_kepek.py                 # → docs/screenshots/
    .venv/bin/python prototipus/eszkozok/showcase_kepek.py --only 02       # csak a 02-vel kezdődő kép
    .venv/bin/python prototipus/eszkozok/showcase_kepek.py --out kepek/

Az animáció-nézet egy beágyazott HTML-felület; a szkript megvárja, amíg betölt.
"""

from __future__ import annotations

import argparse
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
WIDTH, HEIGHT = 1440, 1000

# (fájlnév, útvonal, könyvjelző vagy None, gomb az oldalon vagy None, megvárandó elem)
# Az animációnál a könyvjelző a beágyazott lejátszóban van (iframe), nem az oldalsávban.
KEPEK = [
    ("01-bevezetes", "", None, None, "h1"),
    ("02-teendok", "teendok", "Torlódás (1. it., 2. nap)", None, "h1"),
    ("03-iteracio", "iteracio", "Paramétereltérés (1. it. vége)", None, "h1"),
    ("04-animacio", "animacio", "Torlódás (1. it., 2. nap)", None, "iframe"),
    ("05-szimulacio", "szimulacio", None, "Iteráció indítása", "h1"),
    ("06-tanulas", "tanulas", "Visszatérő hibaosztály (2. it.)", None, "h1"),
    ("07-backlog", "backlog", None, None, "h1"),
]


def szabad_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def szerver_indit(port: int) -> subprocess.Popen:
    folyamat = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "prototipus/streamlit_app.py", "--server.headless", "true",
         "--server.address", "127.0.0.1", "--server.port", str(port)],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )  # fmt: skip
    for _ in range(60):
        try:
            if urllib.request.urlopen(f"http://127.0.0.1:{port}/_stcore/health", timeout=1).status == 200:
                return folyamat
        except OSError:
            time.sleep(0.5)
    folyamat.terminate()
    raise RuntimeError("A szerver nem indult el 30 másodpercen belül.")


def lefut(oldal: Page) -> None:
    """Megvárja, amíg a Streamlit végzett (nincs „Running” jelző), majd egy kis türelem az utómunkának."""
    oldal.wait_for_function("() => !document.querySelector('[data-testid=stStatusWidget]')", timeout=60000)
    oldal.wait_for_timeout(1500)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(ROOT / "docs" / "screenshots"), help="célmappa")
    parser.add_argument("--only", help="csak az ilyen előtagú fájlnevű kép (pl. 02)")
    args = parser.parse_args()
    ki = Path(args.out)
    ki.mkdir(parents=True, exist_ok=True)

    port = szabad_port()
    szerver = szerver_indit(port)
    try:
        with sync_playwright() as p:
            bongeszo = p.chromium.launch()
            oldal = bongeszo.new_page(viewport={"width": WIDTH, "height": HEIGHT})
            for nev, ut, konyvjelzo, gomb, var in KEPEK:
                if args.only and not nev.startswith(args.only):
                    continue
                oldal.goto(f"http://127.0.0.1:{port}/{ut}", wait_until="networkidle")
                oldal.wait_for_selector(var, timeout=30000)
                lefut(oldal)
                for felirat in (konyvjelzo, gomb):
                    if felirat:
                        hol = oldal.frame_locator("iframe").first if var == "iframe" else oldal
                        hol.get_by_role("button", name=felirat, exact=True).first.click()
                        lefut(oldal)
                fajl = ki / f"{nev}.png"
                oldal.screenshot(path=str(fajl))
                print("kész:", fajl.relative_to(ROOT) if fajl.is_relative_to(ROOT) else fajl)
            bongeszo.close()
    finally:
        szerver.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
