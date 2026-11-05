"""A szimulációs motor tesztjei.

A legfontosabb közülük az, hogy a döntések **különbséget tesznek**: ha a
modellkövető és a szabálysértő játék ugyanoda jutna, a szimuláció díszlet volna,
nem gyakorlóeszköz.
"""

from __future__ import annotations

import pytest

from modell import allapot, animacio, jelzesek, szimulacio
from modell.betoltes import ellenoriz
from modell.ugynok import SULYOS, SzimulaltUgynok


def vegigjatszik(mag: int, stilus: str) -> tuple[szimulacio.Allas, dict]:
    """Végigjátssza az iterációt adott stílusban, és visszaadja az állást és a mérleget."""
    allas = szimulacio.indit(mag=mag)
    for _ in range(400):
        d = allas.dontes
        if d is None:
            break
        kodok = [v.kod for v in d.valasztasok]
        if stilus == "gondos":
            valasz = {
                "vallalas": kodok[0],
                "torlodas": "leallit",
                "meretkorlat": "visszabont",
            }.get(d.kod)
            if d.kod == "beolvasztas":
                valasz = "visszakuld" if d.tenyek.talalt else "beolvaszt"
            elif d.kod == "visszatekintes":
                valasz = "kapu"
        else:
            valasz = {
                "vallalas": kodok[1],
                "torlodas": "tovabb",
                "meretkorlat": "igy_hagy",
                "beolvasztas": "beolvaszt",
                "visszatekintes": "semmi",
            }[d.kod]
        allas = szimulacio.dont(allas, valasz)
    return allas, szimulacio.merleg(allas)


@pytest.fixture(scope="module")
def gondos():
    return vegigjatszik(11, "gondos")


@pytest.fixture(scope="module")
def gyors():
    return vegigjatszik(11, "gyors")


# --- Épség ------------------------------------------------------------------------


def test_az_iteracio_lezarul(gondos):
    allas, _ = gondos
    assert allas.kesz
    assert allas.dontes is None


def test_a_szimulalt_naplo_atmegy_az_epsegvizsgalaton(gondos):
    """A modell alapszabálya a szimulált naplóra is érvényes: minden
    beolvasztásnak van megnevezett emberi jóváhagyója."""
    allas, _ = gondos
    ellenoriz(szimulacio.adatok(allas))


def test_a_szimulacio_nem_nyul_a_peldaadathoz(gondos):
    """A referenciaadat érinthetetlen: arra a koncepció 07. dokumentuma hivatkozik."""
    from modell.betoltes import betolt

    allas, _ = gondos
    pelda = betolt()
    assert len(pelda.esemenyek) == 136
    assert set(pelda.elemek["elem_id"]) & set(allas.elemek) == set()


def test_ugyanaz_a_mag_ugyanazt_a_tortenetet_adja():
    elso, _ = vegigjatszik(5, "gondos")
    masodik, _ = vegigjatszik(5, "gondos")
    assert [e["esemeny"] for e in elso.esemenyek] == [e["esemeny"] for e in masodik.esemenyek]
    assert [str(e["idopont"]) for e in elso.esemenyek] == [str(e["idopont"]) for e in masodik.esemenyek]


def test_kulonbozo_mag_kulonbozo_tortenet():
    elso, _ = vegigjatszik(5, "gondos")
    masodik, _ = vegigjatszik(99, "gondos")
    assert [e["esemeny"] for e in elso.esemenyek] != [e["esemeny"] for e in masodik.esemenyek]


# --- A meglévő elemzőréteg működik a szimulált naplón ----------------------------


def test_a_jelzesek_ertekelhetok_a_szimulalt_naplon(gondos):
    """Minden pillanatban, nem csak a végén.

    A végállapotra szűkített változat zöld volt, miközben a felület elszállt az
    iteráció elején: ott még egyetlen bírálat sem zárult le, és a nulla
    validálási idővel a kapacitásképlet nem értelmezhető.
    """
    allas, _ = gondos
    adatok = szimulacio.adatok(allas)
    for idx in range(len(adatok.esemenyek)):
        p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, idx)
        assert len(jelzesek.kiertekel(adatok, p)) == 9


def test_a_jelzesek_ertekelhetok_a_frissen_inditott_szimulacion():
    """Az iteráció legelső pillanata: nulla esemény, nulla lezárt bírálat."""
    allas = szimulacio.indit(mag=3)
    adatok = szimulacio.adatok(allas)
    p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, 0)
    eredmeny = {j.kod: j for j in jelzesek.kiertekel(adatok, p)}
    assert len(eredmeny) == 9
    assert not eredmeny["J7"].aktiv


