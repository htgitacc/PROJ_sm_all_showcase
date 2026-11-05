# 10. Dokumentáció és tudásátadás

## Mit kerestünk

A brief három kérdést tesz fel: mit szükséges dokumentálni és kinek, ki ellenőrzi és hogyan automatizálható úgy, hogy a minőség jó és a dokumentum verziókövetett legyen, illetve készül-e valamiféle csapatindító dokumentum. Ezért egyrészt azt néztük meg, milyen dokumentációs gyakorlatok alakultak ki ténylegesen az ügynökös fejlesztés körül, másrészt azt, hogyan lehet a visszajelzést tartósan beépíteni az ügynökök működésébe.

Ez a dokumentum azért fontosabb, mint amilyennek elsőre látszik: az ügynökös közegben **a dokumentáció nem melléktermék, hanem a rendszer működésének bemenete**.

## Mit találtunk

### Egy új dokumentumtípus: a gépnek szóló projektdokumentáció

A legjelentősebb fejlemény az, hogy megjelent egy olyan dokumentumtípus, amelynek **elsődleges olvasója nem ember, hanem ügynök**. Az `AGENTS.md` nyílt formátum a repozitórium gyökerében egyetlen Markdown fájlban adja meg az ügynöknek a projektkontextust, a build- és tesztparancsokat, a kódolási konvenciókat és a határokat. A formátumot a Linux Foundation alá tartozó Agentic AI Foundation gondozza, több mint 60 ezer nyílt forrású projekt használja, és több mint húsz ügynökös eszköz olvassa (S-31).

Ennek elterjedtségét mérés is alátámasztja. Galster és szerzőtársai AIware '26 konferenciacikke (S-25) 2853 GitHub-repozitórium elemzésével vizsgálta, hogy a fejlesztők hogyan konfigurálják az ügynökös eszközöket. A szerzők nyolc konfigurációs mechanizmust azonosítottak a statikus kontextustól a végrehajtható és külső integrációkig, és három fő megállapításra jutottak:

1. **A kontextusfájlok uralják a terepet**, és gyakran ezek az egyetlen konfigurációs mechanizmus egy repozitóriumban; az `AGENTS.md` interoperábilis szabványként emelkedik ki.
2. **A fejlettebb mechanizmusokat — a képességeket (skills) és az alügynököket — kevés repozitórium alkalmazza**, és a képességek is túlnyomórészt statikus utasításokra, nem végrehajtható parancsfájlokra épülnek.
3. Az egyes eszközök körül **eltérő konfigurációs gyakorlatok** alakulnak ki.

A cikk bevezeti a **hevedermérnökség** (harness engineering) fogalmát, amely a kontextusmérnökség kiterjesztése: nem csupán a modell kontextusát tervezzük meg, hanem a köré épített teljes mechanizmuskészletet. A szerzők ugyanakkor problémákat is azonosítanak: az utasítások dokumentálása következetlen, az ügynök viselkedése nehezen hibakereshető pusztán a konfiguráció felől, nincs bevett módszer az utasítások hatásosságának tesztelésére, és hiányzik az eszköztámogatás a komplex hevederek kezeléséhez.

### Hogyan épül be a visszajelzés az ügynökbe — és honnan tudjuk, hogy beépült?

