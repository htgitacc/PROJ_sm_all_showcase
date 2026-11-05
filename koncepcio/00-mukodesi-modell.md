# 0. A működési modell

> Ez a koncepció magja. A többi dokumentum ebből vezeti le a maga területét, ezért ha itt valami megváltozik, azt végig kell vezetni a többin is.
>
> **Jelölés.** Ahol az állítás mögött kutatási forrás áll, ott `S-nn` hivatkozás szerepel; ezek feloldása a [kutatas/forrasok.md](../kutatas/forrasok.md) fájlban található. Ahol nincs hivatkozás, ott **saját tervezési döntésről** van szó, amelyre nem találtunk bizonyítékot — ezeket a szöveg külön megjelöli, és mindegyikhez tartozik egy mérés, amellyel a pilot alatt eldönthető, hogy jó döntés volt-e.

## Miből vezetjük le a modellt

A hagyományos Scrum abból indul ki, hogy a szűk keresztmetszet a megvalósítás: a csapat annyi munkát vállal egy sprintre, amennyit meg tud írni. Ez a feltevés ügynökös csapatnál nem áll, és ez az egyetlen olyan változás, amelyből az összes többi következik.

A kutatás egybehangzóan azt mutatja, hogy amint a kódírás olcsóvá válik, a szűk keresztmetszet lefelé csúszik az emberi elbírálásra. A LinearB 8,1 millió pull requestet átfogó mérése szerint az AI-generált változtatások átlagosan több mint tizenhat órát várnak arra, hogy egy bíráló egyáltalán hozzájuk nyúljon, míg a segítség nélküli munka mintegy kétszáz percet — ugyanakkor ha az elbírálás egyszer elkezdődött, az AI-s munka *gyorsabban* zárul le (S-06). Ez a részlet dönti el a modell szerkezetét: nem a bírálat lassú, hanem a sor hosszú. A nyílt forrású világban ugyanez a torlódás oda vezetett, hogy az ügynöki pull requestek nyolcvannégy százalékát vagy senki nem nézte át, vagy kizárólag egy másik gép nézte át (S-05). Aki tehát a csapata kapacitását az ügynökök sebességéből számolja, az nem gyorsabb csapatot épít, hanem egy olyat, amelyben a minőségi kapu csendben kikapcsol.

Ebből az következik, hogy a tervezés alapegysége nálunk nem az, hogy mennyi munkát tudunk *elvégezni*, hanem az, hogy mennyit tudunk **felelősséggel átvenni**. Ezt az egységet a továbbiakban bírálati keretnek (review budget) nevezzük, és ez váltja fel a story pontot.

## A csapat

A csapat emberi része a briefben megadott felállást követi: egy Product Owner, egy Scrum Master és két szenior fejlesztő. Az ügynökök nem ehhez a felsoroláshoz adódnak hozzá új „fejekként", hanem a két szenior fejlesztő munkaeszközei és egyben a munkájuk tárgyai: ők írják, hangolják és korlátozzák őket. Ez a megkülönböztetés nem szőrszálhasogatás. Ha az ügynököt csapattagként számoljuk, akkor a kapacitást is hozzáadjuk, és pontosan abba a hibába esünk, amelytől a kutatás óv. Ha eszközként és felügyelendő rendszerként kezeljük, akkor a kapacitás továbbra is kettő ember marad, az ügynökök pedig azt befolyásolják, hogy ez a két ember mire fordítja az idejét.

Az ügynökparkot szerep szerint bontjuk, nem feladat szerint. Ennek oka az, hogy a kutatás szerint a szakterület szerinti elkülönítés működik, ugyanannak a feladatnak a több párhuzamos ügynök közötti szétvágása viszont nem: a párhuzamosan dolgozó alügynökök egymástól függetlenül értik félre a feladatot, és a koordinátor utólag nem tudja összeegyeztetni az eredményeiket (S-07, S-08). A MAST-taxonómia ezt számokkal is alátámasztja, amennyiben a többügynökös rendszerek hibáinak 43,8 százaléka rendszertervezési eredetű, tehát nem a modell képességéből, hanem a felállás rossz megválasztásából fakad (S-10).

