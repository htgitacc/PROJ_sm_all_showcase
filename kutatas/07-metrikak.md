# 7. Mérőszámok — mit tartsunk meg, mit vezessünk be, és ki mondja meg, mi a jó

## Mit kerestünk

A brief négy kérdést tesz fel: mit mérünk és hogyan, mi változik a hagyományos Scrum-méréshez képest, ki határozza meg, hogy mi a jó, és van-e értelme story pontozni, ha az ügynök minden feladattal sokkal gyorsabban végez. Ezért egyrészt a bevett mérési keretrendszereket kerestük, másrészt kifejezetten azt, hogy melyik mérőszám válik **félrevezetővé** ügynökös közegben.

## Mit találtunk

### A meglévő keretrendszerek

A **DORA** négy kulcsmutatója (szállítási gyakoriság, változtatás átfutási ideje, változtatási hibaarány, helyreállítási idő) 2025-ben is érvényes maradt, de a jelentés (S-02) éppen azt mutatja meg, miért nem elég önmagában: az AI-adopció **pozitívan** korrelál az átbocsátással és **negatívan** a stabilitással. Aki csak az első kettőt nézi, javulást lát; aki csak a második kettőt, romlást. A négy mutató együtt olvasva viszont pontosan azt az egyensúlyt írja le, amelyet keresünk.

A **DX Core 4** (S-29) ezt kiegészíti azzal, hogy a DORA, a SPACE és a DevEx kereteit egyesíti négy dimenzióban. A sebességet a fejlesztőnkénti heti beolvasztott pull requestek számával, a hatékonyságot (effectiveness) egy önbevallásos fejlesztői élményindexszel, a minőséget a változtatási hibaaránnyal vagy hibaránnyal, a hatást pedig az innovációs aránnyal — vagyis azzal, hogy az idő vagy a pull requestek hány százaléka megy új képesség létrehozására — méri.

### A kifejezetten AI-ra szabott mérés

A DX AI mérési keretrendszere (S-36) három dimenzióra bontja a kérdést, és ez a felosztás jól illeszkedik a mi helyzetünkhöz:

- **Kihasználtság (utilization):** az AI-eszközök használati aktivitása, az AI-val segített pull requestek aránya, a ténylegesen AI által generált kód aránya, és az ügynököknek kiosztott feladatok száma.
- **Hatás (impact):** közvetlen mérésként az AI-nak tulajdonított időmegtakarítás és a fejlesztői elégedettség; közvetett mérésként a pull request-átbocsátás, a kód karbantarthatósága és a változtatási hibaarány időbeli alakulása.
- **Költség (cost):** fejlesztőnkénti AI-kiadás, nettó időnyereség (megtakarítás mínusz költség), és az ügynökök óradíj jellegű költsége.

A keretrendszer két figyelmeztetést is megfogalmaz, amelyek a mi pilotunkra közvetlenül állnak. Az egyik, hogy **a magas adopció együtt élhet alacsony vagy negatív hatással** — vagyis a kihasználtsági mutatók önmagukban semmit nem bizonyítanak. A másik, hogy a mérőszámok nem alkalmasak egyéni teljesítményértékelésre, és különösen a kódgenerálási mennyiség az, amit könnyű meghamisítani.

### Amit a szakirodalom kifejezetten a story pontokról mond

A brief kérdésére a legkonkrétabb választ Saini adja (S-11): hiba story pontot adni egy ügynöknek, mert a story pont **emberi ráfordítást, kognitív terhelést, kockázatot és bizonytalanságot** mér, márpedig a fáradhatatlanul dolgozó ügynök ezeket nem éli át. Helyette a számítási költséget, a tokenfelhasználást és az **emberi validálási időt** javasolja mérni. A záró gondolata pedig egyenesen tervezési szabály: ha a sprintet az AI generálási sebességére tervezzük, kezelhetetlen torlódást hozunk létre az emberi review-nál.

