"""A Bevezetés nézet tesztjei.

A nézet szövege a lezárt anyag összefoglalója, de a számait és a jelzések neveit a kódból
és az adatokból veszi. Ezek a tesztek azt őrzik, hogy a szöveg ne csússzon el a kódtól.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

GYOKER = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def app():
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=30)
    at.run()
    return at


def _szoveg(at) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_a_bevezetes_a_nyitooldal_hiba_nelkul(app):
    assert not app.exception
    # A nyitóoldalnak nincs külön oldalfejléce: a cím a nyitósávban áll (modell/arculat.py).
    assert not app.title
    sav = [h.proto.body for h in app.get("html") if 'class="sm-hero"' in h.proto.body]
    assert len(sav) == 1 and "Hogyan vezessünk egy Scrum-csapatot" in sav[0]


def test_a_bevezetes_mind_a_kilenc_jelzest_felsorolja(app):
    from modell import jelzesek

    j = jelzesek.kiertekel(app.session_state.adatok, app.session_state.pillanat)
    assert len(j) == 9
    szoveg = _szoveg(app)
    for x in j:
        assert f"{x.kod} · {x.cim}" in szoveg


def test_a_bevezetes_szamai_az_adatokbol_jonnek(app):
    konfig = app.session_state.adatok.konfig
    szoveg = _szoveg(app)
    assert f"legfeljebb {konfig['wip_korlatok']['Bírálatra vár']} elem" in szoveg
    assert f"legfeljebb {konfig['meretkorlat_sor']} sor" in szoveg


def test_a_projekt_fulon_az_iteraciok_nevei_az_adatokbol_jonnek(app):
    szoveg = _szoveg(app)
    for it in app.session_state.adatok.iteraciok:
        assert it["nev"] in szoveg
    assert f"{len(app.session_state.adatok.esemenyek)} naplózott" in szoveg


def test_a_munka_utja_egy_elem_utja_es_kimondja_mi_ismetlodik(app):
    """A hét lépés nem az iteráció köre: az 1–4. előkészít, az 5–7. elemenként ismétlődik."""
    from modell.betoltes import betolt

    adatok = betolt()
    assert "egy backlog-elem útja" in _szoveg(app)
    kepalairas = "\n".join(c.value for c in app.caption)
    assert "Az 1–4. lépés előkészít" in kepalairas
    assert "Az 5–7. lépést minden elem külön járja végig" in kepalairas
    assert f"összesen {len(adatok.elemek)})" in kepalairas
    # A példában tényleg így van: a darabolás jóváhagyása megelőzi az első elem megvalósítását.
    e = adatok.esemenyek
    jovahagyas = e.loc[e["esemeny"] == "darabolas_jovahagyva", "idopont"].min()
    assert jovahagyas < e.loc[e["esemeny"] == "ugynok_indult", "idopont"].min()


def test_a_szamok_backlog_elemet_es_esemenyt_kulon_neveznek(app):
    from modell.betoltes import betolt

    adatok = betolt()
    szoveg = _szoveg(app)
    assert f"{len(adatok.elemek)} backlog-elemének útja ({len(adatok.esemenyek)} naplózott esemény)" in szoveg
