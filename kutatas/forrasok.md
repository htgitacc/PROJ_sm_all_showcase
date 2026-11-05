# Forrásjegyzék

## Hogyan olvasd ezt a jegyzéket

Minden forrás azonosítót (`S-nn`) és **megbízhatósági szintet** kapott. A szintezés célja, hogy egy vezetői egyeztetésen vagy állásinterjún egy pillantással el lehessen dönteni, mekkora súlyt bír el egy állítás.

| Szint | Mit jelent |
|---|---|
| **A** | Lektorált kutatás, kontrollált kísérlet, konferenciacikk, hivatalos szabvány vagy jogszabály |
| **B** | Nagy mintás iparági jelentés vagy mérésen alapuló mérnöki beszámoló, jellemzően nem független kiadótól |
| **C** | Gyártói blog, gyakorlati esszé, egyedi tapasztalat, vélemény |

**Módszertani szabály, amelyet a kutatás során betartottunk:** csak olyan forrás került a dokumentumokba, amelynek tartalmát ténylegesen megnyitottuk és elolvastuk, vagy amelynek adatait a megnyitott elsődleges forrás visszaigazolta. Több olyan, keresés közben felbukkant számadatot szándékosan **kihagytunk**, amelyet nem tudtunk elsődleges forrásból megerősíteni — ezeket a jegyzék végén felsoroljuk.

---

## A források

### S-01 — METR: AI-hatás mérése tapasztalt nyílt forrású fejlesztőkön
*Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* METR, 2025. július 10.
https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
**Szint: A** — randomizált kontrollált kísérlet, 16 fejlesztő, 246 valós feladat.
*Relevancia:* az egyetlen általunk talált RCT; azt mutatja, hogy tapasztalt fejlesztő a saját kiforrott kódbázisán 19%-kal lassabb lett AI-val, miközben gyorsabbnak érezte magát.

### S-02 — DORA: State of AI-assisted Software Development 2025
Google Cloud / DORA, 2025. szeptember 23.
https://dora.dev/dora-report-2025/ · https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
**Szint: B** — közel 5000 fős globális felmérés és több mint 100 óra kvalitatív kutatás.
*Relevancia:* az AI-adopció pozitívan korrelál az átbocsátással, negatívan a stabilitással; az AI „erősítőként" viselkedik.

### S-03 — GitClear: AI Copilot Code Quality, 2025-ös kutatás
https://www.gitclear.com/ai_assistant_code_quality_2025_research
**Szint: B** — 211 millió megváltoztatott kódsor elemzése 2020 januárja és 2024 decembere között, a Google, a Microsoft, a Meta és vállalati ügyfelek repozitóriumaiból.
*Relevancia:* a refaktorálás visszaszorulása (25% → <10%) és a klónozott sorok növekedése (8,3% → 12,3%).
*Ellenőrzési megjegyzés:* a másodlagos összefoglalókban ehhez a jelentéshez kötött „két hetes code churn 3,1%-ról 5,7%-ra nőtt" adatot az elsődleges oldalon **nem találtuk meg**, ezért nem használjuk fel. A churnre a 2026-os jelentés (S-04) elsődlegesen ellenőrzött adatát idézzük.

### S-04 — GitClear: The Maintainability Gap, 2026-os kutatás
https://www.gitclear.com/the_ai_code_quality_maintainability_gap
**Szint: B** — 623 millió változtatás, 2023–2026.
*Relevancia:* a szerkezeti romlás folytatódása: duplikáció +81%, refaktorálás 21%-ról 3,8%-ra.

### S-05 — Duma, Wróblewski, Bobińska, Winiarska, Przymus: These Aren't the Reviews You're Looking For
*How Humans Review AI-Generated Pull Requests.* Nicolaus Copernicus University, Toruń. EASE 2026 (Glasgow), arXiv:2605.02273v1, 2026. május 4.
https://arxiv.org/abs/2605.02273
**Szint: A** — nagy mintás empirikus tanulmány az AIDev adathalmazon (932 ezer+ PR), replikációs csomaggal.
*Relevancia:* a kutatás legfontosabb egyetlen adata — az ügynöki pull requestek 84%-át vagy nem nézi át senki, vagy csak gép nézi át.

