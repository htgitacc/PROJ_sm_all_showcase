"""Az animációs forgatókönyv tesztjei.

A legfontosabb közülük a tábla-egyezés: az animáció nem számolhat mást, mint a
négy táblázatos nézet. Ha valaki új állapotgépet vezetne be a megjelenítőben,
ennek a tesztnek el kell buknia.
"""

from __future__ import annotations

import json

import pytest

from modell import allapot, animacio
from modell.betoltes import betolt


@pytest.fixture(scope="module")
def adatok():
    return betolt()


@pytest.fixture(scope="module")
def forgatokonyv(adatok):
    return animacio.forgatokonyv(adatok)


def kocka(forgatokonyv, cimke: str) -> dict:
    """A megnevezett fejezethez tartozó kocka."""
    idx = next(f["idx"] for f in forgatokonyv["fejezetek"] if f["cimke"].startswith(cimke))
    return forgatokonyv["kockak"][idx]


# --- Épség: egyetlen naplózott esemény sem veszhet el ----------------------------


def test_minden_naplozott_esemeny_kap_kockat(adatok, forgatokonyv):
    naplozott = [k for k in forgatokonyv["kockak"] if k["forras"] == "naplo"]
    assert len(naplozott) == len(adatok.esemenyek)
    assert [k["naplo_idx"] for k in naplozott] == list(range(len(adatok.esemenyek)))


def test_a_forgatokonyv_json_szerializalhato(forgatokonyv):
    """A pandas Timestamp és a NaN itt valós kockázat: némán törné el a nézetet."""
    json.dumps(forgatokonyv, ensure_ascii=False)


# --- A levezetett lépések ---------------------------------------------------------


def test_levezetett_kocka_minden_biralatra_kerules_elott(adatok, forgatokonyv):
    biralatra = (adatok.esemenyek["esemeny"] == "biralatra_kerult").sum()
    levezetett = [k for k in forgatokonyv["kockak"] if k["forras"] == "levezetett"]
    assert len(levezetett) == biralatra
    assert {k["esemeny"] for k in levezetett} == {animacio.LEVEZETETT_ESEMENY}
    assert {k["szereplo"] for k in levezetett} == {"verifikalo-B"}


def test_levezetett_kocka_nem_gyart_idoadatot(forgatokonyv):
    """A levezetett kocka a horgonyeseménye időbélyegét veszi át, nem kitaláltat."""
    kockak = forgatokonyv["kockak"]
    levezetettek = [k for k in kockak if k["forras"] == "levezetett"]
    assert levezetettek, "Levezetett kocka nélkül a teszt nem mondana semmit"
    for k in levezetettek:
        horgony = kockak[k["idx"] + 1]
        assert horgony["esemeny"] == "biralatra_kerult"
        assert horgony["idopont"] == k["idopont"]
        assert horgony["elem_id"] == k["elem_id"]
        assert k["naplo_idx"] is None


def test_levezetett_kocka_a_horgony_elotti_tablat_mutatja(forgatokonyv):
    """A verifikálás pillanatában az elem még nem lehet a bírálati sorban."""
    kockak = forgatokonyv["kockak"]
    for k in kockak:
        if k["forras"] != "levezetett":
            continue
        assert k["elem_id"] not in k["tabla"]["Bírálatra vár"]
        assert k["elem_id"] in kockak[k["idx"] + 1]["tabla"]["Bírálatra vár"]


# --- A tábla nem csúszhat el a táblázatos nézetektől -----------------------------


def test_a_tabla_egyezik_az_allapot_modullal(adatok, forgatokonyv):
    for k in forgatokonyv["kockak"]:
        if k["forras"] != "naplo":
            continue
        p = allapot.pillanat(
            adatok.esemenyek, adatok.elemek, adatok.iteraciok, k["naplo_idx"]
        )
        for sav in animacio.SAVOK:
            assert k["tabla"][sav] == p.oszlop(sav)["elem_id"].tolist(), (
                f"A(z) {k['naplo_idx']}. eseménynél a(z) {sav!r} sáv eltér"
            )


# --- A torlódás: a modell csúcspontja --------------------------------------------


