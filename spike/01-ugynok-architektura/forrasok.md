# Forrásjegyzék — ügynök-architektúra spike

> A spike saját forrásai `U-nn` jelöléssel, hogy ne keveredjenek a lezárt kutatás `S-nn` jegyzékével. A szintezés ugyanaz, mint a [lezárt forrásjegyzékben](../../kutatas/forrasok.md): **A** — lektorált vagy kontrollált kísérlet, benchmark, konferenciacikk; **B** — nagy mintás elemzés vagy mérésen alapuló beszámoló, jellemzően nem független kiadótól; **C** — gyakorlati beszámoló, egyedi eset, vélemény.
>
> A keresés 2026-10-17-én készült, célzottan a lezárt kutatás óta megjelent anyagokra. Több forrás preprint (arXiv), lektorálás előtt; ezt a szint mellett jelzem. Ahol csak az összefoglalót láttam, nem a teljes szöveget, azt is.

## A források

### U-01 — Google Research: Towards a Science of Scaling Agent Systems
*Towards a Science of Scaling Agent Systems: When and Why Agent Systems Work.* arXiv:2512.08296, 2025. december; Google Research blog, 2026. január.
https://arxiv.org/abs/2512.08296 · https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
**Szint: A** (kontrollált kísérletsorozat, preprint) — 180 ügynökkonfiguráció, négy benchmark, öt architektúra (egy ügynök, független, központosított, decentralizált, hibrid).
*Relevancia:* szekvenciális feladatokon **minden** többügynökös változat 39–70%-kal rontott; párhuzamosítható feladaton a központosított koordináció 80,9%-kal javított. A független ügynökök a hibát 17,2-szeresére erősítik, a központosított koordináció 4,4-szeresre.

### U-02 — Benkovich, Valkov: Agyn
*Agyn: A Multi-Agent System for Team-Based Autonomous Software Engineering.* arXiv:2602.01465, 2026. február.
https://arxiv.org/abs/2602.01465
**Szint: B** (saját rendszer saját mérése, preprint) — menedzser, kutató, fejlesztő és bíráló ügynök; a menedzser dönt a további körökről, a lezáráshoz a bíráló ügynök jóváhagyása kell.
*Relevancia:* SWE-bench 500-on 72,2%, ami 7,4 százalékponttal jobb az összevethető modellű együgynökös alapnál. **Ablációt nem közöl**, így nem tudni, a nyereség a szerepekből vagy a bírálati körből jön.

### U-03 — Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures
arXiv:2607.28802, 2026. július.
https://arxiv.org/abs/2607.28802
**Szint: C** (egy dokumentált eset; csak az összefoglalót és a hivatkozó szövegeket láttam).
*Relevancia:* egy orkesztrátor egy alügynökre bízta egy dokumentáció elolvasását; az alügynök kb. 672 KB-ot olvasott el, majd üres választ adott hibajelzés nélkül, így az orkesztrátor nem tudta megkülönböztetni a hibát a „nincs mit jelenteni” esettől.

### U-04 — Jarmak: Engineering Reliable Coding Agents
*Engineering Reliable Coding Agents: Evaluating and Operating the System Around the Model.* arXiv:2608.13867, 2026. augusztus.
https://arxiv.org/abs/2608.13867
**Szint: B** (strukturált áttekintés: 164 tudományos mű, 100 gyakorlati feljegyzés; preprint).
*Relevancia:* a kódoló ügynökök látszólagos modellhibáinak jelentős része a modell körüli rendszerből (heveder, állapot, jogosultság, ellenőrzés, bírálati felület) ered; egy réteg javulása gyakran nem jelenik meg a végeredményben.

### U-05 — Az Agent Skills nyílt szabvány
Anthropic, 2025. december; specifikáció: agentskills.io. Beszámoló: Simon Willison, 2025-12-19.
https://agentskills.io/specification · https://simonwillison.net/2025/Dec/19/agent-skills
**Szint: C** (a szabvány ténye és elterjedése gyakorlati forrásból).
*Relevancia:* a `SKILL.md` alapú képességcsomag nyílt szabvány lett; több kódoló eszköz is támogatja (a pontos átvételi dátumokban a források eltérnek).

### U-06 — SkillsBench
*SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks.* arXiv:2602.12670, 2026. február.
https://arxiv.org/abs/2602.12670
**Szint: A** (benchmark determinisztikus ellenőrzőkkel, 7 ügynök–modell konfiguráció, 7308 futás; preprint).
*Relevancia:* a **gondozott (ember által írt) skillek** átlagosan 16,2 százalékponttal javították a sikerarányt, de **szoftverfejlesztésben csak kb. 4,5 ponttal**; a feladatok egy részén rontottak. A **modell által saját magának írt skillek átlagosan nem hoztak javulást.** A fókuszált (2–3 modulos) skill jobb volt a terjedelmes dokumentációnál.

