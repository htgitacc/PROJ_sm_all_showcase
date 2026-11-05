# 4. Mérés — mit nézünk, ki mondja meg, hogy jó, és mit nem mérünk

> A jelölésről: `S-nn` hivatkozás mögött kutatási forrás áll ([kutatas/forrasok.md](../kutatas/forrasok.md)); ahol nincs hivatkozás, ott saját tervezési döntésről van szó, és a szöveg ezt kimondja.

## Miért kell a mérést a modell részeként megtervezni

Egy pilotnál kísértés a mérést a végére hagyni, aztán elmesélni, hogy jól ment. A kutatás két különböző irányból mutatja meg, hogy ez itt miért nem járható út.

Az egyik a METR randomizált kontrollált kísérlete, amelyben tapasztalt fejlesztők tizenkilenc százalékkal lassabbak lettek AI-val, miközben előzetesen huszonnégy százalékos gyorsulásra számítottak, és a kísérlet **után is** húsz százalékos gyorsulást éltek meg (S-01). Vagyis a résztvevők nem tudták megítélni a saját termelékenységüket, és a tévedés iránya kiszámítható volt. Ha tehát a pilot értékelése a csapat érzetén alapul, sikeresnek fogjuk nyilvánítani akkor is, ha nem az.

A másik a vállalati AI-projektek kudarcairól szóló, sokat idézett jelentés, amely szerint a pilotok kilencvenöt százaléka nem hozott mérhető eredményhatást — ezt a számot ugyan módszertani kritika érte, mert szűk sikerdefiníción és kis mintán alapult (S-32), de a mögötte lévő tanulság a kritikával együtt is áll: a pilotok jellemzően nem azért buknak el, mert a technológia nem működik, hanem mert a siker kritériumát nem rögzítették előre.

Ebből következik a modell mérési alapelve: **minden mérőszámot azelőtt kell rögzíteni, hogy az első iteráció elindulna, és minden feltevéshez tartoznia kell egy mérésnek, amely eldönti a sorsát.**

## Amit megtartunk a hagyományos mérésből

A DORA négy kulcsmutatója — a szállítási gyakoriság, a változtatás átfutási ideje, a változtatási hibaarány és a helyreállítási idő — érvényes marad, és ennek nagyon konkrét oka van: ezek **nem az emberi erőfeszítést mérik, hanem a rendszer viselkedését**, ezért nem torzulnak attól, hogy gép vagy ember írta a kódot.

Ezen belül a két stabilitási mutató, a hibaarány és a helyreállítási idő, a modell szempontjából fontosabb, mint a két sebességi. A DORA 2025-ös felmérése szerint ugyanis az AI-adopció pozitívan korrelál az átbocsátással, de továbbra is negatívan a szállítási stabilitással (S-02). Aki csak az első kettőt nézi, javulást fog látni ott is, ahol valójában adósságot halmoz.

Megtartjuk az **innovációs arányt** is, vagyis azt, hogy a munka hány százaléka megy új képesség létrehozására a karbantartás és a javítás helyett (S-29). Ez a mutató arra a kérdésre válaszol, hogy értéket szállítunk-e vagy csak aktivitást termelünk — vagyis ez az „AI-színház" mérőszáma (S-28).

## Amit elengedünk

### A story pont

A brief kérdése az, hogy van-e értelme story pontozni, ha a feladat komplex marad, de az ügynök mindennel gyorsabban végez. A válasz az, hogy **ügynöki munkára nincs, emberi munkára viszont továbbra is lehet.**

A story pont emberi ráfordítást, kognitív terhelést, kockázatot és bizonytalanságot fejez ki együtt. Egy fáradhatatlanul dolgozó ügynök ezeket nem éli át, tehát a becslés nem mér semmit; Saini éppen ezért nevezi hibának az ügynökök story pontozását, és helyette a számítási költséget, a tokenfelhasználást és az emberi validálási időt javasolja (S-11).

Az „ügynök számára nehéz-e" kérdésre őszintén azt kell mondani, hogy **erre nem találtunk használható mérőszámot**. A tokenköltség a ráfordítást méri, nem a nehézséget; a futásidő ugyanígy. Ami közelít hozzá, az a *következmény* mérése: ha egy feladatnál az ügynök több körben nem tudta teljesíteni az elfogadási feltételt, vagy ha az elem szokatlanul sok bírálati kört igényelt, akkor az utólag nehéznek bizonyult. Ez visszatekintő mutató, tervezésre nem alkalmas, de a darabolás javítására igen.

Az emberi munkára — az architektúradöntésekre, a bírálatra, a specifikációk átnézésére — a ráfordítás becslése továbbra is értelmes, mert ott valódi kognitív terhelés van. Ezt viszont nem story pontban, hanem közvetlenül **időben** érdemes kifejezni, mert a bírálati keret is időalapú.

### A velocity

