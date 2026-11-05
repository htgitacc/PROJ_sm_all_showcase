# 0003 — A szimuláció determinisztikus ügynökkel, interfész mögött

## Státusz

Elfogadva, 2026-09-15.

## Kontextus

A prototípus eddig **megmutatta** a modellt (négy táblázatos nézet) és **bemutatta a működését** (animáció). A következő kérdés az volt, lehet-e belőle olyasmi, ami *gyakoroltatja* is: elindítunk egy példaprojektet, és a modell emberi kapuinál a felhasználó dönt.

Három dolgot kellett eldönteni: mi mozgatja az ügynököket, hova kerül a szimuláció eseménynaplója, és mi legyen az interakció egysége.

## Döntés

**Az ügynök viselkedése interfész mögött van** (`modell/ugynok.py`). A motor csak az `Ugynok.dolgozik()` hívást ismeri; a mostani megvalósítás determinisztikus és forgatókönyv-számon (angolul: seed) alapuló, nem hív külső modellt. A szám a véletlen részt rögzíti (a backlog sorrendjét és az ügynök szerencséjét), a felhasználó döntéseit nem: ugyanaz a szám és ugyanazok a döntések ugyanazt a történetet adják, tehát a viselkedés tesztelhető.

**A szimuláció saját eseménynaplót ír**, a `prototipus/adatok/` alatti példaadathoz nem nyúl — arra a koncepció 07. dokumentuma és a tesztek hivatkoznak. A napló viszont **pontosan ugyanabban a sémában** keletkezik, ezért a teljes elemzőréteg változtatás nélkül működik rajta: az `allapot`, a `jelzesek`, a `kapacitas`, a `tanulas` és az `animacio` is.

**Az interakció egysége a döntés, nem az idő.** A motor addig fut, amíg emberi döntésre nincs szükség, akkor megáll. Nincs „következő nap" gomb: a felhasználó nem az időt lépteti, hanem dönt.

## Alternatívák, amiket elvetettünk

- **Valódi LLM-ügynökök egy játék-repón.** Meggyőzőbb volna, de API-kulcsot, költséget, biztonsági határt és nem determinisztikus viselkedést hoz be, ráadásul a koncepció a platformspecifikus leképezést külön függelékre tervezi. Az interfész emiatt készült: később becsatolható anélkül, hogy a folyamatlogikához hozzá kellene nyúlni.
- **Minden bírálat automatikus elbírálása, csak a végén összegzéssel.** Ezzel elveszne a lényeg: a modell szerint a beolvasztás az a pont, ahol a felelősség keletkezik, tehát épp ott nem szabad automatizálni.
- **Írás a példaadatba.** Egyszerűbb volna, de elrontaná azt a naplót, amelyre a koncepció számai és tizenhárom teszt hivatkozik.

## Következmény

A szimuláció **a modell feltevéseivel számol**, nem a valósággal. Az `R`, `t`, `r` paraméterek, a 200 soros méretkorlát és a jelzésküszöbök a koncepció saját, bizonyíték nélküli döntései. Egy jól kinéző szimulátor könnyen tekintélyt kölcsönözne nekik, ezért az indítópanel ezeket **láthatóan és állíthatóan** kínálja, és külön figyelmeztetés mondja ki, hogy feltevésekről van szó.

A mérleg szándékosan kimondja azt is, ami kellemetlen: a felületes bírálat **szebb mennyiségi mutatókat** termel (magasabb első körös elfogadás, kevesebb átcsúszott elem), miközben több súlyos hibát enged ki. Ha ezt a felület nem mondaná ki, a szimuláció rossz szokást tanítana.