### S-06 — LinearB: 2026 Software Engineering Benchmarks Report
https://linearb.io/resources/software-engineering-benchmarks-report · elemzés: https://linearb.io/blog/8-million-prs-engineering-productivity
**Szint: B** — 8,1 millió pull request, 4800 csapat, 42 ország.
*Relevancia:* az AI-s pull requestek mérete, elfogadási aránya és felvételi ideje; a torlódás a sorban állásból ered, nem a bírálat lassúságából.

### S-07 — Walden Yan (Cognition): Don't Build Multi-Agents
2025. június 12. https://cognition.com/blog/dont-build-multi-agents
**Szint: C** — gyakorlati állásfoglalás a Devin fejlesztőjétől, mérés nélkül.
*Relevancia:* a párhuzamos alügynökök kontextusizolációs törékenységének legvilágosabb megfogalmazása.

### S-08 — Anthropic: When to use multi-agent systems (and when not to)
https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
**Szint: C** — gyártói útmutató.
*Relevancia:* mikor éri meg a több ügynök, a 3–10-szeres tokenszorzó, és a verifikáló alügynök mint az egyetlen ajánlott kódolási minta.

### S-09 — Anthropic: How we built our multi-agent research system
2025. június 13. https://www.anthropic.com/engineering/multi-agent-research-system
**Szint: C** — gyártói mérnöki beszámoló belső értékeléssel.
*Relevancia:* 90,2%-os javulás kutatási feladatokon, ~15-szörös tokenhasználat, és az a megállapítás, hogy a kódolási feladatok kevésbé párhuzamosíthatók.

### S-10 — Cemri, Pan, Yang, Agrawal, Chopra, Tiwari, Keutzer, Parameswaran, Klein, Ramchandran, Zaharia, Gonzalez, Stoica: Why Do Multi-Agent LLM Systems Fail?
UC Berkeley Sky Computing. arXiv:2503.13657, beküldve 2025. március 17., v3: 2025. október 26.
https://arxiv.org/abs/2503.13657 · https://sky.cs.berkeley.edu/project/mast/
**Szint: A** — 1600+ annotált végrehajtási nyomvonal, 7 keretrendszer, Cohen-féle kappa 0,88.
*Relevancia:* a MAST-taxonómia 14 hibamódja; a hibák 43,8%-a rendszertervezési, 24,05%-a verifikációs eredetű.

### S-11 — Sanjay Saini: AI Augmented Scrum Framework — When Half Your Team is Autonomous Agents
Scrum.org blog, 2026. március 8. (eredetileg: Agile Leadership Day India)
https://www.scrum.org/resources/blog/ai-augmented-scrum-framework-when-half-your-team-autonomous-agents
**Szint: C** — gyakorlati írás, mérési háttér nélkül.
*Relevancia:* a legkonkrétabb keretrendszeri javaslat, amelyet találtunk; a Scrum-események átalakítása és a story pontok elvetése ügynöki munkára.

### S-12 — OWASP GenAI Security Project: OWASP Top 10 for LLM Applications
A dokumentum saját megjelölése szerint „Version 2025"; a benne szereplő változásnapló szerint kiadva 2024. november 18-án.
https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf
**Szint: B** — közösségi konszenzuson alapuló, széles körben elfogadott iparági referencia.
*Relevancia:* a nyelvi modellre épülő rendszerek fenyegetési modellje; számunkra elsősorban a prompt-befecskendezés (LLM01) és a túlzott cselekvési jogkör (LLM06).
*Ellenőrzés:* a tíz tétel nevét és a verziójelölést a letöltött PDF szövegéből olvastuk ki.

### S-13 — OWASP GenAI Security Project: Top 10 for Agentic Applications
2025. december 9. Bejelentés: https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/
Erőforráslap: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
**Szint: B** — több mint száz kutató és gyakorló szakember bevonásával készült keretrendszer.
*Relevancia:* a bejelentésben elsődlegesként nevesített három fenyegetés (ügynökviselkedés-eltérítés, eszközvisszaélés és -kihasználás, azonosság- és jogosultsági visszaélés), valamint a további említett kockázatok (célesetérítés, memóriamérgezés, láncolatos hibák, emberi bizalom manipulálása).
*Ellenőrzési megjegyzés:* a teljes, sorszámozott tízes listát csak a letölthető dokumentumból lehet megkapni; mi a nyilvános bejelentésben nevesített tételekre hivatkozunk, és ezt a szövegben is jelezzük.

