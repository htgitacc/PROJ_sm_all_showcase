# 6. Kormányzás — jogosultságok, felelősség, dokumentáció, átadás

> Ez a dokumentum kutatási alapú tervezési javaslat, nem jogi tanácsadás. A pilot éles indítása előtt a benne foglaltakat a szervezet jogi és adatvédelmi funkciójával kell egyeztetni.
>
> A jelölésről: `S-nn` hivatkozás mögött kutatási forrás áll ([kutatas/forrasok.md](../kutatas/forrasok.md)); ahol nincs hivatkozás, ott saját tervezési döntésről van szó, és a szöveg ezt kimondja.

## A kormányzás egyetlen alapelve

A jogi és felelősségi kérdések tucatnyi részletre bomlanak, de mindegyik ugyanabból az egy elvből vezethető le: **a felelősséget az az ember viseli, aki a munkát beengedi a rendszerbe.** Az ügynök nem jogalany, tehát nem lehet felelős; a szervezet felelőssége pedig csak akkor kezelhető, ha a láncban van egy azonosítható emberi döntés.

Ez az elv egybevág a nyílt forrású közösségek kialakult gyakorlatával, ahol a visszatérő szabály az, hogy a hozzájáruló felel a redisztribúciós jogokért, a licenckompatibilitásért és a jogszerű eredetért — vagyis a felelősség azon marad, aki benyújtja, nem az eszközön, amellyel készült (S-24). Ugyanide mutat a szabályozás iránya is: a szerzői jogi elemzés szerint a puszta prompt megadása nem elegendő az emberi szerzőséghez, és a tisztán AI által előállított anyag nem áll szerzői jogi védelem alatt (S-33).

A modell ebből egyetlen, kikényszerített szabályt csinál: **minden beolvasztásnak van megnevezett emberi jóváhagyója, és ez a nyom a verziókezelőben marad.** Ez a pilot legolcsóbb és leghatásosabb egyetlen intézkedése, mert semmilyen technológiát nem igényel, viszont utólag mindent visszakereshetővé tesz.

## Az ügynökök jogosultsági szintjei

A brief azt kérdezi, milyen lehetőségek vannak arra, hogy az AI ne lépjen túl semmilyen határt. A leghatásosabb válasz nem az, hogy megkérjük rá, hanem az, hogy **a jogosultság eleve nincs meg**. Az OWASP ügynöki listája elsődleges fenyegetésként nevesíti az azonosság- és jogosultsági visszaélést, valamint az eszközök visszaélésszerű használatát (S-13) — mindkettő ellen a legerősebb védelem a jogkör szűkítése, mert amit az ügynök nem tud megtenni, azt tévedésből vagy eltérítés hatására sem teheti meg.

A modell háromszintű jogosultsági rendszert használ. A besorolás **saját szerkesztésű**, de minden tétele levezethető a fenyegetési modellből.

| Szint | Mi tartozik ide |
|---|---|
| **Szabad, jóváhagyás nélkül** | a repozitórium olvasása, elemzés, tesztfuttatás elkülönített környezetben, ág létrehozása, javaslat és pull request készítése, dokumentáció írása |
| **Emberi jóváhagyással** | új függőség behozatala, adatbázis-sémamódosítás, konfiguráció- és környezeti változó módosítása, build- és telepítési folyamat módosítása, a szabályfájl módosítása |
| **Tiltott** | hozzáférés éles adathoz és titkokhoz, írás külső szolgáltatásba, jogosultsági és biztonsági beállítások módosítása, a naplózás kikapcsolása vagy a beolvasztási védelmek megkerülése |

A középső szint egyik tételére érdemes külön kitérni. A **szabályfájl módosítása** szándékosan került a jóváhagyandó kategóriába: mivel a tanulási hurok éppen ezen a fájlon keresztül működik ([03-esemenyek-es-tanulas.md](03-esemenyek-es-tanulas.md)), egy magát szabadon módosítani képes ügynök elvben ki tudná írni magából a rá vonatkozó korlátozásokat. Ez nem fenyegetettségi paranoia, hanem egyszerű higiénia: a szabályfájl ugyanolyan bírálandó tárgy, mint bármely más kód.

