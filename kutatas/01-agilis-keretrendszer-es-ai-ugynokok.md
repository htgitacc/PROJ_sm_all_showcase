# 1. Agilis keretrendszerek és AI-ügynökök

## Mit kerestünk

Arra a kérdésre kerestünk választ, hogy létezik-e már dokumentált, működő Scrum- vagy más agilis csapatfelállás, amelyben az AI-ügynökök nem eszközként, hanem csapattagként vesznek részt a munkában. Külön figyeltünk arra, hogy a találatok mögött van-e valódi gyakorlat és mérés, vagy pusztán elméleti javaslatról van szó, illetve hogy a szakmai szervezetek (elsősorban a Scrum.org) foglaltak-e állást a kérdésben.

## Mit találtunk

A legfontosabb megállapítás az, hogy **az ügynökök tényleges elterjedtsége mérhető és gyors ütemben nő, a keretrendszerbeli szabályozásuk viszont lényegében hiányzik**. Robbes és szerzőtársai (S-27) 12 794 olyan GitHub-projektet vizsgáltak, amelyek 2025. augusztus 29. után jöttek létre, és legalább száz commitot, ötezer kódsort és tíz csillagot számláltak. Ezekben a friss projektekben a fájlszintű ügynökhasználat négyszer olyan gyakori, mint a korábbi, régebbi projektekből álló összehasonlító mintában, a konzervatív becslés szerinti összesített adopció pedig a korábbi valamivel több mint egynegyedről több mint kétharmadra emelkedett. A szerzők maguk is jelzik, hogy a heurisztikáik nem érzékelik a használat egészét, tehát ezek alsó becslések. Ez azt jelenti, hogy a mi pilotunk nem különcködés: az iparág már ott tart, ahová a brief el akar jutni, csak épp keretrendszer nélkül.

A keretrendszeri oldalon a legkonkrétabb anyagot a Scrum.org blogján Sanjay Saini publikálta (S-11). Az írás abból a feltevésből indul ki, hogy a csapat fele autonóm ügynök, és végigveszi a Scrum elszámoltathatóságait és eseményeit. A fejlesztők szerepe szerinte „ügynök-karmesterré" (agent orchestrator) alakul, akiknek elsődleges feladata az ügynökök által előállított logika validálása, miközben az emberi elszámoltathatóság nem delegálható. A Product Owner szerepét a szerző kifejezetten nem tartja gépre bízhatónak, mert az empátiát, érdekelti tárgyalást és üzleti stratégiai illesztést igényel; az ember adja a „miért"-et és a „mit"-et, az ügynök a „hogyan" jelentős részét. A Scrum Master feladatköre viszont bővül: a klasszikus emberi facilitáció mellé bejön a rendszerlogok és az API-korlátok figyelése, mert az akadály (impediment) immár algoritmikus is lehet.

Saini két olyan megállapítást is tesz, amely a mi kérdéseinkre közvetlenül válaszol. Az egyik a becslésre vonatkozik: szerinte hiba story pontot adni egy ügynöknek, mert a story pont emberi ráfordítást, kognitív komplexitást és bizonytalanságot mér, márpedig a fáradhatatlanul dolgozó ügynök nem „erőfeszít" ugyanabban az értelemben. Helyette a számítási költséget, a tokenfelhasználást és — hangsúlyosan — az **emberi validálási időt** javasolja mérni. A másik a sebességre vonatkozik, és lényegében megfogalmazza a projektünk központi problémáját: egy összetett algoritmust az ügynök három perc alatt megír, de az architektnek három órájába telhet biztonságosan átnézni és beolvasztani, tehát ha a sprintet az ügynök generálási sebességére tervezzük, kezelhetetlen torlódást hozunk létre az emberi review-nál.

Az események szintjén Saini javaslata az, hogy a Sprint Planning súlypontja a feladatkiosztásra (task attribution) helyeződjön át, és egy backlog-elem addig ne legyen „Ready", amíg az ügynök nem kapja meg a szükséges API-dokumentációt a promptjában. A Daily Scrumon nem az ügynökök „beszélnek", hanem az emberi fejlesztők nézik át az automatikus kimeneti naplókat, a bukott tesztsorozatokat és az alacsony megbízhatósági jelzéseket — az esemény eltérés-kezeléssé alakul. A Retrospektíven a csapat a rendszerpromptot írja újra, vagyis a klasszikus „eszközök és folyamatok" napirendi pont immár szó szerint a konfigurációs fájlok javítását jelenti.

