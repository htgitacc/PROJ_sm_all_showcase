# Spike 01 — Ügynök-architektúra: egy ügynök, orkesztrátor, skillek, MCP

> **Állapot:** lezárva, 2026-10-17. **Döntés:** elméleti összehasonlítás marad; párhuzamos, bemutatható megoldás nem készül (indoklás lent).
>
> Ez egy **spike**: fejlesztési és összehasonlítási ötlet a lezárt anyag mellé. A [kutatás](../../kutatas/00-osszefoglalo.md) és a [koncepció](../../koncepcio/README.md) nem változott; a spike azokra épül, és ahol a friss adat mást mond, azt itt rögzíti.

## A kérdések

1. Ha egy ügynök csinálna mindent, olcsóbb lenne? Mit tenne ez az idővel és a minőséggel?
2. Változna-e a modell egy központi (orkesztrátor) ügynökkel, amely alá a mai szerepek alügynökként kerülnek?
3. Lefedhetők-e a mai ügynökszerepek **skillekkel** egyetlen ügynök alatt, vagy egy **MCP szerver tooljaival**? Érdemes-e ilyen irányba tervezni?

## A dokumentumok

| Fájl | Miről szól |
|---|---|
| [kutatas.md](kutatas.md) | Célzott friss kutatás: mit erősít, árnyal vagy cáfol a lezárt kutatásból |
| [forrasok.md](forrasok.md) | A spike forrásai (`U-01`…`U-14`), szintezve |
| [lekepezes.md](lekepezes.md) | Négy változat (A mai, B egy ügynök, C orkesztrátor, D skill + MCP) ugyanarra a pilotra, a munka útján és a példa kulcspillanatain |

## A válaszok röviden

**1. Egy ügynök olcsóbb, az időn nem segít, a minőséget rontja.** Az idő azért nem változik, mert a szűk keresztmetszet a két szenior bírálata, nem a gép. A minőség azért romlik, mert a modell nem a párhuzamos alkotás miatt többszörözi az ügynököket, hanem a **független ellenőrzés** miatt: ugyanaz az ügynök ugyanabban a kontextusban nem ellenőrzi jól a saját munkáját. A friss mérés ezt árnyalja: a függetlenség jelentős része a **friss kontextusból** jön, nem csak a más gyártó modelljéből ([U-12](forrasok.md)) — de egy ügynök egyetlen munkamenetben éppen ezt sem adja meg.

**2. Orkesztrátor: a kódolásban nem, a kutatásban igen.** Kontrollált mérés szerint szekvenciális feladaton minden többügynökös változat rontott (39–70%), párhuzamosíthatón a központosított koordináció javított ([U-01](forrasok.md)). A kódírás jellemzően szekvenciális, a specifikáció előkészítése és a kutatás párhuzamosítható. Az orkesztrátor legnagyobb kockázata a modellünkben, hogy az ellenőrzők **jelentésére** hagyatkozik (korai győzelem, csendes üres válasz, [U-03](forrasok.md)), és hogy a WIP-korlátot nem tartja be magától — ezt mindkettőt kívülről kellene kikényszeríteni.

**3. Skill + MCP: igen, de nem a független ellenőrzés helyett.** A gondozott, ember által írt skill segít, a modell által magának írt nem ([U-06](forrasok.md)) — ez pontosan a koncepció szabályfájl-elve, kiterjesztve. Az MCP-tool kiválóan alkalmas, hogy az ügynök **munka közben** lefuttassa a gépi kapukat, de a **kötelező kapu** maradjon az ügynöktől független futtatás, különben visszajön a korai győzelem. Az MCP ráadásul új támadási felület (tool poisoning: akár 72,8% siker, [U-09](forrasok.md)). A független bírálat (verifikáló, cáfoló) nem lehet ugyanannak az ügynöknek a skillje; friss kontextusú, külön futtatott bírálat kell, csúcskategóriás modellel.

## Döntés: miért marad elméleti?

A spike előre rögzített kritériuma: **akkor építünk bemutatható megoldást, ha a változat mást kér az embertől** — más kapukat, más jelzéseket, más kapacitás-számítást vagy más SM-döntéseket —, és a különbség a szimulációban megmutatható.

A legjobb változat (D) ezt **nem teljesíti**:

- **Ugyanaz a két emberi kapu**, ugyanaz a bírálati keret, ugyanaz a WIP- és méretkorlát.
- **Ugyanazok az SM-jelzések**; legfeljebb egy új jöhetne („skill-módosítás bírálat nélkül”), amely a meglévő „felügyeleti rés” jelzés párja.
- **A kapacitás-logika ugyanaz.** A javulás egyetlen csatornája, hogy kevesebb hibás elem jut a kapuig, így csökkenhet a javítási körök száma (`r`). Ez a mai szimulációban is beállítható paraméter; feltevésként kb. +0,7 elem/iteráció, nem minőségi változás.
- **A különbség a gép belsejében van** (független CI-kapu, gondozott skillek, MCP-toolok, friss kontextusú bírálat). A szimuláció ügynöke ezt csak úgy tudná megmutatni, hogy más valószínűségeket adunk neki — ez a kívánt eredmény beállítása volna, nem bizonyítéka.

Egy párhuzamos, bemutatható megoldás tehát ugyanazt a felületet és ugyanazokat a döntéseket mutatná, más címkékkel. Ez nem éri meg a párhuzamos fejlesztést.

## Amit a spike ennek ellenére hasznosan rögzít

1. **Egy friss mérés ellentmond a koncepció egyik javaslatának.** A koncepció 09. dokumentuma azt írja, hogy a költség csökkentésére a biztonsági cáfoló olcsóbb modellre állítható. A friss, kontrollált mérés szerint a könnyűsúlyú más modell nem volt jobb a saját modellnél ([U-12](forrasok.md)). Valódi pilotban ezért a cáfoló csúcskategóriás modell maradjon; a megtakarítást a determinisztikus kapuk és az egy alkotó szál adja.
2. **A skill bírálandó termék.** A vizsgált `SKILL.md` fájlok 91,8%-a hibás ([U-08](forrasok.md)); ha a csapat skillekkel dolgozik, a skill módosítása ugyanúgy a bírálati keretből fogyaszt, mint a kód.
3. **Az MCP-toolok a biztonsági kapu tárgyai.** Rögzített verzió, belső forrás, minimális jogosultság; a tool-leírás is bírálandó szöveg.
4. **Ha egyszer valódi LLM-ügynök kerül a szimuláció mögé** (`prototipus/modell/ugynok.py`, a BACKLOG „Valamikor” tétele), a D változat a természetes célarchitektúra: az ügynök interfésze ugyanaz marad, a kapuk a folyamatban vannak.

## Mikor érdemes újranyitni

- Ha megjelenik **kontrollált összehasonlítás kódolásra** egyszálú és orkesztrátoros felállás között, azonos költségkerettel.
- Ha a pilot mérései szerint az `r` (javítási körök) **érdemben** csökken skillekkel és MCP-visszajelzéssel — mert akkor a kapacitás-számítás változik, és az már az embert is érinti.
- Ha a csapat **valódi LLM-ügynököt** köt a szimuláció mögé: akkor a változatok ténylegesen lefuttathatók és összemérhetők, nem csak leírhatók.
