# 11. Iterációs ritmus és a Scrum események sorsa

## Mit kerestünk

A brief feltételezése az, hogy a hagyományos kéthetes sprint túl hosszú, mert az ügynökök néhány óra alatt elkészülnek, és a ritmust inkább az szabja meg, mennyi idő alatt tud a szenior átnézni, visszaadni és újra átvenni a kódot. Ezért arra kerestünk bizonyítékot, hogy létezik-e dokumentált gyakorlat a néhány napos iterációra, és hogy mihez érdemes kötni a ciklus hosszát. Emellett összegyűjtöttük, mi történik a Scrum eseményeivel.

## Mit találtunk

### A rövid iterációra nincs dokumentált mérés — de van tervezési elv

Ezt előre kell bocsátani, mert ez a kutatás egyik legfontosabb negatív eredménye: **nem találtunk olyan publikációt vagy mérést, amely a néhány napos iterációt ügynökös csapatban vizsgálta volna.** Ami van, az tervezési elv, nem bizonyíték.

A leghasználhatóbb elv Yeret írásából (S-28) származik, és azt mondja, hogy a ritmust nem naptári megfontolásból, hanem a **valódi szűk keresztmetszetből** kell levezetni. Az ő „gyorsulási ostorcsapás" fogalma azt írja le, hogy a kódgenerálás sokszorosára gyorsul, miközben az emberhez kötött szakaszok — review, tesztelés, validálás — nem skálázódnak vele, tehát a szűk keresztmetszet lefelé tolódik a review-kapuhoz. Ebből következik a konkrét ajánlása: fejenként egy-két párhuzamos elem a reális szám, és a folyamatkorlátokat nem elég csapatszinten megszabni, hanem a Product Ownernek és a fejlesztőknek együtt kell megtervezniük a végponttól végpontig tartó határokat.

Ehhez adja a méréses hátteret a 3. dokumentum: a LinearB adatai (S-06) szerint az AI-generált pull request átlagosan **több mint tizenhat órát vár** bírálóra, míg a segítség nélküli munka mintegy 200 percet — viszont ha a review elkezdődött, az AI-s munka gyorsabban zárul. Tehát a ciklusidőt nem a bírálat hossza, hanem a **sorban állás** uralja.

Ebből egy egyszerű, de fontos következtetés adódik: **egy iterációnak legalább annyi ideig kell tartania, hogy egy teljes kör beleférjen** — kiosztás, ügynöki munka, emberi bírálat, javítás, ismételt bírálat, beolvasztás. Ha az iteráció ennél rövidebb, akkor a végén mindig lesz félkész munka, ami a Scrum értelmében nem inkrementum.

### Mi történik a Scrum eseményekkel

Saini írása (S-11) végigveszi az eseményeket, és a javaslatai koherensek azzal, amit a mérések mutatnak:

**Sprint Planning.** A súlypont a feladatkiosztásra (task attribution) kerül: mely feladatok igényelnek emberi kreativitást, és melyek adhatók automatizált végrehajtásra. Új „kész a kezdésre" feltétel, hogy a backlog-elem nem „Ready", ha az ügynök nem kapja meg a szükséges dokumentációt a promptjában.

**Daily Scrum.** Az ügynökök nem beszélnek az eseményen. Az emberi fejlesztők átnézik az automatikus kimeneti naplókat: mely ügynökök buktak el tesztsorozatot, hol jeleztek alacsony megbízhatóságot. Az esemény jellege **eltéréskezeléssé** alakul.

**Sprint Review.** Az érdekelteket nem érdekli, hogy AI írta-e a funkciót; az érdekli őket, ki felel az eredményért. Egy emberi vezetőnek kell kontextusba helyeznie és bemutatnia az AI által generált kódot, teljes felelősséget vállalva az inkrementum biztonságáért és működéséért.

**Sprint Retrospective.** A visszatekintés kiegészül az ügynöki működés elemzésével: a token- és futásnaplók áttekintésével, az agentikus munkafolyamatok rendszerezett hibakeresésével. Ha egy ügynök nem szállított használható komponenst, a csapatnak a **rendszerpromptot** kell átírnia — vagyis a klasszikus „eszközök és folyamatok" napirendi pont szó szerint a konfiguráció javítását jelenti. Saini külön felhívja a figyelmet arra, hogy a csapatnak beszélnie kell az emberi kimerülésről is, mert a nagy mennyiségű AI-generált kód átnézése mentálisan fárasztó.