A pilot induló ügynökparkja ezért a következő szerepekből áll, és ez a lista szándékosan rövid, mert a kutatás azt ajánlja, hogy a legegyszerűbb működő felállásból induljunk, és csak bizonyíték alapján bonyolítsunk (S-08):

| Szerep | Mit csinál | Modellcsalád |
|---|---|---|
| **Implementáló** | egy backlog-elemet valósít meg, egyszálúan, teljes kontextussal | „A" család |
| **Verifikáló** | futtatja a teszteket, és önállóan eldönti, teljesül-e a kilépési feltétel | **„B" család** |
| **Biztonsági kereső** | az iteráció változásait vizsgálja a fenyegetési modell szerint | „A" család |
| **Biztonsági cáfoló** | megtámadja a kereső találatait; csak a túlélő megy ember elé | **„B" család** |
| **Kutató** | könyvtárakat, mintákat, dokumentációt keres a specifikációhoz | tetszőleges |

A táblázat egyetlen igazán fontos oszlopa a harmadik. A verifikálónak és a cáfolónak kötelezően más gyártó modelljére kell épülnie, mint az implementálónak, mert az azonos modellcsaládon belüli felülvizsgálat rendszeresen ugyanazokat a hibákat nézi el: egy dokumentált mérésben tizenkilenc javasolt javításból háromnál, tehát az esetek tizenhat százalékában, csak a más családból származó bíráló vette észre a helyességi hibát (S-15). Ugyanennek a vizsgálatnak a hivatkozott mérése szerint a modellek erősen hajlamosak az egyetértésre, ami azt jelenti, hogy két azonos családú példány többszörözése nem ellenőrzés, hanem a hiba megismétlése.

## A bírálati keret

A modell számtani magja egyetlen gondolat: **minden, ami emberi szemet igényel, ugyanabból a véges készletből fogyaszt.** Nem csak a kód. A specifikáció jóváhagyása, a tesztek külön elbírálása, a biztonsági találatok mérlegelése és a javítás utáni ismételt átnézés mind ugyanabból a keretből vesz el.

A keret kiszámításához három paraméterre van szükség. Az első az, hogy egy szenior fejlesztő naponta hány órát tud *ténylegesen* bírálatra fordítani — nem azt, hogy hány órát dolgozik, hanem azt, ami az architektúramunka, az ügynökök hangolása, az egyeztetések és a saját fejlesztői feladatai után marad. A második az, hogy egy méretkorlátos elem érdemi átnézése átlagosan mennyi ideig tart. A harmadik pedig az, hogy egy elem átlagosan hányszor kerül vissza javításra, mielőtt beolvasztható lenne.

Ezt a három számot **nem tudjuk az irodalomból** — a kutatás során kifejezetten kerestük, és nem találtunk hitelesíthető mérést az emberi bírálati kapacitás felső határára. Ezért a modell úgy épül fel, hogy a három szám **paraméter**, nem konstans: a pilot első két iterációja éppen azért van, hogy megmérjük őket. Az alábbi kiinduló értékek saját becslések, és a dokumentum végén szereplő mérési kötelezettség célja az, hogy legkésőbb a harmadik iteráció elején valós adatra cseréljük őket.

| Paraméter | Jelölés | Kiinduló feltevés | Hogyan mérjük |
|---|---|---|---|
| Napi bírálati idő szeniorra | `R` | 3 óra | naptárból és önbevallásból, naponta |
| Egy elem érdemi átnézése | `t` | 70 perc | a bírálat kezdete és lezárása közötti idő |
| Átlagos plusz körök száma | `r` | 0,5 | visszaadott elemek aránya |

