# 9. Kockázatok, sikerkritérium és kilépési feltétel

> A jelölésről: `S-nn` hivatkozás mögött kutatási forrás áll ([kutatas/forrasok.md](../kutatas/forrasok.md)); ahol nincs hivatkozás, ott saját tervezési döntésről van szó, és a szöveg ezt kimondja.

## Miért ez a dokumentum zárja a koncepciót

Egy pilot akkor bukik el a legcsúnyábban, ha soha nem derül ki róla, hogy elbukott. A vállalati AI-projektekről szóló, sokat idézett jelentés — amelyet ugyan módszertani kritika ért a szűk sikerdefiníciója és a kis mintája miatt (S-32) — a kritikával együtt is arra a tanulságra fut ki, hogy a pilotok jellemzően nem a technológia miatt buknak meg, hanem azért, mert a siker kritériumát nem rögzítették előre.

Ez a dokumentum ezért három dolgot rögzít, mielőtt az első iteráció elindulna: mi mehet félre, miről ismerjük fel időben, és mikor mondjuk ki, hogy vége.

## A tizenkét kockázat

### 1. A kapuk gumibélyegzővé válnak

Ez a legvalószínűbb és legalattomosabb kockázat. A modell minden ereje a minőségi kapukban van, márpedig egy jól működő kapu néhány hét alatt formalitássá kopik: ha a darabolás rendszeresen jó, a jóváhagyás automatikussá válik, és onnantól nincs kapu, csak látszat.

*Korai jel:* egy kapunál tartósan nulla az elutasítási arány.
*Ellenszer:* a Scrum Master ezt gyanúsnak, nem sikernek olvassa, és napirendre veszi ([05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md)).

### 2. Az emberi bírálat észrevétlenül gépivé alakul

Ez a kutatás legerősebben dokumentált kockázata. A nyílt forrású projektekben az ügynöki pull requestek nyolcvannégy százaléka úgy jutott át, hogy vagy senki nem nézte át, vagy csak egy másik gép (S-05) — és ami ennél is fontosabb, az emberi jelenlét nem tűnt el, hanem *átalakult*: az emberi hozzászólások negyede már nem elbírálás, hanem a gép utasítgatása lett.

*Korai jel:* az emberi bírálati arány csökkenése, illetve olyan beolvadt elem, amelynek nincs megnevezett emberi jóváhagyója.
*Ellenszer:* ez a mutató a felület legfontosabb jelzése, és a kilépési feltétel része.

### 3. A csapat áthágja a folyamatban lévő munka korlátait

A WIP-korlát rossz érzést kelt, mert szabad gépi kapacitás áll kihasználatlanul — ezt a példa második napja szemléletesen mutatja. A nyomás arra fog hatni, hogy „csak most az egyszer" túllépjük.

*Korai jel:* a bírálati sor tartósan a korlát fölött, vagy egyre több „kivételes" túllépés.
*Ellenszer:* a Scrum Master feladata, hogy a leállást a rendszer helyes működéseként mutassa be, ne hibaként.

### 4. A karbantarthatóság észrevétlenül romlik

Az ipari mérések szerint az AI-val segített fejlesztés mellett a blokkduplikáció 2023 óta 81 százalékkal nőtt, az áthelyezett — vagyis valódi refaktorálásra utaló — kód aránya 21-ről 3,8 százalékra esett, a fájlok közötti függvénykapcsoltság pedig 35 százalékkal csökkent (S-04). Ehhez jön, hogy az AI-val segített változtatásokban a refaktorálás aránya gyakorlatilag nulla (S-06).

Ez a kockázat azért veszélyes, mert **hónapokkal később jelentkezik a költségekben**, egy néhány hetes pilot pedig ebből semmit nem lát, ha nem méri kifejezetten.

*Korai jel:* a duplikációs arány emelkedése és a refaktorálási arány esése.
*Ellenszer:* ezek folyamatosan mért mutatók, és a refaktorálást külön ki kell kényszeríteni, mert magától nem történik meg.

### 5. A lefedettség tényleg leesik

A modell szándékosan nem tesz lefedettségi küszöböt a Definition of Done-ba ([02-minosegi-kapuk.md](02-minosegi-kapuk.md)), és ez a legvitathatóbb döntése. Elképzelhető, hogy a küszöb hiányában a lefedettség érdemben esik, és a döntés mégis rossznak bizonyul.

*Korai jel:* a lefedettség — amelyet tájékoztató mutatóként továbbra is mérünk — meredek esése.
*Ellenszer:* ha ez bekövetkezik, a küszöböt vissza kell vezetni, de nem kapuként, hanem riasztásként.

### 6. A cáfoló lépcső valódi sebezhetőségeket ejt ki

A biztonsági lánc a pontosságra optimalizál, és a hivatkozott forrás maga jelzi, hogy a felidézést nem méri (S-15). Nem tudjuk, hány valódi találatot veszítünk.