def test_az_animacio_lejatssza_a_szimulalt_naplot(gondos):
    """A megjelenítő eseményfolyamot fogyaszt — mindegy neki, honnan jön."""
    allas, _ = gondos
    forgatokonyv = animacio.forgatokonyv(szimulacio.adatok(allas))
    naplozott = [k for k in forgatokonyv["kockak"] if k["forras"] == "naplo"]
    assert len(naplozott) == len(allas.esemenyek)


def test_a_felugyeleti_res_soha_nem_szolal_meg(gondos):
    allas, _ = gondos
    adatok = szimulacio.adatok(allas)
    for idx in range(0, len(adatok.esemenyek), 5):
        p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, idx)
        j = {x.kod: x for x in jelzesek.kiertekel(adatok, p)}["J3"]
        assert not j.aktiv


# --- A modell szerkezete érvényesül ----------------------------------------------


def test_a_torlodas_eloall(gondos):
    """Ha ez elmarad, a szimuláció nem mutatja meg a modell lényegét: az ügynökök
    gyorsabban termelnek, mint amennyit két szenior el tud bírálni."""
    allas, _ = gondos
    korlat = allas.konfig["wip_korlatok"]["Bírálatra vár"]
    adatok = szimulacio.adatok(allas)
    csucs = 0
    for idx in range(len(adatok.esemenyek)):
        p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, idx)
        csucs = max(csucs, len(p.oszlop("Bírálatra vár")))
    assert csucs >= korlat, f"A bírálati sor csúcsa {csucs} volt a {korlat}-es korlát mellett"


def _indulasok_sorhosszal(allas: szimulacio.Allas) -> list[int]:
    """Minden ügynöki munkakezdéshez: mekkora volt akkor a bírálati sor."""
    adatok = szimulacio.adatok(allas)
    hosszak = []
    for idx, sor in adatok.esemenyek.iterrows():
        if sor["esemeny"] != "ugynok_indult":
            continue
        p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, int(idx))
        hosszak.append(len(p.oszlop("Bírálatra vár")))
    return hosszak


def test_telitett_sor_mellett_nem_indul_uj_ugynoki_munka(gondos):
    """A modell szabálya a gondos játékban ténylegesen köt: ha a bírálati sor
    betelt, az ügynökök nem kezdenek új feladatot."""
    allas, _ = gondos
    korlat = allas.konfig["wip_korlatok"]["Bírálatra vár"]
    assert all(h < korlat for h in _indulasok_sorhosszal(allas))


def test_a_tovabbengedes_atlepi_a_korlatot(gyors):
    """Aki a torlódásnál továbbengedi az ügynököket, annak a naplójában látszania
    kell: telített sor mellett is indult új munka."""
    allas, _ = gyors
    korlat = allas.konfig["wip_korlatok"]["Bírálatra vár"]
    assert any(h >= korlat for h in _indulasok_sorhosszal(allas))


def test_a_nagy_csomagot_felületesebben_nezik_at():
    """A méretkorlát létének oka: a nagyobb csomag rosszabb elbírálást vált ki."""
    korlat = 200
    assert szimulacio.felfedezes_esely(150, korlat) > szimulacio.felfedezes_esely(310, korlat)
    assert szimulacio.felfedezes_esely(korlat, korlat) > szimulacio.felfedezes_esely(korlat + 1, korlat)
    assert 0 < szimulacio.felfedezes_esely(310, korlat) < 1


def test_a_gepi_kapu_kizarja_a_hibaosztalyt():
    """A gépi kapu kemény korlát, a szabály csak puha — ez a koncepció állítása."""
    ugynok = SzimulaltUgynok(mag=3)

    class Elem:
        magas_kockazat = True
        bonyolultsag = 3

    kapuval = [ugynok.dolgozik(Elem(), set(), {"HO-02"}) for _ in range(60)]
    assert all("HO-02" not in e.hibak and e.kapu_bukott != "HO-02" for e in kapuval)

    ugynok2 = SzimulaltUgynok(mag=3)
    kapu_nelkul = [ugynok2.dolgozik(Elem(), set(), set()) for _ in range(60)]
    assert any("HO-02" in e.hibak or e.kapu_bukott == "HO-02" for e in kapu_nelkul)


# --- A döntések számítanak --------------------------------------------------------


def test_a_gyors_jatek_tobb_sulyos_hibat_enged_at(gondos, gyors):
    """Ez a szimuláció létjogosultsága. Ha a két stílus ugyanoda jutna, az egész
    díszlet volna."""
    _, m_gondos = gondos
    _, m_gyors = gyors
    sulyos_gondos = sum(len(h) for _, h in m_gondos["sulyos_szokevenyek"])
    sulyos_gyors = sum(len(h) for _, h in m_gyors["sulyos_szokevenyek"])
    assert sulyos_gyors > sulyos_gondos


def test_a_gyors_jatek_szabalyszegeseket_termel(gondos, gyors):
    _, m_gondos = gondos
    _, m_gyors = gyors
    assert m_gondos["szegesek"] == []
    assert len(m_gyors["szegesek"]) >= 3


