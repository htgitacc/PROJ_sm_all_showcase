# Összefoglaló — mit tudunk, mit nem, és mit kerüljünk

Ez a dokumentum a kutatás vezetői összefoglalója. A részleteket és a hivatkozásokat a tematikus dokumentumok tartalmazzák; a teljes forrásjegyzék megbízhatósági szintezéssel a [forrasok.md](forrasok.md), az idegen kifejezések magyarázata a [glossary.md](glossary.md) fájlban található.

## A kutatás egymondatos eredménye

**Az AI-ügynökökkel dolgozó fejlesztőcsapat ma már bizonyítottan létező gyakorlat, de a keretrendszere nincs kidolgozva; a modell egyetlen valódi tervezési korlátja pedig nem az ügynökök sebessége, hanem az emberi kódellenőrzés kapacitása.**

## A hat legfontosabb tanulság

### 1. A review a szűk keresztmetszet — és ez mérve is látszik

Ez a kutatás legerősebben alátámasztott megállapítása. Egy EASE 2026-os empirikus tanulmány (S-05) szerint a nyilvános GitHub-repozitóriumokban az ügynökök által benyújtott pull requestek **84 százalékát vagy egyáltalán nem nézi át senki, vagy kizárólag gép nézi át**; csupán 15,9 százalékuknál látszik bármilyen emberi részvétel. Ugyanezt a jelenséget a folyamat oldaláról méri a LinearB 8,1 millió pull requestet átfogó elemzése (S-06): az AI által generált változtatások két és félszer nagyobbak, elfogadási arányuk 32,7 százalék a segítség nélküli munka 84,5 százalékával szemben, és átlagosan több mint tizenhat órát várnak bírálóra, szemben a segítség nélküli munka mintegy 200 percével.

A legfontosabb részlet, hogy **ha a review egyszer elkezdődött, az AI-s pull request gyorsabban zárul** — vagyis a torlódás nem a bírálat lassúságából, hanem a sorban állásból ered. Nem a bírálót kell gyorsítani, hanem a beérkező mennyiséget korlátozni.

### 2. Az emberi felügyelet nem megszűnik, hanem észrevétlenül átalakul

Ugyanaz a tanulmány (S-05) kimutatta, hogy az emberek jelen vannak az ügynöki pull requesteknél — csak mást csinálnak. Az emberi hozzászólásoknak emberi szerzőségű pull requestnél 93,56 százaléka valódi elbírálás, ügynökinél viszont csak 65,53 százaléka; a különbözet ügynökirányítássá alakul (1,63 százalékról 25,92 százalékra ugrik). Nagy hatásméret mellett (Cramér-féle V = 0,34) ez azt jelenti, hogy **a bíráló egyre inkább utasítgatja a gépet ahelyett, hogy elbírálná a munkáját**.

Ennek közvetlen mérési következménye van: a „hány review történt" típusú mutató AI-korban nem méri az emberi felügyeletet. Külön kell mérni az emberi és a gépi bírálatot.

### 3. Gyorsabb — de instabilabb, és a saját érzetünk megbízhatatlan

A DORA 2025-ös, közel ötezer fős felmérése (S-02) szerint az AI-adopció **pozitívan** korrelál az átbocsátással, ugyanakkor **továbbra is negatívan** a szállítási stabilitással. A jelentés összefoglaló képe szerint az AI erősítőként viselkedik: felnagyítja a szervezet meglévő erősségeit és gyengeségeit.

Emellé kötelező odatenni a METR randomizált kontrollált kísérletét (S-01), amely szerint tapasztalt fejlesztők a saját, kiforrott kódbázisukon **19 százalékkal lassabbak** lettek AI-val — miközben utólag is 20 százalékos gyorsulást éltek meg. A szerzők maguk hangsúlyozzák, hogy ez nem általánosítható minden fejlesztési helyzetre; a mi zöldmezős intranetünk éppen az ellenkező végén van a spektrumnak. De egy dolog átvihető: **a csapat önértékelése nem bizonyíték**.

### 4. A karbantarthatóság csendben erodálódik

