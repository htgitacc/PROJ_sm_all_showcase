# 2. Minőségi kapuk — Definition of Done, tesztek, biztonság

> A jelölésről: `S-nn` hivatkozás mögött kutatási forrás áll ([kutatas/forrasok.md](../kutatas/forrasok.md)); ahol nincs hivatkozás, ott saját tervezési döntésről van szó, és a szöveg ezt kimondja.

## Miért a kapuk döntik el a modell sorsát

A [00-mukodesi-modell.md](00-mukodesi-modell.md) abból indult ki, hogy az emberi bírálat a szűk keresztmetszet. Ebből viszont egy kellemetlen következmény is adódik: minden csábítás arra fog hatni, hogy a szűk keresztmetszetet megkerüljük. A kutatás pontosan ezt dokumentálja — a nyílt forrású projektekben az ügynöki pull requestek nyolcvannégy százaléka úgy jutott át, hogy vagy senki nem nézte át, vagy csak egy másik gép (S-05). Ez nem szándékos szabályszegésből következett, hanem abból, hogy a mennyiség meghaladta a kapacitást, és a rendszer nem tiltotta meg az áteresztést.

A minőségi kapuk feladata ezért kettős. Egyfelől el kell venniük a terhet az emberről mindenütt, ahol a döntés gépiesíthető, mert így a szűkös emberi figyelem oda kerül, ahol tényleg kell. Másfelől meg kell akadályozniuk, hogy bármi ember nélkül átjusson ott, ahol emberi ítélet szükséges.

## A kapuk rendszere

Négy kaput különböztetünk meg, és a köztük lévő különbség nem szigorúságbeli, hanem **abban van, hogy ki hozza a döntést**.

Az első a **determinisztikus kapu**. Ide tartozik minden, aminek a kimenete megismételhető és nem függ nyelvi modelltől: fordítás, a meglévő tesztsorozat lefutása, statikus elemzés, formázás, függőség- és titokvizsgálat, licencellenőrzés. Ezek eredménye igaz vagy hamis, és a rendszer önműködően elutasítja azt, ami elbukik. Emberi figyelmet nem fogyaszt.

A második az **ügynöki kapu**, ahol egy ügynök végez el olyan feladatot, amelyre nincs determinisztikus eszközünk: hiányzó tesztek megírását, biztonsági szempontú átolvasást, a specifikációnak való megfelelés ellenőrzését. Ennek kimenete javaslat, nem ítélet.

A harmadik a **cáfoló kapu**, ahol egy másik modellcsaládra épülő ügynök megtámadja az előző lépés eredményét. Ez a modell egyik legfontosabb eleme, és külön alfejezetet kap.

A negyedik az **emberi kapu**, amely két helyen áll: a darabolás jóváhagyásánál (lásd [01-munka-utja.md](01-munka-utja.md)) és a beolvasztásnál. Ez a két hely az, ahol a felelősség keletkezik, és ezért nem delegálható.

A kapuk sorrendje azért fontos, mert minden lépcső csökkenti a következő terhelését. Ha a determinisztikus kapu elbukik, az elem el se jut az ügynöki kapuig; ha az ügynöki találatot a cáfoló kiejti, az emberhez már el se jut. A cél az, hogy az emberi kapuhoz csak olyan érkezzen, ami valóban emberi ítéletet igényel.

## Miért nem lehet az ügynök a saját munkájának bírája

Egy szabály van, amely mindegyik kapun átível: **a kilépési feltétel teljesülését soha nem az az ügynök állapítja meg, amelyik a munkát végezte.** Ennek két, egymástól független bizonyítéka van.

Az egyik a MAST-taxonómia, amely szerint a többügynökös rendszerek kudarcainak 24,05 százaléka a feladat-verifikációhoz kötődik: a korai lezárás 6,2, a hiányzó vagy részleges ellenőrzés 8,2, a hibás ellenőrzés 9,1 százalékot tesz ki (S-10). A kutatók egyik beavatkozása, a magas szintű célverifikáció beépítése, 15,6 százalékkal javította a sikerarányt egy programfejlesztési feladaton — vagyis az ellenőrzés architekturális elemként kezelése mérhetően használ.

A másik a gyártói útmutató, amely a verifikáló alügynököt egyedüli konzisztensen működő többügynökös mintaként nevezi meg kódolási feladatra, ugyanakkor rögtön megnevezi a hibáját is: a „korai győzelem" problémát, amikor a verifikáló részleges tesztelés után jelent sikert (S-08).