A `t` értékéről érdemes külön szólni, mert ez a legkönnyebben alábecsülhető szám. Egy méretkorlátos, kétszáz soros változtatás **érdemi** átnézése — amelyet nem mi írtunk, tehát a logikát nem tartjuk a fejünkben — nem tizenöt perces munka. Az első becslésünk harmincöt perc volt; ezt a modell kidolgozása közben elvetettük, mert egy ilyen érték mellett a modell azt jósolta volna, hogy a csapat iterációnként húsz elemet tud átvenni, ami nem áll összhangban azzal, amit egy kétfős csapatról hihetőnek tartunk. A hetven perc továbbra is feltevés, de védhetőbb.

Ezekből a napi bruttó bírálati áteresztés szeniononként `R × 60 / t`, ami a kiinduló feltevések mellett nagyjából 2,6 elbírálás. Két szenior esetén ez napi 5,1 bírálati esemény. Mivel azonban minden elem átlagosan `1 + r` körben megy át, a naponta ténylegesen **lezárható** elemek száma `(R × 60 / t) × 2 / (1 + r)`, vagyis nagyjából 3,4.

Ez a 3,4 a modell legfontosabb száma. Nem az, hogy hány ügynököt indítunk, és nem az, hogy hány sort ír a gép: **a csapat naponta körülbelül három-négy elemet tud felelősséggel átvenni.** Egy háromnapos iterációban ez valamivel több mint tíz elem, és ebbe bele kell férnie a specifikációk jóváhagyásának és a biztonsági találatok mérlegelésének is, nem csak a kódnak. Reálisan tehát az iteráció kódelemekre fordítható kerete kilenc körül van.

Fontos, hogy ez a szám milyen irányban téved. Ha a bírálat gyorsabb a vártnál, azt észre fogjuk venni, mert kifogy a munka, és ez könnyen orvosolható.

 Ha viszont lassabb, akkor torlódás keletkezik, ami a kutatás szerint nem fokozatosan romlik, hanem egy ponton átbillen: a nyílt forrású projektekben pontosan ez történt, amikor az AI-generált hozzájárulások áradata meghaladta a karbantartói kapacitást (S-24). Ezért a kiinduló feltevéseket szándékosan **óvatosra** vettük, és az első iterációt inkább alultervezzük.

## A folyamatban lévő munka korlátai

A bírálati keret önmagában nem elég, mert nem akadályozza meg, hogy egyszerre húsz elem kerüljön félkész állapotba. Ezért a keret mellé kemény, oszlopszintű korlátok kellenek, amelyeket a rendszer nem javasol, hanem kikényszerít.

A korlátok közül a legfontosabb a bírálatra váró oszlopé. Yeret ajánlása szerint a reális szám fejenként egy-két párhuzamos elem, mert a valódi korlát az emberi bírálati kapacitás, nem az ügynökök átbocsátása (S-28). Ezt vesszük át, tehát szeniononként legfeljebb két elem várhat elbírálásra, összesen négy. Ha ez a négy betelt, **az ügynökök nem kezdenek új feladatot**, hanem a csapat a meglévő elemek lezárására áll rá. Ez a szabály fogja a legtöbb vitát okozni a pilot alatt, mert szemben áll azzal az ösztönnel, hogy a szabad gépi kapacitást ki kell használni — de éppen ez a lényege.

| Szakasz | Korlát | Miért |
|---|---|---|
| Finomítás alatt álló specifikáció | 3 | hogy legyen mit kiadni, de ne halmozzunk fel elavuló terveket |
| Ügynöki megvalósítás alatt | 4 | a bírálati oszlop kétszerese, hogy legyen utánpótlás |
| **Bírálatra vár** | **4** (szeniononként 2) | ez a valódi szűk keresztmetszet (S-28) |
| Javítás alatt | nincs korlát | mert ez már lekötött bírálati kapacitás |

A javítás alatt lévő elemekre azért nem teszünk korlátot, mert azok már beleszámítottak a keretbe, amikor először bírálat alá kerültek; egy külön korlát itt csak azt eredményezné, hogy a félkész munka egy másik oszlopban gyűlik.

## A változtatások mérete