Ez a brief egyik legélesebb kérdése („Hogy építhető be az AI-ba a visszajelzés? Hogy tudjuk ellenőrizni, hogy beépült?"), és találtunk rá közvetlen, mérésekkel dokumentált választ.

Aggarwal és Ghalaty (Microsoft) 2026 júliusi tanulmánya (S-26) egy zárt hurkú keretrendszert ír le, amelynek alapelve egyszerű: **minden elfogadott review-észrevétel egy önellenőrzési szabállyá alakul**. Ha a bíráló észrevesz valamit, amit az ügynök elmulasztott, a mintázatot kodifikálni kell, hogy legközelebb az ügynök maga vegye észre.

A megvalósítás elemei:

- **Strukturált utasításfájl** Markdownban, viselkedési szabályokra, kódolási sztenderdekre, önellenőrzési listára, antimintákra és munkafolyamat-kiváltókra tagolva. A fájl monoton nő, ahogy új szabályok gyűlnek.
- **Szabályreprezentáció metaadatokkal**: azonosító, kategória, a kiváltó forrás, hatókör, megszorítás, indoklás, az ellenőrzőlistához való hozzárendelés és a visszakövethetőség a konkrét review-eseményhez.
- **Visszacsatolási hurok**: az ügynök kódot generál, lefuttatja az önellenőrzési listát, emberi visszajelzést kap, az elfogadott észrevételek szabállyá válnak, a frissített fájl a következő munkamenetben töltődik be.
- **Automatizált validálás**: gépi ellenőrzések vigyáznak a fájl épségére, a metaadatok érvényességére és a sémának való megfelelésre.

A mért eredmények egy négyhetes, több mint 35 mikroszolgáltatásra kiterjedő bevezetésből:

- A szabálykészlet 5-ről 18 viselkedési szabályra nőtt, mellette 15-nél több nyelvspecifikus kódolási sztenderd és egy 15 pontos önellenőrzési lista jött létre. A fájl mérete mintegy 4809 szó, ami a kontextusablak kevesebb mint 5 százaléka.
- Kilenc követett hibaosztálynál, 74 kumulált szabály utáni előfordulási lehetőség mellett **nulla visszaesést** figyeltek meg a megfigyelési ablakban.
- 36 elemzett pull requestnél a review-észrevételeknek már csak **14 százaléka szólt mechanikus helyességről**, 66 százaléka architektúráról, API-tervezésről és teljesítményről — vagyis a szabályok felszabadították a bírálókat a magasabb szintű kérdésekre.
- A szabályok eredete: emberi bíráló 39, automatizált eszköz 22, önfelfedezett mintázat 22, éles hiba 17 százalék.
- A megfigyelt tudásátadások 60 százaléka átlépett repozitórium-, eszköz- vagy feladattípus-határt.

A szerzők a korlátokat is kimondják: egyetlen csapat, négyhetes megfigyelési ablak, és **kontrollcsoport nélküli** vizsgálat. Ezért ezt B szintű forrásként kezeljük — iparági terepmérés, nem kontrollált kísérlet.

Ennek a modellnek a fontossága abban áll, hogy **mérhető választ ad a brief kérdésére**: a visszajelzés akkor épült be, ha az adott hibaosztály többé nem fordul elő, és ez a szabályfájl verziótörténetéből és a hibaosztályok követéséből ellenőrizhető.

### A specifikáció mint dokumentum

A specifikáció-vezérelt fejlesztés (S-30) azt a megközelítést képviseli, hogy a specifikáció maga legyen az egyetlen igazságforrás, amelyből az ügynök generál, tesztel és validál. Négy szakaszra bontja a munkát: specifikáció (a „mit" és a „miért"), terv (a technikai megvalósítás iránya), feladatok (a darabolás) és megvalósítás. Ez a mi „ki darabolja a backlogot" kérdésünkre is szerkezeti választ ad: a darabolás egy dokumentumból, nem fejből történik, tehát felülvizsgálható és verziókövethető.

### Nyílt forrású gyakorlatok

Yang, He és Zhou (S-24) azt találták, hogy a projektek az AI-ra vonatkozó szabályokat több csatornán rögzítik: hozzájárulási útmutatóban, biztonsági szabályzatban, hibajegy- és pull request-sablonokban, AI-irányelvekben (például `AGENTS.md`-ben) és nyilvános bejelentésekben. A szerzők három kormányzási irányultságot és tizenkét stratégiát azonosítanak; a lényeg számunkra az, hogy **a szabályozás szétszórtsága maga is probléma** — nincs egységes hely, ahol a szabályok laknának.

## Negatív tapasztalatok és buktatók

Az első buktató, hogy a kontextusfájlok dokumentálása következetlen, az ügynök viselkedése pedig nehezen hibakereshető pusztán a konfiguráció felől (S-25). Ha valami nem működik, nehéz megmondani, hogy a szabály hiányzik, rosszul van megfogalmazva, vagy az ügynök figyelmen kívül hagyta.

A második buktató, hogy **nincs bevett módszer az utasítások hatásosságának tesztelésére** (S-25). A szabályfájl írása ma inkább mesterség, mint mérnökség.

A harmadik buktató a szabályfájl kordában tartása. A hivatkozott keretrendszerben (S-26) a fájl monoton nő; négy hét után még csak a kontextusablak öt százalékát foglalta, de hosszabb távon ez nyilvánvalóan nem tartható. A szabályok elévülésének és kigyomlálásának kérdését az irodalom nem oldja meg.

A negyedik buktató, hogy a fejlettebb mechanizmusokat (képességek, alügynökök) kevés projekt használja (S-25), tehát ezekre nincs kiforrott gyakorlat — aki bevezeti, úttörő, nem követő.

Az ötödik buktató a régi ismerős: a **dokumentáció elavulása**. Ügynökös közegben ez súlyosabb, mint korábban, mert az elavult kontextusfájl nemcsak félretájékoztatja az embert, hanem aktívan rossz irányba vezeti az ügynököt.

## Mit jelent ez a mi projektünkre

### Mit dokumentáljunk és kinek

A dokumentáció három közönségre válik szét, és ezt érdemes explicitté tenni:

| Közönség | Dokumentum | Ki írja | Ki ellenőrzi |
|---|---|---|---|
| **Ügynök** | `AGENTS.md` / `CLAUDE.md`: build- és tesztparancsok, konvenciók, tiltások, önellenőrzési lista | szenior fejlesztő | gépi séma-ellenőrzés + review |
| **Csapat** | architektúradöntési feljegyzések (ADR), iterációs jegyzőkönyv, szabályváltozások naplója | aki a döntést hozta | Scrum Master a felülvizsgálat meglétére, szenior a tartalomra |
| **Átvevő / üzemeltető** | üzemeltetési leírás, jóváhagyási nyomvonal, modell- és eszközjegyzék, licencellenőrzés eredménye | csapat közösen | átadási ellenőrzőlista |

### A visszacsatolási hurok mint kötelező elem

A pilot egyik legfontosabb gyakorlata a szabályfájl-alapú tanulási hurok legyen (S-26). Konkrétan:

1. Minden **elfogadott** review-észrevétel után döntsünk arról, hogy általánosítható-e szabállyá. Nem minden az; a döntést az teszi olcsóvá, hogy csak egy igen/nem kérdés.
2. A szabály kapjon **azonosítót, indoklást és visszamutatást** arra a review-észrevételre, amelyből született. Ez teszi később auditálhatóvá.
3. Az iterációs visszatekintésen nézzük meg, **mely hibaosztályok tűntek el** és melyek tértek vissza. A visszatérő hibaosztály azt jelenti, hogy a szabály nem működik — nem azt, hogy az ügynök „rossz".
4. A szabályfájl legyen **verziókövetve, és a változtatása is menjen review-n keresztül**, mint bármely más kód.

Ez egyben a brief „ellenőrizzük, hogy beépült-e" kérdésére adott válasz: a bizonyíték a hibaosztály eltűnése, nem az ügynök ígérete.

### Csapatindító dokumentum

A brief kérdésére — készül-e valami, ami életre hívja a csapatot — a válasz igen, és a kutatás alapján ennek legalább a következőket kell tartalmaznia:

- **Miért létezik a csapat és mi a pilot sikerkritériuma.** A MIT-jelentés (S-32) tanulsága szerint pontosan ennek hiánya a leggyakoribb kudarcok oka; a sikerkritériumot előre és többdimenziósan kell rögzíteni.
- **Ki miért felelős**, és kifejezetten: ki hagyja jóvá a beolvasztást (lásd a 9. dokumentumot).
- **Az ügynökök jogosultsági szintjei** — mi szabad jóváhagyás nélkül, mi jóváhagyással, mi tilos.
- **A folyamatban lévő munka korlátai** és az iteráció ritmusa (lásd a 3. és 11. dokumentumot).
- **A Definition of Done**, benne a tesztelési és biztonsági kapukkal.
- **Az AI-jártassági terv** — ez a 4. cikk (S-22) miatt nem opcionális.
- **A mérési terv**: mit veszünk fel, mikor, ki nézi.
- **A kilépési feltétel**: mikor mondjuk ki, hogy a pilot nem működik. Ennek hiánya a leggyakoribb módja annak, hogy egy kísérlet határozatlan idejű projektté váljon.

### Az automatizálás és a minőség egyensúlya

A brief kérdése, hogyan automatizáljuk a dokumentációt úgy, hogy a minőség jó és verziókövetett legyen. A kutatás alapján a válasz az, hogy **az automatizálás a szabályok betartatására, ne a tartalom előállítására irányuljon**. Gépesíthető a séma ellenőrzése, a kötelező mezők megléte, a hivatkozások épsége, a paranccsal futtatható példák tesztelése és az elavulási figyelmeztetés (ha a kód változott, de a hozzá tartozó dokumentum nem). Az ügynök által generált dokumentumszöveg viszont ugyanolyan review-t igényel, mint a kód — sőt, a 6. dokumentum tanulsága szerint jobbat, mert a hihetően hangzó, de pontatlan szöveget nehezebb kiszúrni, mint a hibás kódot.

## Nyitott kérdések

Nem találtunk módszert a **kontextusfájlok hatásosságának mérésére** — ezt maguk a kutatók is hiányként nevesítik (S-25). Szintén nyitott, hogyan kezeljük a szabályfájl növekedését hosszú távon, és mikor kell egy szabályt visszavonni. Végül a hivatkozott tanulási hurok eredményei (S-26) egyetlen csapat négy hetéből származnak, kontrollcsoport nélkül, tehát a nulla visszaesés lehet a rövid megfigyelési ablak műterméke is.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-25 | Galster, Mohsenimofidi, Lulla, Abubakar, Treude, Baltes: *Harness Engineering for Agentic AI Coding Tools: An Exploratory Study*, AIware '26, arXiv:2602.14690 | A |
| S-26 | Aggarwal, Ghalaty (Microsoft): *Self-Improving AI Coding Agents Through Accumulated Behavioral Rules: A Closed-Loop Framework*, arXiv:2607.13091, 2026-07-13 | B |
| S-24 | Yang, He, Zhou: *To Ban or not to Ban?*, arXiv:2603.26487v2 | A |
| S-30 | GitHub Spec Kit — specifikáció-vezérelt fejlesztés | C |
| S-31 | AGENTS.md nyílt formátum, Agentic AI Foundation (Linux Foundation) | C |
| S-32 | MIT: *The GenAI Divide* és kritikája | C |
| S-22 | EU AI Act 4. cikk — AI-jártasság | A |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
