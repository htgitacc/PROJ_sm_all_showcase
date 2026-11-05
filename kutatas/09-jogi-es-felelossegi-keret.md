# 9. Jogi keretek és felelősségvállalás

> **Fontos megjegyzés:** ez a dokumentum kutatási összefoglaló, nem jogi tanácsadás. A pilot éles indítása előtt a benne foglaltakat a szervezet jogi és adatvédelmi funkciójával kell egyeztetni.

## Mit kerestünk

A brief négy kérdést tesz fel: hogyan akadályozható meg, hogy az AI túllépjen a megengedett határokon; ki vállal felelősséget a fejlesztésért; miben változik az átadás az üzemeltető csapatnak; és hogyan történik a hibaelhárítás. Ezért a hatályos és a közeljövőben hatályba lépő európai szabályozást, a vonatkozó szabványokat, a szerzői jogi helyzetet, valamint a nyílt forrású közösségek kialakult gyakorlatait néztük át.

## Mit találtunk

### A szabályozási naptár

Az **EU mesterségesintelligencia-rendelete (AI Act)** fokozatosan lép hatályba (S-21). A rendelet 2024. augusztus 1-jén lépett életbe; 2025. február 2-tól alkalmazandók a tiltott gyakorlatokra vonatkozó szabályok és az **AI-jártassági kötelezettség**; 2025. augusztus 2-tól az általános célú modellekre és a kormányzási struktúrákra vonatkozó rendelkezések; 2026. augusztus 2-tól a rendelet fennmaradó rendelkezéseinek túlnyomó része. A magas kockázatú rendszerekre vonatkozó egyes határidőket kitolták.

A mi projektünk szempontjából a **4. cikk** a legfontosabb (S-22), mert ez ránk közvetlenül vonatkozik. A rendelkezés szerint az AI-rendszerek szolgáltatóinak és üzembe helyezőinek intézkedéseket kell tenniük annak érdekében, hogy a személyzetük és a nevükben az AI-rendszereket kezelő egyéb személyek megfelelő szintű AI-jártassággal rendelkezzenek, figyelembe véve a technikai tudásukat, tapasztalatukat, képzettségüket és az alkalmazás összefüggéseit. A rendelet meghatározása szerint az AI-jártasság azokat a készségeket, ismereteket és megértést jelenti, amelyek lehetővé teszik a tájékozott alkalmazást, valamint a lehetőségek és kockázatok felismerését. A kötelezettség nem konkrét szintet ír elő, hanem „megfelelő szintet" a szerepekhez és a kontextushoz mérten.

Ez a pilotra nézve konkrét feladatot jelent: **az AI-jártasság dokumentált fejlesztése nem opcionális jó gyakorlat, hanem 2025. február 2. óta jogi kötelezettség** minden olyan szervezetnél, amely AI-rendszert helyez üzembe. A csapatindító dokumentumnak (lásd a 10. dokumentumot) ezt kezelnie kell.

### A termékfelelősségi fordulat

A másik, kevésbé ismert, de nagyon fontos fejlemény az **új európai termékfelelősségi irányelv** (2024/2853), amelyet a tagállamoknak 2026. december 9-ig kell átültetniük, és amely az ezt követően forgalomba hozott vagy üzembe helyezett termékekre alkalmazandó (S-37). Az irányelv kiterjeszti a termék fogalmát a szoftverre és az AI-rendszerekre, vagyis ezekre is a **vétkességtől független (objektív) felelősség** szabályai vonatkoznak, mint korábban a fizikai termékekre. Emellett a felperesek javára bizonyítási könnyítéseket és közlési kötelezettségeket vezet be.

Itt egy fontos megkülönböztetést kell tenni. A mi intranetünk **belső használatra készül, nem kerül forgalomba**, ezért a termékfelelősségi rezsim várhatóan közvetlenül nem alkalmazandó rá. A brief azonban kifejezetten azt kéri, hogy úgy kezeljük a projektet, mintha külső ügyfél rendszerét építenénk — és ebben az esetben ez a szabályozás közvetlenül releváns lenne. A pilot ezért jó alkalom arra, hogy a folyamat már most tartalmazza azokat az elemeket (eredetnyomozás, naplózás, dokumentált felülvizsgálat), amelyeket egy külső szállítású termék megkövetelne.

### Szabványos irányítási keret

Az **ISO/IEC 42001:2023** (S-23) az első nemzetközi MI-irányítási rendszerszabvány. Követelményrendszere négy fő területet fed le: a kockázatkezelést (az AI-specifikus kockázatok azonosítása, értékelése, csökkentése és éles működés közbeni figyelése), az irányítást és elszámoltathatóságot (szerepek, felelősségek és eszkalációs útvonalak meghatározása), az átláthatóságot és dokumentálást (műszaki dokumentáció, szabályzatok, értékelési artefaktumok), valamint az életciklus-kontrollokat (értékelési protokollok, bevezetés utáni figyelés, incidensbejelentés). A szabvány melléklete kategóriákba rendezett kontrollkészletet tartalmaz; a pontos kontrollszámot csak a megvásárolt szabványszövegből lehet hitelesen megadni, ezért itt szándékosan nem idézünk konkrét számot.

