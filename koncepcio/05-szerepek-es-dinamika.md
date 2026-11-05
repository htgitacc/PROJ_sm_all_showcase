# 5. Szerepek, eszkaláció és csapatdinamika

> A jelölésről: `S-nn` hivatkozás mögött kutatási forrás áll ([kutatas/forrasok.md](../kutatas/forrasok.md)); ahol nincs hivatkozás, ott saját tervezési döntésről van szó, és a szöveg ezt kimondja.

## A szerepek átalakulásának logikája

A szerepek változását könnyű úgy leírni, hogy „mindenki magasabb szintre kerül", de ez a megfogalmazás semmit nem mond. Pontosabb így fogalmazni: **az ügynökök elveszik a mechanikus munkát, és cserébe új felügyeleti munkát adnak.** A csere nem automatikusan előnyös, és a modell akkor működik, ha az új felügyeleti munkát valaki ténylegesen elvégzi — ha nem, akkor a mechanikus munka eltűnik, a felügyelet pedig egyszerűen elmarad. A kutatás szerint pontosan ez történt a nyílt forrású világban, ahol az ügynöki hozzájárulások nyolcvannégy százaléka emberi elbírálás nélkül jutott át (S-05).

## Product Owner

A Product Owner átadja a **megfogalmazás mechanikáját**: a felhasználói történetek szövegezését, az elfogadási feltételek első vázlatát, a technikai bontást és a háttérkutatást. Ez az a munka, amely ma az idejének nagy részét eszi.

Nem adja át a **sorrendet és az elfogadhatóságot**. A termékfelelősség — a felhasználói empátia, az érdekeltek közötti egyeztetés és az üzleti illesztés — a szakirodalom szerint elvi okból marad emberi (S-11), és ezt megerősíti az a kutatási eredmény is, amely szerint az ember–AI páros ítéleti és döntési feladatokban negatív együttműködési hozamot mutathat, miközben alkotó feladatokban pozitívat (S-19).

Új feladata viszont keletkezik, és ez a modell egyik legfontosabb újdonsága: **a Product Owner a jóváhagyási kapunál áll.** Nem ő írja a darabolást, de ő mondja ki, hogy a darabolás lefedi-e a specifikációt. Ez időben kevesebb munka, mint a szövegezés, de sűrűbb figyelmet igényel, és — ez a lényeges — **a bírálati keretből fogyaszt**, tehát a tervezésnél számolni kell vele.

## Szenior fejlesztők

A szenior fejlesztők szerepe alakul át a legmélyebben. A kutatásban használt megfogalmazás szerint „ügynök-karmesterré" válnak, akiknek elsődleges feladata az ügynökök által előállított logika validálása, miközben az emberi elszámoltathatóság nem delegálható (S-11).

A gyakorlatban a munkájuk három részre bomlik. Az első a **bírálat**, amely a modell szűk keresztmetszete, és amelyre a védett idősáv szolgál. A második az **ügynökök megírása és hangolása** — a szabályfájlok karbantartása, az eszközök korlátozása, a kontextus összeállítása. A harmadik az **architekturális felügyelet**: annak biztosítása, hogy a lokális ügynöki optimalizálások ne bontsák meg a rendszer egészét (S-11).

Ebben a felállásban komoly kockázat, hogy a bírálat felemészti az idejüket, és a másik két feladatra nem marad kapacitás. A modell ezt azzal kezeli, hogy a napi bírálati időt paraméterként rögzíti — a kiinduló feltevés szerint napi három óra —, és nem engedi, hogy ez korlátlanul nőjön: ha a sor nem apad, akkor nem több bírálat kell, hanem kevesebb bejövő munka.

## Scrum Master

Mivel a brief elsősorban a Scrum Master nézőpontjából kérdez, ez a szerep megérdemel egy részletesebb kifejtést.

### Amit kiadhat a kezéből