A méretkorlát a modell második olyan eleme, amely közvetlenül a kutatásból következik. Az AI-val segített pull requestek a mérések szerint mintegy két és félszer nagyobbak a segítség nélkülieknél, a hetvenötödik percentilisen négyszáz kódsor fölött, szemben a segítség nélküli munka százötvenhét sorával (S-06). Ugyanezen mérés szerint az AI által generált változtatások elfogadási aránya 32,7 százalék, míg a segítség nélkülieké 84,5 százalék. A két szám együtt olvasva egy öngerjesztő kört ír le: a nagyobb csomagot felületesebben nézik át, a felületesebb átnézés miatt több hiba marad benne, a több hiba miatt csökken a bizalom, a csökkenő bizalom miatt pedig még tovább vár a sorban.

Ezt a kört a legegyszerűbben a bemeneti oldalon lehet elvágni. A modell ezért felső határt szab a bírálatra beadható változtatás méretének, és ha egy elem ezt túllépi, akkor nem az elbírálást hosszabbítjuk meg, hanem az elemet bontjuk szét. A konkrét határra nincs kutatási alapunk, ezért ez **saját döntés**: kétszáz nettó megváltoztatott kódsorban húzzuk meg, a generált vagy triviálisan ismétlődő részeket (például migrációkat és lezárt pillanatképeket) nem beleszámítva. Ha a mérés azt mutatja, hogy a szenior ennél nagyobb csomagot is átnéz a becsült időn belül, a határ emelhető.

## Az iteráció ritmusa

Az iterációhosszt szándékosan nem mondjuk ki előre, hanem levezetjük. Az elv az, hogy **egy iterációnak legalább annyi ideig kell tartania, hogy egy teljes kör beleférjen**: a feladat kiadásától az ügynöki munkán, az emberi bíráláton és a javításon át a beolvasztásig. Ha ennél rövidebb, akkor minden iteráció félkész munkával zárul, ami a Scrum értelmében nem inkrementum, és a torlódás iterációról iterációra görgetődik.

A kiinduló hipotézisünk a **háromnapos iteráció**, és ezt két megfontolás támasztja alá. Egyfelől a fenti kapacitásszámítás szerint három nap alatt nagyjából húsz elem fér a bírálati keretbe, ami elég nagy ahhoz, hogy értelmes inkrementum álljon össze belőle, de elég kicsi ahhoz, hogy egy rossz irány gyorsan kiderüljön. Másfelől a méretkorlátos elemek várhatóan egy napon belül átfutnak, tehát a három nap két teljes javítási körre is fedezetet ad. Hangsúlyozni kell azonban, hogy erre a hosszra **nem találtunk publikált mérést**: a kutatás során kifejezetten kerestünk rövid iterációval dolgozó ügynökös csapatról szóló beszámolót, és nem találtunk. A háromnapos ciklus tehát tervezési logikából következő feltevés, amelyet a pilot első két iterációja hivatott igazolni vagy megcáfolni.

A ritmus a következőképpen áll össze. Az iteráció első fél napja a tervezés és a specifikációk jóváhagyása, ami a bírálati keret egy részét már itt felhasználja. Ezután indulnak az ügynökök, és ettől kezdve minden nap ugyanaz a szerkezete: reggel egy rövid eltéréskezelő megbeszélés, majd a nap közepén egy védett bírálati idősáv, amelyet semmi nem szakíthat meg. A védett idősáv nem kényelmi kérdés. A kutatás legkonzisztensebb megállapítása az, hogy a torlódás a sorban állásból ered, nem a bírálat lassúságából (S-06), márpedig ha a bírálat a nap végi maradékidőbe szorul, akkor pontosan a sorban állás nyúlik meg. Az iteráció utolsó fél napja a bemutató és a kétrétegű visszatekintés, amelyről a [03-esemenyek-es-tanulas.md](03-esemenyek-es-tanulas.md) szól részletesen.

## A munka útja dióhéjban