### S-14 — Microsoft Security: Defense at AI speed
*Microsoft's new multi-model agentic security system tops leading industry benchmark.* 2026. május 12.
https://www.microsoft.com/en-us/security/blog/2026/05/12/defense-at-ai-speed-microsofts-new-multi-model-agentic-security-system-tops-leading-industry-benchmark/
**Szint: C** — gyártói beszámoló, de részletes architektúra- és eredményleírással.
*Relevancia:* több mint száz ügynök, több modellcsalád vegyítése, vitáztatás és empirikus bizonyítási kapu; 21/21 elrejtett sebezhetőség nulla téves riasztással, 88,45% a CyberGym benchmarkon.

### S-15 — Abhinav Agarwal: Refute-or-Promote
*An Adversarial Stage-Gated Multi-Agent Review Methodology for High-Precision LLM-Assisted Defect Discovery.* arXiv:2604.19049, 2026. április 22.
https://arxiv.org/abs/2604.19049
**Szint: A** — terepvizsgálat valós eredményekkel; a szerző maga jelzi, hogy nem előre regisztrált értékelés.
*Relevancia:* 79%-os visszamenőleges és 83%-os előretekintő kiejtési arány; az azonos modellcsaládon belüli felülvizsgálat 19-ből 3 esetben (16%) nem vette észre a hibát.

### S-16 — Wang, Xu, Briand, Liu: Mutation-Guided Unit Test Generation with a Large Language Model
arXiv:2506.02954, beküldve 2025. június 3., átdolgozva 2026. április 15.
https://arxiv.org/abs/2506.02954
**Szint: A** — 204 tesztalany két benchmarkon.
*Relevancia:* egyes tesztsorozatok 100%-os lefedettséget értek el 4%-os mutációs pontszám mellett.

### S-17 — Sławomir Radzymiński: Mutation Testing for Agent-Written Code
Awesome Testing, 2026. augusztus 2.
https://www.awesome-testing.com/2026/08/mutation-testing-for-agent-written-code
**Szint: C** — gyakorlati beszámoló négy projekt méréseivel.
*Relevancia:* konkrét mutációspontszám-javulások, és az az eset, amelyben 100%-os sorlefedettség mellett a mutációs pontszám 61,29% volt.

### S-18 — Wang, Wu, Ma, Li, Zhang, Gu, Lu: Adaptive Human-Agent Teaming
*A Review of Empirical Studies from the Process Dynamics Perspective.* arXiv:2504.10918, 2025. április 15.
https://arxiv.org/abs/2504.10918
**Szint: A** — rendszerezett irodalmi áttekintés.
*Relevancia:* a T⁴ keretrendszer négy fázisa, amely a Tuckman-modell helyett ad használható vázat ember–ügynök csapatokra.

### S-19 — Richard Jiarui Tong: From Augmentation to Symbiosis
*A Review of Human-AI Collaboration Frameworks, Performance, and Perils.* arXiv:2601.06030, 2025. november 7.
https://arxiv.org/abs/2601.06030
**Szint: A** — hatvan évet átfogó szintézis metaanalitikus megfigyeléssel.
*Relevancia:* a teljesítményparadoxon — negatív szinergia ítéleti feladatokban, pozitív alkotó feladatokban.

### S-20 — Dell'Acqua, Ayoubi, Lifshitz-Assaf, Sadun, Mollick, Mollick, Han, Goldman, Nair, Taub, Lakhani: The Cybernetic Teammate
*A Field Experiment on Generative AI Reshaping Teamwork and Expertise.* NBER Working Paper w33641; Organization Science.
https://www.nber.org/papers/w33641 · https://pubsonline.informs.org/doi/10.1287/orsc.2025.20702
**Szint: A** — előzetesen regisztrált terepkísérlet 776 szakemberrel a Procter & Gamble-nél.
*Relevancia:* az AI-val dolgozó egyén elérte az AI nélküli kétfős csapat teljesítményét, és az AI lebontotta a funkcionális silókat.