A sebesség mint teljesítménymutató elveszíti az értelmét, mert a nevezője — az ügynökök kapacitása — gyakorlatilag korlátlan. Helyette az áramlás mutatói lépnek be: az átfutási idő, a sor hossza és kora, valamint a folyamatban lévő munka mennyisége.

### A lefedettségi küszöb

Ennek indoklása a [02-minosegi-kapuk.md](02-minosegi-kapuk.md) dokumentumban szerepel. Mérőszámként megtartjuk, kapuként nem: tájékoztató adat marad, amelynek hirtelen esése jelzésértékű, de nem lehet cél.

## Amit bevezetünk

Az alábbi mutatók a modell saját mérőszámai. Ezek adják egyben az SM-felület adatalapját is, amelyet a [08-sm-felulet-specifikacio.md](08-sm-felulet-specifikacio.md) részletez.

| Mérőszám | Mit mond meg | Miért kell | Forrás |
|---|---|---|---|
| **Emberi bírálati arány** | a beolvadt elemek hány százalékát nézte át ténylegesen ember | ez az egyetlen mutató, amely megmondja, hogy a modell működik-e, vagy csak papíron létezik | S-05 |
| **Bírálati sor hossza és kora** | hány elem vár, és mióta a legrégebbi | a torlódás legkorábbi jelzése | S-06, S-28 |
| **Emberi validálási idő elemenként** (`t`) | mennyi ideig tart egy érdemi átnézés | ez a kapacitásszámítás bemenete | S-11 |
| **Napi bírálati idő szeniorra** (`R`) | mennyi idő jut ténylegesen bírálatra | ugyanaz | — |
| **Javítási körök átlaga** (`r`) | hányszor megy vissza egy elem | ugyanaz | — |
| **Első körös elfogadási arány** | hány elem megy át javítás nélkül | az ügynökök minőségének legjobb egyszámos jelzése | S-06 |
| **Változtatás mérete** | sor per beolvadt elem, eloszlással | a nagy csomag rontja az elbírálás minőségét | S-06 |
| **Duplikációs és refaktorálási arány** | a kódbázis szerkezeti állapota | a karbantarthatóság romlásának egyetlen korai jelzése | S-03, S-04 |
| **Mutációs pontszám a magas kockázatú modulokon** | a regressziós védőháló ereje | mert a lefedettség nem méri a tesztek erejét | S-16, S-35 |
| **Hibaosztály-eloszlás ügynökönként** | ki milyen típusú hibát vét ismételten | ez a tanulási hurok visszacsatolása | S-10, S-26 |
| **Szabályfájl növekedése és visszaesések** | beépült-e a visszajelzés | a retro gépi rétegének bizonyítéka | S-26 |
| **Token- és pénzköltség iterációnként** | mennyibe kerül a felállás | mert a többügynökös működés érzékelhető szorzót jelent | S-08, S-36 |

A táblázat első sorát érdemes külön kiemelni. A kutatás legfontosabb egyedi felismerése az volt, hogy az ügynöki pull requesteknél az emberi hozzászólások negyede már nem elbírálás, hanem a gép utasítgatása (S-05) — vagyis a klasszikus „hány review történt" mutató nem az emberi felügyeletet méri. Ezért a modell **külön tartja számon az emberi és a gépi bírálatot**, és a beolvasztás jóváhagyójának nevét külön adatként kezeli.

## Az AI-ra szabott mérés három dimenziója

A fenti mutatók rendezéséhez a DX keretrendszerének felosztását vesszük át, amely kihasználtságra, hatásra és költségre bontja a kérdést (S-36).

A **kihasználtság** azt mondja meg, hogy egyáltalán használjuk-e a rendszert: hány feladat megy ügynökhöz, a beolvadt kód mekkora része származik ügynöktől. Ez a legkönnyebben mérhető és a legkevesebbet mondó dimenzió.

A **hatás** az, ahol a valódi jelzések vannak, és ahol a szervezetek jellemzően alulmérnek. Ide tartoznak a DORA-mutatók, a szerkezeti mutatók és az átfutási idő alakulása.

A **költség** a fejlesztőnkénti AI-kiadás és a nettó időnyereség, vagyis a megtakarítás mínusz a ráfordítás. Ez a dimenzió a pilotnál azért fontos, mert a többügynökös felállás a mérések szerint három-tízszeres tokenhasználatot jelent az együgynökössel szemben (S-08), és ez pénzben is megjelenik.

A keretrendszer két figyelmeztetése közvetlenül ránk is áll. Az egyik, hogy **a magas kihasználtság együtt élhet alacsony vagy negatív hatással** — vagyis az első dimenzió sikere önmagában semmit nem bizonyít. A másik, hogy ezek a mutatók nem alkalmasak egyéni teljesítményértékelésre, és különösen a kódgenerálási mennyiség az, amit könnyű meghamisítani (S-36).