A teljes folyamatot a következő dokumentum ([01-munka-utja.md](01-munka-utja.md)) írja le lépésről lépésre, itt csak a szerkezetét rögzítjük, mert ebből látszik, hol fogyasztunk emberi figyelmet.

A munka egy termékigénnyel indul, amelyet a Product Owner fogalmaz meg. Ebből specifikáció készül, és a darabolást — vagyis azt, hogy a specifikációból milyen konkrét elemek lesznek — már ügynök is elvégezheti. A darabolás eredménye azonban **nem mehet tovább emberi jóváhagyás nélkül**, mert ez a folyamat legolcsóbb ellenőrzési pontja: egy rossz specifikációt egy oldal elolvasásával ki lehet szűrni, egy rossz négyszáz sort viszont csak négyszáz sor elolvasásával. A jóváhagyott elemeket veszi át az implementáló ügynök, a verifikáló futtatja a minőségi kapukat, majd az elem bekerül a bírálati sorba. Innen vagy javításra megy vissza, vagy megnevezett emberi jóváhagyóval beolvad.

Ebben a láncban két helyen áll ember, és mindkettő szándékos. Az egyik a specifikáció jóváhagyása, ahol olcsó a hiba kiszűrése; a másik a beolvasztás jóváhagyása, ahol a felelősség keletkezik.

## Amit ez a modell szándékosan nem enged meg

Érdemes kimondani azt is, mit tilt a modell, mert ezek azok a pontok, ahol a napi gyakorlat el fog csúszni, ha nem őrizzük őket.

Nem engedjük meg, hogy az ügynökök akkor is dolgozzanak, amikor a bírálati oszlop tele van, mert ez pontosan az a mechanizmus, amely a torlódást előállítja. Nem engedjük meg, hogy egy elem gépi elbírálással beolvadjon, mert a kutatás szerint éppen ez az a csendes elcsúszás, amelynek nyomán az emberi felügyelet észrevétlenül ügynökirányítássá alakul (S-05). Nem engedjük meg, hogy ugyanaz a modellcsalád implementáljon és verifikáljon. És nem engedjük meg, hogy a bírálati idősáv „majd ha lesz idő" alapon működjön.

## Mérési kötelezettségek

Mivel a modell számos ponton feltevésre épül, minden feltevéshez tartozik egy mérés, amely a pilot alatt eldönti a sorsát. Ezek részletes tárgyalása a [04-meres.md](04-meres.md) dokumentumban található, de a modell szempontjából a következő négy a kritikus.

A `R`, `t` és `r` paraméterek mérése azért kritikus, mert ezekből számoljuk a kapacitást, és ha bármelyik jelentősen eltér a feltevéstől, az iterációhosszt és a WIP-korlátokat is újra kell szabni. A kétszáz soros méretkorlát azért, mert ha kiderül, hogy indokolatlanul szigorú, akkor feleslegesen darabolunk. A háromnapos iterációhossz azért, mert ez a legingatagabb feltevésünk. Végül az emberi bírálati arány — vagyis hogy a beolvadt elemek hány százalékát nézte át tényleg ember — azért, mert ez az egyetlen mutató, amely megmondja, hogy a modell egyáltalán működik-e, vagy csak papíron létezik.

## Nyitott kérdések

A modell két ponton támaszkodik olyan feltevésre, amelyet a pilot sem fog megnyugtatóan eldönteni. Az egyik az, hogy a bírálati kapacitás vajon állandó-e: elképzelhető, hogy a szeniorok az első hetekben lassabban bírálnak, mert még nem ismerik az ügynökök jellemző hibáit, később viszont felgyorsulnak — vagy éppen ellenkezőleg, a kutatásban leírt kimerülés miatt romlanak (S-11). A másik az, hogy a méretkorlát nem tolja-e át a komplexitást a darabolásra: lehet, hogy tíz kicsi elem együtt nehezebben átlátható, mint egy nagy. Mindkettőre az iterációnkénti visszatekintés adhat jelzést, bizonyítékot nem.