def test_a_gyors_jatek_mennyisegi_mutatoi_jobbnak_latszanak(gondos, gyors):
    """A csapda, amit a mérlegnek ki kell mondania: a felületes bírálat szebb
    számokat termel, miközben rosszabb kódot enged ki."""
    _, m_gondos = gondos
    _, m_gyors = gyors
    assert m_gyors["elso_koros_elfogadas"]["arany"] > m_gondos["elso_koros_elfogadas"]["arany"]
    assert m_gyors["beolvadt"] >= m_gondos["beolvadt"]


def test_a_merleg_kimondja_a_csapdat(gyors):
    _, m_gyors = gyors
    egyben = " ".join(m_gyors["megjegyzesek"])
    assert "felületessé vált bírálat" in egyben


def test_a_tulvallalas_szabalyszegesként_jelenik_meg(gyors):
    _, m_gyors = gyors
    assert any("Túlvállalás" in s for s in m_gyors["szegesek"])


def test_a_mindig_visszakuldo_jatek_nem_allit_elo_inkrementumot():
    """Elfajult eset, amely a felületen valós hibát mutatott: ha semmi nem olvad
    be, a mért paraméterek nem nullák, hanem értelmezhetetlenek."""
    allas = szimulacio.indit(mag=11)
    for _ in range(400):
        d = allas.dontes
        if d is None:
            break
        valasz = {"vallalas": d.valasztasok[0].kod, "torlodas": "leallit",
                  "meretkorlat": "visszabont", "beolvasztas": "visszakuld",
                  "visszatekintes": "semmi"}[d.kod]
        allas = szimulacio.dont(allas, valasz)

    m = szimulacio.merleg(allas)
    assert m["beolvadt"] == 0
    assert m["mert"]["biralatok"] == 0
    assert m["szokevenyek"] == []
    assert any("nem állított elő inkrementumot" in mj for mj in m["megjegyzesek"])


def test_minden_beolvasztast_ember_hagyott_jova(gondos, gyors):
    for _, merleg in (gondos, gyors):
        assert merleg["emberi_biralati_arany"] == 1.0


# --- A súlyos hibák köre ----------------------------------------------------------


def test_sulyos_szokevenyek_reszhalmaza_a_szokevenyeknek(gyors):
    _, m = gyors
    osszes = {eid for eid, _ in m["szokevenyek"]}
    for eid, hibak in m["sulyos_szokevenyek"]:
        assert eid in osszes
        assert all(h in SULYOS for h in hibak)


# --- A lánc: több egymást követő iteráció ----------------------------------------
#
# Ez a szimuláció addig üresen maradt pontja. Egyetlen iterációból nem látszik,
# hogy a visszatekintési döntésnek van-e következménye; a koncepció szerint épp
# az a bizonyíték a tanulási hurokra, hogy a hibaosztály ELTŰNIK (S-26).


def lancot_jatszik(mag: int, stilus: str, iteraciok: int = 3) -> szimulacio.Allas:
    """Több egymást követő iterációt játszik végig ugyanabban a stílusban."""
    allas = szimulacio.indit(mag=mag)
    for kor in range(iteraciok):
        for _ in range(800):
            if allas.dontes is None:
                break
            allas = szimulacio.dont(allas, _valasz(allas.dontes, stilus))
        assert allas.kesz, f"a(z) {kor + 1}. iteráció nem zárult le"
        if kor < iteraciok - 1:
            allas = szimulacio.kovetkezo_iteracio(allas)
    return allas


def _valasz(d: szimulacio.Dontes, stilus: str) -> str:
    """Ugyanaz a két játékstílus, mint az egyiterációs teszteknél."""
    if stilus == "gondos":
        if d.kod == "beolvasztas":
            return "visszakuld" if d.tenyek.talalt else "beolvaszt"
        if d.kod == "visszatekintes":
            return "kapu"
        return {"vallalas": d.valasztasok[0].kod, "torlodas": "leallit",
                "meretkorlat": "visszabont"}[d.kod]
    return {"vallalas": d.valasztasok[1].kod, "torlodas": "tovabb",
            "meretkorlat": "igy_hagy", "beolvasztas": "beolvaszt",
            "visszatekintes": "semmi"}[d.kod]


@pytest.fixture(scope="module")
def gondos_lanc():
    return lancot_jatszik(11, "gondos")


@pytest.fixture(scope="module")
def gyors_lanc():
    return lancot_jatszik(11, "gyors")


def test_a_lanc_harom_iteraciot_zar_le(gondos_lanc):
    assert [it["id"] for it in gondos_lanc.lezart_iteraciok] == [3, 4, 5]
    assert len(gondos_lanc.lezart_merlegek) == 3
    assert [m["iteracio"] for m in gondos_lanc.lezart_merlegek] == [3, 4, 5]


