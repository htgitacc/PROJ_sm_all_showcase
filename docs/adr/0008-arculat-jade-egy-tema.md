# 0008 — Arculat: jáde színvilág egyetlen világos témában, csoportszínű fejlécekkel

**Állapot:** elfogadva (a felhasználó két minta közül választotta, 2026-10-19).

## Kontextus

A felület kék kiemelésű, világos és sötét változatú Streamlit-témával futott; a felhasználó
szerint a pár projekt (PM-mindenes) felülete ingerszegény volt, ezért ott őszi arculat készült
(terrakotta, meleg papírszín háttér, egyetlen téma). Ennél a projektnél frissebb, fiatalosabb,
zöldes színvilágot kért, ugyanabban a szerkezetben. A sötét mód csak azért kellett, mert a fehér
háttér vakított; szemkímélő háttérrel egy téma elég. Két minta készült (Jáde és Türkiz,
képernyőképekkel egymás mellett); a felhasználó a Jádét választotta.

## Döntés

- **Egyetlen világos téma** (`.streamlit/config.toml` `[theme]`, `base = "light"`), sötét mód
  nélkül: halvány mentás háttér `#eef4ef`, sötét fenyőzöld szöveg `#1f2a24`, jáde kiemelés
  `#1f7a5a`, türkiz „info” dobozok. A korábbi `[theme.light]` / `[theme.dark]` szakasz megszűnt.
- **A színek egy helyen** (`modell/arculat.py`, új modul): a menücsoportok színe (Kezdés jáde,
  A példa türkiz, Lejátszás és gyakorlás fűzöld, Amire épül fenyő), a Bevezetés nyitósávja, a
  kártyák és az idézetek kiemelése. Csak CSS és `st.html`; a fejléc egy kulcsos
  `st.container` (`.st-key-fejlec-<n>`), így a Streamlit saját címe és ikonja marad.
- **A jelentést hordozó színek maradnak**: emberi kapu narancs, túllépés piros, ügynök lila,
  beolvadt zöld. Az ábrák kiemelőszíne (`grafikonok.KEK`) és az animáció háttere a palettát követi;
  az animáció sem vált sötét módra.
- A kontrasztot **számoljuk** (WCAG 2.1, `tesztek/test_arculat.py`): minden csoportszín legalább
  4,5:1 fehér szöveggel és a háttéren, a szöveg legalább 7:1 minden felületen.

## Következmények

- Merge után **újraindítás kell** (`config.toml`, `modell/*.py`, az animáció gyorsítótárazott
  HTML-je).
- A Bevezetésnek nincs külön oldalfejléce: a címe a nyitósávban áll.
- A képernyőkép-eszköznek nincs többé sötét változata (`--sotet` megszűnt).
- A HANDOFF régi buktatója („ne csak `[theme]` legyen, különben eltűnik a sötét mód”) érvényét
  veszti: most épp ez a cél.
- A közös belépőoldal (`PROJ_smpm`) színei a két projekt arculatához igazodnak (külön repó).
