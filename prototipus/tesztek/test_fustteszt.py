"""Füsttesztek: a felület minden nézete betöltődik, és egy szimulált iteráció végigjátszható.

A motor tesztjei zöldek lehetnek akkor is, ha a felület elszáll: 2026-09-16-án a `KeyError`
és az `AttributeError` a felületen derült ki élesben, mert a felületi réteget semmi nem
futtatta. Ezek a tesztek a Streamlit `AppTest`-jével valóban lefuttatják az oldalakat.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

GYOKER = Path(__file__).resolve().parent.parent
BELEPES = str(GYOKER / "streamlit_app.py")
KULCS = "szimulacio_allas"

# Az aláhúzással kezdődő fájl közös segédmodul (pl. `_hatter_nezet.py`), nem nézet.
NEZETEK = sorted(p.name for p in (GYOKER / "app_pages").glob("*.py") if not p.name.startswith("_"))


def _app() -> AppTest:
    return AppTest.from_file(BELEPES, default_timeout=60)


def _nezet(fajl: str, kurzor: int | None = None) -> AppTest:
    at = _app()
    at.run()
    if kurzor is not None:
        at.session_state["kurzor"] = kurzor
    at.switch_page(f"app_pages/{fajl}")
    at.run()
    return at


def test_a_nezetek_listaja_nem_ures():
    # Ha valaki átnevezi vagy átköltöztetné a mappát, ez a teszt jelzi, mielőtt a paraméterezett
    # tesztek üresen, „zölden” lefutnának.
    assert len(NEZETEK) >= 9


@pytest.mark.parametrize("fajl", NEZETEK)
def test_minden_nezet_hiba_nelkul_betolt(fajl):
    at = _nezet(fajl)
    assert not at.exception, (fajl, [e.value for e in at.exception])


@pytest.mark.parametrize("fajl", ["teendok.py", "iteracio.py", "elorenezes.py", "tanulas.py"])
@pytest.mark.parametrize("kurzor", [0, 1, 17, 40, 63, 90, 117, 135])
def test_az_idokurzorra_epulo_nezetek_minden_pillanatban_betoltenek(fajl, kurzor):
    at = _nezet(fajl, kurzor)
    assert not at.exception, (fajl, kurzor, [e.value for e in at.exception])


def _dontes_gombok(at: AppTest):
    return [b for b in at.button if (b.key or "").startswith("v_")]


def _vegigjatszik(at: AppTest, valasztas: str, max_lepes: int = 80) -> set[str]:
    """Egy iteráció döntéseit a megadott szabály szerint végigkattintja. Visszaadja a látott döntéstípusokat."""
    latott: set[str] = set()
    for _ in range(max_lepes):
        assert not at.exception, [e.value for e in at.exception]
        allas = at.session_state[KULCS]
        if allas.dontes is None:
            return latott
        latott.add(allas.dontes.kod)
        gombok = _dontes_gombok(at)
        assert gombok, f"nincs döntési gomb a(z) {allas.dontes.kod} döntésnél"
        (gombok[0] if valasztas == "elso" else gombok[-1]).click().run()
    raise AssertionError("az iteráció nem zárult le a lépéskeretben")


def _indit(at: AppTest, szam: int | None = None) -> None:
    if szam is not None:
        at.number_input[-1].set_value(szam)  # forgatókönyv-szám
    gomb = next(b for b in at.button if b.label == "Iteráció indítása")
    gomb.click().run()


@pytest.mark.parametrize("valasztas", ["elso", "utolso"])
def test_egy_szimulalt_iteracio_vegigjatszhato_a_merlegig(valasztas):
    at = _nezet("szimulacio.py")
    gomb = next(b for b in at.button if b.label == "Iteráció indítása")
    gomb.click().run()
    _vegigjatszik(at, valasztas)
    assert not at.exception
    allas = at.session_state[KULCS]
    assert allas.dontes is None
    assert any("mérlege" in h.value for h in at.subheader)
    assert "Emberi bírálati arány" in {m.label for m in at.metric}


def test_a_lanc_masodik_iteracioja_is_lefut():
    at = _nezet("szimulacio.py")
    next(b for b in at.button if b.label == "Iteráció indítása").click().run()
    _vegigjatszik(at, "elso")
    kovetkezo = next(b for b in at.button if "iteráció indítása" in b.label and b.label != "Iteráció indítása")
    kovetkezo.click().run()
    assert not at.exception
    allas = at.session_state[KULCS]
    assert allas.iteracio_id == 4 and len(allas.lezart_iteraciok) == 1
    _vegigjatszik(at, "elso")
    assert not at.exception


def test_a_ket_jatekstilus_egyutt_minden_dontestipust_erint():
    latott: set[str] = set()
    for valasztas in ("elso", "utolso"):
        at = _nezet("szimulacio.py")
        next(b for b in at.button if b.label == "Iteráció indítása").click().run()
        latott |= _vegigjatszik(at, valasztas)
    assert latott >= {"vallalas", "beolvasztas", "visszatekintes"}, latott