def test_a_lancolt_naplo_atmegy_az_epsegvizsgalaton(gondos_lanc, gyors_lanc):
    """A modell alapszabálya a három iteráció együttes naplójára is érvényes."""
    for allas in (gondos_lanc, gyors_lanc):
        ellenoriz(szimulacio.adatok(allas))


def test_minden_esemeny_pontosan_egy_iteracioba_esik(gondos_lanc):
    """Az iterációablakok nem érnek össze, és nem hagynak rést.

    Ezen múlik minden iterációnkénti mérőszám: ha az ablakok átfednének, egy
    bírálat két iteráció mért paraméterébe is beleszámítana.
    """
    import pandas as pd

    for e in gondos_lanc.esemenyek:
        talalat = [
            it for it in gondos_lanc.lezart_iteraciok
            if pd.Timestamp(it["kezdet"]) <= e["idopont"]
            < pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
        ]
        assert len(talalat) == 1, f"{e['idopont']} → {len(talalat)} iteráció"


def test_a_gepi_kapu_utan_eltunik_a_hibaosztaly(gondos_lanc):
    """Ez a láncolás létjogosultsága, és a koncepció központi állítása.

    A gépi kapu kemény korlát: amelyik hibaosztály köré az egyik iteráció
    visszatekintésén kaput építettek, annak a következő iterációkban nulla
    előfordulása lehet.
    """
    hurok = szimulacio.tanulasi_hurok(gondos_lanc)
    kapuzott = [
        s for s in hurok
        if s["beavatkozas"] == "gépi kapu" and s["beavatkozas_iteracio"] is not None
    ]
    assert kapuzott, "a gondos játék egyetlen kaput sem épített — a teszt így vak volna"

    ellenorzott = 0
    for sor in kapuzott:
        kesobbiek = {
            azon: n for azon, n in sor["iteraciok"].items()
            if azon > sor["beavatkozas_iteracio"]
        }
        if not kesobbiek:
            continue  # az utolsó iterációban épült kapunak még nincs utóélete
        ellenorzott += 1
        assert sum(kesobbiek.values()) == 0, (
            f"{sor['hibaosztaly']}: a kapu a {sor['beavatkozas_iteracio']}. "
            f"iterációban épült, mégis visszatért: {kesobbiek}"
        )
    assert ellenorzott, "egyetlen kapunak sem volt következő iterációja"


def test_a_lepes_nelkuli_jatekban_nem_tunik_el_a_hibaosztaly(gondos_lanc, gyors_lanc):
    """A kontraszt: aki a visszatekintésen nem lép, annak a hibaosztály marad.

    Ha ez a kettő ugyanoda jutna, a visszatekintési döntés díszlet volna.
    """
    gondos_hurok = szimulacio.tanulasi_hurok(gondos_lanc)
    gyors_hurok = szimulacio.tanulasi_hurok(gyors_lanc)
    assert any(s["eltunt"] for s in gondos_hurok)
    assert not any(s["eltunt"] for s in gyors_hurok)
    assert any(s["visszatert"] for s in gyors_hurok)


def test_a_szabaly_nem_kemeny_korlat(gyors_lanc):
    """A puha korlát állítása: az örökölt szabály ellenére a hibaosztály visszatér.

    Az `SZ-06` és az `SZ-07` az első iteráció óta él, mégis termel előfordulást —
    a koncepció szerint pontosan ezért kell az eszkalációs létra.
    """
    hurok = {s["hibaosztaly"]: s for s in szimulacio.tanulasi_hurok(gyors_lanc)}
    szabalyos = [s for s in hurok.values() if s["beavatkozas"] == "szabály"]
    assert szabalyos, "nincs szabállyal védett hibaosztály a naplóban"
    assert any(s["visszatert"] for s in szabalyos)


def test_az_atcsuszott_elem_athozodik(gondos_lanc):
    """Az át nem adott munka nem tűnik el: a következő iteráció elején visszakerül."""
    athozott = [e for e in gondos_lanc.esemenyek if e["esemeny"] == "athozva"]
    assert athozott, "egyetlen elem sem csúszott át — a teszt így nem mér semmit"

    for e in athozott:
        kesobbi = [
            k for k in gondos_lanc.esemenyek
            if k["elem_id"] == e["elem_id"] and k["idopont"] > e["idopont"]
        ]
        assert kesobbi, f"{e['elem_id']}: áthoztuk, de nem történt vele semmi"

    # Az áthozott elem az EREDETI iterációjához tartozik: az elsőkörös elfogadást
    # annak az iterációnak a vállalása felől kell nézni, amelyik betette.
    for e in athozott:
        elem = gondos_lanc.elemek[e["elem_id"]]
        assert elem.elem_id.startswith(f"I{elem.iteracio}-")
        assert elem.iteracio < gondos_lanc.iteracio_id