A GitClear 623 millió változtatást átfogó 2026-os elemzése (S-04) szerint a blokk-duplikáció 2023 óta 81 százalékkal nőtt, az áthelyezett — vagyis valódi refaktorálásra utaló — kód aránya a 2022-es 21 százalékról 3,8 százalékra esett, a fájlok közötti függvénykapcsoltság pedig 35 százalékkal csökkent. Ezzel összecseng a LinearB megfigyelése (S-06), hogy az AI-val segített pull requestekben a refaktorálás aránya gyakorlatilag nulla.

Ez a hatás **hónapokkal később jelentkezik a költségekben**, tehát egy néhány hetes pilot nem fogja látni, ha nem méri kifejezetten. Az együttjárás erős, de nem bizonyít okozatot, és a forrás a saját elemzőtermékéhez kapcsolódó kutatást publikál — ezt az adat felhasználásakor mindig érdemes hozzátenni.

### 5. Kódírásra egy ügynök, ellenőrzésre több — és több modellcsalád

A brief „egy ügynök vagy több" kérdésére az irodalom **funkció szerint eltérő választ** ad, és ez a kutatás egyik legpraktikusabb eredménye.

A **kódírás** oldalán az egyszerűség mellett szól a bizonyíték. A MAST-taxonómia (S-10) hét nyílt keretrendszerben 41 és 86,7 százalék közötti hibaarányt mért, és a hibák 43,8 százaléka rendszertervezési, nem modellképességi eredetű volt. A Cognition gyakorlati állásfoglalása (S-07) a párhuzamos alügynökök kontextusizolációját nevezi meg fő törékenységi forrásként, az Anthropic pedig maga is kimondja (S-09), hogy a kódolási feladatok kevésbé párhuzamosíthatók, mint a kutatás.

Az **ellenőrzés** oldalán viszont erős érv szól a többszörözés mellett — de csak akkor, ha az ügynökök nem együttműködnek, hanem **cáfolják egymást**. A Refute-or-Promote módszertan (S-15) 171 jelöltből 79 százalékot ejtett ki, és — ez a döntő részlet — az **azonos modellcsaládon belüli felülvizsgálat 19 esetből 3-ban (16 százalék) nem vette észre a hibát**, amelyet a más gyártótól származó bíráló megtalált. A Microsoft több mint száz ügynökből álló, több modellcsaládot vegyítő biztonsági rendszere (S-14) ugyanezt az elvet valósítja meg ipari léptékben.

### 6. A visszajelzés beépülése mérhető — a szabályfájlon keresztül

