"""A felületen megjelenő magyar címkék és számformátum, egyetlen forrásból.

Az eseménynapló és a hibaosztály-katalógus gépi kódokat használ (`biralatra_kerult`,
`helyesseg`). Ezek az adatban maradnak, mert a tesztek és a koncepció hivatkozik rájuk;
a felhasználó viszont a magyar nevüket látja. Ismeretlen kód esetén a kód maga jelenik
meg, így egy új esemény nem tünteti el az információt, csak a teszt jelez.

Szándékosan új modul: az élő folyamat a már betöltött `modell/*.py` fájlokat nem frissíti
újraindításig, egy új fájl viszont az első importnál frissen töltődik be.
"""

from __future__ import annotations

import json

ESEMENYEK: dict[str, str] = {
    "darabolas_elutasitva": "darabolás visszaküldve",
    "darabolas_jovahagyva": "darabolás jóváhagyva",
    "darabolas_technikai_ok": "darabolás technikai jóváhagyása",
    "spec_jovahagyva": "specifikáció jóváhagyva",
    "ugynok_indult": "ügynök elindult",
    "ugynok_leallitva": "ügynökök leállítva",
    "kapu_bukott": "gépi kapun elbukott",
    "verifikalo_atengedte": "a verifikáló átengedte",
    "biralatra_kerult": "bírálatra került",
    "biralat_indult": "bírálat elkezdődött",
    "biralat_visszakuldve": "visszaküldve javításra",
    "biralat_jovahagyva": "jóváhagyva, beolvadt",
    "meretkorlat_tullepes": "méretkorlát-túllépés",
    "visszabontva": "visszabontva kisebb elemekre",
    "biztonsagi_talalat": "biztonsági találat",
    "talalat_cafolva": "biztonsági találat cáfolva",
    "talalat_elfogadva": "biztonsági találat elfogadva",
    "karakterizacio_eloirva": "karakterizációs tesztréteg előírva",
    "mutacios_alapmeres": "mutációs alapmérés",
    "atcsuszott": "átcsúszott a következő iterációba",
    "athozva": "áthozva az előző iterációból",
    "bemutato": "bemutató",
    "retro_gepi": "visszatekintés — gépi réteg",
    "retro_emberi": "visszatekintés — emberi réteg",
}

KATEGORIAK: dict[str, str] = {
    "adatvedelem": "adatvédelem",
    "hasznalhatosag": "használhatóság",
    "helyesseg": "helyesség",
    "teszteles": "tesztelés",
    "verifikacio": "verifikáció",
    "gepi": "gépi kapu",
}


def esemeny(kod: str) -> str:
    return ESEMENYEK.get(kod, kod)


def kategoria(kod: str) -> str:
    return KATEGORIAK.get(kod, kod)


def szam(ertek: float, tizedes: int = 1) -> str:
    """Magyar tizedesvesszővel: 10.3 → „10,3”."""
    return f"{ertek:.{tizedes}f}".replace(".", ",")


def ora(ertek: float) -> str:
    """Várakozási idő emberi alakban: „most került be”, „4 órája”, „21,2 órája”."""
    if ertek < 0.5:
        return "most került be"
    if ertek < 10:
        return f"{ertek:.0f} órája"
    return f"{szam(ertek)} órája"


def animacio_cimkekkel(oldal_html: str) -> str:
    """Az animáció HTML-jébe beteszi a címketáblát; a színpad ebből írja ki az esemény nevét."""
    szkript = f"<script>window.ESEMENY_CIMKE = {json.dumps(ESEMENYEK, ensure_ascii=False)};</script>"
    hely = oldal_html.find("<script")
    if hely == -1:
        return oldal_html + szkript
    return oldal_html[:hely] + szkript + oldal_html[hely:]
