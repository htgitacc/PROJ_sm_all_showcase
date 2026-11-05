# Kitalált projekt

Egy közepes méretű magyar vállalat úgy dönt, hogy pilot projektet indít, egy spike-ot, olyan Scrum csapatokra, amik nem hagyományos felállásúak, hanem AI csapattagokat használnak. A feladat a cég belső weboldalának, egy intranetnek a megújítása. A projekt, ha nem sikerül, akkor nem sérül az ügyfél érdeke, de mégis úgy kell kezelni a projektet, mintha egy külső cég vállalati intra weboldalát készítenénk el. 

De! És itt jön a lényeg, hogy ez a Scrum csapat nem hagyományos, hanem AI first csapat.

## Csapat

Csak ötlet, nem végleges megoldás

- PO
- SM
- 2 db Szenior fejlesztő
- AI Ügynök munkatársak
    - a szenior fejlesztők megírják az ügynököket, amennyi szükséges és a feladathoz igazítják a futásukat és számukat
    - úgy viselkednek, mint egy junior-medior fejlesztő
    - a szeniorok nem csak sima ódoló ügynököket írnak, hanem tudományos kereső, refaktoráló, bugfix, security check stb., használhatnak MCP szervereket

## Keretrendszer

Hagyományosan Scrum alatt futna, de ez sokkal gyorsabb projekt, ami egészen más iterációt és tervezést követel.

## Kutatás - AI feladat, a legfontosabb!

A te feladatod, hogy végzel egy alapos és mindenre kiterjedő kutatást az interneten és megnézed, hogy találsz-e már ilyen felállású csapatot? Van már dokumentáció, publikáció, blogbejegyzés arról, hogy a Scrum keretrendszer, hogy változik meg, ha AI ügynök munkatársak lesznek a részei? Nem csak scrum, agilis keretrendszereket vizsgálj, fejlesztői környezeteket, amikből valós tapasztalatot meríthetsz és ami kapcsolható a témához. DevOps csapatokat, CI/CD folyamatokat, mindent, ami ide kapcsolódik, mert a keresésed eredménye sokat segíthet, ha a gyakorlatban működő megoldásokat találsz. Az is segít, ha azt találod, hogy a rendszer nem működött az adott környezetben és feladatra. Negatív tapasztalatokat is keress. Miket kell, lehet elkerülni?

A kutatásokról készíts egy vagy több magyar nyelvű dokumentumot, hivatkozásokkal. Az idegen szavakat, kifejezéseket ebből is a glossary-ba tedd bele. Ez támogathatja meg a projekt validitását.

## Kérdések

### Backlog

- Hagyományosan a PO darabolja (esetleg SM segít), majd a csapat finomítja
- Itt szerinted mi lenne a helyes irány? A PO megadja az irányt, célt és már a darabolást is egy backlog ügynökre bízná?
- Ha AI daraból, akkor hogy mérhető, hogy hatékonyabb-e, mint a PO darabolása?

Készíts erre megoldási ötleteket, szerinted mi működne a gyakorlatban?

### Sebesség

- Az AI ügynökök gyorsabban dolgoznak, mint az ember, hogy lehet úgy kiosztani a feladatokat, hogy ne csináljanak meg egyből 30 backlog elemet, miközben a szenior fejlesztők még csak 5-öt tudtak átnézni?
- Milyen léptékben adható át az ügynököknek a feladat?

Erre is készíts megoládási ötleteket.

### Biztonság
- A szenior fejlesztők feladata lenne a kód ellenőrzése, de szerencsés lenne mindél több biztonsági feladatot ügynökkel elvégezni.
- Milyen megoldások vannak erre? Egy ügynök és modell vagy több ügynök és több modell?

Erre is készíts megoládási ötleteket.

### Tesztek

- A tapasztalat azt mutatja, hogy egy refaktorálás közben az AI elronthatja a korábbi kódot. Javit és ront egyszerre.
- Hova és hogy lehet megfelelő mennyiségű tesztet beépíteni, hogy az ne csak iterált legyen a fejlesztés, hanem valóban inkrementális is.

Erre is készíts megoládási ötleteket.

### Scrum események

- Mi történik a Srum eseményekkel? (Daily, Retro, Demo)
- Mit kell megtartani, milyen új eseményt javasolsz?
- Be lehet az AI ügynököket vonni? Pl. rendszeres jelentés a munkájukról, ha igen, hogyan? Pl. jelentenek és visszajelzést kapnak, amit beépítenek és egyre jobbak lesznek
- Egy Demo esemény, amikor a csapat fejlődési ötleteket fogalmaz meg, hogy fog kinézni? Az AI is fogalmazhat meg ötletet? Hogy építhető be az AI-ba a visszajelzés? Hogy tudjuk ellenőrizni, hogy beépült?

Erre is készíts megoládási ötleteket.