A Scrum Master átadhatja az **adatgyűjtést és a státuszriportolást**. Egy olyan csapatban, ahol az ügynökök tevékenységéről automatikus napló készül, és ahol a [04-meres.md](04-meres.md) mutatói folyamatosan rendelkezésre állnak, a haladás összefoglalása gépi feladat. Ugyanígy átadható a napi eltéréslista összeállítása: a bukott kapuk, a torlódó elemek és a méretkorlátot túllépő változtatások összegyűjtése automatizálható.

### Ami újként keletkezik

A Scrum Masternek öt olyan feladata jön be, amely a hagyományos szerepben nem létezik.

Az első az, hogy **az akadály immár algoritmikus is lehet**. Saini megfogalmazása szerint a Scrum Masternek figyelnie kell a rendszernaplókat és az erőforráskorlátokat, hogy az ügynökök ne akadjanak el (S-11). Ez első hallásra technikai feladatnak tűnik, valójában azonban ugyanaz az akadályelhárítás, mint eddig, csak a lista bővült.

A második a **kapuk formálissá válásának megelőzése**. A modell minden ereje a minőségi kapukban van, és ezek a kapuk lassan, észrevétlenül elvesztik a funkciójukat, ha jól működnek: formálissá válnak, és onnantól csak azt a látszatot keltik, mintha valóban működnének. Ha a jóváhagyási kapunál hetek óta nem utasítottak vissza semmit, az nem siker, hanem gyanús. Ez a Scrum Master egyik legfontosabb új figyelési feladata, és **saját javaslat**: a kutatás nem ír le ilyen gyakorlatot, de a mért elcsúszás (S-05) ellen ez a legolcsóbb védekezés.

A harmadik a **bírálati terhelés eloszlásának figyelése**. Ha az egyik szenior aránytalanul többet bírál, az nemcsak kapacitásprobléma, hanem kiégési kockázat is: a nagy mennyiségű AI-generált kód átnézése mentálisan kimerítő (S-11), a DORA felmérése pedig a leggyengébb csapatprofilnál együtt említi a magas instabilitást és a kiégést (S-02).

A negyedik a **tanulási hurok fenntartása**. A visszatekintés gépi rétegének kötelező kimenete van, és a Scrum Master felel azért, hogy ez ne maradjon el, valamint azért, hogy a következő iterációkban visszamérjük, eltűnt-e az érintett hibaosztály ([03-esemenyek-es-tanulas.md](03-esemenyek-es-tanulas.md)).

Az ötödik az **AI-jártasság**. Ez nem szakmai ajánlás, hanem jogi kötelezettség: az EU mesterségesintelligencia-rendeletének 4. cikke 2025. február 2. óta alkalmazandó, és megköveteli, hogy a szervezet gondoskodjon a személyzete megfelelő szintű AI-jártasságáról (S-22). A Scrum Master az a szerep, amelyhez ez természetesen illeszkedik, mert a csapat képességfejlesztése eddig is hozzá tartozott.

### Amit nem vesz át

Nem lesz belőle az ügynökök üzemeltetője. Az ügynökök megírása, hangolása és javítása a szenior fejlesztők dolga; a Scrum Master azt figyeli, hogy a probléma **látható és napirenden** legyen, nem azt oldja meg.

## Ha egy ügynök sokat hibázik

A brief konkrétan kérdezi, hogy ilyenkor a Scrum Master eszkalálja-e a problémát a szenior fejlesztő felé. A kutatásból egy ennél árnyaltabb válasz adódik, és ez a modell egyik legfontosabb átkeretezése.

A kiindulópont az, hogy **az ügynök hibája nem teljesítménykérdés, hanem konfigurációs kérdés.** A MAST-taxonómia szerint a többügynökös rendszerek kudarcainak 43,8 százaléka rendszertervezési eredetű, tehát nem a modell képességéből, hanem a felállás megválasztásából fakad (S-10). Ehhez illeszkedik az a tapasztalat, hogy az elfogadott bírálati észrevételek szabállyá alakítása mérhetően megszünteti a visszatérő hibaosztályokat (S-26).

