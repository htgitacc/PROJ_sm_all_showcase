# 4. Multi-agent architektúra — mikor éri meg több ügynök, és mikor nem

## Mit kerestünk

A brief két helyen is felteszi ugyanazt a kérdést: „Egy ügynök és modell vagy több ügynök és több modell?" A szeniorok által írandó ügynökpark tervezéséhez tudnunk kell, hogy a több, specializált ügynök általában javítja-e az eredményt, vagy csak a hibalehetőségeket sokszorozza. Ezért kerestük egyrészt a gyártói ajánlásokat, másrészt — ennél fontosabban — a **kudarcok rendszerezett elemzését**.

## Mit találtunk

### A legfontosabb adat: a többügynökös rendszerek nagy arányban buknak el

A UC Berkeley Sky Computing kutatócsoportjának MAST-tanulmánya (S-10) az első rendszerezett kudarctaxonómiát adja a többügynökös LLM-rendszerekre. A vizsgálat 1642 annotált végrehajtási nyomvonalra (trace) épül hét nyílt forrású keretrendszerből (többek között ChatDev, MetaGPT, HyperAgent, AppWorld, Magentic-One, OpenManus). A taxonómia 150 nyomvonal hat szakértő általi, megalapozott elmélet (grounded theory) módszerű elemzéséből született; az annotátorok közötti egyetértés Cohen-féle kappája 0,88 volt, az ezt automatizáló LLM-bíró pedig 94 százalékos pontosságot ért el.

A hibaarányok keretrendszertől függően **41 és 86,7 százalék között** mozogtak: a ChatDev 41,4, a MetaGPT 56,4, a Magentic-One 78,6, az OpenManus 86,7 százalékban vallott kudarcot.

A 14 hibamódot három kategóriába sorolják, és az arányok elárulják, hol keressük a bajt:

**Rendszertervezési hibák (43,8 százalék).** A feladatspecifikáció megszegése 11,8, a szerepspecifikációé 1,5, a lépésismétlés 15,7, a beszélgetéstörténet elvesztése 2,8, a leállási feltétel nem ismerete 12,4 százalék. Vagyis a hibák legnagyobb csoportja nem a modell képességéből, hanem a **rendszer felépítéséből** fakad.

**Ügynökök közötti fel nem zárkózás (32,15 százalék).** Ide tartozik a beszélgetés újraindulása (2,2), a pontosítás elmulasztása (6,8), a feladattól való elsodródás (7,4), az információ visszatartása (0,85), a másik ügynök bemenetének figyelmen kívül hagyása (1,9), és a legnagyobb tétel, az érvelés és a cselekvés közötti eltérés (13,2 százalék) — amikor az ügynök helyesen indokol, majd mást csinál.

**Feladat-verifikáció (24,05 százalék).** Korai lezárás 6,2, hiányzó vagy részleges ellenőrzés 8,2, hibás ellenőrzés 9,1 százalék.

A szerzők beavatkozásokat is teszteltek. A ChatDev munkafolyamatának módosítása (végső döntési jog egy szerepnél) 9,4 százalékkal, a magas szintű célverifikáció hozzáadása 15,6 százalékkal javította a sikerarányt egy programfejlesztési feladaton. **Az összteljesítmény azonban így is alacsony maradt**, amiből a szerzők azt a következtetést vonják le, hogy strukturális újratervezésre van szükség, nem csupán jobb modellre — és hogy a kizárólag kontextus- vagy kommunikációs protokollra épülő megoldások gyakran elégtelenek.

### A gyakorlati ellenvélemény: ne építs többügynökös rendszert

Walden Yan, a Devint fejlesztő Cognition mérnöke 2025 júniusában publikált írásában (S-07) élesen amellett érvel, hogy a párhuzamos alügynökökre épülő architektúra produkciós környezetben törékeny. Két elvet fogalmaz meg: osszuk meg a kontextust és a teljes ügynöknyomvonalat, ne csak az egyes üzeneteket; illetve a cselekvések implicit döntéseket hordoznak, és az egymásnak ellentmondó döntések rossz eredményt adnak.

