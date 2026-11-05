# 2. Termelékenység — empirikus adatok és ellenbizonyítékok

## Mit kerestünk

A brief abból a feltevésből indul ki, hogy az AI-ügynökök gyorsabban dolgoznak az embernél, és a projekt egésze ennek a gyorsaságnak a kezelhetővé tételéről szól. Ezt a feltevést szándékosan **cáfolni** próbáltuk: kifejezetten olyan kontrollált kísérleteket és nagy mintás méréseket kerestünk, amelyek a sebességnövekedést kétségbe vonják, vagy a sebesség árát mutatják meg. Aki egy állásinterjún vagy egy vezetői egyeztetésen ezt a modellt védi, annak először ezeket a számokat kell ismernie.

## Mit találtunk

### A legfontosabb ellenbizonyíték: a METR-kísérlet

Az egyetlen olyan valódi randomizált kontrollált kísérlet, amelyet találtunk, a METR 2025. júliusi vizsgálata (S-01). Tizenhat tapasztalt nyílt forrású fejlesztő dolgozott a **saját**, régóta karbantartott kódbázisán (átlagosan 22 ezer csillag, egymillió sor fölött), 246 valós feladaton, amelyeket véletlenszerűen soroltak „AI használható" és „AI tiltott" csoportba. Az eredmény az volt, hogy az AI engedélyezése mellett a feladatok elvégzése **19 százalékkal tovább tartott**.

Ennél is fontosabb az észlelési rés. A fejlesztők előzetesen 24 százalékos gyorsulásra számítottak, és a kísérlet után — miután ténylegesen lassabbak lettek — még mindig 20 százalékos gyorsulást éltek meg. Vagyis a résztvevők nem tudták megítélni a saját termelékenységüket, és a hiba iránya következetes volt: az AI gyorsabbnak *érződik*, mint amilyen. A szerzők a lassulás fő okaként az alacsony megbízhatóságot jelölik meg: az idő jelentős része a kimenet ellenőrzésével telt.

A tanulmány szerzői maguk fogalmazzák meg a legfontosabb korlátot, és ezt kötelező vele együtt idézni: **nem** állítják, hogy az AI általában nem gyorsítja a fejlesztőket. A mintájuk nem reprezentálja a fejlesztői munka többségét, és az eredmény más lehet kevésbé tapasztalt fejlesztőknél vagy ismeretlen kódbázison. A vizsgált helyzet — tapasztalt szakember a saját, jól ismert, kiforrott kódjában — éppen az a helyzet, amelyben az AI a legkevesebb hozzáadott értéket adja, mert a fejlesztő fejében már ott van a kontextus, amit az ügynöknek fel kell építenie.

### A nagy mintás kép: gyorsabb, de instabilabb

A DORA 2025-ös, mesterséges intelligenciával segített szoftverfejlesztésről szóló jelentése (S-02) csaknem ötezer szakember válaszára és több mint száz óra kvalitatív kutatásra épül. Adatai szerint a válaszadók 90 százaléka használ AI-t a munkájában, és több mint 80 százalékuk úgy érzi, hogy ez növelte a termelékenységét — miközben 70 százalékuk csak részben bízik meg az AI által írt kódban, tehát minden harmadik válaszadó kevéssé vagy egyáltalán nem bízik benne.

A jelentés két kulcsösszefüggése ellentétes irányba mutat. Az AI-adopció **pozitívan** korrelál az átbocsátással (throughput) és a termékteljesítménnyel — ez a 2024-es méréshez képest megfordult. Ugyanakkor **továbbra is negatívan** korrelál a szállítási stabilitással: az AI mellett nő az instabilitás. A jelentés összefoglaló üzenete, hogy az AI erősítőként (amplifier) viselkedik, azaz felnagyítja a szervezet meglévő erősségeit és gyengeségeit. Ehhez kapcsolódik a jelentés hét képességből álló modellje, amelyben többek között szerepel az AI-politika tisztázása, az AI bekötése a szervezet belső kontextusába, az alapgyakorlatok elsőbbsége és a „biztonsági hálók megerősítése".

### Az ár: a karbantarthatóság eróziója

A GitClear két, egymásra épülő elemzése a kódbázis szerkezetén méri ugyanezt. A 2025-ös jelentés (S-03) 211 millió megváltoztatott kódsort vizsgált 2020 januárja és 2024 decembere között, a Google, a Microsoft, a Meta és vállalati ügyfelek repozitóriumaiból. Eszerint a refaktoráláshoz köthető sorok aránya a 2021-es 25 százalékról 2024-re tíz százalék alá csökkent, a másolással-beillesztéssel keletkezett sorok aránya pedig 8,3-ról 12,3 százalékra nőtt. 2024 volt az első év, amelyben a másolt kód mennyisége meghaladta az áthelyezett — vagyis refaktorálásra utaló — kódét.

A 2026-os folytatás (S-04) 623 millió változtatást elemzett a 2023–2026 közötti időszakban, és a trend erősödését mutatta ki. A blokk-duplikáció a 2023-as 40,3-ról 73,0-ra emelkedett (plusz 81 százalék), az áthelyezett — vagyis valódi refaktorálásra utaló — kód aránya a 2022-es 21 százalékról 3,8 százalékra zuhant, a másolás-beillesztés pedig 15,7 százalékra nőtt. A fájlok közötti függvénykapcsoltság 2023 óta 35 százalékkal csökkent, a hosszú távú, legacy jellegű karbantartás pedig a 2022-es szint 26 százalékára esett vissza.