Ebből a gyakorlatban az következik, hogy a verifikáló ügynök kimenete nem az lehet, hogy „a tesztek rendben vannak", hanem a tesztfuttató **nyers, gépi kimenete**, amelyet a folyamat maga értékel. Az ügynök szöveges összefoglalója kiegészítő információ, nem döntés.

## Tesztstratégia

### Amit a lefedettségről tudni kell

A tesztstratégia egyetlen kiindulópontja az, hogy **a kódlefedettség AI-generált tesztnél nem alkalmas kapunak.** A legélesebb adat erre az, hogy vizsgáltak olyan tesztsorozatokat, amelyek száz százalékos lefedettséget értek el, miközben a mutációs pontszámuk mindössze négy százalék volt (S-16). Egy gyakorlati mérés hasonlót mutatott: egy adatfolyam-elemző komponens száz százalékos sorlefedettség mellett is csak 61,29 százalékos kiindulási mutációs pontszámot ért el (S-17).

A jelenség oka egyszerű. A lefedettség azt kérdezi, hogy egy kódsor lefutott-e; a mutációs teszt azt, hogy ha ennek a sornak a viselkedését szándékosan elrontanánk, észrevenné-e a tesztsorozat. Egy ügynök könnyen ír olyan tesztet, amely végigfut a kódon, de gyakorlatilag semmit nem állít — vagy ami még rosszabb, hűségesen megismétli ugyanazt a félreértést, ami az implementációban is benne van (S-17).

Ha tehát a Definition of Done lefedettségi küszöbre épül, akkor pontosan azt a mutatót tesszük céllá, amelyet a legkönnyebb kijátszani, és az ügynök nagyon hatékonyan fogja teljesíteni.

### Hol használjuk a mutációs tesztet — és hol nem

Kézenfekvő volna a mutációs pontszámot tenni a lefedettség helyére, de itt óvatosnak kell lenni, mert egy 2026-os replikációs vizsgálat éppen ezt árnyalja. Zhao, Zhou és Cohen azt találták, hogy a lefedettség és a mutációs pontszám hasznossága erősen kontextusfüggő: **regressziós helyzetben, hibátlannak feltételezett kódon értelmes összehasonlítási jelzést adnak, de ha a vizsgált kód maga is tartalmazhat hibát, már nem megbízható jelzők** (S-35).

Ez a megkülönböztetés adja a stratégiánk gerincét, és érdemes végiggondolni, mit jelent. Egy frissen írt, még el nem bírált kódrészletnél a mutációs pontszám azt méri, hogy a tesztek észreveszik-e a kód *megváltoztatását* — de ha maga a kód rossz, akkor a tesztek a hibás viselkedést fogják védeni, és a mutációs pontszám ettől akár magas is lehet. Egy már működő, elbírált és éles használatban lévő modulnál viszont pont ez a jó kérdés: megvédenénk-e ezt a viselkedést egy véletlen elrontástól?

Ezért a mutációs tesztet **regressziós védőhálóként** használjuk, nem új kód minőségi kapujaként. A gyakorlatban ez azt jelenti, hogy a magas kockázatú, már stabilizált modulokra — a hitelesítésre, a jogosultságkezelésre és az üzleti szabályokra — küszöböt írunk elő, és ezt a küszöböt a refaktorálás előtt és után is mérjük. Új kódnál viszont nem a mutációs pontszám a kapu, hanem az elfogadási feltétel teljesülése és az emberi bírálat.

A szelektív alkalmazásnak gyakorlati oka is van: a mutációs teszt lassú, egy háromnapos iterációba nem fér bele repozitóriumszinten, ezért a szakirodalom is a magas kockázatú területekre való szűkítést ajánlja (S-17).

### Karakterizációs tesztek a refaktorálás előtt

A brief központi tesztelési aggálya az volt, hogy a refaktorálás közben az AI „javít és ront egyszerre". Erre a válasz nem több teszt, hanem **más időzítésű** teszt.

A karakterizációs teszt olyan teszt, amelyet nem az elvárt, hanem a jelenlegi viselkedés rögzítésére írunk, mielőtt a kódhoz nyúlnánk. A logikája az, hogy refaktoráláskor definíció szerint nem akarjuk megváltoztatni a külső viselkedést, tehát ha a viselkedés mégis megváltozik, azt egy előre rögzített pillanatképnek el kell buktatnia. Ez a klasszikus válasz a problémára, és ügynökös közegben azért válik még fontosabbá, mert az irodalom szerint az AI-val segített változtatásokban a refaktorálás aránya gyakorlatilag nullára esett (S-06), a kódbázisok szerkezeti mutatói pedig ipari szinten romlanak (S-04). Ha tehát a refaktorálást külön ki kell kényszerítenünk, akkor a védőhálót is előre kell megépítenünk.