A szemléltető példája egy Flappy Bird-klón: az egyik alügynök Super Mario stílusú hátteret épít, a másik ehhez nem illő madarat, a koordinátor pedig nem tudja utólag összeegyeztetni a kettőt. Yan ajánlása az egyszerű, egyszálú, lineáris ügynök; hosszú feladatoknál pedig egy tömörítő modell, amely a beszélgetéstörténetet kulcsdöntésekre és eseményekre sűríti.

### A gyártói ajánlás: differenciáltan

Az Anthropic saját útmutatója (S-08) árnyaltabb, de ugyanabba az irányba mutat. Három esetben javasolja a több ügynököt: ha egy részfeladat sok (ezer tokennél több) olyan tartalmat termel, amely a további munka szempontjából irreleváns, tehát a kontextust védeni kell; ha a feladat valóban párhuzamosítható kutatás vagy keresés; és ha a szakterületek élesen elkülönülnek, vagy az ügynököknek egymásnak ellentmondó viselkedésmódra van szükségük. A költség viszont jelentős: a többügynökös megvalósítás azonos feladatra tipikusan **három-tízszer több tokent** használ.

Kifejezetten a kódolásra vonatkozóan egyetlen mintát emelnek ki következetesen működőként: a **verifikáló alügynököt** (verification subagent). A fő ügynök megvalósítja a funkciót, egy külön ügynök pedig futtatja a teszteket — ez azért működik, mert kevés kontextust kell átadni. Ugyanitt megnevezik a minta jellemző hibáját is, a „korai győzelem" problémáját, amikor a verifikáló részleges tesztelés után sikert jelent.

Az Anthropic kutatási rendszerről szóló mérnöki írása (S-09) számokkal is szolgál: a vezető ügynökből és alügynökökből álló rendszer belső értékelésen 90,2 százalékkal múlta felül az együgynökös változatot **kutatási** feladatokon, miközben nagyjából tizenötször annyi tokent használ, mint egy szokásos beszélgetés. A cikk ugyanakkor kimondja, hogy a kódolási feladatok jellemzően kevesebb valóban párhuzamosítható részt tartalmaznak, mint a kutatás, és hogy az ügynökök egyelőre nem jók a valós idejű koordinációban és delegálásban.

### Ahol a több modell bizonyítottan segít: az ellenőrzés

Fontos megkülönböztetés, hogy a *párhuzamos alkotás* és a *párhuzamos ellenőrzés* nem ugyanaz. Az előbbire szólnak a fenti ellenérvek; az utóbbira ellenben erős bizonyíték van, amelyet az 5. dokumentum részletez. Röviden: a Microsoft több mint száz specializált ügynökből álló, több modellcsaládot vegyítő biztonsági rendszere (S-14) és a Refute-or-Promote nevű ellenérvelő módszertan (S-15) egyaránt azt mutatja, hogy **több, egymást cáfolni hivatott ügynök jelentősen javítja a pontosságot** — feltéve, hogy nem együttműködésre, hanem ellentmondásra vannak beállítva.

## Negatív tapasztalatok és buktatók

A legfontosabb figyelmeztetés az, hogy a MAST szerint a hibák 43,8 százaléka rendszertervezési eredetű (S-10). Aki azt reméli, hogy a következő modellgeneráció megoldja a többügynökös rendszerének problémáit, valószínűleg csalódni fog: a hibák nagyobbik fele nem a modellben van.

A második buktató a kontextusizoláció (S-07). Ha két ügynök nem látja egymás teljes nyomvonalát, akkor egymásnak ellentmondó implicit döntéseket hoz, és ez a kódbázisban stílus- és architektúrabeli inkonzisztenciaként csapódik le — ugyanaz a jelenség, amit a GitClear duplikációs adatai (S-04) makroszinten mutatnak.

