# 3. Az események és a tanulási hurok

> A jelölésről: `S-nn` hivatkozás mögött kutatási forrás áll ([kutatas/forrasok.md](../kutatas/forrasok.md)); ahol nincs hivatkozás, ott saját tervezési döntésről van szó, és a szöveg ezt kimondja.

## Az események célja megváltozik, nem a számuk

A Scrum eseményeit könnyű úgy megreformálni, hogy törlünk belőlük — ez azonban félreérti a problémát. Az események nem azért lesznek működésképtelenek egy ügynökös csapatban, mert túl sokan vannak, hanem mert **a céljuk elavul**. A napi megbeszélés eredetileg azért létezett, hogy a csapattagok tudják, ki mit csinál, mert ez másképp nem derült ki. Egy olyan csapatban, ahol az ügynökök tevékenységéről percre pontos napló készül, ez a kérdés magától megválaszolódik, és az esemény tartalom nélkül marad — hacsak nem adunk neki újat.

A modell ezért minden eseménynél két dolgot rögzít: mi az új célja, és milyen **ellenőrizhető kimenete** van. Az utóbbi azért fontos, mert egy háromnapos iterációban nem engedhetjük meg magunknak, hogy egy esemény pusztán megnyugtató legyen.

## Iterációtervezés

A tervezés súlypontja a feladatok szétosztására kerül: mely elemek igényelnek emberi kreativitást, és melyek adhatók ügynöknek (S-11). Ehhez azonban a modellünkben hozzájön egy második, ennél is fontosabb kérdés, amely a hagyományos Scrumban nem létezik: **mennyi a rendelkezésre álló bírálati keret, és mire osztjuk el?**

A tervezés ezért nem azzal kezdődik, hogy hány elemet vállalunk, hanem azzal, hogy a [00-mukodesi-modell.md](00-mukodesi-modell.md) szerint számított keretből mennyit köt le a specifikációk jóváhagyása, mennyit a biztonsági találatok mérlegelése, és mennyi marad a kódra. Csak ezután beszélünk arról, hogy melyik elem kerül be.

Egy backlog-elem akkor kezdhető el, ha a specifikáció jóváhagyást kapott, és az ügynök megkapja a szükséges technikai kontextust. Saini megfogalmazása szerint az elem nem „Ready", ha az ügynöknek nincs meg a helyes dokumentáció a promptjában (S-11) — a mi modellünkben ez a feltétel a jóváhagyási kapu része.

A tervezés ellenőrizhető kimenete a kiosztott elemek listája, elemenként megadott kontextussal, és a bírálati keret elosztása.

## Napi eltéréskezelés

A napi megbeszélés nem státuszkör, hanem kivételkezelés. A résztvevők nem azt mondják el, min dolgoznak, hanem azt nézik meg, hol tért el a rendszer a várttól: mely ügynökök buktak el minőségi kaput, hol torlódik a bírálati sor, melyik elem lóg ki a méretkorlátból, és melyik ügynök fut túl a rá szabott kereten. Saini ezt „eltéréskezelésnek" nevezi, és azt javasolja, hogy ne az ügynökök „beszéljenek", hanem az emberi fejlesztők nézzék át az automatikus naplókat (S-11).

Az esemény ellenőrizhető kimenete egyetlen döntéstípus: **mit állítunk le, és mit engedünk tovább.** Ha nincs ilyen döntés, az esemény elmaradhat — ez szándékos, mert egy háromnapos iterációban a rituálé drága.

Itt kap szerepet az ügynökök „jelentése", amit a brief külön kérdez. Az ügynökök nem résztvevői az eseménynek, hanem **adatforrásai**: a kimeneti naplóik, az elfogadási arányaik és a hibaosztály-eloszlásuk adja azt a képet, amelyről a csapat dönt. Ez a különbség nem formai. Ha az ügynök „beszámolót" ad, akkor a saját munkájáról alkot ítéletet, ami éppen az a hibamód, amelyet a [02-minosegi-kapuk.md](02-minosegi-kapuk.md) ki akar zárni.

## Védett bírálati idősáv

Ez az egyetlen teljesen új esemény a modellben, és **saját javaslat**: a kutatás nem ír le ilyet, viszont a legkonzisztensebb megállapításából következik.

A mérések szerint az AI-generált változtatások átlagosan több mint tizenhat órát várnak arra, hogy bíráló nyúljon hozzájuk, míg ha a bírálat egyszer elkezdődött, gyorsabban zárul, mint az emberi munkáé (S-06). A torlódás tehát a sorban állásból ered. A sorban állás pedig abból, hogy a bírálat a nap maradékideje — az, ami a „saját" munka után marad.