def test_az_athozott_elem_allapota_a_tabla_elso_oszlopa(gondos_lanc):
    """Az `athozva` esemény ugyanúgy állapotátmenet, mint a többi — nem új fogalom."""
    adatok = szimulacio.adatok(gondos_lanc)
    athozott = [e for e in gondos_lanc.esemenyek if e["esemeny"] == "athozva"]
    idx = list(adatok.esemenyek["esemeny"]).index("athozva")
    p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, idx)
    elso = adatok.esemenyek.loc[idx, "elem_id"]
    sor = p.elemallapot[p.elemallapot["elem_id"] == elso]
    assert athozott
    assert sor.iloc[0]["allapot"] == "Kész a kezdésre"


def test_a_kovetkezo_iteracio_a_mert_parameterekkel_szamol(gondos_lanc):
    """A visszacsatolás: a következő keretet nem a feltevés adja, hanem a mérés."""
    elso_merleg = gondos_lanc.lezart_merlegek[0]
    masodik = gondos_lanc.lezart_iteraciok[1]
    assert masodik["terv_forrasa"] == "A(z) 3. iteráció mért paraméterei"
    assert masodik["parameterek_terv"]["t"] == elso_merleg["mert"]["t"]
    assert masodik["parameterek_terv"]["r"] == elso_merleg["mert"]["r"]
    # A kiinduló feltevés ettől el is tér — ha egyeznének, a teszt vak volna.
    assert masodik["parameterek_terv"] != gondos_lanc.lezart_iteraciok[0]["parameterek_terv"]


def test_az_iteraciok_merlege_kulon_all(gyors_lanc):
    """A szabályszegés az iterációjához tartozik, nem halmozódik át a következőbe.

    Nem a szövegek egyedisége a kérdés — „HO-01: nem léptél rá." mindhárom
    iterációban elhangozhat. A kérdés az, hogy egy iteráció mérlege ne
    hivatkozzon másik iteráció elemére, és ne gyűjtse össze a korábbiakat.
    """
    import re

    merlegek = gyors_lanc.lezart_merlegek
    assert all(m["szegesek"] for m in merlegek), "a gyors játék mindhárom iterációban szeg"

    for m in merlegek:
        sajat = f"I{m['iteracio']}-"
        for sor in m["naplo"] + m["szegesek"]:
            for hivatkozott in re.findall(r"\bI\d+-", sor):
                assert hivatkozott == sajat, (
                    f"a(z) {m['iteracio']}. iteráció mérlege {hivatkozott} elemre hivatkozik: {sor}"
                )

    # A halmozódás ellenpróbája: a mérlegek nem egymás bővítései.
    for korabbi, kesobbi in zip(merlegek, merlegek[1:]):
        assert not set(korabbi["szegesek"]) <= set(kesobbi["szegesek"])


def test_egy_hibaosztalyra_egy_beavatkozas_kerul_a_szabalyfajlba(gondos_lanc):
    """A szabályfájl nem naplófájl: ugyanaz a kapu ne szerepeljen kétszer.

    Ez regresszió: a visszatekintés eredetileg a TELJES láncot nézte, ezért a
    következő iteráció újratárgyalta a már bezárt hibaosztályokat is, és minden
    körben új sort írt a szabályfájlba.
    """
    parok = [(s["hibaosztaly"], s["tipus"]) for s in gondos_lanc.szabaly_sorok]
    assert len(parok) == len(set(parok))
    kodok = [s["kod"] for s in gondos_lanc.szabaly_sorok]
    assert len(kodok) == len(set(kodok))


def test_a_visszatekintes_csak_a_sajat_iteraciojat_nezi(gondos_lanc):
    """Ugyanennek a másik oldala: a kapu után nem születik újabb döntés rá."""
    adatok = szimulacio.adatok(gondos_lanc)
    kapuzott = {
        s["hibaosztaly"] for s in szimulacio.tanulasi_hurok(gondos_lanc)
        if s["beavatkozas"] == "gépi kapu"
    }
    for ho in kapuzott:
        sorok = [s for s in gondos_lanc.szabaly_sorok
                 if s["hibaosztaly"] == ho and s["tipus"] == "gepi_kapu"]
        assert len(sorok) == 1
    assert not adatok.szabalyok.empty


def test_az_animacio_lejatssza_a_lancolt_naplot(gondos_lanc):
    """A színpad három iterációt is lejátszik — ugyanaz a megjelenítő."""
    adatok = szimulacio.adatok(gondos_lanc)
    forgatokonyv = animacio.forgatokonyv(adatok)
    naplozott = [k for k in forgatokonyv["kockak"] if k["forras"] == "naplo"]
    assert len(naplozott) == len(gondos_lanc.esemenyek)
    assert [it["id"] for it in forgatokonyv["iteraciok"]] == [3, 4, 5]
    assert {k["iteracio"] for k in forgatokonyv["kockak"]} == {3, 4, 5}