A harmadik buktató a verifikáció gyengesége: a MAST hibáinak közel negyede (24,05 százalék) az ellenőrzéshez kötődik, és az Anthropic külön nevesíti a „korai győzelem" problémáját (S-08). Egy verifikáló ügynök tehát csak akkor ér valamit, ha a sikerkritériuma nem az, amit ő maga állapít meg.

A negyedik buktató a költség. A három-tízszeres tokenszorzó (S-08) és a kutatási rendszernél mért tizenötszörös szorzó (S-09) azt jelenti, hogy a többügynökös felállásnak érzékelhető pénzügyi ára van, amelyet a pilot költségvetésében meg kell tervezni.

## Mit jelent ez a mi projektünkre

A brief kérdésére — egy ügynök vagy több? — az irodalom alapján **funkció szerint kell szétválasztani a választ**:

- **Az alkotó (kódot író) útvonalon egyszerű, egyszálú ügynököket használjunk**, feladatonként egyet, teljes kontextussal (S-07, S-08). Ne kíséreljük meg ugyanazt a funkciót több párhuzamos ügynökkel megíratni.
- **Az ellenőrző útvonalon viszont többszörözzünk**, méghozzá lehetőleg **eltérő modellcsaládokkal** (S-14, S-15 — részletesen az 5. dokumentumban). A verifikáló alügynök (S-08) az egyetlen kódolási minta, amelyre a gyártó egyértelmű ajánlást ad.
- **A specializációt szerepenként, ne feladatonként képezzük.** A brief említi a tudományos keresőt, refaktorálót, bugfixert, biztonsági ellenőrzőt — ez a felosztás összhangban van az Anthropic „elkülöníthető szakterület" kritériumával (S-08), ellentétben azzal, ha ugyanazt a feladatot vágnánk szét több ügynök között.
- **A MAST hibamódjai közvetlenül használhatók ellenőrzőlistaként** az ügynökök megírásakor. A leállási feltétel hiánya (12,4 százalék), a lépésismétlés (15,7 százalék) és a specifikáció megszegése (11,8 százalék) mind olyan hiba, amelyet a szenior fejlesztő a saját ügynökeiben előre kizárhat, ha tudja, hogy keresnie kell.
- **A tokenköltség mérendő mutató.** Saini javaslata (S-11), hogy az ügynöki feladatokat számítási költséggel mérjük, itt kap empirikus alapot.

## Nyitott kérdések

Nem találtunk kontrollált összehasonlítást arra, hogy egy adott kódolási feladatot egy jól felkészített egyszálú ügynök vagy egy orchestrator-worker felállás old-e meg jobban — az Anthropic 90,2 százalékos javulása kutatási, nem kódolási feladatokra vonatkozik (S-09). Szintén nyitott, hogy a MAST hibaarányai mennyiben tudhatók be a vizsgált keretrendszerek éretlenségének, hiszen a mérés 2025 elején készült, és azóta mind a modellek, mind az eszközök változtak. Végül nincs adatunk arról, hogy a szerepspecializált ügynökpark hány ügynök fölött válik önmagában kezelhetetlenné.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-07 | Walden Yan (Cognition): *Don't Build Multi-Agents*, 2025-06-12 | C |
| S-08 | Anthropic: *When to use multi-agent systems (and when not to)* | C |
| S-09 | Anthropic: *How we built our multi-agent research system*, 2025-06-13 | C |
| S-10 | Cemri és mtsai (UC Berkeley Sky Computing): *Why Do Multi-Agent LLM Systems Fail?*, arXiv:2503.13657 | A |
| S-11 | Sanjay Saini: *AI Augmented Scrum Framework*, Scrum.org, 2026-03-08 | C |
| S-14 | Microsoft Security: *Defense at AI speed — multi-model agentic security system*, 2026-05-12 | C |
| S-15 | Abhinav Agarwal: *Refute-or-Promote*, arXiv:2604.19049, 2026-04-22 | A |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