Ezt egészíti ki Yeret WIP-alapú megközelítése (S-28), amely szerint az áramlás (flow) korlátait kell megtervezni, nem a kapacitást megbecsülni: a valós korlát az emberi review-kapacitás, fejenként nagyjából egy-két párhuzamos elem.

### Miért nem elég a csapat érzete

A METR-kísérlet (S-01) eredménye itt válik mérési kérdéssé. A résztvevők utólag is 20 százalékos gyorsulást éltek meg, miközben 19 százalékkal lassabbak voltak. Ez azt jelenti, hogy **az önbevallásos „gyorsabbak lettünk" adat rendszeresen és nagy mértékben téved**, és a hiba iránya kiszámítható. Ha a pilot értékelése ezen alapul, sikeresnek fogjuk nyilvánítani akkor is, ha nem az.

Ez nem jelenti azt, hogy az önbevallásnak nincs helye — a DX Core 4 hatékonysági dimenziója éppen ilyen (S-29) —, de azt igen, hogy önbevallásos adat nem használható a *sebesség* mérésére.

### Amit a review-oldal mérése hozzátesz

A 3. dokumentum központi tanulsága (S-05) mérési következménnyel is jár: mivel az ügynöki pull requesteknél az emberi hozzászólások negyede már nem elbírálás, hanem ügynökirányítás, a „hány review történt" típusú mutató nem méri az emberi felügyeletet. **Külön kell mérni az emberi és a gépi review-t.**

## Negatív tapasztalatok és buktatók

Az első buktató a **mennyiségi mutatók dominanciája**. Az AI-korszakban a kódsor, a commit és a pull request száma triviálisan növelhető, tehát célként kitűzve azonnal értelmét veszti (S-36). Aki átbocsátásra ösztönöz, azt fogja kapni — a stabilitás rovására (S-02).

A második buktató a **lefedettségi küszöb**, amelyet a 6. dokumentum tárgyal: AI-generált tesztnél a lefedettség és a valódi hibafelderítés között gyenge a kapcsolat (S-16).

A harmadik buktató a **hamis felügyeleti jelzés** (S-05): a review-számok látszólag rendben lehetnek, miközben ember nem nézte át a kódot.

A negyedik buktató az **önbevallás torzítása** (S-01).

Az ötödik buktató a **késleltetett hatás**: a karbantarthatóság romlása (S-04) hónapokkal a pilot után jelentkezik, tehát ha a pilot végén mérünk, semmit nem fogunk látni belőle. Ezt csak folyamatos, szerkezeti mutatókkal (duplikáció, refaktorálási arány) lehet elfogni.

## Mit jelent ez a mi projektünkre

### Amit érdemes megtartani a hagyományos mérésből

A DORA négy mutatója **továbbra is érvényes**, mert nem az emberi erőfeszítést méri, hanem a rendszer viselkedését — és éppen ezért nem torzul attól, hogy gép vagy ember írta a kódot. A hibaarány és a helyreállítási idő különösen fontos, mert ezekben csapódik le az AI stabilitásrontó hatása (S-02).

Megtartandó az **innovációs arány** is (S-29), mert ez válaszol arra a kérdésre, hogy tényleg értéket szállítunk-e, vagy csak aktivitást termelünk — ez Yeret „AI-színház" fogalmának mérőszáma (S-28).

### Amit el kell engedni

A **story pont az ügynöki munkára értelmetlen** (S-11). Ebből viszont nem következik, hogy a becslés egészét el kell dobni: az *emberi* munkára (review, architektúradöntés, validálás) továbbra is hasznos lehet a ráfordítás becslése, mert ott van valódi kognitív terhelés.

A **velocity mint teljesítménymutató** szintén elveszíti az értelmét, mert a nevezője (az ügynök kapacitása) gyakorlatilag korlátlan. Helyette az áramlás mérőszámai jönnek: átfutási idő, sorhossz, folyamatban lévő munka.

### Amit be kell vezetni

