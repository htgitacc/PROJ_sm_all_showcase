# 3. Review és átbocsátóképesség — a modell tartógerendája

## Mit kerestünk

A brief „Sebesség" kérdése így hangzik: hogyan osszuk ki a feladatokat úgy, hogy az ügynökök ne készítsenek el egyszerre harminc backlog-elemet, miközben a szenior fejlesztők ötöt tudtak átnézni? Ezt a kérdést nem ütemezési, hanem **átbocsátóképességi** problémaként kezeltük, és arra kerestünk bizonyítékot, hogy az emberi kódellenőrzés valóban szűk keresztmetszetté válik-e, és ha igen, mi történik akkor, ha ezt nem korlátozzuk.

Ez a dokumentum a kutatás legfontosabb darabja. Az itt következő adatok határozzák meg az iterációhosszt, a folyamatban lévő munka korlátait és az SM-felület fő mutatóit.

## Mit találtunk

### A központi mérés: mi történik valójában az ügynökök pull requestjeivel

Duma és szerzőtársai EASE 2026 konferenciacikke (S-05) az AIDev adathalmaz több mint 932 ezer pull requestjéből azt vizsgálta, hogyan reagálnak emberek az ügynökök által benyújtott módosításokra. A legalább száz csillagos repozitóriumokban 33 596 ügynök-szerzőségű pull requestet elemeztek, és az eredmény lehangoló:

- A pull requestek **61,38 százaléka semmilyen rögzített review-t nem kapott.**
- Amelyik kapott, annak 58,77 százalékát **kizárólag más ügynökök** nézték át; mindössze 10,14 százalék kapott tisztán emberi review-t, 31,09 százalék pedig vegyeset.
- Összesítve: az ügynök-szerzőségű pull requestek **84 százaléka** (28 246 a 33 596-ból) vagy egyáltalán nem kapott review-t, vagy csak gép nézte át. Mindössze 15,9 százaléknál látszik bármilyen emberi részvétel.
- Kommentszinten a 39 122 review-hozzászólás 71,58 százalékát ügynök írta.

A szerzők ugyanezt megvizsgálták emberi és ügynök pull requesteken **ugyanazokban a repozitóriumokban** is, és itt a legérdekesebb eredmény nem a mennyiség, hanem a szerkezet. Az emberi részvétel összaránya nagyjából azonos volt (30,12 százalék az ügynöki, 30,83 százalék az emberi pull requesteknél), a részvétel *formája* viszont élesen eltért. A tisztán emberi review az emberi pull requesteknél 25,21 százalék, az ügynökieknél csak 8,08 százalék (khí-négyzet(2) = 629,4, p < 0,001, Cramér-féle V = 0,25). A legerősebb eltérés az emberi hozzászólások jellegében mutatkozott: az emberi pull requesteknél a hozzászólások 93,56 százaléka valódi értékelő review volt, és az ügynökirányítás (agent steering) gyakorlatilag hiányzott (1,63 százalék), míg az ügynöki pull requesteknél a valódi review aránya 65,53 százalékra esett, az ügynökirányításé pedig 25,92 százalékra ugrott (khí-négyzet(3) = 1280, p < 0,001, V = 0,34, ami nagy hatásméret).

Emberi nyelvre lefordítva: **amikor egy ügynök nyújt be kódot, az ember egyre kevésbé bírálja el, és egyre inkább csak utasítgatja a gépet, hogy javítsa meg.** A szerzők ebből azt a következtetést vonják le, hogy a review-metrikák nagy mintás bányászati vizsgálatokban félrevezetők, mert nem az emberi felügyeletet mérik.

A tanulmány korlátját a szerzők maguk mondják ki: a rögzített review hiánya nem bizonyítja az emberi felülvizsgálat hiányát, mert a karbantartó megnézhet egy pull requestet anélkül, hogy hozzászólna. A vizsgálat a *megfigyelhető* review-interakciót méri. A besoroló szabályrendszert 800 hozzászólás kézi ellenőrzésével validálták, 96,5 százalékos pontossággal.

### Az iparági mérés: a torlódás számokban