Fontos kimondani, hogy a repozitóriumszintű utasításfájlok — az `AGENTS.md` és társai — **puha korlátot** jelentenek: az utasítás nem kikényszerített, hanem követendő szöveg. A kemény korlátot a jogosultságkezelés, a hálózati elzárás és a beolvasztási védelem adja. A kettőt nem szabad összekeverni; az utasításfájl azt írja le, mit *akarunk*, a jogosultság azt, mi *lehetséges*.

## Szabályozási környezet

A jogi hátteret a [kutatas/09-jogi-es-felelossegi-keret.md](../kutatas/09-jogi-es-felelossegi-keret.md) fejti ki, itt csak az szerepel, aminek közvetlen működési következménye van.

A legfontosabb, mert ránk **most is vonatkozik**: az EU mesterségesintelligencia-rendeletének 4. cikke 2025. február 2. óta alkalmazandó, és megköveteli, hogy az AI-rendszereket üzembe helyező szervezet gondoskodjon a személyzete és a nevében eljáró más személyek megfelelő szintű AI-jártasságáról, figyelembe véve a technikai tudásukat, tapasztalatukat, képzettségüket és az alkalmazás összefüggéseit (S-22). A kötelezettség nem konkrét szintet ír elő, hanem „megfelelőt" a szerepekhez mérten — de a *dokumentált szándék* hiánya nehezen védhető. A csapatindító dokumentumnak ezért tartalmaznia kell egy AI-jártassági tervet.

A másik, ami a pilot horizontján túlmutat: az új európai termékfelelősségi irányelv a termék fogalmát kiterjeszti a szoftverre és az AI-rendszerekre, tehát ezekre is a vétkességtől független felelősség szabályai vonatkoznak; az átültetési határidő 2026. december 9., és az azt követően forgalomba hozott vagy üzembe helyezett termékekre alkalmazandó (S-37). A mi intranetünk belső használatra készül, nem kerül forgalomba, ezért ez a rezsim várhatóan közvetlenül nem alkalmazandó rá — a brief viszont kifejezetten azt kéri, hogy úgy kezeljük a projektet, mintha külső ügyfélnek szállítanánk. Ezért a folyamatba már most beépítjük azokat az elemeket, amelyeket egy külső szállítás megkövetelne: az eredetnyomozást, a naplózást és a dokumentált felülvizsgálatot. Ez **saját döntés**, és a pilot költségét némileg növeli, cserébe viszont a modell felskálázása nem kezdődik nulláról.

Végül érdemes az ISO/IEC 42001 szerkezetét ellenőrzőlistaként használni. A szabvány négy területet fed le: a kockázatkezelést, az irányítást és elszámoltathatóságot, az átláthatóságot és dokumentálást, valamint az életciklus-kontrollokat (S-23). Tanúsítás a pilotnál nyilvánvalóan nem cél, de ha a csapatindító dokumentum ezt a négy területet lefedi, akkor egy későbbi komolyabb megfelelési munka nem üres lappal indul.

## Dokumentációs rend

A dokumentáció ügynökös közegben nem melléktermék, hanem **a rendszer működésének bemenete** — ez az egyik legfontosabb szemléletbeli különbség a hagyományos működéshez képest. A modell ezért három közönségre bontja a dokumentációt, és mindegyikhez más ellenőrzési mód tartozik.

| Közönség | Dokumentum | Ki írja | Ki ellenőrzi |
|---|---|---|---|
| **Ügynök** | `AGENTS.md`: build- és tesztparancsok, konvenciók, tiltások, önellenőrzési lista, antiminták | szenior fejlesztő | gépi sémaellenőrzés, majd emberi bírálat |
| **Csapat** | architektúradöntési feljegyzések, iterációs jegyzőkönyv, a szabályváltozások naplója | aki a döntést hozta | Scrum Master a meglétére, szenior a tartalmára |
| **Átvevő** | üzemeltetési leírás, jóváhagyási nyomvonal, modell- és eszközjegyzék, licencellenőrzés eredménye | a csapat közösen | átadási ellenőrzőlista |