### U-07 — Liu és mtsai: How Well Do Agentic Skills Work in the Wild
arXiv:2604.04323, 2026. április.
https://arxiv.org/abs/2604.04323
**Szint: A** (benchmark, 34 ezer valós skillből választó ügynökökkel; preprint).
*Relevancia:* minél valósághűbb a helyzet (az ügynöknek magának kell megtalálnia és kiválasztania a skillt), annál kisebb a skillek haszna, a legnehezebb esetben közel a skill nélküli szintre esik. Célzott finomítással a veszteség nagy része visszahozható.

### U-08 — What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files
arXiv:2608.08453, 2026. augusztus.
https://arxiv.org/abs/2608.08453
**Szint: B** (nagy mintás statikus elemzés; csak az összefoglalót láttam).
*Relevancia:* a vizsgált `SKILL.md` fájlok 91,8%-ában volt legalább egy kimutatható hiba; a helyes leíró metaadat javítja, hogy az ügynök megtalálja a megfelelő skillt.

### U-09 — MCPTox
*MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers.* arXiv:2508.14925, 2025. augusztus; az AAAI 2026-os konferenciakötetében.
https://arxiv.org/abs/2508.14925
**Szint: A** (benchmark, 45 valós MCP szerver, 353 tool, 20 modell; konferenciacikk).
*Relevancia:* a tool-leírásba rejtett utasítással („tool poisoning”) a legrosszabb modellnél 72,8%-os támadási siker; **a jobb képességű modellek gyakran sérülékenyebbek**, mert jobban követik az utasítást; a modellek a támadást szinte sosem utasították el (a legjobb elutasítási arány is 3% alatt).

### U-10 — Are AI-assisted Development Tools Immune to Prompt Injection?
arXiv:2603.21642, 2026. március.
https://arxiv.org/abs/2603.21642
**Szint: B** (hét MCP-kliens összevetése; preprint).
*Relevancia:* a fejlesztői eszközök védelme MCP-n keresztüli befecskendezés ellen erősen eltér; van, amelyik erős korlátokat alkalmaz, van, amelyik könnyen megtéveszthető.

### U-11 — Cloud Security Alliance: MCP Attack Surface — Tool Poisoning and IDE Auto-Execution
CSA Research Note, 2026. július (az Adversa AI 2026. májusi vizsgálatára hivatkozva).
https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-tool-poisoning-auto-execution-20260701/
**Szint: C** (iparági kutatási jegyzet, másodlagos).
*Relevancia:* több kódoló eszköz a mappa megbízhatóságának jóváhagyása után automatikusan elindította a projektben definiált MCP szervereket — a projektfájlból érkező tool tehát ellátási lánc kockázat.

### U-12 — Song: When Does a Second Model Help? Cross-Model Review in LLM Verification
arXiv:2610.01471, 2026. október.
https://arxiv.org/abs/2610.01471
**Szint: A** (kontrollált kísérlet: 30 munkadarab, 150 beültetett hiba, 900 bírálat, három bíráló modell; preprint).
*Relevancia:* **friss munkamenetben** a saját modell bírálata F1-ben nem tért el szignifikánsan egy csúcskategóriás más modell bírálatától; a két bíráló viszont részben más hibákat talált (41,2% átfedés), és **egy saját + egy más modelles bírálat több hibát fogott (56,7%), mint két saját (42,7%)**. Egy könnyűsúlyú más modell nem volt jobb a saját modellnél.

### U-13 — Guey, Bougault: Self-Preference Is Weak or Absent in Verifiable Instruction-Following Revision
arXiv:2606.20093, 2026. június.
https://arxiv.org/abs/2606.20093
**Szint: A** (kontrollált összevetés, négy modellcsalád; preprint).
*Relevancia:* gépileg ellenőrizhető, szűk mozgásterű feladatnál az önpreferencia kicsi (kb. 2 pont). A szerzők szerint ez nem feltétlenül vihető át nyitott kódbírálatra — de azt mutatja, hogy **determinisztikus ellenőrző mellett** a modell saját munkájának megítélése kevésbé torz.

### U-14 — Vaughan: Codex Pay-As-You-Go Pricing — Modelling Costs for Multi-Agent Workflows
2026-04-09.
https://codex.danielvaughan.com/2026/04/09/codex-pay-as-you-go-pricing-multi-agent-cost-modelling/
**Szint: C** (költségmodellezés, gyakorlati beszámoló).
*Relevancia:* a többügynökös tokenszorzó naiv számítása felülbecsül: a közös repó miatt a később induló ügynökök gyorsítótárazott (olcsóbb) bemenetet használnak, a rutin részfeladat pedig olcsóbb modellre tehető.
