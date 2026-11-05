"""A spike-ok tesztjei: a felületen olvashatók, és a forrásaik feloldhatók.

A spike a lezárt kutatás mellé készült fejlesztési ötlet, saját `U-nn` forrásjelöléssel.
"""

from __future__ import annotations

import re
from pathlib import Path

from modell import dokumentumok

GYOKER = dokumentumok.GYOKER
SPIKE = GYOKER / "spike"
KATALOGUS = {d.azonosito: d for d in dokumentumok.katalogus()}


def test_minden_spike_dokumentum_a_katalogusban_van():
    fajlok = sorted(SPIKE.glob("*/*.md"))
    assert fajlok, "nincs spike-dokumentum"
    for f in fajlok:
        azon = f.relative_to(GYOKER).as_posix().removesuffix(".md")
        assert azon in KATALOGUS and KATALOGUS[azon].csoport == "spike", azon


def _forrasok(mappa: Path) -> dict[str, str]:
    szoveg = (mappa / "forrasok.md").read_text(encoding="utf-8")
    reszek = re.split(r"^### (U-\d{2}) — ", szoveg, flags=re.M)
    return {reszek[i]: reszek[i + 1] for i in range(1, len(reszek), 2)}


def test_minden_u_hivatkozas_letezik_a_spike_forrasjegyzekeben():
    for mappa in sorted(p for p in SPIKE.iterdir() if p.is_dir()):
        if not (mappa / "forrasok.md").exists():
            continue
        ismert = set(_forrasok(mappa))
        emlitett = set()
        for f in mappa.glob("*.md"):
            if f.name != "forrasok.md":
                emlitett |= set(re.findall(r"\bU-\d{2}\b", f.read_text(encoding="utf-8")))
        assert emlitett, mappa
        assert emlitett <= ismert, (mappa.name, emlitett - ismert)


def test_minden_spike_forrasnak_van_urlje_es_szintje():
    for mappa in sorted(p for p in SPIKE.iterdir() if p.is_dir()):
        if not (mappa / "forrasok.md").exists():
            continue
        for kod, tartalom in _forrasok(mappa).items():
            assert "https://" in tartalom, kod
            assert re.search(r"\*\*Szint: [ABC]", tartalom), kod
            assert re.search(r"20\d\d", tartalom), kod


def test_a_spike_belso_hivatkozasai_feloldodnak():
    for azon, dok in KATALOGUS.items():
        if dok.csoport != "spike":
            continue
        ki = dokumentumok.belso_hivatkozasok(dok.fajl.read_text(encoding="utf-8"), dok.ut, KATALOGUS)
        for cel in re.findall(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)", ki):
            if cel.startswith(("http", "#")):
                continue
            assert cel.startswith("?dok=") and cel.removeprefix("?dok=") in KATALOGUS, (azon, cel)