A modell ezért minden napra fix, védett idősávot jelöl ki, amelyben a két szenior fejlesztő kizárólag bírál, és ezt semmi nem szakíthatja meg. Yeret ajánlása, hogy a „bírálatra kész" oszlopon szigorú korlát legyen, ami rákényszeríti a csapatot a meglévő elemek közös lezárására (S-28), a naptárban ölt testet: ha az idősáv alatt a sor kiürül, az ügynökök új munkát kapnak; ha nem ürül ki, nem kapnak.

Az esemény ellenőrizhető kimenete a bírálati sor aznapi apadása.

## Iterációs bemutató

A bemutató két dolgot csinál, és a második a fontosabb.

Az első a szokásos: megmutatjuk, mi készült el. A második az, hogy **valaki emberként vállalja az inkrementumot**. Saini megfogalmazása szerint az érdekelteket nem az érdekli, hogy AI írta-e a funkciót, hanem az, hogy ki felel az eredményért, és ezért egy emberi vezetőnek kell kontextusba helyeznie és bemutatnia az AI-generált kódot, teljes felelősséget vállalva (S-11). A mi modellünkben ez nem szertartás: a beolvasztási nyomvonalban amúgy is szerepel minden elem emberi jóváhagyója, a bemutató csak láthatóvá teszi ezt az érdekeltek felé.

A brief külön kérdezi, hogy egy fejlesztési ötleteket megfogalmazó bemutató hogyan néz ki, és hogy az AI is megfogalmazhat-e ötletet. A válasz igen, de éles határral. A kutatás szerint az ember–AI páros **alkotó** feladatokban pozitív együttműködési hozamot mutat, **ítéleti és döntési** feladatokban viszont negatívat (S-19). Ötletet generáltatni tehát ésszerű, sőt hasznos: egy erre felkészített ügynök az iteráció során összegyűlt hibákból, a felhasználói visszajelzésekből és a kódbázis állapotából javaslatokat tud megfogalmazni. A **rangsorolás** viszont emberi marad, mert az ítéleti feladat.

A gyakorlatban ez úgy néz ki, hogy az ügynöki javaslatok ugyanabba a listába kerülnek, mint az emberi ötletek, szerzőségük megjelölése nélkül, és a csapat vakon rangsorol. Ez **saját eljárási javaslat**, amelynek célja az, hogy se a gépi eredet miatti leértékelés, se a technológiai lelkesedés ne torzítsa a döntést.

## Kétrétegű visszatekintés

A visszatekintés az az esemény, amely a legmélyebben átalakul, mert két, egymástól nagyon eltérő logikájú dolgot kell elvégeznie.

### Az emberi réteg

Az egyik réteg a klasszikus csapatvisszatekintés, amely a négyfős emberi csapat együttműködésére vonatkozik. Erre a hagyományos eszközök érvényesek maradnak, mert ezek az emberek egymással alakítanak ki normákat és bizalmat.

Két témát azonban kötelezővé teszünk. Az egyik a **bírálati terhelés eloszlása**: ha az egyik szenior aránytalanul többet bírál, az nemcsak kapacitásprobléma, hanem kiégési kockázat is. Saini külön felhívja a figyelmet arra, hogy a nagy mennyiségű AI-generált kód átnézése mentálisan kimerítő (S-11), a DORA jelentése pedig a leggyengébb csapatprofilnál együtt említi a magas instabilitást és a kiégést (S-02). A másik a **bizalom kalibráltsága**: nem lett-e felületesebb a bírálat azért, mert az ügynökök „általában jók".

### A gépi réteg

A másik réteg nem csapatdinamika, hanem hibakeresés. Itt a csapat az ügynökpark működését elemzi: mely hibaosztályok ismétlődtek, hol futott ki egy ügynök a keretéből, melyik minőségi kapu fogott meg hibát, és melyik engedett át olyat, amit az embernek kellett észrevennie. Saini javaslata szerint ha egy ügynök nem szállított használható komponenst, akkor a csapatnak a rendszerpromptot kell átírnia — vagyis a klasszikus „eszközök és folyamatok" napirendi pont szó szerint a konfiguráció javítását jelenti (S-11).

Ennek a rétegnek **kötelező kimenete van**: legalább egy szabályváltozás, vagy annak indoklása, hogy miért nem kellett.

## A tanulási hurok: hogyan épül be a visszajelzés, és hogyan ellenőrizzük

A brief legélesebb kérdése az volt, hogy hogyan építhető be a visszajelzés az AI-ba, és hogyan tudjuk ellenőrizni, hogy beépült. Erre találtunk mérésekkel dokumentált választ, és ezt vesszük át.

Az alapelv egy mondatban összefoglalható: **minden elfogadott bírálati észrevétel egy önellenőrzési szabállyá alakul.** Ha a bíráló észrevesz valamit, amit az ügynök elmulasztott, a mintázatot kodifikálni kell, hogy legközelebb az ügynök maga vegye észre (S-26).