### Mi történik a szerepkörökkel

A brief külön kérdésköre, hogy miben változnak a szerepek, mit adhat ki a kezéből a Scrum Master és a Product Owner, és mi a teendő, ha egy ügynök sokat hibázik. A talált irodalom erre részben ad választ.

Saini (S-11) szerint a **Product Owner** a „miért"-et és a „mit"-et adja, és ez az elszámoltathatóság elvi okból marad emberi. Amit kiadhat a kezéből, az a mechanikus darabolás — feltéve, hogy a specifikáció, amelyből a darabolás történik, emberi jóváhagyást kap (S-30).

A **Scrum Master** feladatköre bővül: a rendszernaplók és az erőforráskorlátok figyelése bekerül az akadályelhárításba, mert az akadály lehet algoritmikus is. Amit kiadhat a kezéből, az az adatgyűjtés és a státuszriportolás, mert ezt az ügynökök naplói és mérőszámai automatikusan előállítják (lásd a 7. dokumentumot).

A **hibázó ügynök** kérdésére a szakirodalom nem eszkalációs, hanem **rendszerszemléletű** választ ad, és ez a legfontosabb átkeretezés az egész témában. A MAST-taxonómia szerint (S-10) a többügynökös rendszerek hibáinak 43,8 százaléka rendszertervezési eredetű — vagyis a hiba jellemzően nem az ügynök „teljesítménye", hanem a konfigurációja. Ehhez illeszkedik a szabályfájl-alapú tanulási hurok (S-26, lásd a 10. dokumentumot): a visszatérő hibaosztály nem fegyelmi, hanem konfigurációs ügy. A Scrum Master feladata tehát nem az, hogy „eszkalálja az ügynököt a szeniorhoz", hanem hogy **láthatóvá tegye a hibaosztály ismétlődését**, és rávegye a csapatot arra, hogy a szabályfájlon javítson. Az eszkaláció akkor indokolt, ha ugyanaz a hibaosztály a szabály felvétele után is visszatér — mert az már architektúra- vagy eszközválasztási kérdés.

Külön érdemes kiemelni, hogy a Scrum értékeit is újraértelmezi: a nyitottság látható gépi naplókat jelent, a tisztelet az emberi validálási szűk keresztmetszet elismerését, a bátorság pedig azt, hogy a csapat visszautasítja azt az inkrementumot, amely nem felel meg a Definition of Done-nak.

A specifikáció-vezérelt fejlesztés (spec-driven development) irányzata ugyanezt a problémát a folyamat elejéről közelíti meg. A GitHub Spec Kit (S-30) nyílt forrású eszközkészlete a specifikációt teszi meg egyetlen igazságforrásnak, amelyből az ügynök generál, tesztel és validál, és ehhez explicit lépéssorozatot ad: az alapelvek rögzítése (`constitution`), a specifikáció megírása (`specify`), a technikai terv (`plan`), a feladatokra bontás (`tasks`), a megvalósítás (`implement`), végül annak felmérése, hogy a kódbázis mennyire tart együtt a specifikációval (`converge`). Két részlet kiemelten érdekes számunkra: az **alapelvek külön dokumentumba** kerülnek — ez a mi csapatindító dokumentumunk közeli rokona —, és a **darabolás önálló, ellenőrizhető lépés**, nem pedig a kódolás melléktermeke. Erre a 10. és a 11. dokumentumban visszatérünk.

## Negatív tapasztalatok és buktatók

A legfontosabb negatívum az, hogy **az általunk talált keretrendszeri javaslatok egyike sem támaszkodik mérésre**. Saini írása (S-11) tapasztalt gyakorló szakember okfejtése, nem kontrollált vizsgálat; a Scrum.org blogja pedig szerkesztett, de nem lektorált felület. Nem találtunk olyan publikációt, amely egy konkrét, AI-ügynököket csapattagként foglalkoztató Scrum-csapat teljesítményét összehasonlította volna egy hagyományos csapatéval. Ez a hiány önmagában is a pilotunk mellett szóló érv, de óvatosságra int: nincs mihez viszonyítanunk.

