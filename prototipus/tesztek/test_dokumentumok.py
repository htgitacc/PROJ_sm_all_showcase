"""A felületen olvasható háttéranyag tesztjei.

A Bevezetés nem hivatkozhat olyanra, amit a felhasználó kattintással nem ér el.
Ezek a tesztek azt őrzik, hogy minden hivatkozott dokumentum tényleg megnyitható,
és hogy a dokumentumok egymásra mutató hivatkozásai nem maradnak halott fájlhivatkozás.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from modell import dokumentumok, hatter

GYOKER = Path(__file__).resolve().parent.parent
KATALOGUS = {d.azonosito: d for d in dokumentumok.katalogus()}


def test_a_katalogus_tartalmazza_a_hivatkozott_dokumentumokat():
    for a in (
        "brief",
        "koncepcio/00-mukodesi-modell",
        "koncepcio/09-kockazatok-es-kilepes",
        "koncepcio/README",
        "kutatas/00-osszefoglalo",
        "kutatas/forrasok",
        "kutatas/glossary",
    ):
        assert a in KATALOGUS, a


def test_minden_koncepcio_es_kutatasi_dokumentum_olvashato():
    for rel in sorted((dokumentumok.GYOKER / "koncepcio").rglob("*.md")) + sorted(
        (dokumentumok.GYOKER / "kutatas").glob("*.md")
    ):
        assert rel.relative_to(dokumentumok.GYOKER).as_posix().removesuffix(".md") in KATALOGUS


@pytest.mark.parametrize("dok", KATALOGUS.values(), ids=lambda d: d.azonosito)
def test_nem_marad_halott_fajlhivatkozas(dok):
    kimenet = dokumentumok.belso_hivatkozasok(dok.fajl.read_text(encoding="utf-8"), dok.ut, KATALOGUS)
    for cel in re.findall(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)", kimenet):
        if cel.startswith(("http", "#")):
            continue
        assert cel.startswith("?dok="), f"{dok.azonosito}: {cel}"
        assert cel.removeprefix("?dok=") in KATALOGUS, f"{dok.azonosito}: {cel}"


def test_a_relativ_hivatkozas_a_masik_dokumentumra_mutat():
    szoveg = "lásd [a kapuk](02-minosegi-kapuk.md) és [forrás](../kutatas/forrasok.md) és [kód](../prototipus/)"
    kimenet = dokumentumok.belso_hivatkozasok(szoveg, "koncepcio/00-mukodesi-modell.md", KATALOGUS)
    assert "[a kapuk](?dok=koncepcio/02-minosegi-kapuk)" in kimenet
    assert "[forrás](?dok=kutatas/forrasok)" in kimenet
    assert "és kód" in kimenet and "prototipus/)" not in kimenet


def _nezet(dok: str | None) -> AppTest:
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=30)
    if dok:
        at.query_params["dok"] = dok
    oldal = hatter.nezet(dok).oldal if dok in KATALOGUS else "koncepcio"
    at.switch_page(f"app_pages/{oldal}.py")
    at.run()
    return at


def test_a_koncepcio_nezet_megjeleniti_a_kert_dokumentum_szoveget():
    at = _nezet("koncepcio/09-kockazatok-es-kilepes")
    assert not at.exception
    szoveg = "\n".join(m.value for m in at.markdown)
    assert "## Kilépési feltétel" in szoveg
    assert "Leállítjuk, ha" in szoveg


def test_ismeretlen_azonosito_az_alapertelmezett_dokumentumra_esik_vissza():
    at = _nezet("nincs/ilyen")
    assert not at.exception
    assert at.selectbox[0].value == "koncepcio/00-mukodesi-modell"


def test_a_bevezetes_gombja_megnyitja_a_kilepesi_feltetelt():
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=30)
    at.run()
    gomb = next(b for b in at.button if b.key == "dok_koncepcio/09-kockazatok-es-kilepes")
    gomb.click().run()
    assert not at.exception
    szoveg = "\n".join(m.value for m in at.markdown)
    assert "## Kilépési feltétel" in szoveg