A LinearB 2026-os mérnöki benchmarkja (S-06) 8,1 millió pull requestet elemzett 4800 csapatnál, 42 országban. A számok az előző tanulmány következményeit mutatják meg a folyamatban:

- Az AI-val segített pull requestek **mintegy két és félszer nagyobbak**: a 75. percentilisen több mint 400 kódsor, szemben a segítség nélküli munka 157 sorával.
- A refaktorálás aránya a segítség nélküli pull requesteknél a 75. percentilisen mintegy 37 százalék, az AI-val segítetteknél **közel nulla**.
- Az elfogadási arány a segítség nélküli munkánál nagyjából 84,5 százalék, az AI által generáltnál **32,7 százalék** — kevesebb mint a fele.
- A felvételi idő (pickup time), vagyis amíg egy pull request bírálóra vár, az AI által generált munkánál átlagosan **több mint tizenhat óra**, szemben a segítség nélküli munka mintegy 200 percével — több mint ötszörös különbség.
- Ha viszont a review egyszer elkezdődött, az AI-s pull request gyorsabban zárul (mintegy 194 perc a manuális 252 perccel szemben).

Ez utóbbi részlet döntő fontosságú: **a torlódás nem a review lassúságából, hanem a sorban állásból származik.** Az ember nem lassabban nézi át az ügynök kódját, hanem később kezdi el, mert több van belőle, nagyobbak, és kevésbé bízik bennük.

### A nyílt forrású közösségek tapasztalata

Ugyanezt a jelenséget írja le Yang, He és Zhou 67 projekt szabályzatait elemző munkája (S-24). A tanulmány megfogalmazása szerint az olcsóbb generálás nem jelent olcsóbb átnézést, és az így keletkező karbantartási teher kényszerítette a projekteket arra, hogy AI-specifikus szabályokat vezessenek be — egészen az AI-val segített hozzájárulások teljes tiltásáig. A már idézett Node.js-eset (19 000 soros, ügynökkel készült pull request, majd nyolcvan fejlesztő petíciója) azt mutatja, hogy a rendszer nem fokozatosan romlik, hanem egy ponton átbillen.

### Mit tegyünk ellene: a folyamatban lévő munka korlátozása

A gyakorlati válaszra Yuval Yeret 2026 januári írása (S-28) ad használható javaslatot. Ő „gyorsulási ostorcsapásnak" (acceleration whiplash) nevezi azt a helyzetet, amikor a kódgenerálás tízszeresére gyorsul, miközben az emberhez kötött szakaszok — review, tesztelés, validálás — nem skálázhatók vele arányosan, így a szűk keresztmetszet lefelé, a review-kapuhoz tolódik.

Két fogalmat vezet be, amelyek a mi SM-felületünkön is meg fognak jelenni. Az **AI-színház** (AI theater) az, amikor a csapat teljes kapacitáson dolgozik alacsony értékű, nem validált munkán, tehát nagy az aktivitás és kicsi az üzleti hatás. A **felfelé irányuló kiéheztetés** (upstream starvation) az, amikor nincs elég kész, validált munka, és a fejlesztő azért húz be alacsony prioritású elemet, hogy ne álljon.

Konkrét javaslatai: szigorú korlát a „review-ra kész" oszlopon, hogy a csapat rákényszerüljön a meglévő pull requestek közös lezárására; páros vagy hármas munka külön AI-asszisztenssel dolgozó magányos fejlesztők helyett; és korlát a finomítás alatt álló specifikációkon. A legfontosabb mondata számunkra az, hogy **fejenként egy-két párhuzamos elem a reális szám**, mert a korlát az emberi review-kapacitás, nem az ügynök átbocsátása. Yeret azt is hangsúlyozza, hogy a folyamatkorlátokat nem elég csapatszinten meghatározni: a Product Ownernek és a fejlesztőknek együtt kell megtervezniük a végponttól végpontig tartó határokat.

## Negatív tapasztalatok és buktatók

A legveszélyesebb minta az, amit Duma és szerzőtársai (S-05) mérnek: **a felügyelet nem megszűnik, hanem észrevétlenül átalakul**. Egy irányítópulton továbbra is látszik, hogy a pull requestek review-t kapnak, csak épp gépet nézünk gépet ellenőrizni. Ha a pilot mérésébe nem építünk be külön „emberi review történt-e" jelzést, hamis biztonságérzetben fogunk élni.

