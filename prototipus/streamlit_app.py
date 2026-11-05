"""SM-támogató felület — prototípus.

A koncepció [08-sm-felulet-specifikacio.md] szerinti négy nézet, feltöltve a
[07-iteracios-pelda.md] két iterációjának adataival.

A felület beavatkozási felület, nem irányítópult: azt mondja meg, mit kell most
tenni. Jelez, de nem avatkozik be — a döntést ember hozza meg.
"""

from __future__ import annotations

import streamlit as st

from modell import allapot, arculat, betoltes, cimkek, grafikonok, hatter, konyvjelzok

st.set_page_config(
    page_title="AI-first Scrum — SM-támogató felület",
    page_icon=":material/monitoring:",
    layout="wide",
)


@st.cache_data
def adatok_betoltese():
    return betoltes.betolt()


try:
    ADATOK = adatok_betoltese()
except Exception as hiba:  # noqa: BLE001 - a betöltési hibát a felhasználónak kell látnia
    st.error(f"Az adatok betöltése nem sikerült: {hiba}")
    st.stop()

ESEMENYEK = ADATOK.esemenyek


@st.cache_data
def sor_idosor():
    """A bírálati sor hossza minden eseménynél — egyszer számolódik, több nézet rajzol belőle."""
    return grafikonok.sor_idosor(adatok_betoltese())

UTOLSO = len(ESEMENYEK) - 1

# --- Könyvjelzők: a példa demonstrálandó pillanatai ------------------------------
# A definíció a modell/konyvjelzok.py-ban él, mert az animáció fejezetei is
# ugyanezekre a pillanatokra ugranak.

KONYVJELZOK = konyvjelzok.konyvjelzok(ESEMENYEK)

# A kurzor a példa elejéről indul: aki először jár itt, nem tudja, mi a vége, ezért
# elölről lépked vagy a könyvjelzőkkel ugrik (a felhasználó kérése, 2026-10-19).
if "kurzor" not in st.session_state:
    st.session_state.kurzor = 0


def _ugras(cel: int) -> None:
    st.session_state.kurzor = cel


# --- Navigáció -------------------------------------------------------------------
# Csoportokba szedve: felül a csoportok legördülő menüként jelennek meg, így egyetlen
# nézet sem bújik el egy „more” alá, és a látogató látja, mi mire való.

BEVEZETES = st.Page("app_pages/bevezetes.py", title="Bevezetés", icon=":material/info:", default=True)
BEMUTATO = st.Page("app_pages/bemutato.py", title="Vezetett bemutató", icon=":material/tour:")
# A pillanatnézetek egy adott időpont állapotát mutatják; csak ezeken van időkurzor.
# A Backlog elemgyűjtő: mindig a teljes darabolást mutatja, függetlenül attól, hol tart
# a folyamat — ezért a példa csoportjában van, de idővonal nélkül.
PILLANAT_NEZETEK = [
    st.Page("app_pages/teendok.py", title="Teendők", icon=":material/notifications_active:"),
    st.Page("app_pages/iteracio.py", title="Iteráció", icon=":material/checklist:"),
    st.Page("app_pages/elorenezes.py", title="Előretekintés", icon=":material/timeline:"),
    st.Page("app_pages/tanulas.py", title="Tanulás", icon=":material/school:"),
]
BACKLOG = st.Page("app_pages/backlog.py", title="Backlog", icon=":material/format_list_numbered:")

MENU = {
        "Kezdés": [BEVEZETES, BEMUTATO],
        "A példa — két iteráció": [*PILLANAT_NEZETEK, BACKLOG],
        "Lejátszás és gyakorlás": [
            st.Page("app_pages/animacio.py", title="Animáció", icon=":material/play_circle:"),
            st.Page("app_pages/szimulacio.py", title="Szimuláció", icon=":material/videogame_asset:"),
        ],
        # A háttéranyag csoportonként külön nézetben, hogy látszódjon, mire épül a projekt.
        hatter.CSOPORTNEV: [
            st.Page(f"app_pages/{n.oldal}.py", title=n.cim, icon=n.ikon) for n in hatter.NEZETEK
        ],
}
oldal = st.navigation(
    MENU,
    position="top",
    # Telefonon a menü az oldalsávba kerül, és ott alapból csak az első néhány nézet látszik,
    # a többi egy „View more” mögé bújik. Mind a tizenhárom nézet legyen látható.
    expanded=True,
)

# --- Oldalsáv: időkurzor ---------------------------------------------------------
# Csak a pillanatnézeteken van értelme: a Bevezetés, a bemutató, a Backlog (elemgyűjtő),
# az Animáció (saját vezérlése van), a Szimuláció és az „Amire épül” nézetei nem a kurzor
# pillanatát mutatja.