*Korai jel:* nincs jó korai jel — ez a kockázat természeténél fogva láthatatlan.
*Ellenszer:* időszakos ellenőrzés, amelyben ismert sebezhetőségeket telepítünk a kódba, és megnézzük, átjutnak-e a láncon. Ez **saját javaslat**, a modell nem tartalmazza kötelező elemként, mert a bírálati keretből fogyaszt.

### 7. A szeniorok kiégnek

A nagy mennyiségű AI-generált kód átnézése mentálisan kimerítő (S-11), a DORA felmérése pedig a leggyengébb csapatprofilnál együtt említi a magas instabilitást és a kiégést (S-02).

*Korai jel:* egyenetlen bírálati terheléseloszlás, növekvő önbevallásos terhelés, a védett bírálati idősáv túlcsordulása.
*Ellenszer:* a napi bírálati idő nem növelhető korlátlanul; ha a sor nem apad, kevesebb bejövő munka kell, nem több bírálat.

### 8. A szabályfájl elburjánzik

A hivatkozott vizsgálatban a szabályfájl négy hét alatt a kontextusablak kevesebb mint öt százalékára nőtt (S-26), de ez négy hét, egyetlen csapatnál. A szabályok elévülésének és kigyomlálásának kérdését az irodalom nem oldja meg (S-25).

*Korai jel:* a szabályfájl mérete, illetve az, ha egy szabály hónapok óta nem sült el.
*Ellenszer:* időszakos átnézés, amelyben a soha nem aktiválódó szabályokat vagy töröljük, vagy gépi kapuvá alakítjuk.

### 9. A visszatérő hibát szabállyal próbáljuk megoldani

A példa második iterációja mutatja meg ezt a csapdát: az SZ-07 szabály visszatért, és a csábító megoldás a szabály átfogalmazása lett volna. Az utasításfájl azonban **puha korlát** — az utasítás követendő szöveg, nem kikényszerített megkötés —, tehát a visszatérő hibaosztályt géppel kell megfogni ([06-kormanyzas.md](06-kormanyzas.md)).

*Korai jel:* ugyanaz a hibaosztály másodszor is visszatér, immár átfogalmazott szabály mellett.
*Ellenszer:* az eszkalációs létra harmadik foka kötelezően gépi kaput ír elő, nem szövegjavítást.

### 10. A költség elszalad

A többügynökös megvalósítás a mérések szerint azonos feladatra tipikusan három-tízszer több tokent használ (S-08). A modellünk ugyan alkotó oldalon egyszálú, ellenőrző oldalon viszont többszörös, és a cáfoló lépcső minden találatot kétszer dolgoztat fel.

*Korai jel:* az iterációnkénti token- és pénzköltség.
*Ellenszer:* a cáfoló lépcső olcsóbb modellre állítható, ahogy a hivatkozott ipari rendszer is desztillált modelleket használ vitapartnerként a nagy mennyiségű átfutáshoz (S-14).

### 11. Az iterációhossz rossz

A háromnapos ciklus a modell leggyengébben megalapozott feltevése: a kutatás során **nem találtunk publikált mérést** rövid iterációval dolgozó ügynökös csapatról.

*Korai jel:* minden iteráció félkész munkával zárul, vagy fordítva, az iteráció végén tétlenség van.
*Ellenszer:* az iterációhossz a mért ciklusidőből újraszámítható; ez nem kudarc, hanem a modell rendeltetésszerű működése.

### 12. Maga a modell túl bonyolult

Ezt a kockázatot érdemes külön kimondani, mert a többivel ellentétben nem a végrehajtásról szól, hanem a tervezésről. A modell jelentős szabályrendszert ír elő egy négyfős csapatnak: jogosultsági szinteket, kapukat, WIP-korlátokat, méretkorlátot, kétrétegű visszatekintést, eszkalációs létrát és tucatnyi mutatót. Elképzelhető, hogy a betartása több terhet ró a csapatra, mint amennyi hasznot hoz.

*Korai jel:* a szabályok rendszeres, nem kivételes megsértése; az adminisztrációra fordított idő aránya.
*Ellenszer:* ha ez bekövetkezik, a helyes válasz nem a szigorítás, hanem az egyszerűsítés — és a legelőször elhagyandó elemek azok, amelyek mögött nem áll kutatási bizonyíték, hanem saját tervezési döntés. Ezért van az összes ilyen döntés külön megjelölve a dokumentumokban.

## Sikerkritérium

A pilotot **három iteráció után**, tehát nagyjából két hét működés alapján értékeljük először. A kritériumokat három csoportba osztjuk, mert a kutatásból tudjuk, hogy a magas kihasználtság együtt élhet alacsony vagy akár negatív hatással (S-36) — vagyis egyetlen dimenzió mérése félrevezet.

