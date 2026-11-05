# Glossary — idegen szakkifejezések magyarázata

A dokumentumokban az elsődleges szakmai nyelv az angol, mert a hivatkozott irodalom is angol nyelvű. Az alábbi jegyzék minden bevezetett kifejezéshez megadja a magyar megfelelőt és a kifejtett magyarázatot. A jegyzék betűrendben követi az angol alakot.

---

**Agent steering** — *ügynökirányítás.* Az az interakciótípus, amikor egy ember nem elbírálja a kódot, hanem utasítást ad az ügynöknek, hogy javítsa meg (például „@agent javítsd ki a lint hibát"). A kutatás szempontjából azért fontos, mert formailag review-hozzászólásnak látszik, tartalmilag viszont nem minőségi ítélet. Duma és szerzőtársai mérése szerint az ügynöki pull requesteknél az emberi hozzászólások negyede ilyen (lásd [03](03-review-es-atbocsatokepesseg.md)).

**Agentic AI** — *ügynöki mesterséges intelligencia.* Olyan nyelvi modellre épülő rendszer, amely nem csupán válaszol, hanem célt értelmez, részlépésekre bont, eszközöket választ és futtat, majd a visszajelzés alapján módosítja a tervét. A puszta kódkiegészítő asszisztenstől az különbözteti meg, hogy önállóan cselekszik a fejlesztői környezetben.

**AGENTS.md** — *ügynökutasítás-fájl.* A repozitórium gyökerében elhelyezett, nyílt formátumú Markdown fájl, amelyben a projekt megadja az ügynököknek a szükséges kontextust: build- és tesztparancsokat, kódolási konvenciókat, tiltásokat. A Linux Foundation alá tartozó Agentic AI Foundation gondozza. Lásd [10](10-dokumentacio-es-tudasatadas.md).

**AI literacy** — *AI-jártasság.* Az EU mesterségesintelligencia-rendeletének 4. cikkében szereplő fogalom: azok a készségek, ismeretek és megértés, amelyek lehetővé teszik az AI-rendszerek tájékozott alkalmazását, valamint a lehetőségek és kockázatok felismerését. 2025. február 2. óta jogi kötelezettség biztosítani a személyzet megfelelő szintű jártasságát. Lásd [09](09-jogi-es-felelossegi-keret.md).

**AI theater** — *AI-színház.* Yuval Yeret fogalma arra a helyzetre, amikor a csapat teljes kapacitáson dolgozik alacsony értékű, nem validált munkán: nagy az aktivitás, kicsi az üzleti hatás. Lásd [11](11-iteracios-ritmus.md).

**Automation bias** — *automatizálási elfogultság.* Az a torzítás, amikor az ember azért fogadja el a gép javaslatát, mert a gép mondta, nem azért, mert megvizsgálta. Az ember–ügynök csapatmunka egyik központi kockázata.

**Characterization test** — *karakterizációs teszt.* Olyan teszt, amelyet nem az elvárt, hanem a **jelenlegi** viselkedés rögzítésére írunk, mielőtt a kódhoz nyúlnánk. Refaktorálás előtt ez a legolcsóbb védőháló: ha a viselkedés véletlenül megváltozik, a teszt elbukik.

**Code churn** — *kódforgás.* Annak a friss kódnak az aránya, amelyet rövid időn belül (jellemzően két héten belül) újraírnak. Emelkedése éretlen vagy elhamarkodott commitokra utal.

**Code coverage** — *kódlefedettség.* Annak mérőszáma, hogy a tesztek futása közben a kód hány százaléka futott le. Fontos korlátja, hogy csak a végrehajtást méri, azt nem, hogy a teszt állít-e bármit érdemit — AI-generált teszteknél ezért különösen megtévesztő. Lásd [06](06-teszteles-es-regresszio.md).

**Context engineering** — *kontextusmérnökség.* Annak tervezése, hogy egy modellhívás pontosan milyen bemenetet kapjon: mely fájlokat, mely korábbi döntéseket, milyen utasításokat. A prompt megírásánál tágabb, rendszerszintű tevékenység.

**Cramér-féle V** — a khí-négyzet-próbához tartozó hatásméret-mutató kategoriális adatoknál. Nagyjából 0,1 gyenge, 0,3 közepes, 0,5 erős együttjárást jelez. A [03](03-review-es-atbocsatokepesseg.md) dokumentumban ezzel jellemezzük, mennyire eltérő az emberi és a gépi pull requestek elbírálása.

**Cohen-féle kappa** — az annotátorok közötti egyetértés mérőszáma, amely kiszűri a véletlen egyezést. A 0,8 fölötti érték erős egyetértést jelent; a MAST-taxonómia 0,88-as értéke ezért tekinthető megbízhatónak.

**Definition of Done (DoD)** — *a „kész" meghatározása.* A Scrum azon megállapodása, hogy milyen feltételek teljesülése esetén tekinthető egy elem elkészültnek. Ügynökös közegben ez válik a legfontosabb emberi kontrollponttá.

**DORA metrics** — *DORA-mérőszámok.* A DevOps Research and Assessment kutatás négy kulcsmutatója: szállítási gyakoriság, változtatás átfutási ideje, változtatási hibaarány és helyreállítási idő. Előnyük, hogy a rendszer viselkedését mérik, nem az emberi erőfeszítést, ezért AI-korban is torzításmentesek maradnak.

**DX Core 4** — a DORA, a SPACE és a DevEx kereteit egyesítő mérési keretrendszer négy dimenzióval: sebesség, hatékonyság, minőség és hatás. Lásd [07](07-metrikak.md).

**Excessive agency** — *túlzott cselekvési jogkör.* Az OWASP LLM-listájának egyik kockázata: az ügynök több jogosultságot, funkciót vagy autonómiát kap, mint amennyi a feladatához szükséges, így a hibája vagy az eltérítése nagyobb kárt okoz.

**Flow metrics** — *áramlási mérőszámok.* A munkaelemek mozgását mérő mutatók: átfutási idő, sorhossz, folyamatban lévő munka mennyisége. A becslésalapú mérőszámok (például a story point) alternatívái.

**Goal hijacking** — *célesetérítés.* Olyan támadás, amelyben a bemenetbe rejtett utasítás az ügynököt eredeti céljától eltérő cselekvésre veszi rá.

**Grounded theory** — *megalapozott elmélet.* Kvalitatív kutatási módszer, amelyben a fogalmi rendszer az adatokból építkezve, nem előzetes hipotézisből alakul ki. A MAST-taxonómia így született.

**Harness engineering** — *hevedermérnökség.* A kontextusmérnökség kiterjesztése: nem csupán a modell bemenetét tervezzük, hanem a modell köré épített teljes mechanizmuskészletet — utasításfájlokat, eszközöket, alügynököket, ellenőrzési lépéseket. Lásd [10](10-dokumentacio-es-tudasatadas.md).

**Human–agent teaming (HAT)** — *ember–ügynök csapatmunka.* Az a kutatási terület, amely az emberekből és autonóm ügynökökből álló csapatok működését vizsgálja. Lásd [08](08-csapatdinamika.md).

**MAST (Multi-Agent System Failure Taxonomy)** — *többügynökös rendszerek hibataxonómiája.* A UC Berkeley kutatócsoportjának osztályozási rendszere, amely 14 hibamódot sorol három kategóriába: rendszertervezési hibák, ügynökök közötti fel nem zárkózás, és feladat-verifikáció. Lásd [04](04-multi-agent-tapasztalatok.md).

**Mutation score** — *mutációs pontszám.* Annak aránya, hogy a tesztsorozat hány szándékosan bevitt hibát (mutánst) vesz észre. A kódlefedettségnél lényegesen szigorúbb és informatívabb minőségjelzés.

**Mutation testing** — *mutációs teszt.* Az az eljárás, amelyben egy eszköz apró, szándékos hibákat visz a kódba, majd megnézi, hogy a tesztsorozat elbukik-e. Azt a kérdést teszi fel, hogy „ha ez a sor rosszul viselkedne, észrevennénk-e?".

**Orchestrator–worker pattern** — *karmester–munkás minta.* Többügynökös architektúra, amelyben egy vezető ügynök stratégiát alkot és részfeladatokat oszt ki specializált alügynököknek.

**Pickup time** — *felvételi idő.* Az az idő, amely a pull request megnyitásától addig telik, amíg egy bíráló ténylegesen elkezd vele foglalkozni. A LinearB adatai szerint az AI-generált pull requesteknél ez a szakasz nyúlik meg leginkább.

**Prompt injection** — *prompt-befecskendezés.* Olyan támadás, amelyben a modell által feldolgozott adatba (weboldalba, fájlba, hibaüzenetbe) utasításnak álcázott szöveget rejtenek, hogy a modellt eltérítsék. Az OWASP LLM-listájának első helyezettje.

**Pull request (PR)** — *beolvasztási kérelem.* Egy elkülönített ágon készült változtatáscsomag, amelyet a szerző beolvasztásra ajánl. Ez a kódellenőrzés bevett egysége.

**Refactoring** — *refaktorálás.* A kód belső szerkezetének javítása a külső viselkedés megváltoztatása nélkül. Az AI-val segített fejlesztésben mérhetően visszaszorult, ami a karbantarthatóság romlásának fő oka.

**Shadow AI** — *árnyék-AI.* Az AI-eszközök nem engedélyezett, a szervezet látókörén kívüli használata. Mérési szempontból azért probléma, mert a hivatalos telemetria alábecsüli a tényleges használatot.

**Shared mental model (SMM)** — *közös mentális modell.* A csapat tagjainak összehangolt elképzelése a feladatról, az eszközökről és egymás képességeiről. Az ember–ügynök csapatmunka kutatásában a hatékonyság egyik központi feltétele.

**SPACE framework** — a fejlesztői produktivitás öt dimenziós modellje (elégedettség, teljesítmény, aktivitás, kommunikáció, hatékonyság), amely szándékosan több nézőpontot ír elő az egyetlen mérőszám helyett.

**Spec-driven development (SDD)** — *specifikáció-vezérelt fejlesztés.* Az a megközelítés, amelyben a specifikáció az egyetlen igazságforrás, és ebből generál, tesztel és validál az ügynök. Lásd [11](11-iteracios-ritmus.md).

**Story point** — *történetpont.* A Scrumban használt relatív becslési egység, amely az emberi ráfordítást, a komplexitást, a kockázatot és a bizonytalanságot együtt fejezi ki. Ügynöki munkára az irodalom szerint nem alkalmazható értelmesen.

**Subagent / verification subagent** — *alügynök / verifikáló alügynök.* Külön kontextusban futó, meghatározott részfeladatot végző ügynök. A verifikáló változata az egyetlen olyan többügynökös minta, amelyre kódolási feladatnál gyártói ajánlás van: a fő ügynök implementál, a verifikáló futtatja a teszteket.

**Swarming** — *rajzás, közös rávetődés.* Az a gyakorlat, amikor a csapat több tagja egyszerre veti rá magát ugyanarra a folyamatban lévő elemre, hogy azt lezárja, ahelyett hogy mindenki új munkát kezdene. A folyamatban lévő munka korlátozásának szokásos következménye és célja.

**T⁴ framework** — *T⁴ keretrendszer.* Az ember–ügynök csapatmunka négyfázisú modellje: csapatalakítás, feladat- és szerepfejlődés, csapatfejlődés, csapatjavítás. A Tuckman-modell helyett kínál vázat olyan csapatokra, amelyeknek gépi tagjai is vannak. Lásd [08](08-csapatdinamika.md).

**Tautological test** — *tautologikus teszt.* Olyan teszt, amely az implementációt önmagához méri ahelyett, hogy egy függetlenül levezetett elvárt viselkedéshez hasonlítaná. Soha nem bukhat el, hacsak a kód nem dob kivételt, ezért értéktelen — miközben a lefedettségi mutatóban rendes tesztként jelenik meg.

**Throughput** — *átbocsátás.* Adott idő alatt leszállított munkaelemek mennyisége. A DORA 2025-ös jelentése szerint az AI-adopció ezzel pozitívan korrelál — a stabilitással viszont negatívan.

**Tuckman-modell** — a csoportfejlődés klasszikus négyfázisú modellje (forming, storming, norming, performing), magyarul alakulás, viharzás, normázás, működés. Emberi csoportokra készült; gépi csapattagokra való alkalmazhatósága nem igazolt.

**Upstream starvation** — *felfelé irányuló kiéheztetés.* Az a helyzet, amikor nincs elég kész, validált munka, ezért a fejlesztők alacsony prioritású elemeket húznak be, hogy ne álljanak. Ügynökös csapatnál különösen valószínű.

**WIP limit (work in progress limit)** — *folyamatban lévő munka korlátja.* Az egyszerre megkezdhető munkaelemek felső határa. Ügynökös közegben ez a legfontosabb szabályozó eszköz, mert a valódi korlát az emberi review-kapacitás, nem az ügynökök átbocsátása.
