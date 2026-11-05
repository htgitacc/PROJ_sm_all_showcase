"""A felület ábrái: a bírálati sor időben, a kártyás tábla, az eszkalációs létra, a keret-sáv.

Az ábrák ugyanabból az állapotból rajzolnak, mint a táblázatos nézetek (`allapot.pillanat()`),
tehát nem vezetnek be második igazságforrást. A HTML-ábrák színei áttetszők és örökölt
szövegszínre épülnek, így világos és sötét témában is olvashatók; telefonon az oszlopok
egymás alá törnek.

Szándékosan új modul: az élő folyamat a már betöltött `modell/*.py` fájlokat nem frissíti
újraindításig, egy új fájl viszont az első importnál frissen töltődik be.
"""

from __future__ import annotations

import html

import altair as alt
import pandas as pd

from modell import allapot as allapot_modul
from modell import arculat
from modell import cimkek

TABLA_OSZLOPOK = [
    "Kész a kezdésre",
    "Megvalósítás alatt",
    "Bírálatra vár",
    "Bírálat alatt",
    "Javítás alatt",
    "Beolvadt",
]

PIROS = "#dc2626"
NARANCS = "#d97706"
KEK = arculat.KIEMELES  # a téma kiemelőszíne (régen kék, innen a név)


# --- A bírálati sor hossza az időben ------------------------------------------------


def sor_idosor(adatok) -> pd.DataFrame:
    """Eseményenként: hány elem várt bírálatra az esemény után. Minden indexre `pillanat()`."""
    sorok = []
    for i in range(len(adatok.esemenyek)):
        p = allapot_modul.pillanat(adatok.esemenyek, adatok.elemek, adatok.iteraciok, i)
        sorok.append(
            {
                "index": i,
                "sorszam": i + 1,
                "idopont": p.idopont,
                "iteracio": p.iteracio,
                "varakozo": p.darab("Bírálatra vár"),
                "esemeny": adatok.esemenyek.loc[i, "esemeny"],
            }
        )
    return pd.DataFrame(sorok)


def sor_grafikon(df: pd.DataFrame, korlat: int, kurzor: int | None = None,
                 jelolok: dict[str, int] | None = None) -> alt.LayerChart:
    """Lépcsős vonal a várakozók számáról, a korláttal, az iterációk sávjával és a kurzorral."""
    x = alt.X("sorszam:Q", title="Események sorrendje", scale=alt.Scale(nice=False, zero=False))  # 1-től, mint a csúszka
    ymax = max(int(df["varakozo"].max()), korlat) + 1

    savok = (
        df.groupby("iteracio")["sorszam"].agg(["min", "max"]).reset_index()
        .assign(cimke=lambda d: d["iteracio"].astype(str) + ". iteráció")
    )
    hatter = alt.Chart(savok).mark_rect(opacity=0.06, color="gray").encode(
        x="min:Q", x2="max:Q"
    ) + alt.Chart(savok).mark_text(align="left", dx=4, dy=8, baseline="top", color="gray").encode(
        x="min:Q", y=alt.value(0), text="cimke:N"
    )

    vonal = alt.Chart(df).mark_line(interpolate="step-after", color=KEK, strokeWidth=2).encode(
        x=x,
        y=alt.Y("varakozo:Q", title="Bírálatra vár (elem)", scale=alt.Scale(domain=[0, ymax])),
        tooltip=[
            alt.Tooltip("sorszam:Q", title="Esemény"),
            alt.Tooltip("idopont:T", title="Időpont", format="%Y-%m-%d %H:%M"),
            alt.Tooltip("varakozo:Q", title="Bírálatra vár"),
        ],
    )
    tullepes = alt.Chart(df[df["varakozo"] > korlat]).mark_circle(color=PIROS, size=60).encode(
        x="sorszam:Q", y="varakozo:Q",
        tooltip=[alt.Tooltip("varakozo:Q", title="Korlát felett")],
    )
    korlat_vonal = alt.Chart(pd.DataFrame({"y": [korlat]})).mark_rule(
        color=PIROS, strokeDash=[6, 4]
    ).encode(y="y:Q") + alt.Chart(pd.DataFrame({"y": [korlat], "t": [f"WIP-korlát: {korlat}"]})).mark_text(
        align="right", dy=-6, color=PIROS, x="width"
    ).encode(y="y:Q", text="t:N")

    retegek = [hatter, vonal, korlat_vonal, tullepes]

    if jelolok:
        jdf = pd.DataFrame([{"sorszam": i + 1, "cimke": c} for c, i in jelolok.items()])
        retegek.append(
            alt.Chart(jdf).mark_rule(color="gray", opacity=0.35, strokeDash=[2, 3]).encode(
                x="sorszam:Q", tooltip=[alt.Tooltip("cimke:N", title="Kulcspillanat")]
            )
        )
    if kurzor is not None:
        kdf = pd.DataFrame({"sorszam": [kurzor + 1], "t": ["kurzor"]})
        retegek.append(alt.Chart(kdf).mark_rule(color=NARANCS, strokeWidth=2).encode(x="sorszam:Q"))
        retegek.append(
            alt.Chart(kdf).mark_text(color=NARANCS, dy=-4, baseline="bottom", y=0).encode(
                x="sorszam:Q", text="t:N"
            )
        )
    return alt.layer(*retegek).properties(height=220)