Az `AGENTS.md` formátumválasztásnak empirikus alapja van: 2853 GitHub-repozitórium elemzése szerint a kontextusfájlok uralják a konfigurációs terepet, gyakran ezek az egyetlen mechanizmus egy repozitóriumban, és az `AGENTS.md` interoperábilis szabványként emelkedik ki (S-25). A formátumot a Linux Foundation alá tartozó Agentic AI Foundation gondozza, és több mint hatvanezer nyílt forrású projekt használja (S-31). Ugyanez a kutatás azt is megmutatja, hogy a fejlettebb mechanizmusokat — a képességeket és az alügynököket — kevés projekt alkalmazza, tehát ezek bevezetésével úttörők vagyunk, nem követők.

### Automatizálás a dokumentációban

A brief azt kérdezi, hogyan automatizáljuk a dokumentációt úgy, hogy a minőség jó és a tartalom verziókövetett legyen. A válaszunk az, hogy **az automatizálás a szabályok betartatására irányuljon, ne a tartalom előállítására.**

Gépesíthető a séma ellenőrzése, a kötelező mezők megléte, a hivatkozások épsége, a dokumentumban szereplő, paranccsal futtatható példák tényleges lefuttatása, és az elavulási figyelmeztetés — vagyis annak jelzése, ha a kód megváltozott, de a hozzá tartozó dokumentum nem. Ezek mind determinisztikus ellenőrzések, tehát nem fogyasztanak a bírálati keretből.

Az ügynök által generált dokumentumszöveg viszont ugyanolyan bírálatot igényel, mint a kód — sőt, valamivel szigorúbbat, mert a hihetően hangzó, de pontatlan mondatot nehezebb kiszúrni, mint a hibás kódot. Ez **saját megfontolás**, amelyre nem találtunk mérést, de következik abból, amit a tautologikus tesztekről tudunk ([02-minosegi-kapuk.md](02-minosegi-kapuk.md)).

## A csapatindító dokumentum

A brief kérdésére — készül-e valami, ami életre hívja a csapatot — a válasz igen, és ez a modell egyik legfontosabb szállítmánya. A dokumentum sablonja a [sablonok/csapatindito-dokumentum.md](sablonok/csapatindito-dokumentum.md) fájlban található; itt azt rögzítjük, miért kell benne lennie mindannak, ami benne van.

A dokumentum kilenc dolgot rögzít. Elsőként azt, hogy **miért létezik a csapat, és mi a pilot sikerkritériuma**; ennek hiánya a leggyakoribb kudarcok oka, amit a vállalati AI-pilotokról szóló jelentés kritikájával együtt is megerősít (S-32). Másodikként azt, hogy **ki miért felelős**, és kifejezetten azt, hogy ki hagyja jóvá a beolvasztást. Harmadikként az **ügynökök jogosultsági szintjeit**, a fenti táblázat szerint. Negyedikként a **folyamatban lévő munka korlátait és az iteráció ritmusát**. Ötödikként a **Definition of Done**-t. Hatodikként az **AI-jártassági tervet**, a 4. cikk miatt (S-22). Hetedikként a **mérési tervet**, azzal a kikötéssel, hogy az adatgyűjtés csapatszinten aggregált, egyéni bontás nélkül. Nyolcadikként a **döntéshozatali rendet**: mi tartozik a Product Ownerhez, mi a szeniorokhoz, és mi az, amiben a Scrum Master dönthet egyedül. Kilencedikként pedig — és ez a leggyakrabban kihagyott elem — a **kilépési feltételt**: mikor mondjuk ki, hogy a pilot nem működik. Ennek hiánya a leggyakoribb módja annak, hogy egy kísérlet határozatlan idejű projektté váljon.

