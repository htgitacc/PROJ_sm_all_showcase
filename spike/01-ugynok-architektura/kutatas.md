# Célzott kutatás — mi változott a lezárt kutatás óta?

> A spike kutatási része. Nem ismétli meg a [lezárt kutatást](../../kutatas/04-multi-agent-tapasztalatok.md), csak az új tényezőkre keres rá: van-e friss adat az egy ügynök kontra több kérdésre, az orkesztrátorra, a skillekre, az MCP-re és a független ellenőrzésre. A források a [spike forrásjegyzékében](forrasok.md) vannak, `U-nn` jelöléssel; a lezárt kutatás forrásaira `S-nn`-ként hivatkozom.
>
> Minden megállapításnál jelölöm, hogy **mért adat** vagy **gyakorlati beszámoló**, és mit **erősít**, **árnyal** vagy **cáfol** a lezárt kutatásból.

## 1. Egy ügynök vagy több a kódolásban

A lezárt kutatás nyitott kérdésként hagyta, hogy van-e kontrollált összehasonlítás egyszálú és orkesztrátoros kódolás között. Közvetlenül kódolásra ilyet most sem találtam, de egy általános, kontrollált kísérletsorozat már van.

A Google Research 180 ügynökkonfigurációt mért négy benchmarkon ([U-01](forrasok.md)). **Mért adat:** szekvenciális, lépésről lépésre épülő feladatokon minden többügynökös változat 39–70%-kal rontott az egy ügynökhöz képest; párhuzamosítható feladaton a központosított (orkesztrátoros) koordináció 80,9%-kal javított. A mechanizmusra is ad számot: egymástól függetlenül dolgozó ügynökök a hibát 17,2-szeresére erősítik, mert senki nem ellenőrzi a másikét; a központosított koordináció ezt 4,4-szeresre fogja vissza.

Ez **erősíti** a lezárt kutatás következtetését (S-07, S-09): az alkotó, kódot író útvonal jellemzően szekvenciális, ott egy szál a jó; a párhuzamosítható, kutatás-jellegű munkánál éri meg több ügynök. Új benne, hogy most már a hibaerősítés mértéke is mérve van.

A másik irányból az Agyn nevű rendszer ([U-02](forrasok.md)) menedzser–kutató–fejlesztő–bíráló csapata 7,4 százalékponttal jobb lett egy együgynökös alapnál egy SWE-bench változaton. **Gyakorlati beszámoló, abláció nélkül:** nem derül ki, hogy a javulás a szerepekből vagy egyszerűen abból jön-e, hogy van egy kötelező bírálati kör. Ez a lezárt kutatás „verifikáló alügynök” mintájával (S-08) összhangban van: a többszörözés az ellenőrzésnél hoz.

## 2. Orkesztrátor és alügynökök a gyakorlatban

Az orkesztrátor-minta igazolt nyeresége továbbra is a kutatási feladatokra vonatkozik (S-09); kódolásra friss, kontrollált mérést nem találtam. A friss gyakorlati anyag a **hibamódokat** dokumentálja:

- **Csendes üres válasz** ([U-03](forrasok.md), egyetlen dokumentált eset): egy alügynök sok anyag elolvasása után üres választ adott hibajelzés nélkül, és az orkesztrátor nem tudta megkülönböztetni a hibát a „nincs mit jelenteni” esettől. Ez a lezárt kutatás „korai győzelem” hibamódjának (S-08) rokona: az orkesztrátor egy ügynök **jelentésére** hagyatkozik, nem ellenőrizhető kimenetre.
- **A rendszer, nem a modell** ([U-04](forrasok.md), strukturált áttekintés): a látszólagos modellhibák jelentős része a modell körüli rendszerből jön — állapotkezelés, jogosultság, ellenőrzés, bírálati felület. Ez **erősíti** a lezárt kutatás MAST-adatát (S-10: a hibák 43,8%-a rendszertervezési eredetű), és azt az irányt, amit a projekt is követ: a hevedert (a folyamatot, a kapukat, a felületet) kell jól megtervezni, nem a modelltől várni a megoldást.

## 3. Agent Skills

2025 decemberében a `SKILL.md`-alapú képességcsomag nyílt szabvány lett, és több kódoló eszköz átvette ([U-05](forrasok.md)). A lezárt kutatás még csak azt rögzíthette, hogy kevés repó használja (S-25). Azóta mérések is vannak:

- **A gondozott skill segít, a magának írt nem** ([U-06](forrasok.md), mért adat). Az ember által írt, gondozott skillek átlagosan 16,2 százalékponttal javítottak — de **szoftverfejlesztésben csak kb. 4,5 ponttal**, és a feladatok egy részén rontottak. A modell által saját magának írt skillek átlagosan **nem hoztak javulást**. A fókuszált, két-három modulos skill jobb volt a hosszú dokumentációnál.
- **Valósághű helyzetben a haszon zsugorodik** ([U-07](forrasok.md), mért adat): ha az ügynöknek magának kell sok skill közül megtalálnia a jót, a haszon a skill nélküli szint közelébe esik; célzott finomítással visszahozható.
- **A skill is kód, és hibás lehet** ([U-08](forrasok.md), nagy mintás elemzés): a vizsgált `SKILL.md` fájlok 91,8%-ában volt kimutatható hiba.

**Mit jelent ez a modellünkre:** a skill a koncepció *szabályfájljának* (`AGENTS.md`, SZ-06, SZ-07) strukturált formája, és a mérés pontosan azt a feltételt erősíti meg, amit a koncepció a szabályokra már előír: **ember írja vagy hagyja jóvá**, és visszamutat arra az eseményre, amelyből született (S-26). Az ügynök által magának írt skill a mérések szerint nem ér semmit. Új tényező viszont, hogy a skill **bírálandó termék**: a 91,8%-os hibaarány miatt a skill módosítása ugyanúgy a bírálati keretből fogyaszt, mint a kód.

