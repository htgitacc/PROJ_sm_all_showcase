"""Az `S-nn` forráshivatkozások kattinthatósága.

A felület nem hivatkozhat forrásra úgy, hogy az olvasó ne tudja megnyitni.
"""

from __future__ import annotations

import re
from pathlib import Path

from streamlit.testing.v1 import AppTest

from modell import forrasok

GYOKER = Path(__file__).resolve().parent.parent


def test_a_hivatkozas_linkke_alakul_a_forras_kodjaval():
    ki = forrasok.linkek("lásd (S-26) és S-02, S-11.")
    assert "[S-26](dokumentumok?dok=kutatas/forrasok&forras=S-26)" in ki
    assert "[S-02](" in ki and "[S-11](" in ki


def test_a_fejlec_a_kod_es_a_mar_link_valtozatlan():
    assert forrasok.linkek("### S-26 — Cím") == "### S-26 — Cím"
    assert forrasok.linkek("a `S-26` kód") == "a `S-26` kód"
    mar = "[S-26](x)"
    assert forrasok.linkek(mar) == mar
    assert forrasok.linkek("nincs hivatkozás, csak S-nn") == "nincs hivatkozás, csak S-nn"


def test_a_jegyzek_minden_forrasa_kinyerheto():
    b = forrasok.bejegyzesek()
    szoveg = forrasok.JEGYZEK.read_text(encoding="utf-8")
    fejlecek = set(re.findall(r"^### (S-\d{2}) — ", szoveg, flags=re.M))
    assert fejlecek and set(b) == fejlecek
    assert all(cim and tartalom for cim, tartalom in b.values())


def test_minden_a_felulet_szovegeiben_emlitett_forras_letezik_a_jegyzekben():
    """A felület nem hivatkozhat nem létező forrásra: a kód- és oldalfájlok S-hivatkozásai mind feloldhatók."""
    ismert = set(forrasok.bejegyzesek())
    fajlok = list((GYOKER / "app_pages").glob("*.py")) + [GYOKER / "modell" / f for f in ("jelzesek.py", "szimulacio.py", "fogalmak.py")]
    emlitett = set()
    for f in fajlok:
        emlitett |= set(re.findall(r"\bS-\d{2}\b", f.read_text(encoding="utf-8")))
    assert emlitett, "nincs egyetlen S-hivatkozás sem — a teszt üres lenne"
    assert emlitett <= ismert, emlitett - ismert


def _forras_nezet(kod: str) -> AppTest:
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=60)
    at.query_params["dok"] = "kutatas/forrasok"
    at.query_params["forras"] = kod
    at.switch_page("app_pages/kutatas.py")
    at.run()
    return at


def test_a_kutatas_nezet_kiemeli_a_kert_forrast():
    at = _forras_nezet("S-26")
    assert not at.exception
    szoveg = "\n".join(m.value for m in at.markdown)
    assert "**S-26 — " in szoveg
    assert "Lent a teljes forrásjegyzék." in "\n".join(c.value for c in at.caption)


def test_ismeretlen_forras_figyelmeztet_nem_szall_el():
    at = _forras_nezet("S-99")
    assert not at.exception
    assert any("S-99" in w.value for w in at.warning)


def _nezet(fajl: str, kurzor: int | None = None) -> AppTest:
    at = AppTest.from_file(str(GYOKER / "streamlit_app.py"), default_timeout=60)
    at.run()
    if kurzor is not None:
        at.session_state["kurzor"] = kurzor
    at.switch_page(f"app_pages/{fajl}")
    at.run()
    assert not at.exception
    return at


def test_a_tanulas_nezet_szovege_kattinthato_forrast_tartalmaz():
    at = _nezet("tanulas.py", kurzor=len(betolt_esemenyek()) - 1)
    assert "](kutatas?dok=kutatas/forrasok&forras=S-08)" in "\n".join(c.value for c in at.caption)


def test_a_most_nezet_aktiv_jelzesenek_forrasa_kattinthato():
    # A torlódás pillanata (1. iteráció, 2. nap 13:20): a J1 jelzés megszólal, forrása S-28.
    at = _nezet("teendok.py", kurzor=at_torlodas_index())
    szoveg = "\n".join(c.value for c in at.caption)
    assert "](kutatas?dok=kutatas/forrasok&forras=S-28)" in szoveg
    assert "dokumentumok?" not in szoveg, "a megszűnt Dokumentumok nézetre mutat"


def at_torlodas_index() -> int:
    from modell import konyvjelzok
    from modell.betoltes import betolt

    return konyvjelzok.konyvjelzok(betolt().esemenyek)["Torlódás (1. it., 2. nap)"]


def betolt_esemenyek():
    from modell.betoltes import betolt

    return betolt().esemenyek
