# 8. Csapatdinamika és emberi tényezők

## Mit kerestünk

A brief két kérdést tesz fel: alkalmazható-e a Tuckman-modell egy ilyen csapatra, és ha nem, milyen modellt lehetne felállítani, amely megjeleníti a csapat dinamikáját és fejlődési görbéjét. Ehhez az ember–ügynök csapatmunka (human–agent teaming) kutatási irodalmát néztük át, valamint azokat a kísérleteket, amelyekben az AI ténylegesen csapattagként vett részt.

## Mit találtunk

### Tuckman helyett: a T⁴ keretrendszer

A Tuckman-modell (alakulás, viharzás, normázás, működés) emberi csoportokra készült, és a benne leírt folyamatok — a státuszharc, a normák kialakulása, a bizalom felépülése — kölcsönös társas észlelést feltételeznek. Az általunk talált irodalom nem cáfolja a modellt, de nem is alkalmazza gépi csapattagokra; helyette **saját fázismodellt** javasol.

Wang és szerzőtársai áttekintő tanulmánya (S-18) folyamatdinamikai nézőpontból rendszerezi az ember–ügynök csapatmunka empirikus vizsgálatait, és négy fázisból álló, **T⁴** nevű keretrendszert javasol:

1. **Csapatalakítás (Team Formation)** — a csapat összeállítása, az ügynökök kiválasztása és beillesztése.
2. **Feladat- és szerepfejlődés (Task and Role Development)** — a szerepek és felelősségek kialakítása.
3. **Csapatfejlődés (Team Development)** — a működés összecsiszolódása.
4. **Csapatjavítás (Team Improvement)** — a teljesítmény hosszabb távú javítása.

A szerzők kiemelten a második és a harmadik fázissal foglalkoznak, és három tényezőt emelnek ki: a **csapatszerepeket**, a **közös mentális modellt** (shared mental model) és a **támogató viselkedést** (backup behavior). A keretrendszer lényege, hogy a feladat és a csapat dinamikája együtt fejlődik, és hogy az irodalom fő hiányossága éppen az **alkalmazkodóképesség** vizsgálata: a legtöbb kutatás egyetlen fázisra vagy egyetlen problémára (jellemzően a bizalom kalibrálására) összpontosít.

A T⁴ számunkra azért használható, mert **ciklikus, nem lineáris**: a negyedik fázis visszavezet a másodikba és a harmadikba. Egy olyan csapatban, ahol az ügynökök összetétele és konfigurációja iterációról iterációra változhat, ez sokkal élethűbb, mint egy egyszer lefutó fejlődési görbe.

### A teljesítményparadoxon: hol nyer és hol veszít az ember–AI csapat

Tong hatvan évet átfogó áttekintése (S-19) egy metaanalitikus megfigyelést fogalmaz meg, amelyet **teljesítményparadoxonnak** nevez. Az ember–AI csapatok **ítéleti és döntési feladatokban negatív szinergiát** mutatnak, vagyis rosszabbul teljesítenek, mint az AI önmagában; **tartalom-előállítási és problémamegfogalmazási feladatokban** viszont pozitív szinergiát.

A szerző okozati láncot javasol a hatékony csapatmunka mechanizmusára: a **magyarázható AI** (XAI) teszi lehetővé a **kölcsönös alkalmazkodást** (co-adaptation), az pedig a **közös mentális modellek** kialakulását.

Ennek a mi felállásunkra nézve nagyon konkrét jelentése van. A kódírás és a tervezetek megfogalmazása alkotó feladat — itt várhatunk nyereséget. A **döntés arról, hogy egy kód elég jó-e**, viszont ítéleti feladat — és éppen ez az, ahol az irodalom szerint az ember–AI páros alulteljesíthet. Ez független érv amellett, hogy a Definition of Done-t ember mondja ki (lásd a 7. dokumentumot).

### Amit egy nagy terepkísérlet mutat

Dell'Acqua és szerzőtársai előzetesen regisztrált terepkísérlete a Procter & Gamble-nél (S-20) 776 szakembert osztott véletlenszerűen csoportokba aszerint, hogy AI-val vagy anélkül, egyénileg vagy párban dolgoztak-e valós termékfejlesztési feladaton. Két eredmény érdekes számunkra.

Az első: **az AI-val dolgozó egyén elérte az AI nélküli kétfős csapat teljesítményét.** Vagyis az AI a csapatmunka bizonyos előnyeit — a nézőpontok ütköztetését, a hiányzó tudás pótlását — helyettesíteni tudta.

A második: az AI **lebontotta a funkcionális silókat**. AI nélkül a kutatás-fejlesztési szakemberek technikai, a kereskedelmiek üzleti megoldásokat javasoltak; AI-val kiegyensúlyozott javaslatok születtek, függetlenül a szakmai háttértől. Ez a mi kétfős szeniorcsapatunkra nézve annyit jelent, hogy az ügynökök részben pótolhatják a hiányzó szerepeket (például egy dedikált tesztelő vagy egy UX-szakember nézőpontját) — de csak részben, és nem a döntésekben.

A harmadik, kevésbé várt eredmény, hogy az AI-val dolgozó résztvevők **pozitívabb érzelmi állapotról számoltak be**, ami arra utal, hogy az AI részben az emberi csapattárs motiváló szerepét is betölti. Ez a csapatpszichológia szempontjából kétélű: enyhítheti a magányos munka terhét, de növelheti a túlzott bizalom kockázatát is.