## 4. MCP mint kapu és mint támadási felület

A lezárt kutatás az MCP-t a jogosultságok oldaláról érintette (S-13: a jogosultság szűkítése az elsődleges védelem). Azóta az MCP-re szabott mérések jelentek meg:

- **Tool poisoning** ([U-09](forrasok.md), mért adat): ha egy tool leírásába utasítást rejtenek, a modellek nagy arányban követik — a legrosszabb esetben 72,8%-ban. **A jobb képességű modellek gyakran sérülékenyebbek**, mert jobban követik az utasításokat, és a támadást szinte sosem utasítják el.
- **A kliensek védelme eltér** ([U-10](forrasok.md)): a fejlesztői eszközök egy része erős korlátokat alkalmaz, más része könnyen megtéveszthető.
- **Automatikus indítás** ([U-11](forrasok.md), iparági jegyzet): több kódoló eszköz a projektben definiált MCP szervereket a mappa megbízhatóvá tétele után magától elindította — a repóból érkező tool így ellátási lánc kockázat.

**Mit jelent ez a modellünkre:** az MCP-tool alkalmas arra, hogy az ügynök a munka közben **gyors visszajelzést** kérjen a gépi kapuktól (tesztek, statikus elemzés, méret). Ám **a kötelező kapu nem lehet az ügynök hívásán múló tool**: ha az ügynök dönti el, meghívja-e, és ő olvassa ki az eredményt, visszajön a „korai győzelem”. A kötelező kapu a beolvasztás előtti, ügynöktől független futtatás (CI) marad; az MCP ennek a tükre a munka közben. Az MCP szervereket rögzített verzióval, belső forrásból, minimális jogosultsággal kell futtatni, és a tool-leírások maguk is a biztonsági bírálat tárgyai.

## 5. Független ellenőrzés: modellcsalád vagy friss kontextus?

A lezárt kutatás és a koncepció úgy döntött, hogy a verifikáló és a biztonsági cáfoló **más modellcsaládból** jöjjön, mint az implementáló (S-14, S-15). Ehhez most egy kontrollált friss mérés érkezett, amely **árnyalja** a döntést ([U-12](forrasok.md), mért adat):

- **Friss munkamenetben** a saját modell bírálata F1-ben nem tért el szignifikánsan egy csúcskategóriás más modell bírálatától. A függetlenség jelentős része tehát abból jön, hogy a bíráló **nem látja a gyártás előzményét**, nem csak abból, hogy más gyártó modellje.
- A két bíráló **részben más hibákat** talál, és **egy saját + egy más modelles bírálat** több hibát fogott (56,7%), mint két saját (42,7%). A változatosságnak tehát van értéke, ha két bírálat fér bele.
- **Egy könnyűsúlyú más modell nem volt jobb** a saját modellnél. Ez **ellentmond** a koncepció 09. dokumentumában javasolt költségcsökkentésnek, hogy a cáfoló lépcső olcsóbb modellre állítható. A mérés alapján az olcsóbb bíráló a függetlenséget nem pótolja.

Egy másik mérés ([U-13](forrasok.md)) szerint, ha **determinisztikus ellenőrző** dönt (gépileg ellenőrizhető feladat), az önpreferencia kicsi. Ez **erősíti** a koncepció elvét, hogy a kapu kimenete bináris és determinisztikus legyen: ahol lehet, nem egy modell véleménye dönt.

## 6. Költség

A lezárt kutatás 3–10-szeres (S-08) és kutatási rendszernél 15-szörös (S-09) tokenszorzót rögzített. Friss, független, ismételt mérést nem találtam; a gyakorlati becslések szélesen szórnak. Egy költségmodellezés ([U-14](forrasok.md), gyakorlati beszámoló) arra figyelmeztet, hogy a naiv szorzás felülbecsül: a közös repó miatt a később induló ügynökök gyorsítótárazott bemenetet használnak, és a rutin részfeladat olcsóbb modellre tehető. A korábbi tartomány tehát irányadó marad, felső becslésként.

## Összegzés: mit erősít, mit árnyal, mit cáfol

| Lezárt kutatás állítása | Friss adat | Viszony |
|---|---|---|
| Alkotó útvonalon egy szál (S-07, S-09) | szekvenciális feladaton a több ügynök 39–70%-kal ront ([U-01](forrasok.md)) | **erősíti** |
| Ellenőrzésnél érdemes többszörözni (S-08, S-15) | csapat bírálati körrel +7,4 pont ([U-02](forrasok.md)); saját + más bíráló több hibát fog ([U-12](forrasok.md)) | **erősíti** |
| A függetlenséget a más modellcsalád adja (S-14, S-15) | friss kontextusban a saját modell sem rosszabb szignifikánsan ([U-12](forrasok.md)) | **árnyalja** |
| A cáfoló olcsóbb modellre tehető (koncepció 09.) | a könnyűsúlyú más modell nem jobb a sajátnál ([U-12](forrasok.md)) | **cáfolja** |
| A hibák fele rendszertervezési (S-10) | a modellhibák jelentős része a hevederből jön ([U-04](forrasok.md)) | **erősíti** |
| Szabályfájl ember jóváhagyásával (S-26) | gondozott skill segít, magának írt nem ([U-06](forrasok.md)) | **erősíti, és kiterjeszti a skillekre** |
| A jogosultság szűkítése az elsődleges védelem (S-13) | tool poisoning akár 72,8% ([U-09](forrasok.md)) | **erősíti, új támadási felülettel** |
