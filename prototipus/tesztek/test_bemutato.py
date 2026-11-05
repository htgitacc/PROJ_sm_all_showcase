"""A Vezetett bemutató és az új menüszerkezet tesztjei.

A bemutató narrációja a példa adataira hivatkozik („öt elem várna, a korlát négy”). Ezek a
tesztek azt őrzik, hogy a fejezetek pillanatai léteznek, a megnevezett jelzések ott tényleg
megszólalnak, és minden gomb létező nézetre visz — vagyis a történet nem csúszhat el az adattól.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from modell import allapot, bemutato, jelzesek, konyvjelzok
from modell.betoltes import betolt

GYOKER = Path(__file__).resolve().parent.parent
BELEPES = str(GYOKER / "streamlit_app.py")
# Időkurzor csak a pillanatnézeteken; a Backlog elemgyűjtő, idővonal nélkül.
PELDA = ["teendok.py", "iteracio.py", "elorenezes.py", "tanulas.py"]
NEM_PELDA = ["bevezetes.py", "bemutato.py", "backlog.py", "animacio.py", "szimulacio.py",
             "kiindulas.py", "kutatas.py", "koncepcio.py", "spike.py"]


@pytest.fixture(scope="module")
def adatok():
    return betolt()


def test_minden_fejezet_pillanata_letezo_konyvjelzo(adatok):
    kj = konyvjelzok.konyvjelzok(adatok.esemenyek)
    for f in bemutato.FEJEZETEK:
        assert f.konyvjelzo is None or f.konyvjelzo in kj, f.cim


def test_minden_fejezet_nezete_letezo_oldal():
    for f in bemutato.FEJEZETEK:
        assert (GYOKER / f.nezet).is_file(), f.nezet


@pytest.mark.parametrize("f", [f for f in bemutato.FEJEZETEK if f.jelzesek], ids=lambda f: f.cim)
def test_a_fejezet_jelzesei_az_adott_pillanatban_tenyleg_megszolalnak(adatok, f):
    index = konyvjelzok.konyvjelzok(adatok.esemenyek)[f.konyvjelzo]
    p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, index)
    aktiv = {j.kod for j in jelzesek.kiertekel(adatok, p) if j.aktiv}
    assert set(f.jelzesek) <= aktiv, (f.cim, set(f.jelzesek) - aktiv)


def _app(oldal: str | None = None) -> AppTest:
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.run()
    if oldal:
        at.switch_page(f"app_pages/{oldal}")
        at.run()
    assert not at.exception, [e.value for e in at.exception]
    return at


def test_a_bemutato_minden_fejezete_vegiglapozhato():
    at = _app("bemutato.py")
    latott = []
    for _ in range(len(bemutato.FEJEZETEK)):
        latott.append(at.subheader[0].value)
        gomb = next(b for b in at.button if b.key == "bemutato_kovetkezo")
        if gomb.disabled:
            break
        gomb.click().run()
        assert not at.exception, [e.value for e in at.exception]
    assert latott == [f"{i}. {f.cim}" for i, f in enumerate(bemutato.FEJEZETEK)]


def test_a_reszletes_nezet_gomb_a_fejezet_pillanatara_allitja_a_kurzort(adatok):
    i = next(k for k, f in enumerate(bemutato.FEJEZETEK) if f.cim == "Torlódás")
    at = _app("bemutato.py")
    at.session_state["bemutato_fejezet"] = i
    at.run()
    next(b for b in at.button if b.key == f"bemutato_nezet_{i}").click().run()
    assert not at.exception
    vart = konyvjelzok.konyvjelzok(adatok.esemenyek)["Torlódás (1. it., 2. nap)"]
    assert at.session_state["kurzor"] == vart
    assert any("Torlódás a bírálati soron" in w.value for w in [*at.warning, *at.error])


@pytest.mark.parametrize("oldal", PELDA)
def test_az_idokurzor_a_pelda_nezetein_latszik(oldal):
    assert len(_app(oldal).sidebar.slider) == 1


@pytest.mark.parametrize("oldal", NEM_PELDA)
def test_az_idokurzor_mashol_nem_latszik(oldal):
    assert len(_app(oldal).sidebar.slider) == 0


def test_a_bevezetes_gombjai_a_bemutatora_es_a_szimulaciora_visznek():
    at = _app()
    keys = {b.key for b in at.button}
    assert {"hero_bemutato", "hero_szim"} <= keys
    next(b for b in at.button if b.key == "hero_bemutato").click().run()
    assert not at.exception
    assert any(h.value.startswith("0. ") for h in at.subheader)


def _sav_rejtes(at: AppTest) -> bool:
    """Van-e az oldalon az a stílus, amely asztali szélességen elrejti a beragadt oldalsávot."""
    return any("stSidebar" in (getattr(h, "proto", None) and h.proto.body or "") for h in at.get("html"))


@pytest.mark.parametrize("oldal", NEM_PELDA)
def test_kurzor_nelkuli_nezeten_a_beragadt_oldalsav_rejtve(oldal):
    # Kurzoros nézetről átlépve a Streamlit az oldalsávot egy futásig üresen kint hagyja;
    # a stílus ezt rejti el. A böngészős ellenőrzés: docs/HANDOFF.md, Buktatók.
    assert _sav_rejtes(_app(oldal))


@pytest.mark.parametrize("oldal", PELDA)
def test_kurzoros_nezeten_az_oldalsav_nincs_rejtve(oldal):
    assert not _sav_rejtes(_app(oldal))
