# 8. Az SM-támogató felület specifikációja

> Ez a dokumentum a harmadik fázis, a prototípus bemenete. Ellenőrzési feltétele az, hogy **ne vezessen be új fogalmat** azon túl, ami a [07-iteracios-pelda.md](07-iteracios-pelda.md) példájában szerepel. Ha valamihez új fogalom kellene, az azt jelenti, hogy a modell hiányos, és nem a felületet kell bővíteni.

## Milyen kérdésre válaszol a felület

A brief pontosan fogalmazza meg az igényt: a hagyományos Scrumban a Scrum Masternek volt ideje mindenre, itt viszont gyorsan kell látnia, mikor hol és mibe kell beavatkoznia. Ez a mondat elárulja, hogy **nem irányítópultra van szükség, hanem beavatkozási felületre.**

A különbség lényeges. Egy irányítópult azt mutatja meg, hogyan állunk; egy beavatkozási felület azt, hogy **mit kell most tenni, és mi az, ami magától rendben van.** A kutatásból tudjuk, hogy az adatgyűjtés és a státuszriportolás az a munka, amit a Scrum Master kiadhat a kezéből ([05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md)) — vagyis a felület akkor ér valamit, ha nem visszaadja neki ezt a munkát adatnézegetés formájában.

Ebből három tervezési elv következik. A felület **hallgat, amíg nincs baj**: alapállapotban azt kell közölnie, hogy nincs teendő. Ha megszólal, akkor **konkrét döntést kér**, nem tendenciát mutat. És mindenütt megmondja, hogy **mi lesz a következő lépés** — mert a beavatkozási pontok jelentős részénél a teendő a modellből egyértelműen következik.

## A négy nézet

A példa végigvezetése négyféle pillanatot mutatott meg, amikor a Scrum Masternek látnia kellett valamit, és ez a négy pillanat adja a négy nézetet.

### Első nézet: Most

Ez az alapértelmezett képernyő, és a napi eltéréskezelés eszköze. Egyetlen kérdésre válaszol: **mi az, ami most beavatkozást igényel?**

A képernyő tetején a beavatkozást igénylő jelzések állnak, alattuk pedig az áramlás állapota: hány elem van melyik szakaszban, és hol áll a korláthoz képest. A bírálati sor kap kiemelt helyet, mert a modell szerint ez a szűk keresztmetszet, és az iparági mérés szerint a torlódás a sorban állásból ered, nem a bírálat lassúságából (S-06).

A soron belül minden elemnél látszik, mióta vár, és hogy melyik szenior vette fel. Ez utóbbi nem ellenőrzés, hanem a terhelés eloszlásának követése, amelyről a kutatás kiégési kockázatként beszél (S-02, S-11).

A példa második napján ennek a nézetnek azt kellett volna kiírnia, hogy öt elem vár a négyes korláttal szemben, és mellé a modellből következő teendőt: az ügynökök nem indíthatnak új feladatot.

### Második nézet: Iteráció

Ez a nézet azt mutatja meg, hol tartunk a háromnapos ciklusban, és mi van még hátra. A brief kifejezetten említi, hogy akár ellenőrzőlista is lehet — és itt tényleg az a helyes forma, mert az iteráció szakaszai kötött sorrendben követik egymást, és a modell mindegyikhez ellenőrizhető kimenetet rendel ([03-esemenyek-es-tanulas.md](03-esemenyek-es-tanulas.md)).

Az ellenőrzőlista szakaszonként így néz ki:

**Iteráció indulása**
- [ ] Bírálati keret kiszámítva a legutóbb mért paraméterekkel
- [ ] A keretből elkülönítve a specifikációs jóváhagyás és a biztonsági találatok költsége
- [ ] A vállalt elemszám nem lépi túl a maradék keretet
- [ ] Minden elem specifikációja jóváhagyva
- [ ] Minden elemhez megvan az ügynök technikai kontextusa
- [ ] Az előző iteráció átcsúszott elemei betervezve

**Napi ritmus**
- [ ] Eltéréskezelés megtörtént, vagy indokoltan elmaradt
- [ ] Védett bírálati idősáv megtartva
- [ ] A bírálati sor a korláton belül van

**Iteráció zárása**
- [ ] Minden beolvadt elemnek van megnevezett emberi jóváhagyója
- [ ] Bemutató megtörtént, emberi felelősségvállalással
- [ ] Visszatekintés gépi rétege megtörtént, kimenettel
- [ ] Visszatekintés emberi rétege megtörtént (minden második iterációban)
- [ ] Paraméterek újramérve, a következő iteráció vállalása ehhez igazítva