A második buktató a szervezeti szintű kudarcokból látszik. A gyakran idézett MIT-jelentés (S-32) arra jutott, hogy a vállalati generatív AI-pilotok 95%-a nem hozott mérhető eredményhatást, ám ezt a számot módszertani kritika érte: a vizsgálat 52 interjúra és 153 vezetői kérdőívre épült, a sikert kizárólag közvetlen, hat hónapon belüli eredménykimutatási hatásként definiálta, és a hatékonysági vagy minőségi javulást nem számította be. A tanulság nem az, hogy „az AI nem működik", hanem az, hogy **a pilotok jellemzően a mérés hiánya vagy rossz megválasztása miatt bizonyulnak sikertelennek**. Ez a mi projektünkre nézve konkrét feladat: a siker kritériumát előre és több dimenzióban kell rögzíteni.

A harmadik buktató a nyílt forrású közösségek tapasztalata (S-24). Yang, He és Zhou 67 nagy láthatóságú projekt szabályzatait elemezve azt találták, hogy az AI-generált hozzájárulások áradata több ismert projekt karbantartói kapacitását meghaladta. A cikk idéz egy matplotlib-karbantartót, aki szerint az AI megváltoztatja a kódgenerálás és a kód átnézése közötti költségarányt. Amikor a Node.js egyik technikai bizottsági tagja egy 19 000 soros, ügynökkel generált módosítást nyújtott be, több mint nyolcvan fejlesztő írt alá petíciót az AI-val segített hozzájárulások projekt szintű tiltásáért. Ez a legtisztább figyelmeztetés arra, hogy mi történik, ha az ügynökök kimenetét nem korlátozzuk a review-kapacitáshoz.

## Mit jelent ez a mi projektünkre

Először is: a Scrum keretrendszert nem kell elvetnünk, de az eseményeinek célja megváltozik. A Daily nem állapotjelentés, hanem eltéréskezelés; a Retrospektív részben konfigurációjavítás. Ezt a 8. és a 11. dokumentumban részletezzük.

Másodszor: a Product Owner elszámoltathatósága ember marad, a darabolás viszont nem feltétlenül. A brief kérdésére („a PO megadja az irányt, és a darabolást egy backlog-ügynökre bízza?") a szakirodalom nem ad kész választ, de a specifikáció-vezérelt megközelítés (S-30) mutat egy köztes utat: az ügynök daraboljon, de egy ember által jóváhagyott specifikációból, és a darabolás eredménye maga is review tárgya legyen.

Harmadszor, és ez a legfontosabb: **a tervezés alapegysége nem az ügynök sebessége, hanem az emberi validálási kapacitás.** Ezt a megállapítást a 3. dokumentum méréssel is alátámasztja.

Negyedszer: mivel a pilotunk mérési háttér nélküli terepen mozog, a saját mérésünk maga is szállítmány. Amit a 7. dokumentumban javaslunk, azt a pilot alatt ténylegesen fel kell venni, különben ugyanabba a hibába esünk, mint a MIT-jelentésben szereplő szervezetek.

## Nyitott kérdések

Nem találtunk publikált adatot arra, hogy egy AI-ügynökökkel dolgozó csapat milyen összetételnél (hány ember, hány ügynök) teljesít a legjobban; Saini 50/50 aránya illusztráció, nem mérési eredmény. Szintén nyitott, hogy a Scrum elszámoltathatóságai közül a Scrum Master szerepe hogyan alakul hosszabb távon, mivel az általunk talált források erről kizárólag véleményt fogalmaznak meg. Végül nincs adatunk arra, hogy a belső, alacsony kockázatú termék (mint a mi intranetünk) mennyiben viselkedik másként, mint egy ügyfélnek szállított rendszer.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-11 | Sanjay Saini: *AI Augmented Scrum Framework: When Half Your Team is Autonomous Agents*, Scrum.org, 2026-03-08 | C |
| S-24 | Yang, He, Zhou: *To Ban or not to Ban? How Open Source Projects Govern GenAI Contributions*, arXiv:2603.26487v2, 2026-07-30 | A |
| S-27 | Robbes, Matricon, Degueule, Hora, Zacchiroli: *Agentic Very Much! Adoption of Coding Agent in New GitHub Projects*, arXiv:2606.07448v1, 2026-06-05 | A |
| S-30 | GitHub Spec Kit — spec-driven development toolkit | C |
| S-32 | MIT: *The GenAI Divide: State of AI in Business 2025* és annak módszertani kritikája | C |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
