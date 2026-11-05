# 6. Tesztelés és regresszió — hogyan legyen a fejlesztés valóban inkrementális

## Mit kerestünk

A brief pontosan fogalmaz: „a tapasztalat azt mutatja, hogy egy refaktorálás közben az AI elronthatja a korábbi kódot. Javít és ront egyszerre." A kérdés az, hova és hogyan építsünk be elegendő tesztet ahhoz, hogy a fejlesztés ne csak iteratív, hanem valóban inkrementális legyen. Ezért olyan bizonyítékot kerestünk, amely megmutatja, mennyire megbízható az ügynökök által írt teszt, és milyen mérőszám mellett tudjuk ezt megítélni.

## Mit találtunk

### A központi felismerés: a lefedettség nem méri, amit hiszünk róla

A legfontosabb megállapítás az, hogy **a kódlefedettség (code coverage) AI-generált tesztek esetén megtévesztő mérőszám**. Wang, Xu, Briand és Liu tanulmánya (S-16) ezt a lehető legélesebben fogalmazza meg: vizsgálatuk során **egyes tesztsorozatok 100 százalékos lefedettséget értek el, miközben a mutációs pontszámuk mindössze 4 százalék volt**.

A különbség lényege egyszerű, és érdemes magyarul is kimondani. A lefedettség azt kérdezi, hogy egy kódsor lefutott-e a teszt közben. A **mutációs teszt** (mutation testing) ennél nehezebb kérdést tesz fel: ha ennek a sornak a viselkedését szándékosan elrontanánk, a tesztsorozat észrevenné-e? A gyakorlatban egy eszköz apró, szándékos hibákat (mutánsokat) vezet be a kódba, majd megnézi, hány mutánst „öl meg" a tesztsorozat. Az így kapott arány, a mutációs pontszám, sokkal szigorúbb minőségjelzés.

A szerzők MUTGEN nevű módszere a mutációs visszajelzést közvetlenül beépíti az LLM promptjába, és iteratívan újabb teszteket generáltat a túlélő mutánsok megölésére. Ez 204 tesztalanyon jelentősen felülmúlta mind az EvoSuite-ot, mind az egyszerű LLM-alapú megközelítéseket.

### Ugyanez a gyakorlatban

Sławomir Radzymiński 2026 augusztusi mérnöki írása (S-17) ugyanezt a problémát a mi helyzetünkre nézve fogalmazza meg. Az érvelése az, hogy amikor **az ügynök írja mind a termelési kódot, mind a tesztet**, a lefedettség végképp értelmét veszti, mert a generált tesztsorozat végigfuthat minden soron úgy, hogy közben szinte semmit nem állít — vagy hűségesen megismétli ugyanazt a félreértést, amit az implementáció is tartalmaz.

A négy projektet felölelő kísérlete konkrét számokat ad. Egy Java háttéralkalmazásnál a mutációs pontszám 81-ről 89 százalékra, egy React frontendnél 60,26-ról 82,41 százalékra emelkedett a módszer alkalmazásával. A legbeszédesebb eset egy SSE-elemző volt, amely **100 százalékos sorlefedettség mellett is csak 61,29 százalékos kiindulási mutációs pontszámot** ért el.

A javasolt gyakorlatok jól átvehetők:

- **Szelektív mutációs teszt.** Ne az egész repozitóriumon fusson, hanem a magas kockázatú területeken: hitelesítés, üzleti szabályok, pénzkezelés.
- **Kétrétegű megközelítés.** Determinisztikus keretrendszerbeli mutánsok (például PITest vagy StrykerJS) mellé ügynök által generált szemantikus mutánsok.
- **Befagyasztott javítás módszere.** A mutációkat csak eldobható másolatokon alkalmazzuk, és követeljük meg a fordítást és a célzott tesztfuttatást.
- **Szerződésközpontú tesztelés.** Kifejezetten olyan teszteket kell írni, amelyek elbuknak a befagyasztott mutánsokon — ez akadályozza meg, hogy az ügynök állítás nélküli teszteket generáljon.