A modell ezért úgy rendelkezik, hogy **refaktorálási feladat nem indulhat el karakterizációs tesztréteg nélkül**. A tesztréteget megírhatja ügynök, de a jóváhagyása a szenior fejlesztő dolga, mert itt dől el, hogy mit tekintünk megőrzendő viselkedésnek.

### A tesztek külön bírálata

A tesztek elbírálását elkülönítjük a kódétól. Ennek oka az, hogy a tautologikus teszt — vagyis az, amely az implementációt önmagához méri ahelyett, hogy egy függetlenül levezetett elvárt viselkedéshez hasonlítaná — szemre teljesen rendben van, és csak akkor derül ki róla, hogy értéktelen, ha valaki külön felteszi a kérdést: mi az, amit ez a teszt állít, és mikor bukna el?

Ez a bírálat olcsóbb, mint a kódé, mert egyetlen kérdést kell megválaszolni tesztenként, viszont nem hagyható ki. A [04-meres.md](04-meres.md) ezért külön mutatóként tartja számon a tesztbírálatot.

### A legolcsóbb ellenőrzés

Van egy egyszerű gyakorlat, amelyet minden iterációban érdemes lefuttatni, és amely a teljes tesztháló állapotáról többet mond, mint bármelyik mutató. Egy eldobható másolaton szándékosan elrontunk néhány dolgot az iterációban érintett kódban, majd megnézzük, elbukik-e valamelyik teszt. Ez lényegében kézi mutációs teszt, néhány percbe kerül, és a visszatekintésen egyetlen kérdésre lefordítható: **ha most elrontanánk ezt a modult, észrevennénk?** Ha a válasz nem egyértelmű igen, akkor az iteráció nem volt inkrementális, csak iteratív.

## Biztonsági lánc

### Miért nem elég egy biztonsági ügynök

A brief azt kérdezi, hogy egy ügynök és modell kell-e, vagy több. Ez az egyetlen terület, ahol a kutatás egyértelműen a több mellett szól — de nagyon meghatározott módon.

A kiindulópont az, hogy az egymodelles sebezhetőségkeresés téves riasztásokat termel olyan arányban, amely a fogadó oldalon gyakorlatilag használhatatlanná teszi: a hivatkozott irodalom egy dokumentált esetben mintegy huszonnyolc százalékos téves pozitív arányt említ (S-15). Egy ilyen ügynök **több munkát okoz, mint amennyit megspórol**, hiszen minden téves találatot embernek kell megvizsgálnia — vagyis pont a szűk keresztmetszetből venne el.

A megoldás nem az, hogy több ügynököt szavaztatunk. Ugyanez a forrás hivatkozik olyan eredményre, amely szerint egyetlen meggyőző ügynök felülírhatja a többségi szavazást, és amely szerint a modellek erősen hajlamosak az egyetértésre. A működő minta ehelyett az **aszimmetrikus, cáfoló szerep**: a találatnak túl kell élnie egy olyan ügynököt, amelynek kifejezetten az a dolga, hogy megcáfolja. A hivatkozott módszertan így 171 jelöltből 79 százalékot ejtett ki visszamenőleges elemzésben, előretekintő szakaszban pedig harmincból huszonötöt, azaz 83 százalékot (S-15).

A modellcsalád keverése ugyanitt nem stílusbeli kérdés: az azonos családon belüli felülvizsgálat tizenkilenc javasolt javításból háromnál, tehát tizenhat százalékban nem vette észre a helyességi hibát, amelyet a más családból származó bíráló megtalált (S-15). Ipari léptékben ugyanezt az elvet valósítja meg az a rendszer, amely élvonalbeli modellt használ nehéz következtetésre, olcsóbb modelleket vitapartnerként, és egy másik gyártó élvonalbeli modelljét független ellenpontként (S-14).

### A négy lépcső

A biztonsági ellenőrzés ezért négy lépcsőben halad, és minden lépcső csökkenti a következő terhelését.

Az első lépcső **determinisztikus**: statikus elemzés, függőségi sebezhetőségvizsgálat, titokkeresés és licencellenőrzés. Ezeket nem nyelvi modell végzi, tehát az eredményük megismételhető, és nyelvi modelltől független alapot adnak.