## Negatív tapasztalatok és buktatók

Az első buktató a **bizalom rossz kalibrálása**. Az irodalom (S-18) a bizalom kalibrálását a terület központi problémájaként kezeli. Két irányba lehet tévedni: a túlzott bizalom automatizálási elfogultsághoz vezet, amikor az ember elfogadja a gép javaslatát anélkül, hogy érdemben megvizsgálná; a túl kevés bizalom viszont felesleges duplikált munkát okoz. A 3. dokumentum adatai (S-05) arra utalnak, hogy a gyakorlatban az első irányba szoktunk tévedni.

A második buktató az **ítéleti feladatok delegálása** (S-19). Ha a csapat az AI-t abban is bevonja, hogy eldöntse, jó-e valami, a teljesítményparadoxon szerint romolhat az eredmény.

A harmadik buktató, amelyet Saini is nevesít (S-11), az emberi oldal kimerülése: a nagy mennyiségű AI-generált kód átnézése mentálisan fárasztó. Ez nem apró részlet — a DORA 2025 (S-02) a „Foundational Challenges" csapatprofilnál kifejezetten együtt említi a magas instabilitást és a kiégést, és megállapítja, hogy az instabilitás rontja a jóllétet.

A negyedik buktató a **mérés hiánya**. A T⁴ (S-18) fázisokat és tényezőket ad, de nem ad kész mérőeszközt; a közös mentális modell és a támogató viselkedés operacionalizálása nyitott kérdés marad.

## Mit jelent ez a mi projektünkre

A brief kérdésére — alkalmazható-e a Tuckman-modell — a válasz az, hogy **részben, és nem a gépi tagokra**. A csapatnak van emberi rétege (PO, SM, két szenior), amelyre a klasszikus csoportdinamikai modellek továbbra is érvényesek, hiszen ezek az emberek egymással alakítanak ki normákat és bizalmat. Az ügynökök viszont nem viharzanak és nem normáznak: ők **konfigurációval fejlődnek**, nem társas tanulással.

Ebből az következik, hogy **kétrétegű modellt** érdemes felállítani:

- **Emberi réteg:** klasszikus csapatdinamika, ahol a Scrum Master a szokásos eszközeivel dolgozik. Itt van értelme a Tuckman-fázisoknak, a pszichológiai biztonságnak és a retrospektívnek a hagyományos értelemben.
- **Szociotechnikai réteg:** a T⁴ ciklusa (S-18), amelyben az ügynökpark összetétele, szerepei és konfigurációja fejlődik. Itt a „viharzás" megfelelője az, amikor az ügynökök egymásnak ellentmondó változtatásokat hoznak, és a „normázásé" az, amikor a szabályfájlok (lásd a 10. dokumentumot) letisztulnak.

A **mérés** kérdésére a következőket javasoljuk. Mivel a T⁴ nem ad kész eszközt, a fejlődési görbét közvetett jelzőkkel érdemes megjeleníteni:

| Mit jelez | Mérőszáma | Melyik réteg |
|---|---|---|
| Bizalom kalibráltsága | első körös elfogadási arány, és ennek szórása szeniorok között | szociotechnikai |
| Közös mentális modell érettsége | a szabályfájlok stabilizálódása: hány új szabály születik iterációnként | szociotechnikai |
| Emberi terhelés | review-ra fordított idő aránya a teljes munkaidőben; önbevallásos terhelés | emberi |
| Csapat együttműködése | hány elemet zárnak le közösen (swarming), hány marad egyetlen emberen | emberi |
| Ügynökpark érettsége | ismétlődő hibaosztályok száma iterációnként | szociotechnikai |

A Scrum Master számára a legfontosabb figyelmeztető jel a **review-terhelés eloszlása**: ha az egyik szenior aránytalanul többet bírál, az nemcsak kapacitásprobléma, hanem kiégési kockázat is (S-02, S-11).

## Nyitott kérdések

A legnagyobb hiány az, hogy **nem találtunk validált mérőeszközt** az ember–ügynök csapat érettségének mérésére; a fenti táblázat javaslat, nem bevált gyakorlat. Szintén nyitott, hogy a teljesítményparadoxon (S-19) mennyire általánosítható szoftverfejlesztési feladatokra, hiszen a hivatkozott metaanalízis nem erre a területre készült. Végül nem találtunk vizsgálatot arra, hogyan hat a csapat kohéziójára az, ha a csapat „létszámának" nagy része cserélhető konfiguráció — vagyis mennyire lehet egyáltalán csapatként gondolni egy ilyen felállásra.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-18 | Wang, Wu, Ma, Li, Zhang, Gu, Lu: *Adaptive Human-Agent Teaming: A Review of Empirical Studies from the Process Dynamics Perspective*, arXiv:2504.10918, 2025-04-15 | A |
| S-19 | Richard Jiarui Tong: *From Augmentation to Symbiosis: A Review of Human-AI Collaboration Frameworks, Performance, and Perils*, arXiv:2601.06030 | A |
| S-20 | Dell'Acqua és mtsai: *The Cybernetic Teammate*, NBER w33641 / Organization Science | A |
| S-02 | DORA: *State of AI-assisted Software Development 2025* | B |
| S-05 | Duma és mtsai: *These Aren't the Reviews You're Looking For*, EASE 2026 | A |
| S-11 | Sanjay Saini: *AI Augmented Scrum Framework*, Scrum.org | C |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