A második buktató a pull request mérete (S-06). Az AI-val segített változtatások két és félszer nagyobbak, márpedig a nagyobb változtatás felületesebb elbírálást vált ki. Ez öngerjesztő: nagyobb csomag → gyengébb review → több hiba → kevesebb bizalom → hosszabb sorban állás.

A harmadik buktató a refaktorálás eltűnése az AI-s pull requestekből (S-06, összhangban S-04-gyel). Ha az ügynök csak hozzáad, de soha nem takarít, a kódbázis szerkezete romlik, miközben minden egyes pull request külön-külön elfogadhatónak látszik.

A negyedik buktató a foglalkoztatottság illúziója: az ügynökök könnyen elérik, hogy mindenki elfoglaltnak *tűnjön*, miközben az érték nem szállítódik le (S-28 „AI-színház" fogalma).

## Mit jelent ez a mi projektünkre

Ez a dokumentum adja a modell egyik legkonkrétabb tervezési szabályát. Ha egy szenior fejlesztő naponta reálisan négy-hat érdemi review-t végez el, akkor **ez a szám a csapat tényleges átbocsátóképessége**, függetlenül attól, hány ügynök fut. Két szenior fejlesztővel ez napi nyolc–tizenkét elem felső korlátot jelent, és ebbe a keretbe bele kell férnie az újranyitott, javítás után visszatérő elemeknek is.

Ebből következően:

1. **A folyamatban lévő munka korlátja legyen explicit és fejenkénti**, Yeret ajánlása szerint egy-két elem szenioronként (S-28). Az ügynökök ne induljanak új feladatra, amíg a review-sor tele van.
2. **A feladatok mérete legyen korlátozva.** Mivel a nagy pull request rontja a review minőségét (S-06), érdemes felső határt szabni a változtatás méretének, és nagyobb feladatot inkább több, egymásra épülő lépésre bontani.
3. **Külön kell mérni az emberi és a gépi review-t** (S-05). A „hány review történt" mutató önmagában értéktelen.
4. **A refaktorálást külön kell kikényszeríteni**, mert magától nem történik meg (S-06, S-04).
5. Az iteráció hossza ne naptári megfontolásból következzen, hanem abból, hogy mennyi idő alatt fut le egy teljes kör: kiosztás → ügynöki munka → emberi review → javítás → beolvasztás. Erre a 11. dokumentum tesz javaslatot.

Az SM-felület központi kijelzője ebből adódóan nem az elkészült elemek száma, hanem **a review-sor hossza és kora**, mert ez az a mutató, amely a torlódást a leghamarabb jelzi.

## Nyitott kérdések

Nem találtunk mérést arra, hogy mennyi az emberi review reális napi felső határa AI-generált kódnál — a hivatkozott források a sorban állást mérik, nem a bíráló kapacitását. Szintén nyitott, hogy az automatizált review-eszközök (amelyek a mért esetek nagy részét adják) mennyiben helyettesítik érdemben az emberi elbírálást, és milyen hibaosztályokat hagynak ki rendszeresen. Végül nincs adatunk arról, hogy a Yeret által javasolt egy-két elemes korlát honnan származik — ez tapasztalati ajánlás, nem mérés.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-05 | Duma, Wróblewski, Bobińska, Winiarska, Przymus: *These Aren't the Reviews You're Looking For: How Humans Review AI-Generated Pull Requests*, EASE 2026, arXiv:2605.02273v1 | A |
| S-06 | LinearB: *2026 Software Engineering Benchmarks Report*, 8,1 M pull request, 4800 csapat, 42 ország | B |
| S-24 | Yang, He, Zhou: *To Ban or not to Ban? How Open Source Projects Govern GenAI Contributions*, arXiv:2603.26487v2 | A |
| S-28 | Yuval Yeret: *Limiting Work in Progress (WIP) in Scrum with Kanban in the AI Age*, 2026-01-23 | C |
| S-04 | GitClear: *The Maintainability Gap*, 2026 | B |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