A második lépcső az **ügynöki keresés**: egy biztonsági ügynök átnézi az iteráció változásait a fenyegetési modell szempontjai szerint. A fenyegetési modellt az OWASP két listája adja — a nyelvi modellekre vonatkozó tízes lista, amelyből számunkra elsősorban a prompt-befecskendezés és a túlzott cselekvési jogkör releváns (S-12), valamint az ügynöki alkalmazásokra vonatkozó lista, amely elsődlegesként az ügynökviselkedés eltérítését, az eszközök visszaélésszerű használatát és az azonosság- és jogosultsági visszaélést nevesíti (S-13).

A harmadik lépcső a **cáfolás** egy másik modellcsaládra épülő ügynökkel. Ennek nem az a feladata, hogy megerősítse a találatot, hanem hogy megpróbálja megsemmisíteni: kimutatni, hogy a feltételezett támadási út nem járható, hogy a bemenet nem befolyásolható, vagy hogy a hatás nem az, aminek látszik.

A negyedik lépcső az **ember**, aki csak azt kapja, ami a cáfolást túlélte. Az ő dolga a kockázat üzleti súlyozása és a döntés arról, hogy javítunk, elfogadjuk vagy elhalasztjuk.

Fontos elvárásmenedzsment, hogy az ipari példa (S-14) több mint száz ügynökre épül, amit a mi kétfős csapatunk nem fog reprodukálni. Amit átveszünk, az az architektúra elve — több modellcsalád, cáfolás, empirikus bizonyítási igény —, nem a méret. Azt is ki kell mondani, hogy a cáfoló architektúra a pontosságra optimalizál, és a hivatkozott forrás maga jelzi, hogy a felidézést nem méri (S-15): nem tudjuk, hány valódi sebezhetőséget ejt ki a szűrő. A belső intranet kockázati szintjén ezt a cserét vállalhatónak tartjuk, de ez **saját döntés**, nem bizonyíték.

## A Definition of Done

Az eddigiekből összeáll az, hogy egy elem mikor tekinthető késznek. A megfogalmazásnál arra ügyeltünk, hogy minden pont eldönthető legyen — vagyis vagy gépi kimenet felel meg neki, vagy egy megnevezett ember mondja ki.

Egy elem akkor kész, ha teljesülnek a saját elfogadási feltételei, és ezt a specifikációra visszavezethetően igazolni lehet. Le kell futnia a teljes meglévő tesztsorozatnak, és ezt a folyamatnak kell megállapítania a tesztfuttató nyers kimenetéből, nem az ügynök összefoglalójából. Rendelkeznie kell olyan új tesztekkel, amelyeket külön elbíráltak abból a szempontból, hogy mit állítanak és mikor buknának el. Ha az elem magas kockázatú modult érint, a modul mutációs pontszáma nem csökkenhet a változtatás hatására. Ha az elem refaktorálás, akkor előtte karakterizációs tesztréteg készült, és az változatlanul fut. Át kell mennie a determinisztikus biztonsági kapukon, és a cáfolást túlélő biztonsági találatokat vagy javítani kell, vagy megnevezett emberi döntéssel elfogadni. A változtatás mérete nem lépheti túl a megállapított korlátot, vagy ha túllépi, akkor az eltérést külön jóvá kell hagyni. Végül a beolvasztásnak megnevezett emberi jóváhagyója van, és ez a nyom a verziókezelőben marad.

Ez a lista szándékosan nem tartalmaz lefedettségi küszöböt, és ez a modell egyik legvitathatóbb döntése. Aki hozzászokott ahhoz, hogy a Definition of Done tartalmaz egy százalékot, hiányolni fogja. A [09-kockazatok-es-kilepes.md](09-kockazatok-es-kilepes.md) ezért külön kockázatként kezeli azt az esetet, ha a lefedettség a mérés szerint mégis érdemben esik.

## Nyitott kérdések

Nem tudjuk, milyen mutációspontszám-küszöb reális és gazdaságos a magas kockázatú modulokra: az irodalom módszert ad, küszöböt nem. Nem tudjuk, mennyi valódi biztonsági találatot veszítünk a cáfoló lépcsőn. És nem tudjuk, hogy a tesztek külön bírálata mennyivel terheli a bírálati keretet — ezt a pilot első két iterációjában mérni kell, mert ha jelentős, akkor a kapacitásszámítást módosítani kell.