A hivatkozott keretrendszer szerkezete a következő. Az ügynökök egy verziókövetett, strukturált utasításfájlból dolgoznak, amely viselkedési szabályokat, kódolási sztenderdeket, önellenőrzési listát és antimintákat tartalmaz. Minden szabály metaadatokat kap: azonosítót, kategóriát, a kiváltó forrást, a hatókört, magát a megszorítást, az indoklást és a visszakövethetőséget arra a bírálati eseményre, amelyből született. Az ügynök kódot generál, lefuttatja az önellenőrzési listát, emberi visszajelzést kap, az elfogadott észrevételek szabállyá válnak, és a frissített fájl a következő munkamenetben töltődik be. A fájl épségét, a kötelező mezők meglétét és a sémának való megfelelést gépi ellenőrzés őrzi.

A mért eredmények egy négyhetes, több mint harmincöt mikroszolgáltatásra kiterjedő bevezetésből származnak (S-26). A szabálykészlet öt viselkedési szabályról tizennyolcra nőtt, és mellé tizenötnél több nyelvspecifikus sztenderd és egy tizenöt pontos önellenőrzési lista került; a fájl mérete mintegy 4809 szó volt, ami a kontextusablak kevesebb mint öt százaléka. Kilenc követett hibaosztálynál, hetvennégy kumulált szabály utáni előfordulási lehetőség mellett nulla visszaesést figyeltek meg. A bírálati észrevételeknek már csak tizennégy százaléka szólt mechanikus helyességről, hatvanhat százalékuk architektúráról, API-tervezésről és teljesítményről — vagyis a szabályok felszabadították a bírálókat a magasabb szintű kérdésekre. A szabályok eredete megoszlott: emberi bíráló harminckilenc, automatizált eszköz huszonkettő, önfelfedezett mintázat huszonkettő, éles hiba tizenhét százalék.

Ezt a forrást B szintűként kezeljük, mert a szerzők maguk jelzik a korlátait: egyetlen csapat, négyhetes megfigyelési ablak, és kontrollcsoport nélküli vizsgálat. A nulla visszaesés tehát lehet a rövid ablak műterméke is.

**Az ellenőrzés kérdésére a válasz ebből következik.** A visszajelzés akkor épült be, ha az adott hibaosztály többé nem fordul elő — és ez két helyről igazolható: a szabályfájl verziótörténetéből látszik, hogy a szabály mikor került be, a hibaosztályok követéséből pedig az, hogy azóta hányszor bukkant fel újra. A bizonyíték tehát nem az ügynök ígérete, hanem a hiba eltűnése.

Ha egy hibaosztály a szabály felvétele után is visszatér, az nem az ügynök „hibája", hanem azt jelenti, hogy a szabály nem működik. Ilyenkor vagy a megfogalmazás rossz, vagy a probléma nem szabállyal oldható meg, hanem eszköz- vagy architektúraváltással — és ez az a pont, ahol a Scrum Masternek eszkalálnia kell a szenior fejlesztők felé (lásd [05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md)).

## Az eseményekre fordított idő

Egy háromnapos iterációban a szertartások aránya könnyen elszalad, és ezt a kockázatot a kutatás során magunk azonosítottuk, választ viszont nem találtunk rá az irodalomban. A modell ezért **saját döntéssel** különbözteti meg az iterációnkénti és a ritkábban tartott eseményeket.

| Esemény | Gyakoriság | Becsült időigény |
|---|---|---|
| Iterációtervezés | minden iteráció | 60–90 perc |
| Napi eltéréskezelés | naponta, ha van eltérés | 15 perc |
| Védett bírálati idősáv | naponta | a bírálati keret része, nem külön költség |
| Iterációs bemutató | minden iteráció | 30 perc |
| Visszatekintés, gépi réteg | **minden iteráció** | 20–30 perc |
| Visszatekintés, emberi réteg | **minden második iteráció** | 45–60 perc |

A gépi réteg azért marad minden iterációban, mert rövid, mechanikus, és a tanulási hurok tőle függ: ha kihagyjuk, a szabályfájl nem gyarapszik, és a hibaosztályok visszatérnek. Az emberi réteg azért ritkítható, mert a csapatdinamikai kérdések nem háromnapos ciklusban változnak. Ez a felosztás nagyjából heti egy hosszabb és iterációnként egy rövid visszatekintést jelent.

## Nyitott kérdések

Nem tudjuk, hogy a szabályfájl növekedése hosszabb távon kezelhető marad-e, és mikor kell egy szabályt visszavonni; a hivatkozott vizsgálat négy hete erre nem ad választ, és az elévülés kérdését az irodalom sem oldja meg (S-25, S-26). Nem tudjuk, hogy a vak rangsorolás a bemutatón valóban semlegesíti-e a gépi eredet miatti torzítást. És nem tudjuk, hogy a kétrétegű visszatekintés ritmusa jó-e: elképzelhető, hogy az emberi réteg kétiterációnyi késése túl lassú visszacsatolás egy induló csapatnak.
