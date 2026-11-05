# Leképezés a mostani feladatra — négy változat ugyanarra a pilotra

> Ugyanaz a feladat (vállalati intranet, két iteráció: munkatárs-kereső, távollét-igénylés), ugyanaz a csapat (PO, SM, két szenior), négy ügynök-architektúra. A kérdés nem az, melyik a „modernebb”, hanem az, hogy **mit kér másképp az embertől**, és mit tesz a minőséggel és a költséggel. A forrásokat lásd: [kutatás](kutatas.md), [forrásjegyzék](forrasok.md).

## A négy változat

| | Mi dolgozik | Ki orkesztrál |
|---|---|---|
| **A — a mai modell** | implementáló ügynök (A modellcsalád), verifikáló (B család), biztonsági kereső (A) és cáfoló (B), kutató | determinisztikus folyamat (WIP, méretkorlát, kapuk) és az emberek |
| **B — egy ügynök** | ugyanaz az ügynök implementál, ellenőriz, keres és cáfol, ugyanabban a kontextusban | az ügynök maga, a folyamat korlátai között |
| **C — orkesztrátor + alügynökök** | egy vezető (menedzser) ügynök osztja ki a munkát; a mai szerepek alügynökök | a vezető ügynök dönti el a köröket (az Agyn-minta, [U-02](forrasok.md)) |
| **D — egy ügynök + skillek + MCP + független ellenőrzés** | egy implementáló ügynök gondozott skillekkel; MCP-toolok a munka közbeni gyors visszajelzéshez; a kötelező kapu az ügynöktől független futtatás (CI); független bírálat friss kontextusban; a kutatás párhuzamos alügynökként | determinisztikus folyamat és az emberek, mint az A-ban |

**Ami mind a négyben azonos, mert a modell alapszabálya:** a két emberi kapu (a darabolás jóváhagyása és a megnevezett emberi beolvasztás), a bírálati keret (`R`, `t`, `r`), a WIP-korlát és a 200 soros méretkorlát. Egyik változat sem hagyhatja el ezeket; a kérdés az, mennyire nehéz őket betartani.

## A munka útja, lépésenként

| Lépés | A — mai | B — egy ügynök | C — orkesztrátor | D — skill + MCP |
|---|---|---|---|---|
| 1. Termékigény | PO | PO | PO | PO |
| 2. Specifikáció | ügynök a PO vázlatából | ugyanaz | a vezető ügynök, kutató alügynökökkel | ügynök, a specifikáció-formát gondozott skill adja |
| 3. Darabolás | daraboló ügynök | ugyanaz az ügynök | a vezető ügynök | daraboló ügynök + DoR-skill (méret, egy szabály egy elem) |
| 4. **Jóváhagyás** | **PO + szenior** | **PO + szenior** | **PO + szenior** | **PO + szenior** |
| 5. Megvalósítás | implementáló, egy szál | ugyanaz az ügynök | fejlesztő alügynök(ök) | implementáló, egy szál, skillekkel; MCP-vel menet közben teszt, elemzés, méret |
| 6. Gépi kapuk | verifikáló (B család), nyers kimenetből | az ügynök a saját munkáját | verifikáló alügynök, a vezetőnek jelent | **CI, ügynöktől függetlenül, nyers kimenetből**; független bírálat friss kontextusban |
| 7. **Bírálat és beolvasztás** | **szenior, névvel** | **szenior, névvel** | **szenior, névvel** | **szenior, névvel** |

A táblázat lényege a 6. lépés: **ott különböznek a változatok, ahol a gép ellenőrzi a gépet.**

## A példa kulcspillanatai, változatonként

### Darabolás és jóváhagyás (1. iteráció, első reggel)
A daraboló ügynök a láthatósági szabályt három elem közé szórta szét; a PO visszaküldte.
- **A, B:** ugyanúgy történik; a PO kapuja fogja meg.
- **C:** a vezető ügynök kutató alügynökökkel gazdagabb specifikációt adhat — ez a párhuzamosítható, kutatás-jellegű rész, ahol az orkesztrátor mérten hasznos ([U-01](forrasok.md)). A hibát továbbra is a PO kapuja fogja meg.
- **D:** egy gondozott DoR-skill („egy üzleti szabály egy elemben”) már a darabolásnál jelezhetné; a PO kapuja marad a döntés helye. *Feltevés:* a mérések szerint a gondozott skill szoftverfejlesztésben szerényen segít ([U-06](forrasok.md)), tehát csökkenti, de nem szünteti meg az ilyen visszaküldést.

### Korai „kész” (1. iteráció, 2. nap)
A verifikáló sikert jelentett, holott a 11 tesztből 2 futott le; a DoD fogta meg, mert a nyers tesztkimenetet követeli.
- **A:** a DoD megfogja, de csak akkor, ha valaki tényleg a nyers kimenetet nézi.
- **B:** a legrosszabb: ugyanaz az ügynök ír és jelent sikert a saját munkájáról. Ha a kapu nem független, a hiba átjut.
- **C:** a vezető ügynök a verifikáló **jelentésére** hagyatkozik; a csendes üres válasz ([U-03](forrasok.md)) és a korai győzelem (S-08) itt összeadódik. A javulást (U-02) is a kötelező bírálati kör adja, nem a vezető.
- **D:** **szerkezetileg zárja ki**: a kötelező kapu a CI, amely nem az ügynök döntésén múlik és nem az ügynök összefoglalóját olvassa. Az MCP-n kapott menet közbeni visszajelzés miatt ráadásul kevesebb hiányos elem jut el a kapuig.