def test_a_jelzesek_ertekelhetok_a_lancolt_naplon(gondos_lanc):
    """Minden mintavett pillanatban mind a kilenc jelzés kiértékelhető."""
    adatok = szimulacio.adatok(gondos_lanc)
    for idx in range(0, len(adatok.esemenyek), 5):
        p = allapot.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, idx)
        assert len(jelzesek.kiertekel(adatok, p)) == 9


def test_a_lanc_nem_indul_ujra_lezaratlan_iteraciobol():
    """A következő iteráció csak lezárt iteráció után indulhat."""
    allas = szimulacio.indit(mag=11)
    assert not allas.kesz
    elotte = (allas.iteracio_id, len(allas.esemenyek))
    allas = szimulacio.kovetkezo_iteracio(allas)
    assert (allas.iteracio_id, len(allas.esemenyek)) == elotte


def test_az_athozott_elem_fogyasztja_a_kovetkezo_keretet():
    """A túlvállalás ára: az áthozott elem a következő iteráció keretéből megy el."""
    allas = lancot_jatszik(11, "gondos", iteraciok=1)
    allas = szimulacio.kovetkezo_iteracio(allas)
    d = allas.dontes
    assert d is not None and d.kod == "vallalas"
    athozott = d.tenyek.athozott
    assert athozott > 0, "nem csúszott át elem — a teszt így nem mér semmit"
    # A javasolt vállalás a keretből levonja az áthozott elemeket is.
    assert int(d.valasztasok[0].kod) == max(1, int(d.tenyek.keret) - 1 - athozott)


def test_a_visszatekintes_csak_a_sajat_iteracioja_hibait_szamolja():
    """Regresszió: a visszatekintés eredetileg a TELJES láncot nézte.

    Emiatt a 4. iteráció újratárgyalta a 3. hibaosztályait is, és olyanra is
    döntést kért, amely abban az iterációban elő sem fordult. Nem elég a
    szabályfájl duplikációját nézni: azt a duplikációs őr önmagában is
    megakadályozza, tehát az a teszt erre a hibára vak.
    """
    import pandas as pd

    allas = szimulacio.indit(mag=11)
    retrok = []
    for kor in range(3):
        for _ in range(800):
            d = allas.dontes
            if d is None:
                break
            if d.kod == "visszatekintes":
                retrok.append(
                    (allas.iteracio_id, d.tenyek.hibaosztaly, d.tenyek.elofordulas)
                )
            allas = szimulacio.dont(allas, _valasz(d, "gondos"))
        if kor < 2:
            allas = szimulacio.kovetkezo_iteracio(allas)

    assert retrok, "egyetlen visszatekintési döntés sem született"
    assert any(azon > 3 for azon, _, _ in retrok), "csak az első iteráció tárgyalt hibát"

    ablakok = {}
    for it in allas.lezart_iteraciok:
        kezdet = pd.Timestamp(it["kezdet"])
        veg = pd.Timestamp(it["veg"]) + pd.Timedelta(days=1)
        ablakok[int(it["id"])] = [
            e for e in allas.esemenyek if kezdet <= e["idopont"] < veg
        ]

    for azon, ho, elofordulas in retrok:
        sajat = sum(1 for e in ablakok[azon] if e["hibaosztaly"] == ho)
        assert elofordulas == sajat, (
            f"a(z) {azon}. iteráció visszatekintése {ho}-ra {elofordulas} előfordulást "
            f"mondott, a saját időablakában viszont {sajat} van"
        )
        assert sajat >= 2, f"{ho} nem ismétlődött a(z) {azon}. iterációban, mégis napirendre került"


def test_a_lezart_merlegek_a_sajat_iteraciojukra_szamolnak(gondos_lanc):
    """Regresszió: a mérleg eredetileg mindig az ELSŐ iteráció ablakára számolt.

    A hiba egyetlen iterációnál láthatatlan volt, mert ott az első ablak az
    egyetlen ablak.
    """
    merlegek = gondos_lanc.lezart_merlegek

    osszes_beolvadas = sum(
        1 for e in gondos_lanc.esemenyek if e["esemeny"] == "biralat_jovahagyva"
    )
    assert sum(m["beolvadt"] for m in merlegek) == osszes_beolvadas

    # Az első iterációba nem hozhattunk át semmit, a másodikba viszont igen.
    assert merlegek[0]["athozott"] == 0
    assert merlegek[1]["athozott"] > 0

    mertek = [tuple(sorted(m["mert"].items())) for m in merlegek]
    assert len(set(mertek)) == len(mertek), "a három iteráció mért paraméterei egyformák"