### Az ellenpont: ahol az AI mérhetően használ

A képet kiegyensúlyozza Dell'Acqua és szerzőtársai előzetesen regisztrált terepkísérlete a Procter & Gamble-nél (S-20), amelyben 776 szakembert osztottak véletlenszerűen csoportokba aszerint, hogy AI-val vagy anélkül, egyénileg vagy párban dolgoztak-e termékfejlesztési feladaton. Az eredmény szerint az **AI-val dolgozó egyén elérte az AI nélküli kétfős csapat teljesítményét**, tehát az AI a csapatmunka bizonyos előnyeit helyettesíteni tudta. Emellett lebontotta a funkcionális silókat: AI nélkül a kutatás-fejlesztési szakemberek technikai, a kereskedelmiek üzleti javaslatok felé húztak, AI-val ez a különbség eltűnt.

Ez azért fontos, mert megmutatja, hol nyer az AI: **új dolog létrehozásában és a szakterületi korlátok átlépésében**, nem pedig egy kiforrott rendszer óvatos módosításában.

## Negatív tapasztalatok és buktatók

Az első és legsúlyosabb buktató az **önértékelés megbízhatatlansága** (S-01). Ha a saját csapatunk azt fogja mondani a retrospektíven, hogy gyorsabbak lettek, az önmagában semmit sem bizonyít — a METR résztvevői pontosan ugyanezt mondták, miközben lassabbak voltak. Ebből következik, hogy a pilot értékelése nem alapulhat kizárólag a csapat érzetén.

A második buktató az, hogy **a gyorsulás és a stabilitás egymás rovására mozog** (S-02). Aki csak az átbocsátást méri, sikert fog látni ott is, ahol valójában adósságot halmozott fel.

A harmadik buktató, hogy a minőségromlás **nem azonnal jelentkezik**. A GitClear adatai (S-03, S-04) szerkezeti mutatókat mérnek — duplikációt, kapcsoltságot, refaktorálási arányt —, amelyek hatása hónapokkal később, a karbantartási költségben csapódik le. Egy néhány hetes pilot ebből semmit nem lát, ha nem méri kifejezetten.

Fontos megjegyezni a GitClear-adatok korlátját is: a szolgáltató a saját elemzőtermékéhez kapcsolódó kutatást publikál, a megfigyelt együttjárás pedig nem bizonyítja, hogy okozati kapcsolat van az AI használata és a szerkezeti romlás között. Az időbeli egybeesés erős, de nem kontrollált kísérlet.

## Mit jelent ez a mi projektünkre

A pilot céljának megfogalmazását ezek az adatok érdemben módosítják. Nem azt kell bizonyítanunk, hogy „az AI gyorsabb" — ez a legjobb esetben is feltételes. Azt kell megvizsgálnunk, hogy **a gyorsaságot át tudjuk-e alakítani leszállított, stabil és karbantartható értékké**, mert az irodalom szerint pontosan ez a lépés szokott elmaradni.

Ebből három konkrét következtetés adódik. Egy: a pilot mérési tervének a stabilitási és karbantarthatósági mutatókat ugyanolyan súllyal kell tartalmaznia, mint a sebességet — erre a 7. dokumentum tesz javaslatot. Kettő: mivel az intranet zöldmezős fejlesztés, a METR-kísérlet legrosszabb esete (tapasztalt fejlesztő kiforrott kódbázison) ránk kevésbé érvényes, tehát az AI-tól valószínűleg tényleges gyorsulást várhatunk — de ez az előny a projekt előrehaladtával, a kódbázis érésével csökkenni fog. Három: a duplikáció és a refaktorálási arány mérése nem opcionális, mert ezek az egyetlen korai jelzések arra, hogy adósságot halmozunk.

## Nyitott kérdések

Nem találtunk olyan mérést, amely a **zöldmezős** fejlesztésre nézve adna kontrollált eredményt; a METR-kísérlet ennek éppen az ellenkezőjét vizsgálta. Szintén nyitott, hogy a szerkezeti romlás (S-04) mennyiben tudható be az AI-nak, és mennyiben az iparág egyéb változásainak. Végül nincs adatunk arról, hogy a mi méretünkhöz hasonló, néhány fős csapatoknál hogyan alakulnak ezek az összefüggések — a hivatkozott mérések nagy szervezetekre és nagy repozitóriumokra vonatkoznak.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-01 | METR: *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*, 2025-07-10 | A |
| S-02 | DORA / Google Cloud: *State of AI-assisted Software Development 2025*, 2025-09-23 | B |
| S-03 | GitClear: *AI Copilot Code Quality — 2025 Research*, 211 M kódsor, 2020–2024 | B |
| S-04 | GitClear: *The Maintainability Gap — 2026 AI Code Quality Research*, 623 M változtatás, 2023–2026 | B |
| S-20 | Dell'Acqua és mtsai: *The Cybernetic Teammate: A Field Experiment on Generative AI Reshaping Teamwork and Expertise*, NBER w33641 / Organization Science | A |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
