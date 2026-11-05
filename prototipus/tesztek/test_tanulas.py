"""A hibaosztály-magyarázatok tesztjei.

A felhasználó a „Tautologikus teszt" (HO-03) nevet értette, de nem tudta, mi
történik vele a gyakorlatban. A magyarázatnak kód nélkül, egy mondatban kell
elmondania, mit jelent — ez a teszt ezt a két elvárást őrzi.
"""

from __future__ import annotations

from modell import tanulas


def test_ho03_magyarazata_letezik_es_kod_nelkuli():
    magyarazat = tanulas.HIBAOSZTALY_MAGYARAZAT.get("HO-03")
    assert magyarazat, "hiányzik a HO-03 (Tautologikus teszt) magyarázata"
    # „Kód nélkül": ne legyen benne kódrészlet vagy programozási szintaxis.
    for tiltott in ("```", "def ", "assert ", "==", "print("):
        assert tiltott not in magyarazat, f"a magyarázat kódrészletet tartalmaz: {tiltott!r}"


def test_nem_minden_hibaosztalynak_van_magyarazata():
    """A hiányzó bejegyzés szándékos — csak azokhoz készült, amire visszajelzés jött."""
    assert "HO-01" not in tanulas.HIBAOSZTALY_MAGYARAZAT