KURZOROS = oldal.url_path in {p.url_path for p in PILLANAT_NEZETEK}

if not KURZOROS:
    # Az előző nézet oldalsávja nézetváltáskor egy futásig üresen kint marad (Streamlit-
    # viselkedés), ha az új nézet nem ír bele semmit. Asztali szélességen ezért elrejtjük;
    # telefonon nem, mert ott a felső menü is az oldalsávba kerül.
    st.html(
        "<style>@media (min-width: 768px) {"
        "[data-testid='stSidebar'], [data-testid='stSidebarCollapsedControl'] {display: none;}"
        "}</style>"
    )

if KURZOROS:
    with st.sidebar:
        st.markdown("### :material/schedule: Időkurzor")
        st.caption(
            "A példa két lezárult iterációja, az elejétől. Léptesd előre, vagy ugorj bármely "
            "pillanatra — az állapot mindig az eseménynaplóból számolódik."
        )

        # A csúszka 1-től számoz, mint az alatta álló „n. / N esemény” felirat; a kurzor
        # maga 0-tól indexel, ezért itt váltunk.
        st.session_state.kurzor = st.slider(
            "Esemény sorszáma",
            min_value=1,
            max_value=UTOLSO + 1,
            value=st.session_state.kurzor + 1,
            label_visibility="collapsed",
            help="Fókuszban a nyilakkal egyesével léptethető.",
        ) - 1

        # Egyesével léptetés: egérrel a csúszka túl finom ahhoz, hogy egy eseményt lépjünk.
        vissza, elore = st.columns(2)
        vissza.button(
            "Vissza", icon=":material/chevron_left:", key="kurzor_vissza", width="stretch",
            disabled=st.session_state.kurzor <= 0,
            on_click=_ugras, args=(st.session_state.kurzor - 1,),
        )
        elore.button(
            "Előre", icon=":material/chevron_right:", key="kurzor_elore", width="stretch",
            disabled=st.session_state.kurzor >= UTOLSO,
            on_click=_ugras, args=(st.session_state.kurzor + 1,),
        )

        aktualis = ESEMENYEK.loc[st.session_state.kurzor]
        st.markdown(f"**{aktualis['idopont']:%Y-%m-%d %H:%M}**")
        st.caption(
            # A „\\.” nélkül a Markdown a sor eleji „134.”-et számozott listának veszi.
            f"{st.session_state.kurzor + 1}\\. / {UTOLSO + 1} esemény — "
            f"**{cimkek.esemeny(aktualis['esemeny'])}**"
            + (f" · {aktualis['elem_id']}" if aktualis["elem_id"] else "")
        )
        if aktualis["reszlet"]:
            st.caption(f"_{aktualis['reszlet']}_")

        st.divider()
        st.markdown("**Ugrás a példa kulcspillanataihoz**")
        for cimke, cel in KONYVJELZOK.items():
            st.button(
                cimke,
                key=f"kj_{cel}_{cimke}",
                width="stretch",
                on_click=_ugras,
                args=(cel,),
            )

        st.divider()
        st.caption(
            "A mérőszámok csapatszinten aggregáltak. A bírálók megjelenítése a "
            "terheléseloszlás követése miatt van, **nem** egyéni értékelés céljából."
        )

# --- Megosztott állapot ----------------------------------------------------------

PILLANAT = allapot.pillanat(ESEMENYEK, ADATOK.elemek, ADATOK.iteraciok, st.session_state.kurzor)

st.session_state.adatok = ADATOK
st.session_state.pillanat = PILLANAT
st.session_state.sor_idosor = sor_idosor()
st.session_state.konyvjelzok = KONYVJELZOK

# --- Arculat: a menücsoport színe az oldalfejlécben ---------------------------------
# A Bevezetésnek saját nyitósávja van (app_pages/bevezetes.py), ott nincs külön fejléc.

st.html(arculat.css())
if oldal.url_path != BEVEZETES.url_path:
    csoport = next(cs for cs, oldalak in MENU.items() if oldal.url_path in {o.url_path for o in oldalak})
    with st.container(key=arculat.fejlec_kulcs(csoport)):
        st.caption(csoport)
        st.title(f"{oldal.icon} {oldal.title}")
if KURZOROS and st.session_state.kurzor == 0:
    st.info(
        "Az időkurzor a példa **elején** áll: itt még nem történt semmi. Léptesd előre az oldalsáv "
        "**Előre** gombjával, vagy ugorj egy kulcspillanatra (például a **Torlódás**ra).",
        icon=":material/start:",
    )
oldal.run()