### S-21 — EU mesterségesintelligencia-rendelet: végrehajtási idővonal
https://artificialintelligenceact.eu/implementation-timeline/
**Szint: A** — jogszabályi hatálybalépési rend.
*Relevancia:* mely kötelezettség mikortól alkalmazandó.

### S-22 — EU AI Act, 4. cikk: AI-jártasság
https://artificialintelligenceact.eu/article/4/
**Szint: A** — jogszabályszöveg.
*Relevancia:* 2025. február 2. óta alkalmazandó kötelezettség a személyzet megfelelő szintű AI-jártasságának biztosítására.

### S-23 — ISO/IEC 42001:2023 — Mesterségesintelligencia-irányítási rendszer
https://www.iso.org/standard/42001
**Szint: A** — nemzetközi szabvány.
*Relevancia:* kockázatkezelés, irányítás és elszámoltathatóság, átláthatóság és dokumentálás, életciklus-kontrollok. *Megjegyzés: a szabvány teljes szövegét nem vásároltuk meg, ezért csak a nyilvános leírásból következő szerkezetre hivatkozunk.*

### S-24 — Yang, He, Zhou: To Ban or not to Ban? How Open Source Projects Govern GenAI Contributions
Peking University. arXiv:2603.26487v2, 2026. július 30.
https://arxiv.org/abs/2603.26487
**Szint: A** — 67 nagy láthatóságú nyílt forrású projekt kvalitatív elemzése.
*Relevancia:* az „olcsóbb generálás nem jelent olcsóbb átnézést" tétel; három kormányzási irányultság és tizenkét stratégia; a Node.js 19 000 soros pull request esete.

### S-25 — Galster, Mohsenimofidi, Lulla, Abubakar, Treude, Baltes: Harness Engineering for Agentic AI Coding Tools
*An Exploratory Study.* AIware '26 (3rd ACM International Conference on AI-Powered Software). arXiv:2602.14690v5, 2026. június 30.
https://arxiv.org/abs/2602.14690
**Szint: A** — 2853 GitHub-repozitórium empirikus elemzése.
*Relevancia:* nyolc konfigurációs mechanizmus; a kontextusfájlok dominanciája; az `AGENTS.md` mint interoperábilis szabvány; a képességek és alügynökök alacsony elterjedtsége.

### S-26 — Aggarwal, Ghalaty (Microsoft): Self-Improving AI Coding Agents Through Accumulated Behavioral Rules
*A Closed-Loop Framework.* arXiv:2607.13091, 2026. július 13.
https://arxiv.org/abs/2607.13091
**Szint: B** — iparági terepmérés, négy hét, 35+ mikroszolgáltatás, **kontrollcsoport nélkül** (ezt a szerzők maguk is korlátként jelölik).
*Relevancia:* a review-visszajelzés szabállyá alakításának zárt hurka, és annak mérése, hogy a visszajelzés beépült-e.

### S-27 — Robbes, Matricon, Degueule, Hora, Zacchiroli: Agentic Very Much! Adoption of Coding Agent in New GitHub Projects
arXiv:2606.07448v1, 2026. június 5.
https://arxiv.org/abs/2606.07448
**Szint: A** — 12 794 új GitHub-projekt heurisztikus elemzése, összehasonlítva egy korábbi mintával.
*Relevancia:* az ügynökhasználat elterjedtsége az új projektekben a korábbi valamivel több mint egynegyedről több mint kétharmadra nőtt.

### S-28 — Yuval Yeret: Limiting Work in Progress (WIP) in Scrum with Kanban in the AI Age
2026. január 23.
https://yuvalyeret.com/blog/limiting-work-in-progress-wip-in-scrum-with-kanban-what-when-who-how/
**Szint: C** — tapasztalati alapú módszertani írás.
*Relevancia:* a „gyorsulási ostorcsapás", az „AI-színház" és a „felfelé irányuló kiéheztetés" fogalma; a fejenként egy-két párhuzamos elemre vonatkozó ajánlás.