### Harmadik nézet: Előretekintés

A brief kéri, hogy körülbelül egy iterációval előre is látszódjon, mi fog történni. Ez a nézet erre való, és három dolgot mutat.

Az első a **következő iteráció kapacitása**, a legutóbb mért paraméterekből számolva. A példában ez az a pillanat, amikor az első iteráció végén kiderült, hogy a mért értékek alapján kilenc helyett nyolc elem fér bele.

A második az, ami **átgörgetődik**: a be nem fejezett elemek, a javítás alatt lévők és a halasztott biztonsági találatok. Ezek már lefoglalják a következő iteráció keretének egy részét, tehát a szabad kapacitás kisebb, mint a nyers szám.

A harmadik a **visszamérendő szabályok** listája: mely szabályok kerültek be az előző visszatekintéseken, és melyik hibaosztályt kell figyelni ahhoz, hogy eldőljön, fogtak-e. A példában ez az a lista, amelyen az SZ-06 és az SZ-07 szerepelt, és amelyből kiderült, hogy az egyik fogott, a másik nem.

### Negyedik nézet: Tanulás

Ez a nézet az ügynökpark állapotát mutatja, és a visszatekintés gépi rétegének munkaeszköze.

Középpontjában a **hibaosztályok** állnak: melyik hányszor fordult elő, mikor született rá szabály, és azóta hányszor tért vissza. A modell szerint ez az egyetlen bizonyíték arra, hogy a visszajelzés beépült — nem az ügynök ígérete, hanem a hiba eltűnése (S-26).

Minden hibaosztálynál látszik, hogy hol tart az eszkalációs létrán, és hogy mi a következő fok teendője ([05-szerepek-es-dinamika.md](05-szerepek-es-dinamika.md)). A példában az SZ-07 esete itt vált volna láthatóvá: a szabály felvétele utáni visszatérés automatikusan a harmadik fokra emeli a hibaosztályt, aminek a teendője a szeniorok felé való eszkaláció.

Ugyanitt látszik a szabályfájl növekedése is. Ennek olvasata kétértelmű, és ezt a felületnek ki kell mondania: ha az új szabályok száma csökken, miközben a hibaosztályok is fogynak, az érettség; ha az új szabályok száma csökken, de a hibaosztályok nem, akkor a csapat valószínűleg kihagyja a visszatekintés gépi rétegét.

## A beavatkozási jelzések

A felület akkor ér valamit, ha nem a Scrum Masternek kell kitalálnia, mikor van baj. Az alábbi jelzések mindegyike a modellből vagy a példából származik, és mindegyikhez a modell adja a teendőt.

| Jelzés | Mikor szólal meg | Mi a teendő | Honnan |
|---|---|---|---|
| **Torlódás** | a bírálati sor eléri a korlátot | az ügynökök nem indíthatnak új feladatot | S-28 |
| **Öregedő elem** | egy elem a küszöbnél régebben vár | soron kívüli bírálat, vagy tudatos elengedés | S-06 |
| **Felügyeleti rés** | beolvadt elem megnevezett emberi jóváhagyó nélkül | azonnali kivizsgálás; ez a modell alapszabályának sérülése | S-05 |
| **Gumibélyegző-gyanú** | egy kapunál tartósan nulla az elutasítás | napirendre a visszatekintésen — ez nem siker, hanem gyanús | saját |
| **Egyenetlen terhelés** | a két szenior bírálati aránya tartósan eltér | terheléskiegyenlítés; kiégési kockázat | S-02, S-11 |
| **Visszatérő hibaosztály** | szabály felvétele után újra előfordul | eszkaláció a 3. fokra: nem szabály kell, hanem gépi kapu | S-26 |
| **Paramétereltérés** | a mért `R`, `t` vagy `r` érdemben eltér a tervezettől | a következő iteráció vállalásának újraszámítása | saját |
| **Méretkorlát-túllépés** | egy elem meghaladja a határt | visszabontás, nem hosszabb bírálat | S-06 |
| **Lazulásgyanú** | a validálási idő csökken, az elfogadási arány nő, **és** a hibaarány is nő | a bírálat felületessé válhatott; a visszatekintésen ki kell mondani | saját, S-20 alapján |

