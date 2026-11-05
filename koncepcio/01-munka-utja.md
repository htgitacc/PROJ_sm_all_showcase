# 1. A munka útja — a backlogtól a beolvasztásig

> A jelölésről: `S-nn` hivatkozás mögött kutatási forrás áll ([kutatas/forrasok.md](../kutatas/forrasok.md)); ahol nincs hivatkozás, ott saját tervezési döntésről van szó, és a szöveg ezt kimondja.

## Miért ez a legfontosabb kérdés a backlogban

A brief így teszi fel a kérdést: hagyományosan a Product Owner darabolja a munkát, esetleg a Scrum Master segítségével, majd a csapat finomítja — mi lenne itt a helyes irány, és ha az AI darabol, hogyan mérhető, hogy ez jobb-e?

A kérdést érdemes átfogalmazni, mert így élesebb. Nem az a tét, hogy ember vagy gép írja-e le a backlog-elemeket, hanem az, hogy **hol helyezzük el a folyamatban azt a pontot, ahol az ember először mond igent valamire.** A kutatás legerősebb gazdasági érve az, hogy a hiba kiszűrése annál olcsóbb, minél korábban történik: egy félreértett specifikációt egy oldal elolvasásával ki lehet szűrni, de ha ugyanez a félreértés kódba fordul, akkor a mérések szerint már négyszáz sor fölötti csomagot kell elolvasni hozzá (S-06). Mivel az emberi figyelem a legszűkösebb erőforrásunk, azt oda kell tenni, ahol a legtöbbet ér.

Ebből következik az alapállásunk: **a darabolást végezze ügynök, de a darabolás eredménye emberi jóváhagyás nélkül ne mehessen tovább.** A Product Owner nem a leírásokat írja, hanem a kapunál áll.

## A folyamat lépései

A munka hét lépésen halad végig. A lépések sorrendje kötött, mert mindegyik a megelőző kimenetére épül, és a kihagyásuk pontosan azokat a hibamódokat hozza vissza, amelyeket a modell ki akar zárni.

**1. Termékigény.** A Product Owner megfogalmazza, mit és miért akarunk. Ez a lépés semmit nem változik a hagyományos Scrumhoz képest, és nem is szabad, hogy változzon: a szakirodalom egybehangzóan azt mondja, hogy a termékfelelősség — a felhasználói empátia, az érdekeltek közötti egyeztetés és az üzleti illesztés — elvi okból marad emberi (S-11). Az AI itt legfeljebb kutatóként segít, például versenytárselemzéssel vagy meglévő megoldások feltérképezésével.

**2. Specifikáció.** Az igényből egy strukturált specifikáció készül, amely rögzíti a célt, az elfogadási feltételeket, a nem funkcionális elvárásokat és a határokat. Ezt már készítheti ügynök a Product Owner vázlatából, mert a szövegezés alkotó feladat, és a kutatás szerint az ember–AI páros éppen alkotó feladatokban mutat pozitív együttműködési hozamot (S-19). A specifikáció formátumát a specifikáció-vezérelt fejlesztés gyakorlatából vesszük át, amelyben a specifikáció az egyetlen igazságforrás, és belőle generál, tesztel és validál az ügynök (S-30).

**3. Darabolás.** Egy erre a célra írt ügynök a specifikációból konkrét, megvalósítható elemeket állít elő. Minden elemhez megadja az elfogadási feltételt, a becsült érintett fájlokat és azt, hogy melyik minőségi kapuk vonatkoznak rá. Az elemeknek meg kell felelniük a [00-mukodesi-modell.md](00-mukodesi-modell.md) méretkorlátjának, tehát a darabolónak eleve úgy kell bontania, hogy egyetlen elem se lépje túl a kétszáz nettó sort.