### S-29 — DX: DX Core 4
https://getdx.com/dx-core-4/ · https://docs.getdx.com/dx-core-4
**Szint: C** — szolgáltatói keretrendszer, a DORA/SPACE/DevEx szerzőinek közreműködésével.
*Relevancia:* négy dimenzió — sebesség, hatékonyság, minőség, hatás —, benne az innovációs arány mint értékmutató.

### S-30 — GitHub Spec Kit
https://github.com/github/spec-kit · https://github.github.com/spec-kit/
**Szint: C** — a GitHub által kiadott nyílt forrású eszközkészlet és módszertani leírás.
*Relevancia:* a specifikáció-vezérelt fejlesztés megnevezett lépései — `constitution` (alapelvek), `specify`, `plan`, `tasks`, `implement`, `converge` (a kódbázis és a specifikáció együttállásának felmérése) —, amelyek explicit emberi ellenőrzési pontot tesznek a darabolás után és a kódolás előtt.

### S-31 — AGENTS.md nyílt formátum
https://agents.md/
**Szint: C** — formátumleírás; a Linux Foundation alá tartozó Agentic AI Foundation gondozza.
*Relevancia:* több mint 60 ezer nyílt forrású projekt és több mint húsz eszköz használja.

### S-32 — MIT: The GenAI Divide — State of AI in Business 2025, és annak kritikája
Kritikai elemzés: https://www.marketingaiinstitute.com/blog/mit-study-ai-pilots
**Szint: C** — *fontos korlát: az eredeti jelentést magát nem nyitottuk meg; a tartalmára és a módszertani kritikájára másodlagos forrásból hivatkozunk.*
*Relevancia:* a széles körben idézett „95% megbukik" adat, valamint az, hogy ez az adat szűk sikerdefiníción (hat hónapon belüli közvetlen eredményhatás) és kis mintán (52 interjú, 153 vezetői válasz) alapul.

### S-33 — U.S. Copyright Office: Copyright and Artificial Intelligence, Part 2 — Copyrightability
A jelentés címlapján szereplő dátum: 2025. január.
https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf
**Szint: A** — hivatalos hatósági jelentés, több mint tízezer beérkezett észrevétel feldolgozásával.
*Relevancia:* a jelentés vezetői összefoglalójából ellenőrzött következtetések — a kérdések a hatályos jog alapján megválaszolhatók; a szerzői jog nem terjed ki a tisztán AI által előállított anyagra; a promptok önmagukban nem biztosítanak elegendő ellenőrzést; az emberi szerzőt megilleti a jog a kimenetben felismerhető saját művére, valamint a kreatív kiválogatásra, elrendezésre és módosításokra.
*Ellenőrzés:* a jelentés PDF-jét letöltöttük, és a vezetői összefoglaló pontjait szó szerint kiolvastuk.

### S-35 — Zhao, Zhou, Cohen: Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability Study)
arXiv:2607.22880, beküldve 2026. július 24.
https://arxiv.org/abs/2607.22880
**Szint: A** — nagy mintás replikációs vizsgálat.
*Relevancia:* a lefedettség és a mutációs pontszám hasznossága erősen kontextusfüggő. Regressziós helyzetben, hibátlannak feltételezett kódon értelmes összehasonlítási jelzést adnak; ha a vizsgált kód maga is tartalmazhat hibát, már nem megbízható jelzők. A szerzők kevés bizonyítékot találtak arra, hogy a tesztsorozat mérete lenne a meghatározó zavaró tényező.

### S-36 — DX: AI Measurement Framework
https://getdx.com/blog/ai-measurement-framework-guide/ · https://getdx.com/whitepaper/ai-measurement-framework/
**Szint: C** — szolgáltatói mérési keretrendszer.
*Relevancia:* kihasználtság, hatás és költség dimenziói; az a figyelmeztetés, hogy a magas adopció együtt élhet negatív hatással, és hogy a mérőszámok nem alkalmasak egyéni értékelésre.