A pilot szintjén a tanúsítás nyilvánvalóan nem cél, de a szabvány **szerkezete kiváló ellenőrzőlista**: ha a csapatindító dokumentum ezt a négy területet lefedi, akkor a későbbi felskálázás nem kezdődik nulláról.

### Szerzői jog és licenc

Az Egyesült Államok Szerzői Jogi Hivatalának 2025 januárjában kiadott, a szerzői jogi védhetőségről szóló jelentése (S-33) a következő megállapításokat teszi. A védhetőség kérdései a **hatályos jog alapján megválaszolhatók**, jogalkotásra nincs szükség. Az AI eszközként való használata — vagyis amikor segíti, nem pedig helyettesíti az emberi alkotást — nem érinti a védelem elérhetőségét. A szerzői jog **nem terjed ki a tisztán AI által előállított anyagra**, sem arra, ahol az ember nem gyakorolt elegendő ellenőrzést az expresszív elemek fölött. Azt, hogy az emberi hozzájárulás elegendő-e a szerzőséghez, esetről esetre kell megítélni, és a jelentés kifejezetten kimondja, hogy a jelenleg általánosan elérhető technológia működése mellett **a promptok önmagukban nem biztosítanak elegendő ellenőrzést**. Ha viszont a szerző saját, védett műve felismerhető a kimenetben, arra megilleti a szerzői jog, ahogyan a kimenetben lévő anyag kreatív kiválogatására, összeállítására vagy elrendezésére, illetve a kimenet kreatív módosításaira is.

Ez a mi helyzetünkben leginkább a szellemitulajdon-nyilvántartás szempontjából érdekes: a projekt kimenetének egy része valószínűleg nem áll szerzői jogi védelem alatt, ami belső rendszernél nem kockázat, de tudni kell róla.

A gyakorlatban ennél sürgetőbb a **licenckeveredés** kérdése. Yang, He és Zhou 67 projekt szabályzatait elemző munkája (S-24) azt mutatja, hogy a nyílt forrású közösségek egy része eredet- és licencalapon utasítja el az AI-generált hozzájárulásokat, mások az AI-használat közlését és a hozzájárulóra terhelt elszámoltathatósági feltételeket írják elő, megint mások repozitóriumszintű utasításokkal (például AGENTS.md-vel) korlátozzák magát az ügynököt. A szerzők három irányultságot és tizenkét kormányzási stratégiát azonosítanak, és azt a következtetést vonják le, hogy a GenAI kormányzása jóval túlmutat a tiltás kérdésén: összehangolt választ kíván az **elszámoltathatóság, a verifikáció, a review-kapacitás, a kóderedet és a platforminfrastruktúra** területén.

Az általánosan visszatérő elv az, hogy a hozzájáruló felel a redisztribúciós jogokért, a licenckompatibilitásért és a jogszerű eredetért — vagyis **a felelősség azon a személyen marad, aki a kódot benyújtja**, nem az eszközön, amellyel készült.

### Az operatív korlátozás eszközei

Arra a kérdésre, hogy „hogyan akadályozzuk meg, hogy az AI túllépjen a határokon", a kiindulópontot az OWASP ügynöki fenyegetéslistája adja (S-13, részletesen az 5. dokumentumban), amely az azonosság- és jogosultsági visszaélést, valamint az eszközök visszaélésszerű használatát a három legfontosabb ügynöki kockázat közé sorolja. Ebből az következik, hogy a legerősebb védelem a jogosultság szűkítése: amit az ügynök nem tud megtenni, azt nem is teheti meg tévedésből vagy eltérítés hatására. Ezt egészíti ki a repozitóriumszintű utasításfájlok gyakorlata (S-25, S-31), amely a korlátokat a kódbázisban, verziókövetve rögzíti — ez azonban puha korlát, mert az utasítás nem kikényszerített, hanem követendő szöveg.

## Negatív tapasztalatok és buktatók

Az első buktató a **felelősségi lánc elmosódása**. Ha egy hibás kódot ügynök írt, ügynök nézett át, és ügynök tesztelt (ami a 3. dokumentum adatai szerint az ügynöki pull requestek 58,77 százalékánál a review oldalán így is van, S-05), akkor a hiba beazonosítható emberi döntési pont nélkül jut ki. Jogilag ez nem menti a szervezetet, de gyakorlatilag lehetetlenné teszi a tanulást.

A második buktató a **licenc- és eredetkockázat láthatatlansága**. Az AI által javasolt kódrészletnek nincs kísérő eredetinformációja, tehát ha nem építünk be automatizált licencellenőrzést, nem is fogjuk tudni, hogy probléma van.