A pilothoz a következő, új mérőszámokat javasoljuk. Ezek adják az SM-felület adatalapját is:

| Mérőszám | Miért | Forrás |
|---|---|---|
| **Emberi review-arány** — az elemek hány százalékát nézte át valóban ember | mert a review-szám nem méri a felügyeletet | S-05 |
| **Review-sor hossza és kora** — hány elem vár bírálóra, és mióta | ez a legkorábbi torlódásjelzés | S-06, S-28 |
| **Emberi validálási idő elemenként** | ez a valódi kapacitáskorlát, nem az ügynök sebessége | S-11 |
| **Első körös elfogadási arány** — hány ügynöki elem megy át javítás nélkül | az ügynökök minőségének legjobb egyszámos jelzése | S-06 |
| **Változtatás mérete** (sor/pull request) | mert a nagy csomag rontja a review minőségét | S-06 |
| **Duplikációs és refaktorálási arány** | a karbantarthatóság korai jelzése | S-03, S-04 |
| **Mutációs pontszám a magas kockázatú modulokon** | mert a lefedettség nem méri a tesztek erejét | S-16, S-17 |
| **Ügynökönkénti hibaosztály-eloszlás** — ki milyen típusú hibát vét | ez adja az ügynökjavítás visszacsatolását | S-10, S-26 |
| **Token- és pénzköltség iterációnként** | mert a többügynökös felállás 3–15-szörös szorzót jelent | S-08, S-09, S-36 |

### Ki mondja meg, hogy mi a jó?

Ez a brief legfilozofikusabb kérdése, de a kutatásból adódik rá válasz. Három szint különül el, és keverésük a leggyakoribb hiba:

1. **Az elfogadhatóság kritériumát az ember határozza meg**, és ez a Definition of Done. Az ügynök nem dönthet arról, hogy a saját munkája kész-e — a MAST korai lezárási hibamódja (S-10) és az Anthropic „korai győzelem" figyelmeztetése (S-08) ugyanezt mondja.
2. **A megfelelést lehetőleg gép ellenőrizze**, determinisztikusan: tesztek, statikus elemzés, mutációs küszöb. Ami automatizálható, azt ne emberi ítéletre bízzuk, mert az a szűkös erőforrás.
3. **Az értéket a Product Owner ítéli meg**, és ez nem automatizálható. Saini érvelése szerint ez az egyetlen elszámoltathatóság, amely elvi okból marad emberi (S-11).

A Scrum Master feladata ebben az, hogy a három szint ne csússzon össze, és hogy a mérés ne váljon egyéni teljesítményértékeléssé (S-36).

## Nyitott kérdések

Nem találtunk validált mérőszámot arra, hogy egy **ügynök** teljesítménye hogyan hasonlítható össze egy másikéval a feladat nehézségét is figyelembe véve — a story pont helyére javasolt tokenköltség csak a ráfordítást méri, a nehézséget nem. Szintén nyitott, hogy az emberi validálási idő hogyan mérhető megbízhatóan anélkül, hogy megfigyelési nyomást gyakorolnánk a fejlesztőkre. Végül nincs adatunk arról, hogy a fenti mutatók közül melyik jelzi előre a legjobban a pilot hosszú távú sikerét — ezt a pilot maga fogja megmutatni.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-01 | METR randomizált kontrollált kísérlet, 2025-07-10 | A |
| S-02 | DORA: *State of AI-assisted Software Development 2025* | B |
| S-05 | Duma és mtsai: *These Aren't the Reviews You're Looking For*, EASE 2026 | A |
| S-06 | LinearB: *2026 Software Engineering Benchmarks Report* | B |
| S-11 | Sanjay Saini: *AI Augmented Scrum Framework*, Scrum.org | C |
| S-28 | Yuval Yeret: *Limiting WIP in Scrum with Kanban in the AI Age*, 2026-01-23 | C |
| S-29 | DX: *DX Core 4* keretrendszer | C |
| S-36 | DX: *AI Measurement Framework* | C |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