Ehhez jön hozzá — és ez a kutatás egyik legerősebb hozzájárulása —, hogy a visszatekintésnek van egy **ellenőrizhető kimenete**: a szabályfájlba felvett új szabályok, és annak nyomon követése, hogy az érintett hibaosztályok eltűnnek-e (S-26, részletesen a 10. dokumentumban). Ez teszi a retrospektívet mérhetővé abban a részében, amely az ügynökökre vonatkozik.

### A specifikáció mint a ciklus kezdőpontja

A specifikáció-vezérelt megközelítés (S-30) önálló, megnevezett lépésekre bontja a munkát az alapelvek rögzítésétől a specifikáción, a technikai terven és a feladatokra bontáson át a megvalósításig. A mi szempontunkból ez azért érdekes, mert **explicit ellenőrzési pontot tesz a darabolás után és a kódolás előtt** — vagyis egy olyan helyre, ahol az emberi bírálat sokkal olcsóbb, mint a kód szintjén. Ha a specifikáció rossz, azt egy oldal elolvasásával ki lehet szűrni; ha a belőle generált négyszáz sor rossz, azt csak négyszáz sor elolvasásával.

Ez közvetlenül enyhíti a review-torlódást is, mert a hibák egy részét a folyamat olcsó szakaszában fogja ki. A 3. dokumentum adatai (S-06) szerint az AI-s pull requestek a 75. percentilisen 400 sor fölöttiek — egy elfogadott specifikáció ennél nagyságrenddel gyorsabban elbírálható.

## Negatív tapasztalatok és buktatók

Az első buktató a **túl rövid iteráció**. Ha a ciklus rövidebb, mint egy teljes review-kör, akkor minden iteráció félkész munkával zárul, a torlódás pedig görgetődik. A brief feltételezése (három–öt nap) valószínűleg helyes irány, de a hosszt méréssel kell megerősíteni, nem előre kimondani.

A második buktató a **ceremóniák elszaporodása**. Rövidebb iterációnál ugyanaz az eseménykészlet arányaiban sokkal több időt eszik. Ha egy háromnapos iterációba beleteszünk egy tervezést, egy demót és egy visszatekintést, akkor a munkaidő jelentős része eseményekre megy. Erre nem találtunk kész választ az irodalomban; ez tervezési döntés lesz.

A harmadik buktató az **AI-színház** (S-28): magas aktivitás alacsony értékű, nem validált munkán. Ez rövid iterációknál nehezebben vehető észre, mert a gyors ciklus önmagában is a haladás érzetét kelti.

A negyedik buktató a **felfelé irányuló kiéheztetés** (S-28): ha nincs elég kész, validált munka, a csapat alacsony prioritású elemeket húz be, csak hogy dolgozzon. Ügynökös csapatnál ez különösen valószínű, mert az ügynökök kapacitása gyakorlatilag korlátlan, tehát mindig lesz szabad kéz.

Az ötödik buktató, hogy **a demónál az AI-ötletek beépítésének nincs kiforrott gyakorlata**. A brief kifejezetten kérdezi, hogy az AI is megfogalmazhat-e fejlesztési ötletet; erre az irodalomban nem találtunk sem támogató, sem cáfoló bizonyítékot. Amit tudunk (S-19), az az, hogy az ember–AI csapat **alkotó** feladatokban jól teljesít, **ítéleti** feladatokban viszont alulteljesíthet — vagyis ötletet generáltatni ésszerű, a rangsorolást viszont emberre kell hagyni.

## Mit jelent ez a mi projektünkre

### Az iteráció hossza

Javaslatunk, hogy az iterációhosszt **ne kimondjuk, hanem levezessük**. A pilot első két iterációjában mérjük meg, mennyi idő telik el egy elem kiosztásától a beolvasztásáig, majd az iterációt ennek a ciklusidőnek a másfél-kétszeresére állítsuk be, hogy a javítási kör is beleférjen. A rendelkezésre álló adatok (S-06) alapján a **három-öt napos iteráció valószínűleg reális**, de ez becslés, nem mérés.

Amit biztosan tudunk: az iteráció **átbocsátóképessége** nem az ügynökök számától függ, hanem attól, hány elemet tud két szenior érdemben átnézni. Ez a szám a tervezés kiindulópontja.

