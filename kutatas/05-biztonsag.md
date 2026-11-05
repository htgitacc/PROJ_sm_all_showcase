# 5. Biztonság — fenyegetési modell és az ellenőrző ügynökök architektúrája

## Mit kerestünk

A brief két kérdést tesz fel: milyen megoldások vannak arra, hogy a biztonsági feladatokat minél nagyobb részben ügynökök végezzék, és hogy ehhez egy ügynök és egy modell kell-e, vagy több. Ehhez két irányban kutattunk. Egyrészt a fenyegetési oldalon: milyen új kockázatot hoz be maga az, hogy ügynökök dolgoznak a kódbázisunkon. Másrészt az eszközoldalon: mennyire megbízhatóan képesek az ügynökök sebezhetőséget találni, és milyen architektúra mellett.

## Mit találtunk

### A fenyegetési modell két rétege

Az OWASP GenAI Security Project két listát tart karban, és a mi helyzetünkben mindkettő releváns. Az **OWASP Top 10 for LLM Applications** 2025-ös kiadása (S-12; a dokumentum megjelölése szerint „Version 2025", kiadva 2024. november 18-án) a nyelvi modellre épülő alkalmazások tíz legfontosabb kockázatát rögzíti: prompt-befecskendezés (LLM01), érzékeny információ kiszivárgása (LLM02), ellátási lánc (LLM03), adat- és modellmérgezés (LLM04), a kimenet helytelen kezelése (LLM05), túlzott cselekvési jogkör (LLM06), rendszerprompt-szivárgás (LLM07), vektor- és beágyazásbeli gyengeségek (LLM08), félretájékoztatás (LLM09) és korlátlan erőforrás-fogyasztás (LLM10).

Ezek közül a mi felállásunkra a legközvetlenebbül a **prompt-befecskendezés** és a **túlzott cselekvési jogkör** vonatkozik. Az ügynökeink kódot olvasnak, függőségeket telepítenek, esetleg külső MCP-kiszolgálókat hívnak — vagyis olyan tartalmat dolgoznak fel, amelyet nem mi írtunk, és amely utasításnak álcázott szöveget tartalmazhat. A túlzott cselekvési jogkör pedig pontosan az a kérdés, amit a brief a jogi fejezetben feszeget: mit szabad az ügynöknek megtennie.

Erre épül rá a 2025. december 9-én kiadott **OWASP Top 10 for Agentic Applications** (S-13), amely kifejezetten az autonóm és többügynökös rendszerekre szabott kockázatokat gyűjti össze, több mint száz biztonsági kutató és gyakorló szakember bevonásával. A bejelentés három fenyegetést emel ki elsődlegesként: az **ügynök viselkedésének eltérítését** (agent behavior hijacking), az **eszközök visszaélésszerű használatát és kihasználását** (tool misuse and exploitation), valamint az **azonosság- és jogosultsági visszaélést** (identity and privilege abuse). További nevesített kockázatok a célesetérítés, a memóriamérgezés, a prompt-befecskendezés, az adatszivárgás, az autonóm rendszereken végigfutó láncolatos hibák, az emberi bizalom manipulálása és a szabályt szegő autonóm viselkedés. A javasolt enyhítések iránya következetes: valós idejű szándékkontroll és alkalmazkodó védőkorlátok, az ügynökhasználat felderítése és értékelése a szervezetben, valamint a tervezéstől az üzemeltetésig több ponton beépített megelőzés.

### Mennyire jók az ügynökök biztonsági ellenőrzésre?

Itt a legerősebb bizonyíték a Microsoft 2026 májusában közzétett rendszerének leírása (S-14). Az architektúra több mint száz specializált ügynököt hangol össze, és — ez a döntő részlet — **több modellcsaládot vegyít**: élvonalbeli modellt használ nehéz következtetésre, desztillált modelleket költséghatékony vitapartnerként a nagy mennyiségű átfutáshoz, és egy **másik gyártótól származó élvonalbeli modellt** független ellenpontként. A folyamat öt szakaszból áll: előkészítés, letapogatás, validálás (vitázó ügynökök mérlegelik a találatokat), duplikátumszűrés és bizonyítás (a rendszer ténylegesen előállítja és lefuttatja a hibát kiváltó bemenetet).

A közölt eredmények: egy zárt tesztmeghajtón mind a 21 elrejtett sebezhetőséget megtalálta nulla téves riasztás mellett; öt év megerősített biztonsági eseteinek egy részhalmazán 96 százalékos, egy másikon 100 százalékos felidézést ért el; a nyilvános CyberGym benchmarkon 1507 valós sebezhetőségen 88,45 százalékos sikerarányt hozott. A rendszer 2026 májusában tizenhat sebezhetőséget talált a Windows hálózati veremben, köztük négy kritikus távoli kódfuttatási hibát.

### Miért kell több modellcsalád, és nem több példány ugyanabból?

Erre a kérdésre Abhinav Agarwal Refute-or-Promote nevű módszertana (S-15) ad a leghasznosabb választ. A kiindulópontja az, hogy az LLM-alapú hibakeresésnek pontossági válsága van: a modellek sok téves riasztást termelnek, ami a fogadó oldalon gyakorlatilag szolgáltatásmegtagadási támadásként hat.

A módszertan lényege, hogy a jelöltek nem együttműködő vitában, hanem **szakaszos cáfolati kapukon** kelnek át: minden találatnak túl kell élnie az ellene érvelő ügynököket, mielőtt megerősítettként továbbmehetne. A mért eredmények: a folyamat 171 jelöltből **79 százalékot ejtett ki** visszamenőleges elemzésben, előretekintő szakaszban pedig 30-ból 25-öt, azaz 83 százalékot. A kiesés elöl sűrűsödik: az A szakasz a belépők 63 százalékát, a B szakasz a túlélők további 42 százalékát ejti.

A legfontosabb megállapítás a **modellcsaládok keverésére** vonatkozik. Az azonos modellcsaládon belüli felülvizsgálat 19 javasolt javításból háromban (16 százalék) nem vette észre a helyességi hibát, amelyet a más családból származó bíráló megtalált. Ennek elméleti alapja az, hogy ha a generáló és az értékelő ugyanazon a tanítóadaton osztozik, ugyanazokat a torzításokat is örökli. Agarwal hivatkozik olyan mérésre is, amely szerint a modellek hajlamosak az egyetértésre — a hivatkozott vizsgálatban 96 százalékos valódi pozitív arány mellett 25 százalék alatti valódi negatív arány adódott —, és ahol a kisebbségi vétójog kétszeresen felülmúlt egy tizennégy modellből álló szavazó együttest. A tanulmány dokumentál egy esetet, amelyben nyolcvannál több ügynök tévedett, és egyetlen bíráló ejtette ki a hibás találatot.

A módszertan korlátait a szerző maga rögzíti: a folyamat a **pontosságra optimalizál, a felidézést nem méri**, szerkezetileg egyirányú (a téves pozitívak ellen véd, a téves negatívak ellen nem), és az írás terepvizsgálat, nem előre regisztrált kísérlet.

## Negatív tapasztalatok és buktatók

Az első buktató a **téves riasztások terhe**. A hivatkozott irodalom szerint az egymodelles fehérdobozos vizsgálat jellemzően jelentős, tíz százalék fölötti téves pozitív arányt produkál (S-15 egy dokumentált esetben mintegy 28 százalékot idéz). Ez a gyakorlatban azt jelenti, hogy egy szűretlen biztonsági ügynök **több munkát okoz, mint amennyit megspórol**, mert minden téves találatot embernek kell megvizsgálnia. A brief eredeti szándéka — „minél több biztonsági feladatot ügynökkel elvégezni" — így csak szűrő architektúrával teljesíthető.

A második buktató az **együttműködő vita törékenysége**. Ha az ügynököket konszenzusra állítjuk be, egyetlen meggyőző ügynök felülírhatja a többségi szavazást (S-15 hivatkozott eredménye). Ebből az következik, hogy a több ügynök önmagában nem véd: a szerepeket **aszimmetrikusan**, cáfolatra kell beállítani.

A harmadik buktató, hogy az egy modellcsaládon belüli többszörözés hamis biztonságérzetet ad (S-15). Két Claude-példány, vagy két GPT-példány nagyrészt ugyanazokat a hibákat fogja elkövetni és elnézni.

A negyedik buktató magának az ügynökös munkafolyamatnak a támadási felülete (S-12, S-13). Az ügynök, amely automatikusan olvas be külső tartalmat és futtat parancsokat, új belépési pontot nyit. Ez nem elméleti: az OWASP kifejezetten a memória- és kontextusmérgezést, valamint az eszközvisszaélést emeli ki.

## Mit jelent ez a mi projektünkre

A brief kérdésére a válasz egyértelmű és jól alátámasztott: **a biztonsági ellenőrzéshez több ügynök és több, eltérő gyártótól származó modell kell**, méghozzá nem együttműködő, hanem cáfoló szerepben. Ez az egyetlen olyan pont a kutatásban, ahol a többügynökös felállás mellett erős, mérésekkel alátámasztott érv szól — szemben a kódírással, ahol az irodalom az egyszerűséget ajánlja (lásd a 4. dokumentumot).

A gyakorlatba átültetve a következő felállást javasoljuk megfontolásra:

1. **Determinisztikus alapréteg.** A statikus elemzés, a függőségvizsgálat és a titokszivárgás-keresés ne LLM-re épüljön, hanem hagyományos eszközökre, amelyek megismételhető eredményt adnak. Az ügynök szerepe ezek eredményének értelmezése és rangsorolása.
2. **Ügynöki keresőréteg.** A biztonsági ügynök átnézi az iteráció változásait a fenyegetési modell (S-12, S-13) szempontjai szerint.
3. **Cáfoló réteg más modellcsaláddal.** Minden találatot egy másik gyártó modelljére épülő ügynöknek kell megtámadnia. Csak az kerül ember elé, ami ezt túléli (S-15).
4. **Emberi kapu a következményes műveleteknél.** Az ügynök ne kapjon jogot arra, hogy éles rendszert módosítson, titkot olvasson vagy külső szolgáltatásba írjon. Ez a mi következtetésünk az OWASP fenyegetéslistájából: ha az azonosság- és jogosultsági visszaélés a három legfontosabb ügynöki kockázat egyike (S-13), akkor a legolcsóbb védekezés az, ha a jogosultság eleve nincs meg.
5. **Az ügynökök jogosultsága legyen feladathoz szabott és naplózott.** Ez egyszerre biztonsági és — a 9. dokumentumban tárgyalt — felelősségi követelmény.

Fontos elvárásmenedzsment: a Microsoft eredményei (S-14) egy több mint száz ügynökből álló, dedikált rendszerre vonatkoznak, amit a mi kétfős csapatunk nem fog reprodukálni. Amit átvehetünk, az az **architektúra elve** — több modellcsalád, vitáztatás, empirikus bizonyítási kapu —, nem a méret.

## Nyitott kérdések

Nem találtunk mérést arra, hogy a Refute-or-Promote-hoz hasonló cáfoló architektúra hogyan teljesít **kis** csapatnál, néhány ügynökkel; a hivatkozott eredmények nagy rendszerekből származnak. Szintén nyitott, mekkora felidézési veszteséggel jár a pontosságra optimalizálás (S-15 ezt maga is a korlátai közt sorolja fel) — vagyis nem tudjuk, hány valódi sebezhetőséget ejt ki a szűrő. Végül nincs adatunk arról, hogy egy belső intranet kockázati szintjén mennyi ebből az arzenálból indokolt, és hol lép be a túlbiztosítás.

## Források

| Azonosító | Forrás | Szint |
|---|---|---|
| S-12 | OWASP GenAI Security Project: *OWASP Top 10 for LLM Applications 2025* (v2.0, 2024-11-18) | B |
| S-13 | OWASP GenAI Security Project: *Top 10 Risks and Mitigations for Agentic AI Security / Top 10 for Agentic Applications*, 2025-12-09 | B |
| S-14 | Microsoft Security Blog: *Defense at AI speed: Microsoft's new multi-model agentic security system tops leading industry benchmark*, 2026-05-12 | C |
| S-15 | Abhinav Agarwal: *Refute-or-Promote: An Adversarial Stage-Gated Multi-Agent Review Methodology for High-Precision LLM-Assisted Defect Discovery*, arXiv:2604.19049, 2026-04-22 | A |

A teljes bibliográfiai adatokat és az URL-eket a [forrasok.md](forrasok.md) tartalmazza.