def test_torlodas_a_kulcspillanatban(forgatokonyv):
    """1. it., 2. nap 13:20 — öt elem vár a négyes korláttal szemben."""
    k = kocka(forgatokonyv, "Torlódás")
    assert k["elem_id"] == "I1-7"
    assert k["varakozok"] == 5
    assert k["torlodas"] is True
    assert len(k["tabla"]["Bírálatra vár"]) == 5


def test_torlodas_jelzes_meg_is_tud_szolalni_es_el_is_hallgatni(forgatokonyv):
    """A jelző nem lehet beragadva: kell lennie nyugodt és torlódó kockának is."""
    kockak = forgatokonyv["kockak"]
    korlat = forgatokonyv["konfig"]["wip_korlatok"]["Bírálatra vár"]
    nyugodt = [k for k in kockak if not k["torlodas"]]
    torlodo = [k for k in kockak if k["torlodas"]]
    assert nyugodt and torlodo
    assert all(k["varakozok"] < korlat for k in nyugodt)
    assert all(k["varakozok"] >= korlat for k in torlodo)


def test_az_ugynokok_leallitasa_a_torlodas_utan_jon(forgatokonyv):
    """A leállítás emberi döntés: a Scrum Master mondja ki, nem a rendszer."""
    kockak = forgatokonyv["kockak"]
    leallitas = next(k for k in kockak if k["esemeny"] == "ugynok_leallitva")
    torlodas = kocka(forgatokonyv, "Torlódás")
    assert leallitas["idx"] > torlodas["idx"]
    assert leallitas["szereplo"] == "Tóth Bence (SM)"
    assert leallitas["torlodas"] is True


# --- Méretkorlát -----------------------------------------------------------------


def test_meretkorlat_majd_visszabontas_sorrendben(forgatokonyv):
    kockak = forgatokonyv["kockak"]
    tullepes = next(k for k in kockak if k["esemeny"] == "meretkorlat_tullepes")
    visszabontas = next(k for k in kockak if k["esemeny"] == "visszabontva")
    assert tullepes["elem_id"] == visszabontas["elem_id"] == "I2-6"
    assert tullepes["idx"] < visszabontas["idx"]
    korlat = forgatokonyv["konfig"]["meretkorlat_sor"]
    assert forgatokonyv["elemek"]["I2-6"]["meret_sor"] > korlat


# --- A biztonsági lánc -----------------------------------------------------------


def test_biztonsagi_lanc_szamai(forgatokonyv):
    """4 találatból 3 kiesik, majd a 2. iterációban 2-ből 1 — a cáfoló szűr."""
    szamok = [
        (k["esemeny"], k["talalat_szam"])
        for k in forgatokonyv["kockak"]
        if k["talalat_szam"] is not None
    ]
    assert szamok == [
        ("biztonsagi_talalat", 4),
        ("talalat_cafolva", 3),
        ("biztonsagi_talalat", 2),
        ("talalat_cafolva", 1),
    ]


def test_talalat_szam_csak_illeszkedo_szovegbol(forgatokonyv):
    """Ha az adat elmozdul, inkább semmit ne mutassunk, mint rosszat."""
    assert animacio._talalat_szam("4 találat a láthatósági szabály környékén") == 4
    assert animacio._talalat_szam("nincs benne szám") is None
    assert animacio._talalat_szam("310 nettó sor a 200-as korlát ellenében") is None


# --- Szereplők -------------------------------------------------------------------


def test_ugynokok_es_emberek_szetvalnak(forgatokonyv):
    szereplok = {s["azonosito"]: s for s in forgatokonyv["szereplok"]}
    assert szereplok["implementalo-A"]["tipus"] == "ugynok"
    assert szereplok["Kovács Kata"]["tipus"] == "ember"
    assert szereplok["Kovács Kata"]["szerep"] == "Szenior fejlesztő"
    assert szereplok["Tóth Bence (SM)"]["szerep"] == "SM"
    # A modell sarokpontja: a verifikáló más modellcsaládból való, mint az implementáló.
    assert szereplok["implementalo-A"]["modellcsalad"] == "A"
    assert szereplok["verifikalo-B"]["modellcsalad"] == "B"
    assert szereplok["cafolo-B"]["modellcsalad"] == "B"