### S-37 — Az Európai Parlament és a Tanács (EU) 2024/2853 irányelve a hibás termékekért való felelősségről
Átültetési határidő: 2026. december 9.
https://eur-lex.europa.eu/eli/dir/2024/2853/oj
**Szint: A** — uniós jogszabály.
*Relevancia:* a termék fogalma kiterjed a szoftverre és az AI-rendszerekre, tehát ezekre is a vétkességtől független felelősség szabályai vonatkoznak. *A mi belső, forgalomba nem hozott intranetünkre várhatóan közvetlenül nem alkalmazandó — lásd a [09](09-jogi-es-felelossegi-keret.md) dokumentum kifejtését.*

---

## Kiszűrt állítások — amit szándékosan nem használtunk fel

A kutatás során több olyan, kézenfekvőnek látszó számadat került elő, amelyet **nem tudtunk elsődleges forrásból megerősíteni**, ezért nem került be a dokumentumokba. Az átláthatóság kedvéért itt soroljuk fel őket. Ha valaki ezekre hivatkozik egy vitában, érdemes visszakérdezni a forrásra.

- **„Az AI PR-ek 4,6-szer hosszabban várnak felvételre, de a review 2×-gyorsabb"** (Faros AI 2026-nak tulajdonítva) — nem nyitottuk meg az eredeti jelentést. A hasonló irányú, de eltérő nagyságrendű LinearB-adatot (S-06) viszont elsődleges forrásból ellenőriztük, és azt használjuk.
- **„Az AI a commitolt kód 42%-át adja; a fejlesztők 96%-a nem bízik meg benne teljesen; csak 48% ellenőrzi mindig"** (Sonar 2026 State of Code-nak tulajdonítva) — nem ellenőriztük. A bizalomra a DORA (S-02) elsődleges forrásból ellenőrzött adatát használjuk.
- **„A feature branch throughput 59%-kal nőtt, a medián csapat main-branch throughputja viszont csökkent"** (CircleCI 2026-nak tulajdonítva) — nem ellenőriztük.
- **„Az AI-generált kód 35%-a licencszabálytalanságot tartalmaz"** és **„a Black Duck 2026-os jelentése az auditált kódbázisok 68%-ában talált licenckonfliktust"** — mindkettő másodlagos blogforrásból származott, elsődlegesen nem ellenőriztük. A licenckockázatot ezért kvalitatívan, a lektorált S-24 alapján tárgyaljuk.
- **„A Scrum Masterek 40%-kal kevesebb időt töltenek adminisztrációval AI-val"** és **„egy 2024-es esettanulmány szerint a Scrum Masterek 86%-a 30 perc és 2 óra közötti időt spórolt sprintenként"** — képzési anyagokból származó, visszakövethetetlen számok.
- **„A szervezetek 84%-a jelent AI-adopciót az agilis módszertanán belül"** — kereskedelmi blogból származó, forrás nélküli szám.
- **„A munkáltatók 55%-a megbánta az AI miatti elbocsátásokat"** (Forresternek tulajdonítva) és a hozzá kapcsolódó „visszavételi hullám" beszámolók — nem ellenőriztük, és a projektünk szempontjából amúgy sem érdemi.
- **„A GitClear 2025-ös jelentése szerint a két hetes code churn 3,1%-ról 5,7%-ra nőtt 2020 és 2024 között"** — a hivatkozott elsődleges oldalon ezt a bontást nem találtuk meg (lásd az S-03 ellenőrzési megjegyzését).

## A hivatkozások elérhetőségének ellenőrzése

A jegyzékben szereplő minden URL-t automatikusan meghívtunk. Negyvenhárom cím közül negyven HTTP 200 vagy 202 státusszal válaszolt. Három esetben a szerver a gépi lekérést utasította el, nem a cím hibás:

- `iso.org/standard/42001` és `sky.cs.berkeley.edu/project/mast/` — HTTP 403, robotszűrés. Böngészőből mindkettő elérhető; a MAST-tanulmány tartalmát az arXiv-változatból ellenőriztük.
- A két `linearb.io` cím — HTTP 429, sebességkorlátozás. A tartalmat korábban, egyenkénti lekéréssel sikeresen kiolvastuk.

## Összesítés

| Szint | Források száma |
|---|---|
| A | 17 |
| B | 7 |
| C | 12 |
| **Összesen** | **36** |

*(Az S-34 azonosító szándékosan üresen maradt: az ehhez rendelt forrás az ellenőrzés során kiesett.)*