### Ami körültekintésre int a mutációs pontszámmal kapcsolatban

A képhez hozzátartozik, hogy a mutációs pontszám sem tökéletes helyettesítő mutató. Zhao, Zhou és Cohen 2026-os replikációs tanulmánya (S-35) azt vizsgálta, hogy az LLM-generált tesztsorozatoknál a lefedettség és a mutációs pontszám mennyire korrelál a **valódi hibák megtalálásával**. A következtetésük árnyalt, és pontosan a mi helyzetünkre szabott: a két mutató hasznossága **erősen kontextusfüggő**. Regressziós helyzetben, amikor feltételezzük, hogy a vizsgált kód hibátlan, értelmes összehasonlítási jelzést adnak a modellek között. Amikor viszont a vizsgált kód maga is tartalmazhat hibát, **már nem megbízható jelzők**. A szerzők emellett — a korábbi, emberi tesztekre vonatkozó eredményekkel szemben — kevés bizonyítékot találtak arra, hogy a tesztsorozat mérete lenne a meghatározó zavaró tényező.

Ennek a mi pilotunkra nézve konkrét jelentése van: a mutációs pontszámot **regressziós védőhálóként** érdemes használni — vagyis annak mérésére, hogy egy már működő kódrészt megvédenénk-e egy elrontástól —, nem pedig annak megítélésére, hogy egy frissen írt, még nem validált kód jó-e.

### A verifikáció mint architekturális elem

A 4. dokumentumban tárgyalt MAST-taxonómia (S-10) itt kap közvetlen jelentőséget: a többügynökös rendszerek hibáinak **24,05 százaléka a feladat-verifikációhoz kötődik**. Ezen belül a korai lezárás 6,2, a hiányzó vagy részleges ellenőrzés 8,2, a hibás ellenőrzés 9,1 százalékot tesz ki. A kutatók egyik beavatkozása — magas szintű célverifikáció beépítése — 15,6 százalékkal javította a sikerarányt egy programfejlesztési feladaton. Ez azt jelenti, hogy **az ellenőrzés nem a folyamat végén elhelyezett lépés, hanem architekturális elem**.

Ehhez illeszkedik az Anthropic egyetlen egyértelműen ajánlott kódolási mintája, a **verifikáló alügynök** (S-08): a fő ügynök megvalósít, egy külön ügynök futtatja a teszteket. Ugyanitt nevezik meg a minta buktatóját is: a „korai győzelem" problémát, amikor a verifikáló részleges tesztelés után jelent sikert.

## Negatív tapasztalatok és buktatók

Az első és legsúlyosabb buktató a **biztonságérzet illúziója**. Egy zöld tesztfuttatás és egy magas lefedettségi szám AI-generált kód esetén nagyon gyenge bizonyíték (S-16, S-17). Ha a Definition of Done lefedettségi küszöbre épül, akkor pontosan azt fogjuk optimalizálni, ami nem méri a minőséget — és az ügynök nagyon hatékonyan fogja ezt a célt teljesíteni.

A második buktató a **tautologikus teszt**: az olyan teszt, amely az implementációt önmagához méri, nem pedig egy függetlenül levezetett elvárt viselkedéshez. Ilyen teszt soha nem bukhat el, hacsak a kód nem dob kivételt. Ez különösen akkor jelentkezik, ha a tesztet ugyanaz az ügynök írja, amelyik az implementációt (S-17).

A harmadik buktató a refaktorálás elmaradása. Mivel az AI-val segített pull requestekben a refaktorálás aránya gyakorlatilag nulla (S-06), és a duplikáció ipari szinten nő (S-04), a „javít és ront egyszerre" probléma nem is jut el a tesztekig: a kód szerkezete romlik anélkül, hogy bármelyik teszt elbukna.

