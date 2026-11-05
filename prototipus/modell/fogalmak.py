"""Fogalmak, amelyeket a felület több helyen használ: a magyarázat egy forrásból jön.

A „gépi kapu” a Bevezetés munkaútjában, a Teendők nézet J6 jelzésének teendőjében, a Tanulás
eszkalációs létráján és a Vezetett bemutatóban is előkerül, de korábban sehol nem volt kimondva,
mit jelent. A szöveg a koncepció 02. dokumentumának kapurendszerét foglalja össze, új állítás
nélkül.

Szándékosan külön, új modul: az élő folyamat a már betöltött `modell/*.py` fájlokat nem frissíti
újraindításig, egy új fájl viszont az első importnál frissen töltődik be.
"""

from __future__ import annotations

GEPI_KAPU_CIM = "Mi a gépi kapu — és lehet-e ügynök?"

GEPI_KAPU = """
A **gépi kapu** automatikus ellenőrzés, amely minden változtatásnál lefut, és ami elbukik rajta,
azt önműködően visszautasítja: a változtatás addig nem kerül emberi bírálatra, amíg át nem megy.
Az eredménye igen vagy nem, ugyanarra a kódra mindig ugyanaz, nem függ nyelvi modelltől, és nem
fogyaszt emberi figyelmet. A koncepció *determinisztikus kapunak* is hívja.

**Példák:**

- a teljes tesztkészlet lefutása (egység- és integrációs tesztek);
- egy célzott teszt egyetlen hibaosztályra — a példában az **AT-01** architektúrateszt: bármely
  kontaktadatot elérő útvonal a láthatósági szűrő megkerülésével elbukik;
- fordítás, statikus elemzés (linter, típusellenőrzés), formázás;
- függőség-, titok- és licencvizsgálat.

**Miért erősebb a szabálynál?** A szabályfájl (`AGENTS.md`) az ügynöknek szóló utasítás:
követendő szöveg, amelyet az ügynök elnézhet vagy félreérthet — ez a *puha korlát*. A gépi kapu
akkor is megfogja a hibát, ha az ügynök nem tartotta be a szabályt — ez a *kemény korlát*. Ezért
ha egy hibaosztály a szabály felvétele után is visszatér, nem a szabályt kell átfogalmazni,
hanem gépi kaput kell építeni köré.

**Lehet-e ügynök a kapu?** Futtatni igen, dönteni nem. A verifikáló ügynök indítja a teszteket,
de az átengedésről a tesztfuttató nyers, gépi kimenete dönt, nem az ügynök összefoglalója: a
verifikáló ügynök hajlamos részleges tesztelés után sikert jelenteni („korai győzelem”, S-08).
A koncepció ismer *ügynöki kaput* is (hiányzó tesztek megírása, biztonsági átolvasás, a
specifikációnak való megfelelés ellenőrzése), de annak kimenete **javaslat, nem ítélet** —
visszatérő hibára ezért nem elég, mert ugyanúgy elnézheti a hibát, mint a szabályt. Ügynök
viszont megírhatja a gépi kaput: ha az általa írt tesztet egy szenior átnézi és beépíti,
onnantól az a teszt a kapu.

Részletesen: [Minőségi kapuk (koncepció, 2. dokumentum)](koncepcio?dok=koncepcio/02-minosegi-kapuk).
""".strip()