### Teljesítmény

- Mit mérünk és hogy? Mi változik egy hagyományos scrum méréshez képest?
- Milyen korábbi mérőszámot érdemes megtartani, mert reális marad és milyen újakat kellene bevezetni?
- Ki határozza meg, hogy mi a jó? 
- Van értelme story pontozni? Vagy milyen más mérőszámot lehet bevezetni? A feladat komplex marad akkor is, ha Agent végzi, de mi határozza meg, hogy az számára nehéz vagy nem, hiszen egy hagyományos fejlesztőhöz képest bármilyen feladattal sokkal gyorsabban végez.

Erre is készíts megoládási ötleteket.

### csapatpszichológia

- Tuckman modell alkalmazható egy ilyen csapatra?
- Milyen modellt lehetne felállítani egy ilyen csapatra? Egy ilyen csapatnak is van dinamikája, fejlődési görbéje... de hogy jeleníthető meg? Hogy és mi mérhető?

Erre is készíts megoládási ötleteket.

### Jogi keretek - felelősségvállalás

- Milyen lehetőségek vannak arra, hogy az AI ne lépjen túl semmilyen határt, ne használjon olyan eszközt, tudást, bármit, ami tilos?
- Ki vállal felelősséget a fejlesztésért egy ilyen fejlesztés keretében?
- Ha át kell adni a fejlesztést, üzemeltetést pl. a helyi informatikai csapatnak, akkor miben változik egy ilyen csapatnál?
- A hibaelhárítás hogy történik? Ügynök, Szenior?

Erre is készíts megoládási ötleteket.

### Szerepkör változások és feladatok

- Miben változnak az egyes szerepkörök és feladatok?
- Mit adhat ki a kezéből az SM, PO?
- Milyen plusz feladatai vannak az SM-nek? Ha pl. egy ügynök nem jól végzi a munkáját, pl. sokat hibázik, akkor az SM a szenior fejlesztő felé eszkalálja a problémát vagy mi a helyzet ilyenkor?

Erre is készíts megoládási ötleteket.

### Dokumentáció

- Mit szükséges dokumentálni és kinek?
- Ki ellenőrzi? Ebben eddig is volt automatizálás, de hogy lehet úgy automatizálni, hogy jó legyen a minőség és verziókezelt legyen?
- Készül valami csapatindító dokumentum? Hasonlóan, mint a projekteknél, mi az, ami életre hívja a csapatot és meghatározza, hogy miért jött létre, mi a célja?

Erre is készíts megoládási ötleteket.

## Cél

A végső cél a fenti kérdéseken való gondolkodás, ötletelés, leginkább az SM szemszögéből. További cél egy SM segítő felület kidolgozása, ami gyorsan segít átlátni, hogy egy ilyen közegben miket kell csinálnia és hol tart benne. A hagyományos Scrumban volt ideje mindenre, de itt gyorsan kell látni és tudni, hogy mikor hol és mit kell beavatkozni. Például egy olyan felület, ahol ott van minden szükséges iteráció, jól átlatható, hogy éppen hol tartunk és kb. egy iterációval előre is látszik, hogy mi fog történni. Lehet akár egy cheklist is. Szándékosan nem írom azt, hogy Jira vagy hagyományos 2 hetes sprint, mert lehet, hogy a fenti megoldásban nincs ilyen. Lehet, hogy 3 vagy 5 napos iterációk vannak, mert az Ügynökök pár óra alatt elkészülnek és a Szeinoroknak eddig tart átnézni, újra visszaadni javításra stb. a kódot. A megoldás attól függ, hogy az ötletelés alatt mire jutunk, abból kell kialakítani. Könnyítse ás tegye áttekinthetővé az SM munkáját. Aztán ezt lehet később tovább fejleszteni.

Nem kell leprogramozni egy komplett alkalmazást, inkább csak egy példán keresztül megmutatni, hogy 1-2 iterációt, hogy kellene egy ilyen modellben végigvinni.

A cégvezetés azt szeretné, hogy gyorsan és hatékonyan dolgozzanak, megelőzve a versenytársakat, de még nincs kialakult kerete egy ilyen felállásnak. Ezt keressük és próbáljuk validálni a megvalósíthatóságát.

# Tech stack

Python és Streamlit kombinációra gondoltam, hogy minél egyszerűbb legyen, de javasolhatsz mást. Egyelőre csak magamnak készül.

Az elsődleges szakmai nyelv az angol, de magyarul is szerepeltesd, aminek van magyar megfelelője. A dokumentumok nyelve magyar legyen és az idegen szavakhoz készíthetsz egy külön glossary-t. Ne csak felsorolásokat használj, hanem kerek mondatokban válaszolj és fejtd ki a dokumentumot.

# Ami kimaradt

Ennyi jutott eszembe, egészítsd ki mindennel, ami a kutatásod során felmerül.