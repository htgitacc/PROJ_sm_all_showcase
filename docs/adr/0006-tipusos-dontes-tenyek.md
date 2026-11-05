# 0006 — A `Dontes.tenyek` típusos, döntéstípushoz kötött osztályok

## Státusz

Elfogadva, 2026-10-17.

## Kontextus

A szimuláció minden döntési pontja egy `Dontes`, amelynek `tenyek` mezője azt hordozta, amit a felület a döntéskártyán kirajzol. Ez szabad formátumú szótár volt, öt döntéstípusra más-más kulcsokkal. Semmi nem kényszerítette ki, hogy egy típus mindig ugyanazokat a kulcsokat hordozza, ezért egy bővítés vagy elgépelés csak olvasáskor, futás közben, egy távoli helyen derült ki.

2026-09-16-án ez két egymást követő éles hibát okozott: egy `KeyError: 'sulyos'`-t, majd a javítása nyomán egy szélesebb `AttributeError`-sorozatot (lásd `docs/HANDOFF.md`).

## Döntés

A `tenyek` öt kötelező-mezős, `kw_only`, `frozen` dataclass (`VallalasTenyek`, `BeolvasztasTenyek`, `TorlodasTenyek`, `MeretkorlatTenyek`, `VisszatekintesTenyek`), a `modell/szimulacio.py`-ban. A `Dontes.__post_init__` a `TENYEK_TIPUSA` táblából ellenőrzi, hogy a döntés kódja és a tények típusa egyezik. Egy hiányzó, elgépelt vagy rossz típushoz kötött mező így a `Dontes` létrehozásakor `TypeError`/`ValueError`, nem a felület olvasásakor `KeyError`. A `SEMA_VERZIO` 3-ra emelkedett, mert az `Allas` mentett alakja változott.

A felület és a tesztek attribútumként olvassák a tényeket (`d.tenyek.meret_sor`). **Átmenetileg** (a bevezetés napján) a közös ősosztály a szótár-szerű olvasást (`t["kulcs"]`, `t.get`) is támogatta, mert a felületi oldalak (`app_pages/*.py`) a lemezről frissen futnak, a `modell/*.py` viszont csak újraindításig cserélődik, tehát a két rétegnek egy ideig mindkét alakot olvasnia kellett. Miután az éles folyamat újraindult a típusos `modell`-lel, ezt a kompatibilitást töröltük, és a felület attribútum-olvasásra állt át; így egy elgépelt mezőnév a füsttesztben `AttributeError`.

## Nem csináljuk

- Nem építünk automatikus kulcs-ellenőrzést a `SEMA_VERZIO`-ba: a típusok ezt kiváltják, a verziószám kézi emelése elég.

## Következmények

- A szeptemberi hibaosztály a létrehozásnál, a motor tesztjeiben megfogható. A `tesztek/test_tenyek.py` ezt rögzíti, mutációval ellenőrizve (kihagyott mező, rossz típus).
- A `tesztek/test_fustteszt.py` füsttesztjei a felületet is lefuttatják, így az olvasási oldalt is védik.