**4. Jóváhagyási kapu.** A Product Owner és — technikai kérdésekben — az egyik szenior fejlesztő átnézi a darabolást. Nem a szöveg minőségét bírálják, hanem három dolgot: hogy az elemek együtt lefedik-e a specifikációt, hogy egyenként értelmezhető és lezárható egységek-e, és hogy az elfogadási feltételek ellenőrizhetők-e. Ez a kapu fogyaszt a bírálati keretből, és ezt a tervezéskor be kell kalkulálni.

**5. Ügynöki megvalósítás.** Az implementáló ügynök egy elemet vesz át, egyszálúan, teljes kontextussal. Nem osztjuk szét egy elem megvalósítását több párhuzamos ügynök között, mert a kutatás szerint a párhuzamos alügynökök egymástól függetlenül értik félre a feladatot, és a koordinátor utólag nem tudja összeegyeztetni az eredményeiket (S-07). Ha egy elem túl nagynak bizonyul egyetlen ügynöknek, az nem több ügynököt indokol, hanem azt, hogy a darabolás volt rossz — vagyis vissza kell menni a harmadik lépéshez.

**6. Gépi kapuk.** A verifikáló ügynök és az automatizált eszközök lefuttatják a minőségi kapukat, amelyeket a [02-minosegi-kapuk.md](02-minosegi-kapuk.md) részletez. Itt a lényeg annyi, hogy ezek kimenete **bináris és determinisztikus**: az elem vagy átment, vagy nem, és ezt nem az ügynök szöveges összefoglalója dönti el. Ez a megkötés a MAST-taxonómia egyik gyakori hibamódját zárja ki, a korai lezárást, amely a mért kudarcok 6,2 százalékát adta (S-10), és amelyre a gyártói útmutató is külön figyelmeztet „korai győzelem" néven (S-08).

**7. Emberi bírálat és beolvasztás.** Az elem bekerül a bírálati sorba, ahonnan vagy javításra megy vissza, vagy megnevezett emberi jóváhagyóval beolvad. A jóváhagyó neve a verziókezelőben marad, mert ez egyszerre felelősségi és tanulási követelmény: a [06-kormanyzas.md](06-kormanyzas.md) a jogi oldalát tárgyalja, a [04-meres.md](04-meres.md) pedig azt, hogy ebből mérjük az emberi bírálati arányt.

## Hogyan mérjük, hogy az ügynöki darabolás jobb-e

A brief kérdése itt a legkonkrétabb, és megérdemel egy konkrét választ. A nehézség az, hogy a darabolás minősége nem közvetlenül figyelhető meg: csak abból derül ki, hogy a belőle készült munka mennyire simán fut át a folyamaton.

**A pilot első két iterációjában vak összehasonlítást javaslunk.** Ugyanarra a specifikációra a Product Owner és a daraboló ügynök egymástól függetlenül, egymás eredményét nem látva elkészíti a saját darabolását. A két változatot azonos formátumra hozzuk, a szerzőségüket eltávolítjuk, és a jóváhagyási kapunál a szenior fejlesztők vakon értékelik őket. Ez a módszer nem tudományos igényű, mert a minta kicsi és az értékelők nem függetlenek a projekttől, de arra elég, hogy egy nyilvánvaló minőségi különbséget kimutasson — és a pilot szintjén ennyi kell.

Az összehasonlítás mellett négy olyan mutatót érdemes követni, amelyek a darabolás minőségét *utólag*, a folyamat viselkedéséből mérik.

Az első a **kapunál elutasított elemek aránya**: hány elemet kellett a jóváhagyásnál visszaküldeni átdolgozásra. Ez a leggyorsabb visszajelzés, de csak a nyilvánvaló hibákat fogja.

A második a **darabolás utáni visszabontás gyakorisága**: hányszor derült ki a megvalósítás közben, hogy egy elem valójában több elem, vagy hogy nem is önállóan lezárható. Ez a mutató a rossz darabolás legdrágább következményét méri, mert ilyenkor a már megkezdett munkát kell újratervezni.