## Ki mondja meg, hogy mi a jó?

Ez a brief legfilozofikusabb kérdése, és a kutatásból három, egymástól élesen elváló szint adódik. A leggyakoribb hiba az, hogy ezeket összekeverik.

Az első szint az **elfogadhatóság**, vagyis hogy egy elem kész-e. Ezt ember határozza meg, és ez a Definition of Done. Az ügynök nem dönthet arról, hogy a saját munkája kész-e — ezt egyfelől a MAST korai lezárási hibamódja indokolja (S-10), másfelől a gyártói útmutató „korai győzelem" figyelmeztetése (S-08).

A második szint a **megfelelés**, vagyis hogy egy elem teljesíti-e az elfogadhatóság feltételeit. Ezt lehetőleg gép ellenőrizze, determinisztikusan. Ami automatizálható, azt nem szabad emberi ítéletre bízni, mert az emberi ítélet a szűkös erőforrás.

A harmadik szint az **érték**, vagyis hogy amit csinálunk, egyáltalán érdemes-e. Ezt a Product Owner ítéli meg, és nem automatizálható. Ez az az elszámoltathatóság, amely a szakirodalom szerint elvi okból marad emberi (S-11), és amelyet a kutatás azzal is alátámaszt, hogy az ember–AI páros ítéleti feladatokban alulteljesíthet (S-19).

A Scrum Master feladata ebben nem az, hogy ő döntse el, mi a jó, hanem hogy **a három szint ne csússzon össze**, és hogy a mérés ne váljon egyéni teljesítményértékeléssé.

## A pilot mérési terve

A mérés két, egymástól elkülönülő célt szolgál, és ezt érdemes szétválasztani, mert máskülönben a napi működés adatai összekeverednek a kísérleti adatokkal.

Az első cél a **modell paramétereinek kalibrálása**. A [00-mukodesi-modell.md](00-mukodesi-modell.md) három paramétere — a napi bírálati idő, az elemenkénti validálási idő és a javítási körök átlaga — feltevés, és az első két iterációnak elsősorban az a dolga, hogy ezeket valós adatra cserélje. Ha bármelyik jelentősen eltér, akkor az iterációhosszt és a folyamatban lévő munka korlátait újra kell szabni.

A második cél a **pilot sikerének megítélése**. Erre a kritériumokat előre rögzítjük, és a [09-kockazatok-es-kilepes.md](09-kockazatok-es-kilepes.md) dokumentum tartalmazza őket, mert ott találkoznak a kilépési feltétellel.

Az adatgyűjtés módjáról egy megjegyzés kívánkozik ide. A bírálati idő és a napi bírálati kapacitás mérése óhatatlanul megfigyelési nyomást gyakorol a fejlesztőkre, és ez torzíthatja is az adatot. Ezért a mérésnek **csapatszinten aggregáltan** kell történnie, egyéni bontás nélkül, és ezt a csapatindító dokumentumban ki kell mondani. Ez **saját döntés**, de összhangban van azzal a figyelmeztetéssel, hogy ezek a mutatók nem valók egyéni értékelésre (S-36).

## Amit szándékosan nem mérünk

Nem mérünk kódsort, commitszámot és pull request-darabszámot teljesítménymutatóként. Ezek AI-korban triviálisan növelhetők, tehát célként kitűzve azonnal értelmüket vesztik, és a kutatás kifejezetten a kódgenerálási mennyiséget nevezi meg a leginkább manipulálható mutatóként (S-36).

Nem mérünk ügynökök közötti „teljesítménysorrendet" sem. Az ügynök nem munkavállaló, a hibája nem fegyelmi ügy, hanem konfigurációs kérdés — a MAST szerint a többügynökös rendszerek hibáinak 43,8 százaléka rendszertervezési eredetű (S-10). Ami helyette számít, az a hibaosztály-eloszlás, mert az javítható.

És nem mérünk önbevallásos sebességet. Az elégedettség és a terhelés önbevallása értékes és megtartandó (S-29), de a *gyorsulás* önbevallása a METR eredménye alapján bizonyítottan félrevezető (S-01).

## Nyitott kérdések

Nem tudjuk, mely mutató jelzi előre a legjobban a pilot hosszú távú sikerét — erre az irodalomban nincs válasz, és a pilot maga sem fogja megnyugtatóan eldönteni ilyen rövid idő alatt. Nem tudjuk, hogy az emberi validálási idő mérhető-e megbízhatóan anélkül, hogy a mérés maga megváltoztatná a mért viselkedést. És nem tudjuk, hogy a szerkezeti mutatók — a duplikáció és a refaktorálási arány — néhány iteráció alatt egyáltalán elmozdulnak-e annyira, hogy a jelzés kiemelkedjen a zajból; a hivatkozott ipari mérések évekre visszamenő adatsorokon dolgoztak (S-03, S-04).