# --- Kártyás tábla ------------------------------------------------------------------

_STILUS = """<style>
.kb{display:flex;flex-wrap:wrap;gap:8px;font-size:13px;line-height:1.3;color:inherit}
.kb .osz{flex:1 1 150px;min-width:140px;border:1px solid rgba(128,128,128,.3);border-radius:10px;padding:8px}
.kb .osz.tul{border:2px solid #dc2626;background:rgba(220,38,38,.07)}
.kb .fej{display:flex;justify-content:space-between;font-weight:600;margin-bottom:6px}
.kb .fej .db{font-weight:400;opacity:.75}
.kb .osz.tul .fej .db{color:#dc2626;opacity:1;font-weight:600}
.kb .k{border:1px solid rgba(128,128,128,.3);border-left:4px solid KIEMELES;border-radius:6px;padding:4px 6px;margin-bottom:5px;background:rgba(128,128,128,.06)}
.kb .k.kock{border-left-color:#d97706}
.kb .k.nagy{border:2px solid #dc2626;border-left:4px solid #dc2626}
.kb .id{font-weight:600}
.kb .meta{font-size:11px;opacity:.7}
.kb .ures{font-size:12px;opacity:.5;font-style:italic}
.kb-jel{font-size:11px;opacity:.7;margin-top:6px}
.kb .tulj{font-size:11px;font-weight:600;color:#dc2626;margin:-2px 0 6px}
</style>"""


def tabla_html(elemallapot: pd.DataFrame, korlatok: dict[str, int], meretkorlat: int,
               max_beolvadt: int = 4) -> str:
    """A pillanat elemei oszlopokba rendezve. A korlátot túllépő oszlop és a túl nagy elem piros."""
    oszlopok = []
    for nev in TABLA_OSZLOPOK:
        elemek = elemallapot[elemallapot["allapot"] == nev]
        korlat = korlatok.get(nev)
        tul = korlat is not None and len(elemek) > korlat
        db = f"{len(elemek)} / {korlat}" if korlat is not None else str(len(elemek))
        kartyak = []
        lista = elemek.tail(max_beolvadt) if nev == "Beolvadt" else elemek
        for _, e in lista.iterrows():
            osztaly = ["k"]
            if str(e.get("magas_kockazat", "")) in ("igen", "True", "true"):
                osztaly.append("kock")
            meret = int(e["meret_sor"]) if pd.notna(e.get("meret_sor")) else 0
            if meret > meretkorlat:
                osztaly.append("nagy")
            meta = []
            if meret:
                meta.append(f"{meret} sor")
            if nev == "Bírálat alatt" and e.get("biralo"):
                meta.append(html.escape(str(e["biralo"])))
            if nev == "Bírálatra vár" and pd.notna(e.get("varakozas_ora")):
                meta.append("most került be" if e["varakozas_ora"] < 0.5 else f"{cimkek.ora(e['varakozas_ora'])} vár")
            cim = html.escape(str(e["cim"]))
            kartyak.append(
                f'<div class="{" ".join(osztaly)}" title="{cim}"><span class="id">{html.escape(str(e["elem_id"]))}</span> '
                f'{cim[:34] + ("…" if len(cim) > 34 else "")}<div class="meta">{" · ".join(meta)}</div></div>'
            )
        if nev == "Beolvadt" and len(elemek) > max_beolvadt:
            kartyak.insert(0, f'<div class="ures">+{len(elemek) - max_beolvadt} korábbi</div>')
        if not kartyak:
            kartyak.append('<div class="ures">üres</div>')
        oszlopok.append(
            f'<div class="osz{" tul" if tul else ""}"><div class="fej"><span>{nev}</span>'
            f'<span class="db">{db}</span></div>'
            f'{"<div class=tulj>korlát felett</div>" if tul else ""}{"".join(kartyak)}</div>'
        )
    jelmagyarazat = (
        '<div class="kb-jel">Zöld csík: elem · narancs: magas kockázatú · piros keret: a méretkorlát '
        f"({meretkorlat} sor) felett · piros oszlop: a WIP-korlát felett</div>"
    )
    return _STILUS.replace("KIEMELES", KEK) + '<div class="kb">' + "".join(oszlopok) + "</div>" + jelmagyarazat


# --- Eszkalációs létra --------------------------------------------------------------