### Torlódás (1. iteráció, 2. nap, 13:20)
Öt elem várna bírálatra a négyes korláttal szemben; az ügynökök leállnak.
- **A, B, D:** ugyanaz: a szűk keresztmetszet a két szenior, a változat nem gyorsít rajta.
- **C:** új kockázat: egy vezető ügynök hajlamos „kihasználni a kapacitást” és újabb alügynököket indítani — a túlzott indítás dokumentált hiba: az Anthropic kutatási rendszerének korai változatai egyszerű kérdésekre is túl sok alügynököt indítottak (S-09). A WIP-korlátot ezért **a sornak kell kikényszerítenie, nem a vezető ügynök belátásának.**

### Biztonsági lánc (1. iteráció, 2. nap)
A kereső négy találatot jelzett, a más családból származó cáfoló hármat kiejtett, egy valódi maradt.
- **A:** így működik.
- **B:** ugyanaz az ügynök keres és cáfol: vagy mindent megtart (zaj az embernek), vagy a sajátját „cáfolja”. A független ellenőrzés elvész.
- **C:** ugyanaz, mint A, ha az alügynökök valóban más modellt és friss kontextust kapnak.
- **D:** a cáfoló friss kontextusban, a gyártás előzménye nélkül fut. A friss mérés ([U-12](forrasok.md)) szerint ez a függetlenség jelentős része; és a cáfoló **csúcskategóriás** modell legyen, mert a könnyűsúlyú nem volt jobb a sajátnál.

### Méretkorlát (2. iteráció, 2. nap)
Az igénylőfelület 310 sorral érkezett; vissza kellett bontani.
- **A, B, C:** a méretkapu a bírálatra kerüléskor jelez.
- **D:** az ügynök már menet közben látja (MCP-méretmérés), és **jelez a darabolásnak** — a bontás továbbra is ember által jóváhagyott darabolás, de egy bírálati kör megspórolható.

### Visszatérő hibaosztály (2. iteráció)
Az SZ-07 szabály nem fogott; a csapat gépi kaput épített (architektúrateszt).
- **A:** az eszkalációs létra: 2. fok szabály, 3. fok gépi kapu.
- **B, C:** ugyanaz, de a szabályt egy ügynök olvassa — a puha korlát gyengesége nem változik.
- **D:** a létra ugyanaz, csak szerkezettebb: **2. fok = gondozott skill vagy szabály** (ember írja vagy hagyja jóvá; a magának írt skill a mérések szerint nem segít, [U-06](forrasok.md)); **3. fok = CI-kapu**, amelyet az ügynök MCP-n keresztül munka közben is lefuttathat.

## Mit kér másképp az embertől?

| | A | B | C | D |
|---|---|---|---|---|
| Emberi kapuk | 2 | 2 | 2 | 2 |
| Bírálati keret, WIP, méretkorlát | alap | ugyanaz | ugyanaz, de a WIP-et kívülről kell kikényszeríteni | ugyanaz |
| Az SM jelzései (J1–J9) | alap | ugyanaz | **+ a vezető ügynök felügyelete** (túlindítás, csendes hiba) | ugyanaz; legfeljebb egy új: *skill-módosítás bírálat nélkül* (a „felügyeleti rés” párja) |
| Új bírálandó termék | — | — | — | **skillek** (a keretből fogyasztanak, [U-08](forrasok.md)) és **MCP-toolok** (biztonsági bírálat, [U-09](forrasok.md)) |
| Minőségi kockázat | alap | **nő** (önellenőrzés) | **nő** a jelentésre hagyatkozás miatt; a bírálati kör kompenzál | **csökken** (független CI-kapu, friss kontextusú bírálat) |
| Költség (tokenben) | alap | **legkisebb** | **legnagyobb** (3–15×, S-08, S-09) | **A-nál kisebb** (determinisztikus toolok, egy alkotó szál), a független bírálat marad a drága rész |
| Kapacitás | alap | ugyanaz | ugyanaz | *feltevés:* ha kevesebb hibás elem jut a kapuig, az `r` csökkenhet; `r` = 0,625 → 0,5 esetén a 2. iteráció kerete kb. 8,0 → 8,7 elem |

## Következtetés a döntéshez

- **B** olcsóbb, de a modell egyik alapját, a független ellenőrzést adja fel; a friss mérések ezt nem igazolják. **Nem javasolt.**
- **C** a kutatás-jellegű részeken (specifikáció, darabolás előkészítése) hoz, a kódolásban nem; cserébe új felügyeleti feladatot ad az SM-nek, és a legdrágább. **Csak a kutatói szerepre javasolt.**
- **D** a mai modell **ugyanazokkal az emberi kapukkal és ugyanazzal a kapacitás-logikával**; a különbség a gép belsejében van: a kötelező kapu függetlenebb, a tudás (skillek) gondozott és bírált, a költség kisebb. Két új bírálandó termék (skill, MCP-tool) és egy lehetséges új jelzés jelenik meg — ezek kicsik.

A döntést és az indoklását a [spike áttekintője](README.md) tartalmazza.