# --- A szakszavak érthetősége ----------------------------------------------------
#
# A felhasználó a 3. iteráció egy döntéskártyáján futott bele, hogy a „Súlyos
# találat van benne." mondatból nem derül ki sem az, hogy ez baj-e, sem az,
# hogy mit lehet vele kezdeni, sem az, hogy hol nézhető meg. A kód önmagában
# (`HO-02`) szintén semmit nem mond annak, aki nem ismeri a katalógust.


def _beolvasztasi_dontes(mag: int, felteteI) -> szimulacio.Dontes:
    """Az első beolvasztási döntés, amelyre a feltétel igaz.

    Ha nincs ilyen, **hibát dob** — nem csendben kihagyja magát. Ez a teszt
    első változatában valódi hiba volt: egy korai `return` miatt sosem mért,
    és a mutációs ellenőrzés mutatta ki, hogy díszlet.
    """
    allas = szimulacio.indit(mag=mag)
    for _ in range(400):
        d = allas.dontes
        if d is None:
            break
        if d.kod == "beolvasztas" and felteteI(d):
            return d
        allas = szimulacio.dont(allas, _valasz(d, "gondos"))
    raise AssertionError("nem született a feltételnek megfelelő beolvasztási döntés")


def _sulyos_dontes(mag: int = 11) -> szimulacio.Dontes:
    return _beolvasztasi_dontes(mag, lambda d: bool(d.tenyek.sulyos))


def _kifogas_nelkuli_dontes(mag: int = 11) -> szimulacio.Dontes:
    return _beolvasztasi_dontes(mag, lambda d: not d.tenyek.talalt)


def test_a_hibaosztaly_leiro_nevet_es_sulyossagot_ad():
    """A kód mellé mindig jár olvasható név — enélkül a `HO-02` üres jel."""
    leiro = szimulacio.hibaosztaly_leiro("HO-02")
    assert leiro["nev"] == "Láthatósági szűrő megkerülése"
    assert leiro["kategoria"] == "adatvedelem"
    assert leiro["sulyos"] is True

    enyhe = szimulacio.hibaosztaly_leiro("HO-03")
    assert enyhe["nev"] == "Tautologikus teszt"
    assert enyhe["sulyos"] is False

    assert szimulacio.hibaosztaly_cimke("HO-02") == "HO-02 — Láthatósági szűrő megkerülése"


def test_a_katalogus_minden_hibaosztalya_nevesitheto():
    """Amit az ügynök előállíthat, azt a felület ki is tudja írni névvel."""
    from modell.ugynok import HIBAOSZTALYOK

    for kod in HIBAOSZTALYOK:
        leiro = szimulacio.hibaosztaly_leiro(kod)
        assert leiro["nev"] != "ismeretlen hibaosztály", kod
        assert leiro["kategoria"] != "—", kod


def test_a_sulyos_talalat_meg_van_magyarazva_a_dontesben():
    """A döntéskártya mondja meg, mit jelent a súlyos, és mit lehet vele kezdeni."""
    d = _sulyos_dontes()
    szoveg = d.magyarazat

    assert "Mit jelent a súlyos?" in szoveg
    assert szimulacio.SULYOS_MAGYARAZAT in szoveg, "a súlyosság feloldása hiányzik"
    assert szimulacio.ENYHE_MAGYARAZAT in szoveg, "az enyhébbel való szembeállítás hiányzik"
    # Hol lehet javítani: a szöveg nevezze meg a tényleges gombot.
    assert "Visszaküldöm javításra" in szoveg
    assert any(v.cimke == "Visszaküldöm javításra" for v in d.valasztasok)
    # És mondja meg, mi történik, ha mégis beolvasztod.
    assert "szökevény" in szoveg


def test_a_dontes_nevesitve_adja_at_a_hibaosztalyokat_a_feluletnek():
    """A felület a kód mellé nevet és kategóriát is ki tud írni."""
    d = _sulyos_dontes()
    leirok = d.tenyek.hibaosztalyok

    assert leirok, "üres hibaosztály-lista súlyos találat mellett"
    assert [x["kod"] for x in leirok] == d.tenyek.talalt
    assert all(x["nev"] and x["nev"] != "ismeretlen hibaosztály" for x in leirok)
    # A súlyos halmaz és a leírók súlyossági jelzése nem csúszhat el egymástól.
    assert {x["kod"] for x in leirok if x["sulyos"]} == set(d.tenyek.sulyos)


def test_a_kifogas_nelkuli_dontes_nem_beszel_sulyossagrol():
    """Ahol nincs találat, ott ne jelenjen meg a súlyosság-magyarázat.

    Enélkül a szöveg minden kártyán ugyanazt a bekezdést tolná az olvasó elé,
    és épp az veszne el, hogy mikor van tényleg baj.
    """
    d = _kifogas_nelkuli_dontes()
    assert d.tenyek.talalt == []
    assert d.tenyek.sulyos == []
    assert d.tenyek.hibaosztalyok == []
    assert "nem talált kifogást" in d.magyarazat
    assert "Mit jelent a súlyos?" not in d.magyarazat
    assert szimulacio.SULYOS_MAGYARAZAT not in d.magyarazat
    assert "szökevény" not in d.magyarazat


