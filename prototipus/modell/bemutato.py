"""A Vezetett bemutató fejezetei.

Annak szól, aki kívülről érkezik, és nem tudja, mit kellene a nézetekben keresnie.
A fejezetek a példa ugyanazon kulcspillanataira épülnek, mint az oldalsáv könyvjelzői
és az animáció fejezetei (`modell/konyvjelzok.py`), a narráció pedig a
`koncepcio/07-iteracios-pelda.md` összefoglalása — új tartalmi állítás nélkül.

Szándékosan új modul: az élő folyamat a már betöltött `modell/*.py` fájlokat nem
frissíti újraindításig, egy új fájl viszont az első importnál frissen töltődik be.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Fejezet:
    cim: str
    alcim: str
    narracio: list[str]
    konyvjelzo: str | None  # a `konyvjelzok.konyvjelzok()` kulcsa; None: nincs időpillanata
    nezet: str  # az a nézet, ahol részletesen megnézhető
    nezet_cim: str
    jelzesek: list[str] = field(default_factory=list)  # a megmutatandó jelzések kódjai
    tanulsag: str = ""


FEJEZETEK: list[Fejezet] = [
    Fejezet(
        cim="A munka útja",
        alcim="Hol áll ember, és miért ott",
        narracio=[
            "A csapat egy Product Ownerből, egy Scrum Masterből és két szenior fejlesztőből áll; "
            "mellettük AI-ügynökök dolgoznak, de ők a szeniorok **eszközei**, nem plusz fejek.",
            "Egy elem hét lépésen megy végig. Ebből ötöt gép is elvégezhet, **kettőnél viszont "
            "kötelezően ember áll**: a darabolás jóváhagyásánál (itt a legolcsóbb kiszűrni egy rossz "
            "tervet) és a beolvasztásnál (itt keletkezik a felelősség).",
            "Az ügynökök órák alatt elkészülnek, az emberi bírálat nem. Ezért a csapat kapacitását "
            "nem az ügynökök sebessége adja, hanem az, hogy a két szenior mennyit tud **felelősséggel "
            "átvenni** — ez a *bírálati keret*, és a bírálatra váró sor hossza korlátos.",
        ],
        konyvjelzo=None,
        nezet="app_pages/backlog.py",
        nezet_cim="Backlog — hogyan lett darabolva a munka",
        tanulsag="A szűk keresztmetszet az emberi bírálat, nem a gép.",
    ),
    Fejezet(
        cim="Darabolás és jóváhagyás",
        alcim="1. iteráció, az első reggel",
        narracio=[
            "A Product Owner megfogalmazza az igényt: kereshető munkatárs-adatlap és szervezeti fa. "
            "Egy szabály a példa gerince lesz: a telefonszámot és az irodahelyet csak az azonos vagy "
            "a fölérendelt egységben dolgozók láthatják.",
            "Ugyanarra a specifikációra az ügynök és a PO egymástól függetlenül darabol. Az ügynök "
            "változata alaposabb (11 elem a PO 7-ével szemben), de **a láthatósági szabályt három "
            "elem közé szórta szét**.",
            "A PO ezért visszaküldi a darabolást, és az ügynök egy elembe vonja össze a szabályt. "
            "Így lesz kilenc elem. A hibát egy oldal elolvasásával kiszűrték, nem négyszáz sor "
            "átnézésével — ezért áll itt ember.",
        ],
        konyvjelzo="Iteráció eleje",
        nezet="app_pages/backlog.py",
        nezet_cim="Backlog — a kilenc elem és a feltételeik",
        tanulsag="Az első emberi kapu a legolcsóbb hely a hiba megfogására.",
    ),
    Fejezet(
        cim="Torlódás",
        alcim="1. iteráció, 2. nap, 13:20",
        narracio=[
            "Az ügynökök gyorsan termelnek, a bírálat lassabban fogy: **öt elem várna bírálatra, "
            "a korlát négy.**",
            "A felület megszólal, és konkrét teendőt ad: az ügynökök nem kapnak új feladatot, amíg a "
            "sor nem apad. A csapatnak ez rosszul esik, mert szabad gépi kapacitás áll kihasználatlanul.",
            "A Scrum Master feladata itt az, hogy a leállást **a rendszer helyes működéseként** mutassa "
            "be, ne hibaként. Ha a sor korlát nélkül nőne, a bírálat felületessé válna, és a minőségi "
            "kapu csendben kikapcsolna.",
        ],
        konyvjelzo="Torlódás (1. it., 2. nap)",
        nezet="app_pages/teendok.py",
        nezet_cim="Teendők — a jelzés és a teendő",
        jelzesek=["J1", "J2"],
        tanulsag="A leálló ügynök nem hiba, hanem a korlát működése.",
    ),
    Fejezet(
        cim="Paramétereltérés",
        alcim="1. iteráció vége",
        narracio=[
            "A bírálati keret három feltevésre épült (napi bírálati idő, egy elem átnézése, javítási "
            "körök). Az iteráció végén ezeket megmérik.",
            "A legfontosabb eltérés: egy elem érdemi átnézése **70 helyett 90 percig tartott**. Mivel "
            "ez a szám a nevezőben van, egymagában lehúzza a kapacitást — a következő iterációra "
            "**kilenc helyett nyolc elemet** vállalnak.",
            "Közben a legfontosabb egészségjelző rendben van: mind a nyolc beolvadt elemet ember "
            "nézte át.",
        ],
        konyvjelzo="Paramétereltérés (1. it. vége)",
        nezet="app_pages/elorenezes.py",
        nezet_cim="Előretekintés — a mért paraméterekből számolt keret",
        jelzesek=["J7"],
        tanulsag="A modell feltevésekkel indul, és a mérés felülírja őket.",
    ),
    Fejezet(
        cim="Méretkorlát",
        alcim="2. iteráció, 2. nap",
        narracio=[
            "Az igénylőfelület **310 sorral** érkezik a 200 soros korlát ellenében. Az AI-val "
            "segített változtatások a mérések szerint jellemzően nagyobbak, a nagy csomagot pedig "
            "felületesebben nézik át.",
            "A teendő ezért nem a hosszabb bírálat, hanem a **visszabontás**: külön lesz belőle az "
            "űrlap és a naptárnézet. Ez egy plusz bírálati esemény, de mindkét rész átnézhető méretű.",
        ],
        konyvjelzo="Méretkorlát (2. it., 2. nap)",
        nezet="app_pages/teendok.py",
        nezet_cim="Teendők — a méretkorlát-jelzés",
        jelzesek=["J8"],
        tanulsag="A túl nagy csomagot bontani kell, nem tovább nézni.",
    ),
    Fejezet(
        cim="Visszatérő hibaosztály",
        alcim="2. iteráció, visszatekintés",
        narracio=[
            "Az első iteráció két ismétlődő hibájából szabály lett a szabályfájlban (SZ-06, SZ-07). "
            "A bizonyíték arra, hogy a tanulás beépült, nem az ügynök ígérete, hanem az, hogy **a "
            "hibaosztály eltűnik**.",
            "Az egyik szabály fogott: a korai „kész” jelentés nem tért vissza. A másik nem: az új "
            "távollét-végpont ismét szűretlenül adta ki a telefonszámot. Ezzel az eszkalációs létra "
            "**harmadik fokára** lépnek.",
            "A döntés: a visszatérő hibát **nem újabb szabállyal, hanem géppel** fogják meg. Az "
            "utasításfájl puha korlát, a determinisztikus teszt kemény.",
        ],
        konyvjelzo="Visszatérő hibaosztály (2. it.)",
        nezet="app_pages/tanulas.py",
        nezet_cim="Tanulás — hibaosztályok és az eszkalációs létra",
        jelzesek=["J6"],
        tanulsag="Ami visszatér, azt gépi kapuval kell megfogni.",
    ),
]

# --- „A munka útja” folyamatábra ------------------------------------------------------
# HTML, nem SVG: a lépések kártyái telefonon egymás alá törnek, és a szöveg olvasható marad.
# A színek áttetszőek és `currentColor`-ra épülnek, így világos és sötét témában is működnek.

LEPESEK = [
    ("1", "Termékigény", "Product Owner", False),
    ("2", "Specifikáció", "ügynök írja, a PO vázlatából", False),
    ("3", "Darabolás", "ügynök", False),
    ("4", "Jóváhagyás", "PO + szenior", True),
    ("5", "Megvalósítás", "implementáló ügynök", False),
    ("6", "Gépi kapuk", "verifikáló ügynök, tesztek", False),
    ("7", "Bírálat és beolvasztás", "szenior, névvel", True),
]


def munka_utja_html(bir_korlat: int) -> str:
    kartyak = []
    for i, (szam, cim, ki, ember) in enumerate(LEPESEK):
        osztaly = "lepes ember" if ember else "lepes"
        cimke = '<span class="cimke">emberi kapu</span>' if ember else ""
        kartyak.append(
            f'<div class="{osztaly}"><div class="szam">{szam}</div>'
            f'<div class="cim">{cim}</div><div class="ki">{ki}</div>{cimke}</div>'
        )
        if szam == "6":
            kartyak.append(
                f'<div class="sor" title="A bírálatra váró sor korlátos">'
                f"bírálatra vár<br><b>legfeljebb {bir_korlat}</b></div>"
            )
        elif i < len(LEPESEK) - 1:
            kartyak.append('<div class="nyil">→</div>')
    return (
        """<style>
.mu{display:flex;flex-wrap:wrap;align-items:stretch;gap:6px;font-size:14px;line-height:1.3;color:inherit}
.mu .lepes{flex:1 1 110px;min-width:96px;border:1px solid rgba(128,128,128,.35);border-radius:10px;padding:8px 10px;position:relative}
.mu .lepes.ember{border:2px solid #d97706;background:rgba(217,119,6,.10)}
.mu .szam{font-size:12px;opacity:.6}
.mu .cim{font-weight:600}
.mu .ki{font-size:12px;opacity:.75}
.mu .cimke{display:inline-block;margin-top:4px;font-size:11px;font-weight:600;color:#b45309;background:rgba(217,119,6,.15);border-radius:6px;padding:1px 6px}
.mu .nyil{align-self:center;opacity:.5;font-size:18px}
.mu .sor{align-self:center;font-size:12px;text-align:center;border:1px dashed rgba(220,38,38,.7);color:#dc2626;border-radius:8px;padding:4px 8px}
</style><div class="mu">"""
        + "".join(kartyak)
        + "</div>"
    )
