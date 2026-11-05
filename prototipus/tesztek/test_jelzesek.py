"""A beavatkozási jelzések tesztjei.

A prototípus ellenőrzési feltétele az volt, hogy a példa három kulcspillanatában
a megfelelő jelzés **demonstrálhatóan** megszólaljon. Az itt következő tesztek ezt
rögzítik: ha valaki elrontja a jelzéslogikát vagy a példa adatait, elbuknak.
"""

from __future__ import annotations

import pandas as pd
import pytest

from modell import allapot, jelzesek
from modell.betoltes import betolt


@pytest.fixture(scope="module")
def adatok():
    return betolt()


def index(adatok, esemeny: str, elem: str = "", idopont: str = "") -> int:
    maszk = adatok.esemenyek["esemeny"] == esemeny
    if elem:
        maszk &= adatok.esemenyek["elem_id"] == elem
    if idopont:
        maszk &= adatok.esemenyek["idopont"] == pd.Timestamp(idopont)
    talalat = adatok.esemenyek[maszk]
    assert not talalat.empty, f"Nincs ilyen esemény: {esemeny} {elem} {idopont}"
    return int(talalat.index[0])


def jelzes_ott(adatok, idx: int, kod: str):
    p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, idx)
    return {j.kod: j for j in jelzesek.kiertekel(adatok, p)}[kod]


# --- A három kulcspillanat -------------------------------------------------------


def test_torlodas_az_elso_iteracio_masodik_napjan(adatok):
    """1. it., 2. nap 13:20 — öt elem vár a négyes korláttal szemben."""
    idx = index(adatok, "biralatra_kerult", "I1-7", "2026-09-03 13:20")
    j = jelzes_ott(adatok, idx, "J1")
    assert j.aktiv, "A torlódásjelzésnek meg kell szólalnia"
    assert "5 elem" in j.uzenet
    assert "nem indíthatnak új feladatot" in j.teendo


def test_torlodas_elotte_meg_csendben(adatok):
    """A közvetlenül megelőző eseménynél még négy elem vár — a jelzés a küszöbön szólal meg."""
    idx = index(adatok, "biralatra_kerult", "I1-6", "2026-09-03 13:05")
    j = jelzes_ott(adatok, idx, "J1")
    assert j.aktiv, "Négy elemnél a korlát már elérve, a jelzés aktív"
    korabbi = jelzes_ott(adatok, idx - 1, "J1")
    assert not korabbi.aktiv, "Három elemnél még csendben kell lennie"


def test_meretkorlat_a_310_soros_elemnel(adatok):
    """2. it. — az igénylőfelület 310 sorral érkezik a 200-as korlát ellenében."""
    idx = index(adatok, "meretkorlat_tullepes", "I2-6")
    j = jelzes_ott(adatok, idx, "J8")
    assert j.aktiv
    assert "I2-6" in " ".join(j.reszletek)
    assert "Visszabontás" in j.teendo


def test_meretkorlat_a_visszabontas_utan_elnemul(adatok):
    idx = index(adatok, "visszabontva", "I2-6")
    j = jelzes_ott(adatok, idx, "J8")
    assert not j.aktiv, "A visszabontás után a jelzésnek el kell némulnia"


def test_visszatero_hibaosztaly_a_masodik_iteracioban(adatok):
    """Az SZ-07 szabály felvétele után a HO-02 újra előfordul — eszkaláció a 3. fokra."""
    idx = index(adatok, "talalat_elfogadva", "I2-7")
    j = jelzes_ott(adatok, idx, "J6")
    assert j.aktiv
    assert "HO-02" in " ".join(j.reszletek)
    assert "gépi kaput" in j.teendo


def test_visszatero_hibaosztaly_az_elso_iteracioban_meg_nem(adatok):
    """Az 1. iteráció végén a szabály még csak most született — nincs visszatérés."""
    idx = index(adatok, "retro_gepi", "", "2026-09-04 17:20")
    j = jelzes_ott(adatok, idx, "J6")
    assert not j.aktiv


# --- A modell alapszabálya -------------------------------------------------------


def test_felugyeleti_res_soha_nem_szolal_meg(adatok):
    """Minden beolvasztásnak van megnevezett emberi jóváhagyója — végig, minden pillanatban."""
    for idx in range(0, len(adatok.esemenyek), 7):
        j = jelzes_ott(adatok, idx, "J3")
        assert not j.aktiv, f"Felügyeleti rés a(z) {idx}. eseménynél"


# --- Az összetett jelzés ---------------------------------------------------------


def test_lazulasgyanu_nem_szolal_meg_de_indokolja(adatok):
    """Két komponens teljesül, a harmadik nem — a jelzésnek csendben kell maradnia,
    de meg kell mutatnia, miért."""
    j = jelzes_ott(adatok, len(adatok.esemenyek) - 1, "J9")
    assert not j.aktiv
    reszletek = " ".join(j.reszletek)
    assert "✓ a validálási idő csökken" in reszletek
    assert "✓ az elfogadási arány nő" in reszletek
    assert "✗ a hibaarány nő" in reszletek


def test_gumibelyegzo_kevés_adattal_csendben(adatok):
    """Három lezárt iteráció kell hozzá; kettőnk van, tehát nem szólalhat meg."""
    j = jelzes_ott(adatok, len(adatok.esemenyek) - 1, "J4")
    assert not j.aktiv
    assert "Kevés adat" in " ".join(j.reszletek)