def test_a_dontes_szovege_nem_tartalmaz_nevelohibat():
    """Regresszió: a szöveg korábban „ez a 1. kör"-t írt, ami magyarul hibás.

    Az 1-et „első"-nek mondjuk ki, tehát „az" névelő járna hozzá — a 2-höz
    viszont „a". A megoldás a névelő elhagyása, nem a kivételkezelés.
    """
    allas = szimulacio.indit(mag=11)
    latott = 0
    for _ in range(400):
        d = allas.dontes
        if d is None:
            break
        if d.kod == "beolvasztas":
            latott += 1
            assert "ez a 1." not in d.magyarazat
            assert "ez a 5." not in d.magyarazat
            assert "bírálati kör" in d.magyarazat
        allas = szimulacio.dont(allas, _valasz(d, "gondos"))
    assert latott >= 3, "túl kevés beolvasztási döntés ahhoz, hogy a teszt mérjen"


def test_a_merleg_megjegyzese_feloldja_a_sulyos_szot(gyors):
    """A mérleg sem hivatkozhat magyarázat nélkül a súlyos hibára."""
    _, m = gyors
    sulyosat_emlito = [mj for mj in m["megjegyzesek"] if "súlyos" in mj]
    assert sulyosat_emlito, "a gyors játékban kell lennie súlyos hibát említő megjegyzésnek"
    assert all(szimulacio.SULYOS_MAGYARAZAT in mj for mj in sulyosat_emlito)


# --- A torlódás-döntés szövege ----------------------------------------------------


def test_a_torlodas_szovege_nem_a_kihasznaltsagot_allitja_elore():
    """Regresszió: a szöveg korábban a szabad kapacitás kihasználását sugallta
    kívánatosnak (,,Ez rosszul esik, mert szabad gépi kapacitás áll
    kihasználatlanul''), miközben a modell éppen ez ELLEN a reflex ellen véd."""
    allas = szimulacio.indit(mag=11)
    for _ in range(400):
        d = allas.dontes
        if d is None:
            break
        if d.kod == "torlodas":
            assert "nem könnyű meghozni" in d.magyarazat
            assert "üresen" in d.magyarazat
            assert "ez a korlát ezt akadályozza meg" in d.magyarazat
            return
        allas = szimulacio.dont(allas, _valasz(d, "gyors"))
    raise AssertionError("nem született torlódás-döntés")


# --- A mentett állapot sémaverziója -----------------------------------------------
#
# Élesben (`sm-all-ui.service`) a Streamlit `session_state` egy kódfrissítés
# UTÁN is megtartja a régi `Allas`-t — ez okozott valós `KeyError`-t, amikor a
# felület egy azóta bővült `tenyek` kulcsot (`sulyos`) olvasott egy régi
# döntésről. Az `allapot_ervenyes()` ezt hivatott kiszűrni, MIELŐTT a felület
# bármit olvasna az állapotból.


def test_allapot_ervenyes_a_friss_allasra():
    allas = szimulacio.indit(mag=11)
    assert szimulacio.allapot_ervenyes(allas)


def test_allapot_ervenyes_none_re_is():
    """A `None` (nincs még szimuláció) nem érvénytelen állapot, hanem hiánya —
    a felület ezt külön ágon kezeli, ide nem szabad `False`-t adni."""
    assert szimulacio.allapot_ervenyes(None)


def test_allapot_ervenytelen_regi_semaval():
    """Egy korábbi kódverzióból származó objektum régi sémaverzióval érkezik."""
    allas = szimulacio.indit(mag=11)
    allas.sema_verzio = szimulacio.SEMA_VERZIO - 1
    assert not szimulacio.allapot_ervenyes(allas)


def test_allapot_ervenytelen_semaverzio_mezo_nelkul():
    """A védelem bevezetése ELŐTTI `Allas`-nak még nem is volt `sema_verzio`
    mezője — ezt ugyanúgy érvénytelennek kell látni, nem elszállni rajta.

    Egy valódi `Allas`-on `del`-lel nem szimulálható: a dataclass egyszerű
    (nem `field(default_factory=...)`) alapértéke osztályszintű attribútum is
    lesz, tehát a `getattr` a törlés után is visszaadná a JELENLEGI
    verziószámot. Egy csupasz állványt kell adni, aminek tényleg nincs ilyen
    mezője — sem példányon, sem osztályon.
    """
    class NincsSemaverzioja:
        pass

    assert not szimulacio.allapot_ervenyes(NincsSemaverzioja())
