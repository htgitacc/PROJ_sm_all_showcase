"""A „gépi kapu” magyarázata: egy forrásból, és ott látszik, ahol a fogalom előkerül.

A J6 jelzés teendője, a bemutató tanulsága és az eszkalációs létra harmadik foka gépi kaput kér,
de korábban sehol nem volt kimondva, mi az. A magyarázat példája (AT-01) és hivatkozásai a
példaadatra és a dokumentumokra mutatnak: ha azok elmozdulnak, a teszt elbukik.
"""

from __future__ import annotations

import re
from pathlib import Path

from streamlit.testing.v1 import AppTest

from modell import bemutato, dokumentumok, fogalmak, forrasok, hatter, konyvjelzok
from modell.betoltes import betolt

GYOKER = Path(__file__).resolve().parent.parent
BELEPES = str(GYOKER / "streamlit_app.py")
VEGE = len(betolt().esemenyek) - 1  # a kurzor az elejéről indul; a Tanulás a végén mutat mindent


def test_a_peldaul_hozott_gepi_kapu_letezik_a_peldaadatban():
    szabalyok = betolt().szabalyok
    at01 = szabalyok[szabalyok["kod"] == "AT-01"].iloc[0]
    assert at01["tipus"] == "gepi_kapu"
    assert "szűrő megkerülésével elbukik" in at01["cim"]
    assert "a láthatósági szűrő megkerülésével elbukik" in " ".join(fogalmak.GEPI_KAPU.split())


def test_a_magyarazat_hivatkozasai_feloldhatok():
    katalogus = {d.azonosito for d in dokumentumok.katalogus()}
    ki = hatter.linkek(fogalmak.GEPI_KAPU)
    celok = re.findall(r"\]\(([a-z]+)\?dok=([^)&]+)", ki)
    assert ("koncepcio", "koncepcio/02-minosegi-kapuk") in celok
    assert all(cel in katalogus and oldal == hatter.nezet(cel).oldal for oldal, cel in celok)
    assert set(re.findall(r"\bS-\d{2}\b", fogalmak.GEPI_KAPU)) <= set(forrasok.bejegyzesek())


def _expander_cimek(at: AppTest) -> list[str]:
    """Az ikonos `st.expander`-t az AppTest „status” blokknak látja, ezért mindkettőt nézzük."""
    return [e.label for e in at.expander] + [e.label for e in at.get("status")]


def _oldal(fajl: str, **allapot) -> AppTest:
    at = AppTest.from_file(BELEPES, default_timeout=60)
    at.run()
    for k, v in allapot.items():
        at.session_state[k] = v
    at.switch_page(f"app_pages/{fajl}")
    at.run()
    assert not at.exception
    return at


def test_a_bevezetes_es_a_tanulas_megmagyarazza():
    assert fogalmak.GEPI_KAPU_CIM in _expander_cimek(_oldal("bevezetes.py"))
    assert fogalmak.GEPI_KAPU_CIM in _expander_cimek(_oldal("tanulas.py", kurzor=VEGE))


def test_a_most_nezet_a_j6_jelzesnel_megmagyarazza():
    esemenyek = betolt().esemenyek
    kj = konyvjelzok.konyvjelzok(esemenyek)
    assert fogalmak.GEPI_KAPU_CIM in _expander_cimek(_oldal("teendok.py", kurzor=kj["Visszatérő hibaosztály (2. it.)"]))
    # A torlódásnál más jelzés szól (J1), J6 nem: ott a magyarázat sem jelenik meg.
    torlodas = _oldal("teendok.py", kurzor=kj["Torlódás (1. it., 2. nap)"])
    assert torlodas.error or torlodas.warning, "a pillanatban kell aktív jelzés, különben a teszt üres"
    assert fogalmak.GEPI_KAPU_CIM not in _expander_cimek(torlodas)


def test_a_bemutato_visszatero_hibaosztaly_fejezete_megmagyarazza():
    idx = next(i for i, f in enumerate(bemutato.FEJEZETEK) if "J6" in f.jelzesek)
    assert fogalmak.GEPI_KAPU_CIM in _expander_cimek(_oldal("bemutato.py", bemutato_fejezet=idx))
    masik = next(i for i, f in enumerate(bemutato.FEJEZETEK) if "J6" not in f.jelzesek)
    assert fogalmak.GEPI_KAPU_CIM not in _expander_cimek(_oldal("bemutato.py", bemutato_fejezet=masik))


def test_a_tanulas_a_gepi_kapu_kodja_melle_a_cimet_is_kiirja():
    at = _oldal("tanulas.py", kurzor=VEGE)
    szoveg = "\n".join(m.value for m in at.markdown)
    assert "Gépi kapu: **AT-01** — Architektúrateszt" in szoveg


def test_a_szimulacio_kimondja_az_orokolt_szabalyokat():
    """Az `SZ-06` és az `SZ-07` kód önmagában semmit nem mond: a cím és a hibaosztály is kell."""
    from modell import szimulacio as szim

    at = _oldal("szimulacio.py")
    szoveg = "\n".join(m.value for m in at.markdown)
    orokolt = szim.indit(mag=1).szabaly_sorok
    assert {s["kod"] for s in orokolt} == {"SZ-06", "SZ-07"}
    for s in orokolt:
        ho = szim.hibaosztaly_leiro(s["hibaosztaly"])
        assert f"- **{s['kod']}** — {s['cim']} _(hibaosztály: {ho['kod']} · {ho['nev']})_" in szoveg
    assert "csak a **következő** iterációban látszik meg" in szoveg
    assert fogalmak.GEPI_KAPU_CIM in _expander_cimek(at)