# --- Paramétereltérés ------------------------------------------------------------


def test_parameter_elteres_az_elso_iteracio_utan(adatok):
    """A mért bírálati idő 70 helyett 90 perc lett — a vállalást csökkenteni kell."""
    idx = index(adatok, "retro_emberi")
    j = jelzes_ott(adatok, idx, "J7")
    assert j.aktiv
    reszletek = " ".join(j.reszletek)
    assert "t: terv 70" in reszletek
    assert "8,0 elem" in j.teendo  # magyar tizedesvessző (UX 3. csomag)


# --- Épség -----------------------------------------------------------------------


def test_minden_jelzes_kiertekelheto_minden_pillanatban(adatok):
    """Egyetlen eseményindexnél sem dobhat hibát a kiértékelés."""
    for idx in range(len(adatok.esemenyek)):
        p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, idx)
        eredmeny = jelzesek.kiertekel(adatok, p)
        assert len(eredmeny) == 9


# --- Az időkurzor épsége: semmi nem látszhat a keletkezése előtt -----------------


def test_szabaly_nem_letezik_a_visszatekintes_elott(adatok):
    """A szabályok a visszatekintésen születnek, nem a nap elején.

    Ez a teszt egy valós hibát rögzít: eredetileg a szabály létrehozását dátumként
    tároltuk, így éjféltől létezőnek látszott — az AT-01 gépi kapu órákkal korábban
    jelent meg, mint amikor a csapat megalkotta.
    """
    from modell import tanulas

    # Az SZ-07 a 2026-09-04 17:20-as visszatekintésen születik.
    elotte = index(adatok, "biralat_jovahagyva", "I1-8")  # 2026-09-04 16:50
    p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, elotte)
    osszes = tanulas.hibaosztaly_osszesites(adatok, p)
    ho02 = osszes[osszes["kod"] == "HO-02"].iloc[0]
    assert ho02["szabaly"] == "", "A szabály még nem létezhet a visszatekintés előtt"
    assert ho02["gepi_kapu"] == ""


def test_gepi_kapu_csak_a_masodik_retro_utan(adatok):
    """Az AT-01 a 2. iteráció visszatekintésén születik, nem a találat pillanatában."""
    from modell import tanulas

    talalatkor = index(adatok, "talalat_elfogadva", "I2-7")  # 2026-09-09 13:35
    p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, talalatkor)
    osszes = tanulas.hibaosztaly_osszesites(adatok, p)
    ho02 = osszes[osszes["kod"] == "HO-02"].iloc[0]
    assert ho02["szabaly"] == "SZ-07"
    assert ho02["visszateres_szabaly_utan"] == 1
    assert ho02["gepi_kapu"] == "", "A gépi kapu még nem született meg"
    assert ho02["letrafok"] == 3, "A visszatérés önmagában a 3. fokra emel"

    vegen = allapot.pillanat(
        adatok.esemenyek, adatok.elemek, adatok.iteraciok, len(adatok.esemenyek) - 1
    )
    ho02_veg = tanulas.hibaosztaly_osszesites(adatok, vegen)
    ho02_veg = ho02_veg[ho02_veg["kod"] == "HO-02"].iloc[0]
    assert ho02_veg["gepi_kapu"] == "AT-01", "A retro után már látszik a gépi kapu"


# --- A szakszavak feloldása -------------------------------------------------------
#
# A felhasználó nem értette, mit jelent a „gumibélyegző" és a „lazulásgyanú" —
# egyik szó sem magyarázta meg magát, és egyikhez sem volt angol eredeti (a
# gumibélyegző a "rubber-stamping" tükörfordítása, a lazulásgyanú saját
# szóalkotás). A koncepció saját, világosabb megfogalmazását vettük át.


def test_j4_cime_nem_a_gumibelyegzo_szot_hasznalja(adatok):
    """A cím és a teendő szövege együtt magyarázza a jelenséget, zsargon nélkül."""
    j = jelzes_ott(adatok, len(adatok.esemenyek) - 1, "J4")
    assert j.cim == "Formálissá vált jóváhagyási kapu"
    assert "gumibélyegz" not in j.cim.lower()
    assert "gumibélyegz" not in j.teendo.lower()
    assert "elvesztette a funkcióját" in j.teendo
    assert "formálissá vált" in j.teendo


def test_j9_cime_nem_a_lazulas_szot_hasznalja(adatok):
    """A modellben már bevett „felületessé válás" kifejezést kapja a cím is."""
    j = jelzes_ott(adatok, len(adatok.esemenyek) - 1, "J9")
    assert j.cim == "Bírálat felületessé válása"
    assert "lazulás" not in j.cim.lower()


def test_j9_cime_kevés_adattal_is_egyezik(adatok):
    """A korai visszatérési ág (kevés lezárt iteráció) ugyanazt a címet adja,
    mint a rendes kiértékelés — a két hely korábban két külön szöveget tartott,
    ami könnyen elcsúszhat egymástól."""
    from modell.jelzesek import lazulasgyanu

    j = lazulasgyanu(adatok, allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, 0))
    assert j.cim == "Bírálat felületessé válása"