**Alapfeltételek.** Ezeknek mind teljesülniük kell, különben a modell nem működik, függetlenül attól, mennyi értéket termelt.

| Kritérium | Küszöb |
|---|---|
| Emberi bírálati arány | legalább 95% |
| Beolvadt elem megnevezett emberi jóváhagyó nélkül | nulla |
| Éles biztonsági incidens, amelyet a lánc átengedett | nulla |

**Értékteremtés.** Ezek azt mérik, hogy a modell hoz-e valamit.

| Kritérium | Elvárás |
|---|---|
| Iterációnként beolvadt elemek száma | nem csökken |
| Első körös elfogadási arány | javuló irány |
| Visszatérő hibaosztályok száma | csökkenő irány |
| Innovációs arány | nem romlik |

**Fenntarthatóság.** Ezek azt mérik, hogy meddig bírjuk.

| Kritérium | Elvárás |
|---|---|
| Szeniorok önbevallásos terhelése | nem nő tartósan |
| Bírálati terhelés eloszlása a két szenior között | nem tartósan egyenetlen |
| Duplikációs arány | nem romlik érdemben |
| Iterációnkénti költség | a keretben marad |

Fontos hozzátenni, hogy három iteráció alapján **trendet megállapítani nem lehet**, ahogy azt a példa is kimondja. Az „irány" jellegű kritériumok ezért nem éles kapuk, hanem beszélgetést indító jelzések; egyedül az alapfeltételek élesek.

## Kilépési feltétel

A pilotot akkor állítjuk le, ha az alábbiak bármelyike bekövetkezik. Ezt a listát a csapatindító dokumentumnak is tartalmaznia kell, mert a kilépési feltétel hiánya a leggyakoribb módja annak, hogy egy kísérlet határozatlan idejű projektté váljon ([06-kormanyzas.md](06-kormanyzas.md)).

Leállítjuk, ha az **emberi bírálati arány két egymást követő iterációban 80 százalék alá esik**, és a folyamatban lévő munka korlátjának szigorításával sem lehet visszahozni. Ez azt jelenti, hogy a modell alapszabálya nem tartható ezzel a kapacitással, márpedig e nélkül a felállás pontosan az a rendszer, amelytől a kutatás óv.

Leállítjuk, ha **éles biztonsági incidens** történik, amelyet a négylépcsős lánc átengedett. Ilyenkor nem az a kérdés, hogy folytassuk-e, hanem az, hogy mit rontottunk el a láncban.

Leállítjuk, ha a **szeniorok terhelése tartósan nő, miközben az átbocsátás nem**. Ez azt jelenti, hogy a modell drágábbá tette a munkát anélkül, hogy többet szállítana.

Leállítjuk, ha **hat iteráció után a kapacitásparaméterek nem stabilizálódnak**, vagyis iterációról iterációra jelentősen ugrálnak. Ekkor a modell nem tervezhető, tehát nem is működtethető.

És leállítjuk, ha a **költség meghaladja az előre rögzített keretet** anélkül, hogy az értékteremtési kritériumok teljesülnének.

Egyik kilépési feltétel sem jelenti azt, hogy „az AI-ügynökökkel dolgozó csapat nem működik". Azt jelenti, hogy **ez a modell, ebben a csapatban, ezekkel az eszközökkel nem működött** — és a pilot pontosan ezért van. A negatív eredmény is eredmény, feltéve, hogy a mérés megbízható volt, és hogy le tudjuk írni, mi és miért nem működött.

## Mit teszünk, ha sikerül

Ha a három iteráció után az alapfeltételek teljesülnek, és az értékteremtési kritériumok legalább semlegesek, a javaslat az, hogy a pilot **további három iterációval folytatódjon** változatlan modellel, mert a paraméterek stabilizálódásához több adat kell. A modell módosítását ekkor még kerülni érdemes, mert a folyamatos változtatás lehetetlenné teszi az összehasonlítást.

A felskálázás kérdése — több csapat, éles ügyfélprojekt, platformfüggetlen működés — csak ezután merül fel, és akkor is elsőként azzal a kérdéssel, hogy a modell melyik eleme mögött állt tényleges bizonyíték, és melyik mögött saját tervezési döntés. A jelölés éppen ezért van végig a dokumentumokban.

## Nyitott kérdések

Nem tudjuk, hogy három iteráció elég-e bármit is megállapítani; valószínűleg nem, de ennél hosszabb ideig felelőtlenség volna értékelés nélkül futtatni. Nem tudjuk, hogy a kilépési küszöbök jó helyen vannak-e — ezek saját döntések, viszonyítási alap nélkül. És nem tudjuk, hogy a tizenkettedik kockázat, a modell túlbonyolítottsága, mennyire valós: ez az egyetlen kockázat, amelyet a modell maga nem tud mérni, csak a csapat tud róla beszélni.