A negyedik buktató a verifikáló ügynök megbízhatósága. Ha ugyanaz a modell verifikál, mint amelyik írt, ugyanazt a félreértést fogja megerősíteni — ez ugyanaz a modellcsaládon belüli torzítás, amelyet a biztonsági fejezetben (S-15) is láttunk.

## Mit jelent ez a mi projektünkre

A brief kérdése az volt, hova és hogyan építsünk be elegendő tesztet. A kutatás alapján a válasz nem az, hogy „többet", hanem hogy **másképp mérve és más helyre**.

Konkrét javaslatok a pilothoz:

1. **A Definition of Done ne lefedettségi százalékra épüljön.** Helyette a magas kockázatú modulokra írjunk elő mutációspontszám-küszöböt (S-16, S-17). A többi területen a lefedettség maradhat tájékoztató mutató, de nem kapu.
2. **Készüljön karakterizációs tesztréteg minden refaktorálás előtt.** A meglévő viselkedést rögzítő tesztek nélkül a refaktorálás nem ellenőrizhető — ez a klasszikus válasz a „javít és ront egyszerre" problémára, és ügynökös közegben még fontosabb.
3. **A verifikáló ügynök ne ugyanaz a modell legyen, mint az implementáló.** Ez az 5. dokumentum modellcsalád-keverési tanulságának alkalmazása a tesztelésre.
4. **A verifikáció sikerkritériumát ne az ügynök állapítsa meg.** A MAST korai lezárási hibamódja (S-10) és az Anthropic „korai győzelem" figyelmeztetése (S-08) ugyanarra mutat: kívülről, determinisztikusan kell eldönteni, hogy a teljes tesztsorozat lefutott-e.
5. **A tesztek review-ja külön elbírálandó**, nem a kódéval együtt. A tautologikus teszt szemre rendben van; csak akkor derül ki róla, hogy értéktelen, ha valaki külön megnézi, mit állít.
6. **Fusson szándékos regressziópróba.** Iterációnként legalább egyszer érdemes szándékosan hibát bevinni a kódba (befagyasztott másolaton), és megnézni, elbukik-e valamelyik teszt. Ez a legolcsóbb módja annak, hogy a tesztháló valódi állapotát lássuk.

Az SM szempontjából mindebből egy egyszerű kérdés következik, amelyet az iterációs áttekintésben fel kell tenni: **„Ha most elrontanánk ezt a modult, észrevennénk?"** Ha a válasz nem egyértelmű igen, akkor az iteráció nem inkrementális volt, hanem csak iteratív.

## Nyitott kérdések

Nem tudjuk, milyen mutációspontszám-küszöb reális és gazdaságos egy belső intranet esetében; az irodalom módszert ad, küszöböt nem. Szintén nyitott, hogy a mutációs teszt futásideje mennyire fér bele egy néhány napos iterációba — a hivatkozott gyakorlatok éppen ezért javasolják a szelektív alkalmazást. Végül a replikációs vizsgálat (S-35) éppen azt mutatja, hogy a mutációs pontszám ott a legkevésbé megbízható, ahol a legjobban jönne: az még nem validált, potenciálisan hibás kód megítélésénél. Erre a helyzetre nem találtunk működő helyettesítő mutatót — marad az emberi bírálat.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-16 | Wang, Xu, Briand, Liu: *Mutation-Guided Unit Test Generation with a Large Language Model*, arXiv:2506.02954 | A |
| S-17 | Sławomir Radzymiński: *Mutation Testing for Agent-Written Code*, 2026-08-02 | C |
| S-35 | *Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability Study)*, arXiv:2607.22880 | A |
| S-10 | *Why Do Multi-Agent LLM Systems Fail?* (MAST), arXiv:2503.13657 | A |
| S-08 | Anthropic: *When to use multi-agent systems (and when not to)* | C |
| S-06 | LinearB: *2026 Software Engineering Benchmarks Report* | B |
| S-04 | GitClear: *The Maintainability Gap*, 2026 | B |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