def letra_html(letra: dict[int, tuple[str, str]], hanyan: dict[int, int]) -> str:
    """Az öt fok lépcsőként; ahol hibaosztály áll, ott kiemelve, darabszámmal."""
    fokok = []
    for fok in sorted(letra):
        nev, teendo = letra[fok]
        db = hanyan.get(fok, 0)
        szin = {1: "128,128,128", 2: "217,119,6", 3: "220,38,38"}.get(fok, "127,29,29")
        aktiv = db > 0
        fokok.append(
            f'<div class="fok" style="margin-top:{(5 - fok) * 12}px;'
            f'border-color:rgba({szin},{0.9 if aktiv else 0.3});background:rgba({szin},{0.14 if aktiv else 0.03})">'
            f'<div class="sz">{fok}. fok</div><div class="n">{html.escape(nev)}</div>'
            f'<div class="t">{html.escape(teendo)}</div>'
            f'<div class="db">{db} hibaosztály</div></div>' if aktiv else
            f'<div class="fok" style="margin-top:{(5 - fok) * 12}px;border-color:rgba({szin},0.3)">'
            f'<div class="sz">{fok}. fok</div><div class="n">{html.escape(nev)}</div>'
            f'<div class="t">{html.escape(teendo)}</div></div>'
        )
    return (
        """<style>
.lt{display:flex;flex-wrap:wrap;gap:6px;align-items:flex-start;font-size:12px;line-height:1.3;color:inherit}
.lt .fok{flex:1 1 150px;min-width:130px;border:2px solid;border-radius:10px;padding:8px}
.lt .sz{opacity:.7}
.lt .n{font-weight:600;font-size:13px}
.lt .t{opacity:.8;margin-top:2px}
.lt .db{margin-top:6px;font-weight:600}
</style><div class="lt">"""
        + "".join(fokok)
        + "</div>"
    )


# --- Keret és vállalás --------------------------------------------------------------


def keret_sav_html(vallalt: float, keret: float, cimke_vallalt: str = "vállalt",
                   cimke_keret: str = "bírálati keret") -> str:
    """Vízszintes sáv: mennyi fér bele (keret) és mennyit vállaltak; a túlvállalás piros."""
    skala = max(vallalt, keret) * 1.1 or 1
    tul = vallalt > keret
    szin = PIROS if tul else KEK
    keret_szoveg = f"{keret:.1f}".replace(".", ",")
    return f"""<div style="font-size:13px;color:inherit;margin:4px 0 10px">
<div style="position:relative;height:22px;border-radius:6px;background:rgba(128,128,128,.12)">
<div style="position:absolute;left:0;top:0;bottom:0;width:{vallalt / skala * 100:.1f}%;background:{szin};opacity:.75;border-radius:6px"></div>
<div style="position:absolute;top:-3px;bottom:-3px;left:{keret / skala * 100:.1f}%;border-left:2px dashed {NARANCS}"></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:3px;opacity:.8">
<span><b style="color:{szin}">{vallalt:g}</b> {cimke_vallalt}{" — túlvállalás" if tul else ""}</span>
<span style="color:{NARANCS}">{cimke_keret}: {keret_szoveg}</span></div></div>"""


# --- Terv és mérés ------------------------------------------------------------------


def parameter_elteres_grafikon(terv: dict, mert: dict) -> alt.Chart:
    """A három paraméter eltérése a tervtől, százalékban. A `t` növekedése és az `R` csökkenése
    egyaránt a keretet szűkíti, ezért a színezés az irányt a keretre gyakorolt hatás szerint adja."""
    nevek = {"R": "Napi bírálati idő (R)", "t": "Egy elem átnézése (t)", "r": "Javítási körök (r)"}
    # Melyik irány szűkíti a keretet: R kisebb, t nagyobb, r nagyobb.
    szukit = {"R": -1, "t": 1, "r": 1}
    sorok = []
    for k, nev in nevek.items():
        if not terv.get(k):
            continue
        elteres = (float(mert.get(k, 0) or 0) - float(terv[k])) / float(terv[k]) * 100
        rossz = elteres * szukit[k] > 0
        sorok.append({"Paraméter": nev, "Eltérés (%)": round(elteres, 1),
                      "Hatás": "szűkíti a keretet" if rossz else "bővíti vagy semleges",
                      "Terv": terv[k], "Mért": mert.get(k)})
    df = pd.DataFrame(sorok)
    return alt.Chart(df).mark_bar().encode(
        y=alt.Y("Paraméter:N", title=None, sort=None),
        x=alt.X("Eltérés (%):Q", title="Eltérés a tervtől (%)"),
        color=alt.Color("Hatás:N", scale=alt.Scale(domain=["szűkíti a keretet", "bővíti vagy semleges"],
                                                    range=[PIROS, KEK]), legend=alt.Legend(orient="bottom", title=None)),
        tooltip=["Paraméter", "Terv", "Mért", "Eltérés (%)"],
    ).properties(height=130)