A harmadik a **méreteloszlás egyenletessége**. Egy jó darabolásból hasonló nagyságrendű elemek születnek; ha az elemek mérete nagyon szór, az azt jelzi, hogy a bontás nem a munka természetes törésvonalai mentén történt. Ezt a beolvadt változtatások sorszámának szórásával lehet megfogni.

A negyedik az **első körös elfogadási arány**, vagyis hogy az elemek hány százaléka ment át javítás nélkül. Ez ugyan a megvalósítás minőségét is tükrözi, de a darabolásét is: egy homályos elfogadási feltétel kikényszeríti a javítási kört.

Fontos hozzátenni, hogy ezekre a mutatókra **nem találtunk irodalmi viszonyítási alapot** — nem tudjuk, mi számít jónak. A pilot ezért nem abszolút értéket mér, hanem a két darabolási mód különbségét, ami sokkal robusztusabb kérdés.

## Mit ad ki a kezéből a Product Owner, és mit nem

A modell szerint a Product Owner átadja a **megfogalmazás mechanikáját**: a felhasználói történetek szövegezését, az elfogadási feltételek első vázlatát, a technikai bontást és a kapcsolódó dokumentáció felkutatását. Ez az a munka, amely ma az idejének nagy részét eszi, és amelyben az ügynök gyors és — a jóváhagyási kapu miatt — kockázatmentesen javítható.

Nem adja ki viszont a **sorrendet és az elfogadhatóságot**. A rangsorolás ítéleti feladat, márpedig a kutatás szerint az ember–AI csapat éppen ítéleti és döntési feladatokban mutathat negatív együttműködési hozamot, miközben alkotó feladatokban pozitívat (S-19). Ez nem elővigyázatosság, hanem a rendelkezésre álló legjobb bizonyítékkal összhangban lévő szereposztás: generáltassunk ötletet és szöveget, de a „melyik a fontosabb" és a „ez így jó-e" kérdést tartsuk meg.

## Hol csúszik el ez a gyakorlatban

Három elcsúszást érdemes előre nevesíteni, mert a Scrum Masternek ezekre kell figyelnie.

Az első a **jóváhagyási kapu formálissá válása**. Ha a darabolás rendszeresen jó, a jóváhagyás pár hét után gumibélyegzővé alakul, és onnantól nincs kapu. Az ellenszere az, hogy a kapu mérhető nyomot hagy: ha az elutasítási arány tartósan nulla, az nem siker, hanem gyanús, és a visszatekintésen napirendre kell venni.

A második a **specifikáció megkerülése**. Sürgős helyzetben csábító közvetlenül feladatot adni az ügynöknek, kihagyva a második és harmadik lépést. Ez rövid távon működik, de megszünteti azt az olcsó ellenőrzési pontot, amelyre az egész modell gazdaságossága épül.

A harmadik a **darabolás mint rejtett tervezés**. Ha a daraboló ügynök nemcsak felbontja a munkát, hanem közben architekturális döntéseket is hoz — például eldönti, hogy melyik réteg felelős miért —, akkor ezek a döntések átcsúsznak a kapun anélkül, hogy bárki döntésként ismerné fel őket. Ezért a jóváhagyási kapun a szenior fejlesztő feladata kifejezetten az, hogy megkeresse a darabolásban rejlő tervezési döntéseket, és ha talál, azokat külön emelje ki.

## Nyitott kérdések

Nem tudjuk, hogy a vak összehasonlítás két iteráció alatt ad-e értékelhető jelzést; elképzelhető, hogy a különbség kisebb, mint a zaj. Szintén nyitott, hogy a Product Owner rangsorolási munkája mennyire szenved attól, ha a leírásokat nem ő írja: lehetséges, hogy a szövegezés maga is a megértés része, és a kiadásával a rangsorolás minősége romlik. Erre a visszatekintés adhat jelzést, mérés nem.