Az utolsó sor a legérdekesebb, mert **összetett jelzés**: egyik komponense sem rossz hír önmagában. A gyorsuló bírálat lehet gyakorlottság, a növekvő elfogadási arány lehet az ügynökök javulása. A három együtt viszont azt is jelentheti, hogy a csapat egyszerűen kevésbé nézi meg a munkát. A kutatás ehhez azt teszi hozzá, hogy az AI-val dolgozók pozitívabb érzelmi állapotról számolnak be (S-20), ami a bizalom irányába tolhat — ezért a jelzés nem automatikus ítélet, hanem beszélgetésre kötelező.

## Milyen adatokból él a felület

A prototípus szempontjából fontos, hogy az adatigény szerény és jórészt automatikusan előálló legyen. Négy forrásból dolgozik.

A **verziókezelőből** jön a beolvadt elemek listája, a jóváhagyó neve, a változtatás mérete és időbélyegei, a bírálati körök száma és a bírálók azonosítója. Ez adja a felület adatainak nagy részét, és ami a legfontosabb: az emberi bírálati arányt.

A **folyamatkezelő eszközből** — vagy a pilot szintjén akár egy egyszerű táblázatból — jön az, hogy melyik elem melyik szakaszban van, és mikor lépett oda.

Az **ügynökök futásnaplóiból** jön a bukott minőségi kapuk listája, a token- és költségadat, valamint a hibaosztály-besorolás nyersanyaga.

A **szabályfájl verziótörténetéből** jön az, hogy melyik szabály mikor került be, és milyen bírálati eseményre vezethető vissza — ezt a formátum metaadatai teszik lehetővé (S-26).

Emellett marad néhány adat, amelyet **kézzel kell felvinni**, és ezt nem szabad szégyellni: a napi bírálati idő, az önbevallásos terhelés és a hibaosztályok emberi besorolása. A pilot méretében ez néhány perc naponta, és cserébe nem kell hozzá integrációt építeni.

## Amit a felület szándékosan nem csinál

Nem mutat egyéni teljesítménybontást. A mérőszámok csapatszinten aggregáltak, mert a kutatás kifejezetten figyelmeztet arra, hogy ezek nem alkalmasak egyéni értékelésre, és a mennyiségi mutatók a legkönnyebben manipulálhatók (S-36). A bírálók megjelenítése a terheléseloszlás miatt van, nem rangsorolás céljából, és ezt a felületen ki is kell írni.

Nem mutat velocity-t és nem összegez story pontot, mert a modell ezeket elhagyta ([04-meres.md](04-meres.md)).

Nem próbál előre jelezni. Az „előretekintés" nézet a mért paraméterekből számol, nem modellez: azt mondja meg, mennyi fér bele, nem azt, hogy mi fog történni.

És nem hoz döntést. Minden jelzéshez teendő tartozik, de a teendőt ember hajtja végre — a felület nem állítja le az ügynököket, csak megmondja, hogy le kell állítani. Ez **saját döntés**, és vitatható: technikailag automatizálható volna. Azért nem tesszük, mert a pilot célja többek között annak megfigyelése, hogy a csapat mikor és miért lépné át a saját szabályait; egy automatikus tiltás ezt az információt elrejtené.

## Technikai megjegyzés a prototípushoz

A brief Pythont és Streamlitet javasol, és ez a célra jó választás: az adatmennyiség kicsi, a nézetek táblázatosak, és a lényeg a gyors iterálás a felület tartalmán, nem a megjelenésén.

A prototípus szintjén elegendő, ha az adatok egy szerkeszthető állományból — például néhány CSV- vagy JSON-fájlból — jönnek, és a példa két iterációjának adatai vannak feltöltve. Ez azért fontos, mert a prototípus célja **nem egy működő eszköz**, hanem annak megmutatása, hogy egy ilyen közegben mit kell látnia a Scrum Masternek. A valós integrációk kérdése akkor merül fel, ha a modell egyáltalán beválik.

## Nyitott kérdések

Nem tudjuk, hogy a beavatkozási jelzések küszöbei hol vannak jól — a felsorolt jelzések logikája a modellből következik, a konkrét határértékek viszont a mért paraméterektől függnek, amelyeket a pilot állít elő. Nem tudjuk, hogy a „lazulásgyanú" összetett jelzése működik-e a gyakorlatban, vagy túl sok téves riasztást ad. És nyitott, hogy a hibaosztályok besorolása mennyire automatizálható: a példában ezt ember végezte, és nem világos, hogy ez a munka hogyan skálázódik.