Érdemes megjegyezni, hogy a specifikáció-vezérelt fejlesztés eszközkészletében is szerepel egy ehhez hasonló, alapelveket rögzítő dokumentum (S-30) — vagyis nem egyedi ötletről van szó, hanem egy formálódó gyakorlatról.

## Átadás az üzemeltetésnek

A brief azt kérdezi, miben változik az átadás, ha ilyen csapat fejlesztett. A válasz az, hogy **az átadás tárgya bővül**, és ez a bővülés nem formalitás.

A hagyományos csomag — a kód, a dokumentáció és az üzemeltetési leírás — mellé négy dolog kerül be. Az első az **ügynökök konfigurációja és a szabályfájlok**, mert e nélkül az átvevő csapat nem tudja ugyanazon a módon karbantartani a rendszert; a szabályfájl gyakorlatilag a projekt felhalmozott tapasztalatának hordozója (S-26). A második a **jóváhagyási nyomvonal**, vagyis hogy melyik változtatást ki hagyta jóvá. A harmadik a **felhasznált modellek és eszközök jegyzéke**, verziószámmal, mert egy későbbi hiba vizsgálatánál ez lehet a kiindulópont. A negyedik a **licenc- és eredetellenőrzés eredménye**.

Az átadás legnagyobb kockázata az, amit **átadási szakadéknak** nevezünk: ha az átvevő olyan kódot kap, amelyet nem ember írt, és amelynek részleteit senki nem értette meg mélységében, akkor az első incidens első lépése a kód megértése lesz — pontosan akkor, amikor erre a legkevesebb idő van. Ez ellen két dolog véd. Az egyik az architektúradöntési feljegyzések vezetése, mert ezek magyarázzák a *miérteket*, amelyeket a kódból nem lehet visszaolvasni. A másik az, hogy az átadás előtti utolsó iterációban az átvevő csapat egy tagja ténylegesen bíráljon néhány elemet — ez **saját javaslat**, és a bírálati keretből fogyaszt, de olcsóbb, mint az első éles incidens.

## Hibaelhárítás

A brief kérdése az, hogy a hibaelhárítást ügynök vagy szenior végezze. A modell **rétegzett választ** ad.

Az első szintű diagnosztikát — a naplók összegyűjtését, a hiba reprodukálását, a lehetséges okok felsorolását, a kapcsolódó változtatások visszakeresését — végezheti ügynök, és ez érdemi időnyereség, mert ez a munka nagyrészt mechanikus. A **javítás jóváhagyása és az éles beavatkozás azonban emberi döntés marad.**

Ennek nemcsak felelősségi, hanem nagyon gyakorlati oka is van. Éles incidens közben a legrosszabb pillanat kideríteni, hogy egy ügynök korán zárta le a vizsgálatot — márpedig a korai lezárás a többügynökös rendszerek dokumentált hibamódja, amely a mért kudarcok 6,2 százalékát adta (S-10). Incidens alatt a hibás magabiztosság drágább, mint a lassúság.

Ehhez kapcsolódik egy szabály, amelyet érdemes előre kimondani: **incidens alatt a jogosultsági szintek nem lazulnak.** A „gyorsan adjunk hozzáférést az ügynöknek, hogy megoldja" a legveszélyesebb pillanatban nyitná ki azt, amit a modell zárva tart.

## Nyitott kérdések

Nem találtunk jogi elemzést arról, hogy a belső, nem forgalomba hozott szoftverre az új termékfelelősségi rezsim pontosan hogyan vonatkozik; ez a tagállami átültetés után válik megválaszolhatóvá. Nem tudjuk, milyen dokumentáció elegendő az AI-jártassági kötelezettség teljesítéséhez, mert a rendelet „megfelelő szintet" ír elő, konkrét mércét nem. És nincs kialakult gyakorlat arra, hogyan kell az AI-val készült kód eredetét olyan mélységben nyomon követni, amely egy jogvitában bizonyító erejű lenne.