Ebből egy fokozatos eszkalációs létra következik, amelyet a Scrum Master vezet. A létra **saját szerkesztésű**, de minden foka a fenti forrásokra épül.

1. **Egyedi hiba.** A bíráló javíttatja, és ennyi. Nincs teendő, és kifejezetten káros lenne minden egyedi hibából ügyet csinálni.
2. **Ismétlődő hibaosztály** — ugyanaz a hibatípus egy iterációban legalább kétszer. A Scrum Master felveszi a visszatekintés gépi rétegének napirendjére. A kimenet egy új szabály a szabályfájlban, azonosítóval és visszamutatással arra a bírálati eseményre, amelyből született (S-26).
3. **A szabály nem fog.** Ha a hibaosztály a szabály felvétele után is visszatér, akkor a szabály rossz vagy nem elegendő. **Ez az első valódi eszkalációs pont a szenior fejlesztők felé**, és a kérdés itt nem az, hogy „miért hibázik az ügynök", hanem az, hogy a promptot, a kontextust vagy az eszközkészletet kell-e átalakítani.
4. **A konfiguráció sem segít.** Ha az átalakítás után is visszatér, akkor ez már architektúra- vagy modellválasztási kérdés: lehet, hogy a feladat nem illik ehhez az ügynökszerephez, vagy más modellcsalád kell hozzá. Ide már a Product Ownert is be kell vonni, mert a váltás ütemezést és költséget érint.
5. **Több ügynöknél ugyanaz.** Ha ugyanaz a hibaosztály több, egymástól független ügynöknél is felbukkan, akkor nagy valószínűséggel nem az ügynökökkel van baj, hanem **a folyamattal vagy a kódbázissal**: hiányos a specifikáció, félreérthető a szerkezet, vagy a minőségi kapuk rossz helyen vannak.

A létra lényege az, hogy a Scrum Master ne az egyes hibákat továbbítsa, hanem a **mintázatot** tegye láthatóvá. Ez az a munka, amelyet más nem fog elvégezni, és amelyhez a [08-sm-felulet-specifikacio.md](08-sm-felulet-specifikacio.md) szerinti felület adja az adatot.

## A csapat fejlődési modellje

A brief azt kérdezi, alkalmazható-e a Tuckman-modell egy ilyen csapatra, és ha nem, milyen modell állítható fel helyette.

A válasz az, hogy **részben, és nem a gépi tagokra**. A Tuckman-modell fázisai — az alakulás, a viharzás, a normázás és a működés — kölcsönös társas észlelést feltételeznek: státuszharcot, normaalkotást, bizalomépítést. Az ügynökök nem viharzanak és nem normáznak, ők **konfigurációval fejlődnek**, nem társas tanulással.

A modell ezért két réteget különböztet meg.

Az **emberi réteg** a négyfős csapat: a Product Owner, a Scrum Master és a két szenior fejlesztő. Erre a klasszikus csoportdinamikai modellek továbbra is érvényesek, mert ezek az emberek egymással alakítanak ki normákat és bizalmat. Itt a Scrum Master a megszokott eszközeivel dolgozik.

A **szociotechnikai réteg** az ügynökparkkal együtt vett rendszer, és erre a T⁴ keretrendszert vesszük át, amely négy fázist ír le: csapatalakítás, feladat- és szerepfejlődés, csapatfejlődés, csapatjavítás (S-18). Ez a modell két okból illik jobban ide, mint a Tuckman. Egyfelől **ciklikus, nem lineáris**: a negyedik fázis visszavezet a másodikba és a harmadikba, ami élethű egy olyan csapatnál, ahol az ügynökök összetétele iterációról iterációra változhat. Másfelől a szerzők éppen az **alkalmazkodóképességet** teszik a középpontba, és a második-harmadik fázisnál három tényezőt emelnek ki: a csapatszerepeket, a közös mentális modellt és a támogató viselkedést.