### Az események átalakítása

A kutatás alapján a következő eseménykészletet javasoljuk megfontolásra. A hangsúly azon van, hogy **mindegyik eseménynek legyen olyan kimenete, amely ellenőrizhető**:

| Esemény | Gyakoriság | Mi a célja | Ellenőrizhető kimenete |
|---|---|---|---|
| **Iterációtervezés** | iteráció elején | feladatkiosztás ember és ügynök között, a WIP-korlát meghatározása | kiosztott elemek listája, ügynökönként megadott kontextussal |
| **Napi eltéréskezelés** | naponta, rövid | nem státusz, hanem kivételek: bukott tesztek, torlódó review-sor, kifutó ügynökök | döntés arról, mit állítunk le és mit engedünk tovább |
| **Review-blokk** *(új esemény)* | naponta fix idősáv | a szeniorok védett ideje a bírálatra | az aznapi review-sor leapasztása |
| **Iterációs bemutató** | iteráció végén | értékbemutatás, emberi felelősségvállalás az inkrementumért | a bemutató mögött megnevezett emberi jóváhagyó |
| **Visszatekintés (két rétegben)** | iteráció végén | emberi együttműködés + ügynökpark hangolása | **új szabályok a szabályfájlban**, és a hibaosztályok követése |

A **review-blokk** azért javaslat, mert a kutatás legkonzisztensebb megállapítása az, hogy a review a szűk keresztmetszet (S-05, S-06, S-24, S-28). Ha ez nem kap védett időt a naptárban, akkor a nap végén marad, és így torlódik.

A **visszatekintés kettéválasztása** azért fontos, mert a két réteg más logikát követ: az emberi réteg klasszikus csapatdinamikai eszközöket kíván (lásd a 8. dokumentumot), az ügynöki réteg pedig konfigurációs hibakeresést és szabályírást (S-11, S-26).

### Az AI bevonása az eseményekbe

A brief kérdésére — bevonhatók-e az ügynökök, például rendszeres jelentéssel — a kutatásból az alábbi válasz adódik:

- **Igen, jelentésként.** Az ügynökök outputnaplói, elfogadási arányai és hibaosztályai adják a napi eltéréskezelés és a visszatekintés adatalapját (S-11).
- **Igen, ötletgenerálásként.** A demón megfogalmazott fejlesztési ötletekhez az ügynök hozzájárulhat, mert ez alkotó feladat (S-19, S-20).
- **Nem, döntéshozóként.** A rangsorolás és az elfogadhatóság megítélése ítéleti feladat, ahol az irodalom negatív szinergiát jelez (S-19), és ahol a felelősség jogilag is emberi (lásd a 9. dokumentumot).
- **A visszajelzés beépülése ellenőrizhető** a szabályfájl és a hibaosztályok követésével (S-26).

## Nyitott kérdések

A legnagyobb hiány, hogy **nincs publikált mérés a rövid iterációra ügynökös csapatban**. A három-öt napos javaslat tervezési logikából következik, nem adatból. Szintén nyitott, hogyan kell az eseményeket rövid iterációnál arányosítani, hogy ne egyék meg a munkaidőt. Végül nem találtunk gyakorlatot arra, hogyan lehet az ügynökök „jelentését" úgy strukturálni, hogy ne váljon zajjá — a jelenlegi eszközök sok naplót termelnek, de kevés döntéstámogató összegzést.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-28 | Yuval Yeret: *Limiting WIP in Scrum with Kanban in the AI Age*, 2026-01-23 | C |
| S-11 | Sanjay Saini: *AI Augmented Scrum Framework*, Scrum.org, 2026-03-08 | C |
| S-06 | LinearB: *2026 Software Engineering Benchmarks Report* | B |
| S-05 | Duma és mtsai: *These Aren't the Reviews You're Looking For*, EASE 2026 | A |
| S-19 | Tong: *From Augmentation to Symbiosis*, arXiv:2601.06030 | A |
| S-20 | Dell'Acqua és mtsai: *The Cybernetic Teammate* | A |
| S-24 | Yang, He, Zhou: *To Ban or not to Ban?*, arXiv:2603.26487v2 | A |
| S-26 | Aggarwal, Ghalaty: *Self-Improving AI Coding Agents*, arXiv:2607.13091 | B |
| S-30 | GitHub Spec Kit | C |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