A brief egyik legélesebb kérdésére („hogyan építhető be az AI-ba a visszajelzés, és hogyan ellenőrizzük, hogy beépült?") találtunk konkrét, mért választ. Egy Microsoft-csapat zárt hurkú keretrendszere (S-26) minden elfogadott review-észrevételt önellenőrzési szabállyá alakít egy verziókövetett utasításfájlban. Négy hét alatt, 35-nél több mikroszolgáltatáson a szabálykészlet 5-ről 18 viselkedési szabályra nőtt, kilenc követett hibaosztálynál 74 lehetséges előfordulás mellett **nulla visszaesést** mértek, és a review-észrevételeknek már csak 14 százaléka szólt mechanikus helyességről (66 százalékuk architektúráról és API-tervezésről).

A bizonyíték tehát nem az ügynök ígérete, hanem **az adott hibaosztály eltűnése** — ez ellenőrizhető, és az iterációs visszatekintés mérhető kimenetévé tehető. A tanulmány korlátja, hogy egyetlen csapat négy hetéből származik, kontrollcsoport nélkül.

## Amire nem találtunk választ

Ezek a hiányok legalább annyira fontosak, mint a talált eredmények, mert megmutatják, hol vagyunk úttörők, és hol kell a saját mérésünkre támaszkodnunk.

- **Nem létezik publikált mérés az általunk tervezett felállásra.** Nem találtunk olyan vizsgálatot, amely egy AI-ügynököket csapattagként foglalkoztató Scrum-csapatot hasonlított volna össze egy hagyományossal.
- **Nincs adat a rövid iterációra.** A három-öt napos ciklus mellett szóló érvelés tervezési logikából következik, nem mérésből.
- **Nincs validált mérőeszköz az ember–ügynök csapat érettségére.** A T⁴ keretrendszer (S-18) fázisokat és tényezőket ad, mérőeszközt nem.
- **Nincs módszer a kontextusfájlok hatásosságának mérésére** — ezt a kutatók maguk nevesítik hiányként (S-25).
- **Nincs mérőszám az ügynöki feladat „nehézségére".** A story pont helyére javasolt tokenköltség a ráfordítást méri, a komplexitást nem.
- **Nem tudjuk, hány valódi hibát ejt ki a cáfoló szűrő.** A Refute-or-Promote a pontosságra optimalizál, a felidézést nem méri (S-15).

## Mit kerüljünk — ellenőrzőlista

1. **Ne tervezzünk az ügynökök sebességére.** A kapacitás felső korlátja az, hány elemet tud a két szenior érdemben átnézni. (S-05, S-06, S-11, S-28)
2. **Ne fogadjuk el a review-számot a felügyelet bizonyítékának.** Külön kell mérni, hogy ember nézte-e át. (S-05)
3. **Ne engedjünk nagy pull requesteket.** A nagy csomag felületesebb elbírálást vált ki, és az AI-s változtatások alapból két és félszer nagyobbak. (S-06)
4. **Ne alapozzuk a Definition of Done-t kódlefedettségre.** Vizsgáltak olyan tesztsorozatot, amely 100 százalékos lefedettség mellett 4 százalékos mutációs pontszámot ért el. (S-16)
5. **Ne verifikáltassunk ugyanazzal a modellcsaláddal, amelyik írta.** Az azonos családon belüli bírálat rendszeresen ugyanazokat a hibákat nézi el. (S-15)
6. **Ne állítsuk az ügynököket együttműködő konszenzusra biztonsági kérdésben.** Egyetlen meggyőző ügynök felülírhatja a többségi szavazást; a szerepeket cáfolásra kell beállítani. (S-15)
7. **Ne bízzuk ítéleti döntést AI-ra.** Az ember–AI csapat ítéleti és döntési feladatokban negatív szinergiát mutathat, alkotó feladatokban pozitívat. (S-19)
8. **Ne hagyjuk, hogy a csapat érzete legyen a siker mércéje.** (S-01)
9. **Ne induljunk el sikerkritérium és kilépési feltétel nélkül.** A vállalati AI-pilotok jellemző kudarcoka a mérés hiánya vagy rossz megválasztása. (S-32)
10. **Ne felejtsük el az AI-jártassági kötelezettséget.** Az EU AI Act 4. cikke 2025. február 2. óta alkalmazandó minden AI-t üzembe helyező szervezetre. (S-22)
11. **Ne maradjon beolvasztás megnevezett emberi jóváhagyó nélkül.** A felelősség jogilag és gyakorlatilag is emberi. (S-24, S-33)
12. **Ne engedjük el a refaktorálást.** Magától nem történik meg; külön ki kell kényszeríteni. (S-04, S-06)

## Hol keresd a brief kérdéseire adott anyagot

A [sm-all.md](../sm-all.md) kilenc kérdésköre a következő dokumentumokban kapott feldolgozást. Minden dokumentum „Mit jelent ez a mi projektünkre" szakasza válaszol közvetlenül a kérdésre — ez lesz a koncepciófázis bemenete.

| A brief kérdésköre | Hol válaszolunk rá |
|---|---|
| **Backlog** — ki darabol, és hogyan mérhető, hogy jobb-e | [01](01-agilis-keretrendszer-es-ai-ugynokok.md) (specifikáció-vezérelt darabolás), [07](07-metrikak.md) (mérhetőség), [11](11-iteracios-ritmus.md) (a darabolás mint ellenőrzési pont) |
| **Sebesség** — hogyan ne készüljön 30 elem 5 átnézett mellett | [03](03-review-es-atbocsatokepesseg.md) *(fő dokumentum)*, [11](11-iteracios-ritmus.md) |
| **Biztonság** — egy ügynök és modell, vagy több | [05](05-biztonsag.md) *(fő dokumentum)*, [04](04-multi-agent-tapasztalatok.md) |
| **Tesztek** — hogyan legyen inkrementális, ne csak iteratív | [06](06-teszteles-es-regresszio.md) *(fő dokumentum)* |
| **Scrum események** — mi marad, mi új, bevonható-e az AI | [11](11-iteracios-ritmus.md) *(fő dokumentum)*, [10](10-dokumentacio-es-tudasatadas.md) (a visszajelzés beépülése) |
| **Teljesítmény** — mit mérünk, van-e értelme story pontnak | [07](07-metrikak.md) *(fő dokumentum)*, [02](02-termelekenyseg-empirikus-adatok.md) |
| **Csapatpszichológia** — Tuckman helyett mi | [08](08-csapatdinamika.md) *(fő dokumentum)* |
| **Jogi keretek, felelősség, átadás, hibaelhárítás** | [09](09-jogi-es-felelossegi-keret.md) *(fő dokumentum)* |
| **Szerepkör-változások, hibázó ügynök kezelése** | [01](01-agilis-keretrendszer-es-ai-ugynokok.md) („Mi történik a szerepkörökkel" szakasz) |
| **Dokumentáció, csapatindító dokumentum** | [10](10-dokumentacio-es-tudasatadas.md) *(fő dokumentum)* |

## A dokumentumok

| Dokumentum | Miről szól |
|---|---|
| [01 — Agilis keretrendszer és AI-ügynökök](01-agilis-keretrendszer-es-ai-ugynokok.md) | Létezik-e már ilyen felállás; mit mondanak a szakmai szervezetek |
| [02 — Termelékenység, empirikus adatok](02-termelekenyseg-empirikus-adatok.md) | Tényleg gyorsabb-e; mi az ára |
| [03 — Review és átbocsátóképesség](03-review-es-atbocsatokepesseg.md) | **A modell tartógerendája:** a review mint szűk keresztmetszet |
| [04 — Multi-agent tapasztalatok](04-multi-agent-tapasztalatok.md) | Egy ügynök vagy több; a MAST hibataxonómia |
| [05 — Biztonság](05-biztonsag.md) | Fenyegetési modell és a cáfoló ellenőrző architektúra |
| [06 — Tesztelés és regresszió](06-teszteles-es-regresszio.md) | Hogyan legyen a fejlesztés valóban inkrementális |
| [07 — Mérőszámok](07-metrikak.md) | Mit tartsunk meg, mit engedjünk el, mit vezessünk be |
| [08 — Csapatdinamika](08-csapatdinamika.md) | Tuckman helyett T⁴; a teljesítményparadoxon |
| [09 — Jogi és felelősségi keret](09-jogi-es-felelossegi-keret.md) | AI Act, termékfelelősség, szerzői jog, átadás |
| [10 — Dokumentáció és tudásátadás](10-dokumentacio-es-tudasatadas.md) | A gépnek szóló dokumentáció és a tanulási hurok |
| [11 — Iterációs ritmus](11-iteracios-ritmus.md) | Az iteráció hossza és a Scrum események sorsa |
| [glossary.md](glossary.md) | Idegen kifejezések magyarázata |
| [forrasok.md](forrasok.md) | Teljes forrásjegyzék megbízhatósági szintezéssel |

## Mi következik ebből

A kutatás alapján a koncepciófázisnak három kérdésre kell elsőként választ adnia, mert ezekből következik minden más:

1. **Mennyi a csapat tényleges emberi review-kapacitása?** Ez a szám a modell összes többi paraméterét meghatározza.
2. **Mi kerül a Definition of Done-ba**, és melyik kapu gépi, melyik emberi?
3. **Mi a pilot sikerkritériuma és kilépési feltétele**, több dimenzióban mérve?

Ezekre a 3., 6. és 7. dokumentum ad kiindulási anyagot. A koncepciófázis külön terv alapján, ennek az anyagnak az áttekintése után indul.