A harmadik buktató az **AI-jártassági kötelezettség figyelmen kívül hagyása** (S-22). Ez egy csendes megfelelési hiányosság: nincs, aki számonkérje egy belső pilotnál, de a szervezet szintjén már 2025 februárja óta fennáll.

A negyedik buktató az **átadási szakadék**. Ha az üzemeltetést átvevő csapat olyan kódot kap, amelyet nem ember írt és nem ember értett meg részleteiben, akkor az incidenskezelés első lépése a kód megértése lesz — pontosan akkor, amikor erre a legkevesebb idő van.

## Mit jelent ez a mi projektünkre

### Ki vállal felelősséget?

A kutatás alapján a válasz egyértelmű: **a kódot benyújtó és jóváhagyó ember**. Ez a nyílt forrású gyakorlat kialakult álláspontja (S-24), és összhangban van a szabályozás irányával, amely szerint az AI-t üzembe helyező viseli a kimenetért a felelősséget. Az ügynök nem jogalany, nem lehet felelős, és nem lehet „hibáztatható" a retrospektíven sem.

Ebből konkrétan az következik, hogy **minden beolvasztott változtatásnak legyen megnevezett emberi jóváhagyója**, és ez a nyom maradjon fenn a verziókezelőben. A pilot során ez a legolcsóbb és leghatásosabb egyetlen intézkedés.

### Mit szabad az ügynöknek?

Javaslatunk egy háromszintű jogosultsági modell, amelyet a csapatindító dokumentumban kell rögzíteni:

1. **Szabadon, jóváhagyás nélkül:** olvasás, elemzés, tesztfuttatás elkülönített környezetben, javaslat készítése.
2. **Emberi jóváhagyással:** új függőség behozatala, sémamódosítás, konfigurációváltoztatás, bármi, ami az éles rendszert érinti.
3. **Tiltott:** hozzáférés éles adathoz és titkokhoz, külső szolgáltatásba írás, jogosultság- és biztonsági beállítás módosítása, a naplózás kikapcsolása.

### Az átadás és a hibaelhárítás

A brief kérdésére — miben változik az átadás — a válasz az, hogy **az átadás tárgya bővül**. A hagyományos csomag (kód, dokumentáció, üzemeltetési leírás) mellé bekerül:

- az ügynökök konfigurációja és a szabályfájlok, mert ezek nélkül a rendszer nem karbantartható ugyanúgy;
- a jóváhagyási nyomvonal, vagyis hogy melyik változtatást ki hagyta jóvá;
- a felhasznált modellek és eszközök jegyzéke, verzióval;
- a licenc- és eredetellenőrzés eredménye.

A hibaelhárítás felelősségére nézve **a rétegzett modellt javasoljuk**: az első szintű diagnosztikát (naplógyűjtés, hibareprodukció, hipotézisállítás) végezheti ügynök, de a **javítás jóváhagyása és az éles beavatkozás emberi döntés marad**. Ennek nemcsak jogi, hanem gyakorlati oka is van: éles incidens közben a legrosszabb pillanat kideríteni, hogy egy ügynök helytelenül zárta le a vizsgálatot (vö. a MAST korai lezárási hibamódjával, S-10).

## Nyitott kérdések

Nem találtunk jogi elemzést arról, hogy a **belső, nem forgalomba hozott** szoftverre az új termékfelelősségi rezsim pontosan hogyan vonatkozik — ez a szakmai kérdés a tagállami átültetés után válik majd megválaszolhatóvá. Szintén nyitott, hogy az AI-jártassági kötelezettség teljesítéséhez milyen dokumentáció elegendő; a rendelet „megfelelő szintet" ír elő, konkrét mércét nem. Végül nincs kialakult gyakorlat arra, hogyan kell az AI-val készült kód eredetét nyomon követni olyan mélységben, amely egy jogvitában bizonyító erejű lenne.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-21 | EU mesterségesintelligencia-rendelet — végrehajtási idővonal | A |
| S-22 | EU AI Act 4. cikk — AI-jártasság, alkalmazandó 2025-02-02-től | A |
| S-23 | ISO/IEC 42001:2023 — mesterségesintelligencia-irányítási rendszer | A |
| S-24 | Yang, He, Zhou: *To Ban or not to Ban?*, arXiv:2603.26487v2 | A |
| S-33 | U.S. Copyright Office: *Copyright and Artificial Intelligence, Part 2: Copyrightability*, 2025-01-29 | A |
| S-37 | (EU) 2024/2853 irányelv a hibás termékekért való felelősségről, átültetési határidő 2026-12-09 | A |
| S-13 | OWASP: *Top 10 for Agentic Applications*, 2025-12-09 | B |
| S-05 | Duma és mtsai: *These Aren't the Reviews You're Looking For*, EASE 2026 | A |
| S-10 | *Why Do Multi-Agent LLM Systems Fail?* (MAST), arXiv:2503.13657 | A |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
