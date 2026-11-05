"""A felület arculata: színek, a nyitósáv, az oldalfejlécek és a kiemelések CSS-e.

A téma alapja a `.streamlit/config.toml` (kiemelőszín, szöveg, háttér, keret); ez a modul azt
adja hozzá, amit a téma nem tud: a menücsoportok saját színét az oldalfejlécben, a Bevezetés
nyitósávját, a kártyák és az idézetek kiemelését. Friss, zöldes színvilág egyetlen témában:
halvány mentás háttér (nem vakít, félhomályban sem kell hozzá sötét mód), sötét fenyőzöld szöveg,
jáde kiemelés. A pár projekt (PM-mindenes) ugyanezt a szerkezetet használja őszi színekkel.

Szándékosan külön, új modul: az élő folyamat a már betöltött `modell/*.py` fájlokat nem frissíti
újraindításig, egy új fájl viszont az első importnál frissen töltődik be.
"""

from __future__ import annotations

import html

KIEMELES = "#1f7a5a"   # jáde: a kiemelőszín (= primaryColor a config.toml-ban)
HALVANY = "#dcece3"    # az idézetek halvány háttere
KARTYA = "#f6faf7"     # a kártyák háttere, a háttérnél egy árnyalattal világosabb
SZOVEG = "#1f2a24"     # sötét fenyőzöld szöveg (= textColor)
HATTER = "#eef4ef"     # halvány menta (= backgroundColor)
NYITOSAV = ("#245a46", "#1f7a5a", "#0f766e")  # a nyitósáv színátmenete: fenyő → jáde → türkiz

# A menücsoportok színe az oldalfejlécben; mind ≥ 4,5:1 kontraszttal fehér szöveggel és a
# háttéren (a teszt számolja). A nevek a `streamlit_app.py` menüjének csoportjai.
CSOPORTOK = {
    "Kezdés": "#1f7a5a",                  # jáde
    "A példa — két iteráció": "#0f766e",  # türkiz
    "Lejátszás és gyakorlás": "#2f7d32",  # fűzöld
    "Amire épül": "#245a46",              # fenyő
}


def csoport_szin(csoport: str) -> str:
    return CSOPORTOK.get(csoport, KIEMELES)


def fejlec_kulcs(csoport: str) -> str:
    """Az oldalfejléc `st.container(key=…)` kulcsa: a csoport sorszáma, mert a név nem CSS-osztály."""
    return f"fejlec-{list(CSOPORTOK).index(csoport)}" if csoport in CSOPORTOK else "fejlec-x"


def css() -> str:
    fejlecek = "\n".join(
        f".st-key-{fejlec_kulcs(cs)} {{ background: {szin}; }}" for cs, szin in CSOPORTOK.items()
    )
    return f"""<style>
[data-testid="stMarkdownContainer"] blockquote {{
  border-left: 4px solid {KIEMELES}; background: {HALVANY};
  padding: .55rem 1rem; margin: .8rem 0; border-radius: 0 .5rem .5rem 0; color: {SZOVEG};
  opacity: 1;  /* a Streamlit 0,6-ra halványítja az idézetet */
}}
[data-testid="stMarkdownContainer"] blockquote :is(p, li, strong, em) {{ color: {SZOVEG}; }}
[data-testid="stMarkdownContainer"] blockquote p {{ margin: .25rem 0; }}
[class*="st-key-fejlec-"] {{
  border-radius: .9rem; padding: 1rem 1.4rem 1.1rem; margin-bottom: .4rem; gap: .35rem;
}}
[class*="st-key-fejlec-"] [data-testid="stHeading"] {{ margin: 0; }}
[class*="st-key-fejlec-"] h1 {{ color: #fff; padding: 0; margin: 0; font-size: 2.1rem; line-height: 1.2; }}
[class*="st-key-fejlec-"] h1 span[data-testid="stIconMaterial"] {{ color: #fff; }}
[class*="st-key-fejlec-"] [data-testid="stCaptionContainer"],
[class*="st-key-fejlec-"] [data-testid="stCaptionContainer"] p {{
  color: #fff; opacity: .92; margin: 0; letter-spacing: .08em; text-transform: uppercase; font-size: .75rem;
}}
{fejlecek}
.sm-hero {{
  background: linear-gradient(120deg, {NYITOSAV[0]} 0%, {NYITOSAV[1]} 55%, {NYITOSAV[2]} 100%);
  color: #fff; border-radius: .9rem; padding: 1.5rem 1.8rem 1.3rem; margin-bottom: .6rem;
}}
.sm-hero h1 {{ color: #fff; margin: 0; padding: 0; font-size: 2.3rem; line-height: 1.15; }}
.sm-hero p {{ color: #ecf7f1; margin: .45rem 0 1rem; font-size: 1.05rem; max-width: 52rem; }}
.sm-kicker {{ font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; opacity: .85; }}
.sm-stats {{ display: flex; flex-wrap: wrap; gap: .5rem; }}
.sm-stat {{ background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.35);
  border-radius: 2rem; padding: .25rem .8rem; font-size: .95rem; }}
.sm-stat b {{ font-size: 1.1rem; }}
[class*="st-key-kartya-"] {{ background: {KARTYA}; border-top: 5px solid {KIEMELES} !important; }}
.st-key-kartya-2 {{ border-top-color: {csoport_szin("A példa — két iteráció")} !important; }}
@media (max-width: 640px) {{
  .sm-hero {{ padding: 1.1rem 1.1rem 1rem; }}
  .sm-hero h1 {{ font-size: 1.6rem; }}
  [class*="st-key-fejlec-"] {{ padding: .75rem 1rem .9rem; }}
  [class*="st-key-fejlec-"] h1 {{ font-size: 1.5rem; line-height: 1.3; }}
}}
</style>"""


def nyitosav_html(cim: str, alcim: str, szamok: list[tuple[int, str]]) -> str:
    """A Bevezetés nyitósávja: kérdés, alcím és az adatokból számolt darabszámok."""
    chips = "".join(f'<span class="sm-stat"><b>{n}</b> {html.escape(c)}</span>' for n, c in szamok)
    return (
        '<div class="sm-hero"><div class="sm-kicker">Agilis · AI-first Scrum</div>'
        f"<h1>{html.escape(cim)}</h1><p>{html.escape(alcim)}</p>"
        f'<div class="sm-stats">{chips}</div></div>'
    )