A megfeleltetés a mi működésünkre így néz ki. A „viharzás" megfelelője az, amikor az ügynökök egymásnak ellentmondó változtatásokat hoznak, vagy amikor a szabályok még hiányoznak, és minden bírálat egyedi felfedezés. A „normázásé" az, amikor a szabályfájl letisztul, és a bírálók egyre inkább architekturális kérdésekkel foglalkoznak a mechanikus helyesség helyett — ezt a hivatkozott mérés konkrét számmal is megfogja: a bírálati észrevételeknek négy hét után már csak tizennégy százaléka szólt mechanikus helyességről (S-26).

## Mit mérünk a csapat érettségén

Mivel a T⁴ fázisokat és tényezőket ad, mérőeszközt viszont nem, az érettséget közvetett jelzőkkel jelenítjük meg. Az alábbi táblázat **saját javaslat**, nem bevált gyakorlat, és a pilot egyik feladata éppen az, hogy kiderítse, mennyire használhatók.

| Mit jelez | Mérőszáma | Réteg |
|---|---|---|
| A bizalom kalibráltsága | első körös elfogadási arány, és ennek szórása a két szenior között | szociotechnikai |
| A közös mentális modell érettsége | hány új szabály születik iterációnként — a csökkenő ütem letisztulást jelez | szociotechnikai |
| Az ügynökpark érettsége | ismétlődő hibaosztályok száma iterációnként | szociotechnikai |
| A bírálat mélységének eltolódása | a mechanikus helyességre vonatkozó észrevételek aránya az összeshez | szociotechnikai |
| Emberi terhelés | bírálatra fordított idő aránya, és önbevallásos terhelés | emberi |
| Együttműködés | hány elemet zárnak le közösen, hány marad egyetlen emberen | emberi |

A második sorhoz tartozik egy figyelmeztetés, amely megkülönbözteti a jó és a rossz olvasatot. Ha az új szabályok száma azért csökken, mert az ügynökök tényleg jobbak lettek, az érettség. Ha azért, mert a csapat kihagyja a visszatekintés gépi rétegét, az hanyagság. A kettőt csak a hibaosztályok követésével lehet megkülönböztetni: érettségnél a hibaosztályok is fogynak, hanyagságnál nem.

## Egy ellentmondásos kutatási eredmény

Érdemes rögzíteni egy eredményt, amely a csapatpszichológia szempontjából kétélű. A Procter & Gamble-nél végzett, 776 fős terepkísérletben az AI-val dolgozó résztvevők **pozitívabb érzelmi állapotról számoltak be**, ami arra utal, hogy az AI részben betölti az emberi csapattárs motiváló szerepét (S-20). Ugyanez a kísérlet mutatta ki, hogy az AI-val dolgozó egyén elérte az AI nélküli kétfős csapat teljesítményét, és hogy az AI lebontotta a funkcionális silókat.

Ez jó hír a magányos munka terhének enyhítése szempontjából, ugyanakkor kockázat is: a kellemesebb együttműködési élmény könnyen vezethet túlzott bizalomhoz, ami éppen a bírálat felületessé válásához visz. A Scrum Masternek ezért ezt a két jelet együtt kell olvasnia — ha a csapat elégedettsége nő, miközben az első körös elfogadási arány is nő és a bírálati idő csökken, az nem feltétlenül érettség, hanem lazulás is lehet.

## Nyitott kérdések

Nem találtunk validált mérőeszközt az ember–ügynök csapat érettségének mérésére, tehát a fenti táblázat javaslat, és a pilot alatt derül ki, mennyit ér. Nem tudjuk, hogy a bírálati kapacitás állandó-e: elképzelhető, hogy a szeniorok az első hetekben lassabban bírálnak, mert még nem ismerik az ügynökök jellemző hibáit, később viszont felgyorsulnak — vagy éppen ellenkezőleg, a kimerülés miatt romlanak. És nem találtunk vizsgálatot arra, hogyan hat a csapat kohéziójára az, ha a „létszám" nagy része cserélhető konfiguráció.
