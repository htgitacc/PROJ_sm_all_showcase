/* Az animációs színpad lejátszója.
   A forgatókönyvet a Python oldal állítja elő (modell/animacio.py), itt csak
   megjelenítés történik: a tábla állapotát nem ez a fájl számolja, hogy ne
   keletkezzen az állapotgép második, elcsúszni képes megvalósítása. */

const NS = "http://www.w3.org/2000/svg";

// --- Színpadgeometria ------------------------------------------------------------

const OSZLOPOK = {
  "Kész a kezdésre":     { x: 16,  w: 150, kartya: 130 },
  "Megvalósítás alatt":  { x: 182, w: 168, kartya: 148 },
  "Bírálatra vár":       { x: 400, w: 168, kartya: 148 },
  "Bírálat alatt":       { x: 584, w: 236, kartya: 104 },
  "Beolvadt":            { x: 836, w: 188, kartya: 52 },
};
// A javítási sáv a fő sor alatt, balra kerül: a visszavezető ív így jól látható
// irányt ad — a bírálatból vissza, majd fel az ügynökökhöz.
const JAVITAS = { x: 16, y: 400, w: 540, h: 100, kartya: 128 };
// A biztonsági lánc panelje mellé, nem rá: korábban takarta a javítási sávot.
const LANC = { x: 576, y: 400, w: 448, h: 100 };

const CIM_Y = 52;            // az oszlopcímek alapvonala
const SOR_Y = 124;           // a fő sor oszlopainak teteje
const SOR_H = 216;
const ELSO_REKESZ = 158;     // az első rekesz felső széle
const REKESZ_H = 34;
const REKESZ_LEPES = 44;
const KAPU_X = 375;

const forgatokonyv = window.FORGATOKONYV;
const kockak = forgatokonyv.kockak;
const elemek = forgatokonyv.elemek;
const korlatok = forgatokonyv.konfig.wip_korlatok;
const szeniorok = forgatokonyv.konfig.szeniorok;

let mutato = 0;
let sebesseg = 4;
let jatszik = false;
let idozito = null;

// --- Segédek ---------------------------------------------------------------------

function el(tag, attrs = {}, szulo = null) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (szulo) szulo.appendChild(e);
  return e;
}

function rovidit(szoveg, hossz) {
  return szoveg.length <= hossz ? szoveg : szoveg.slice(0, hossz - 1) + "…";
}

function idopontra(s) {
  return new Date(s.replace(" ", "T"));
}

function korlatoz(ertek, also, felso) {
  return Math.min(Math.max(ertek, also), felso);
}

// --- Állandó díszlet -------------------------------------------------------------

const svg = document.getElementById("szinpad");
const oszlopCsoportok = {};

function oszlopotRajzol(nev) {
  const o = OSZLOPOK[nev];
  const korlat = korlatok[nev];
  const g = el("g", { class: "oszlop" }, svg);
  // A bírálati sor a modell szűk keresztmetszete, ezért kap eltérő keretet.
  if (nev === "Bírálatra vár") g.classList.add("szuk-keresztmetszet");

  el("rect", { class: "oszlop-keret", x: o.x, y: SOR_Y, width: o.w, height: SOR_H, rx: 8 }, g);
  // A cím magasan van, hogy a korlátból kilógó kártyának maradjon hely az oszlop
  // fölött — épp ez a kilógás mutatja meg, hogy nincs hova betenni.
  el("text", { class: "oszlop-cim", x: o.x + 10, y: CIM_Y }, g).textContent = nev;
  if (korlat !== undefined) {
    el("text", { class: "oszlop-korlat", x: o.x + 10, y: SOR_Y + 18 }, g).textContent =
      "WIP-korlát: " + korlat;
    // A korlát fizikai rekesz: pontosan annyi hely látszik, amennyi szabad.
    for (let i = 0; i < korlat; i++) {
      el("rect", {
        class: "rekesz", x: o.x + 10, y: ELSO_REKESZ + i * REKESZ_LEPES,
        width: o.kartya, height: REKESZ_H,
      }, g);
    }
  }
  oszlopCsoportok[nev] = g;
  return g;
}

Object.keys(OSZLOPOK).forEach(oszlopotRajzol);

// A „Bírálat alatt" két alsávja a két szenior neve.
szeniorok.forEach((nev, i) => {
  const x = OSZLOPOK["Bírálat alatt"].x + 10 + i * 116;
  el("text", { class: "oszlop-korlat", x: x, y: SOR_Y + 18 }, oszlopCsoportok["Bírálat alatt"])
    .textContent = nev;
});

// Javítás alatt: visszavezető sáv a fő sor alatt.
const javitasG = el("g", { class: "oszlop" }, svg);
el("rect", { class: "oszlop-keret", x: JAVITAS.x, y: JAVITAS.y, width: JAVITAS.w, height: JAVITAS.h, rx: 8 }, javitasG);
el("text", { class: "oszlop-cim", x: JAVITAS.x + 10, y: JAVITAS.y - 10 }, javitasG).textContent = "Javítás alatt";
el("text", { class: "oszlop-korlat", x: JAVITAS.x + 128, y: JAVITAS.y - 10 }, javitasG).textContent =
  "nincs korlát — ez már lekötött bírálati kapacitás";

// A visszacsatolási hurok két szakasza: a bírálatból le a javításba, majd onnan
// vissza fel az ügynökökhöz. Az újramunka így kétszer fogyaszt bírálati keretet.
const SOR_ALJA = SOR_Y + SOR_H + 8;
el("path", {
  class: "oszlop-keret",
  d: `M ${OSZLOPOK["Bírálat alatt"].x + 40} ${SOR_ALJA} C ${OSZLOPOK["Bírálat alatt"].x + 10} ${JAVITAS.y - 16}, ${JAVITAS.x + 560} ${JAVITAS.y}, ${JAVITAS.x + 524} ${JAVITAS.y}`,
  "stroke-dasharray": "5 4",
  fill: "none",
}, svg);
el("text", { class: "oszlop-korlat", x: JAVITAS.x + 540, y: JAVITAS.y - 28 }, svg)
  .textContent = "visszaküldve";

const vissza_x = OSZLOPOK["Megvalósítás alatt"].x + 84;
el("path", {
  class: "oszlop-keret",
  d: `M ${vissza_x} ${JAVITAS.y} L ${vissza_x} ${SOR_ALJA}`,
  "stroke-dasharray": "5 4",
  fill: "none",
}, svg);
el("text", { class: "oszlop-korlat", x: vissza_x + 8, y: JAVITAS.y - 32 }, svg)
  .textContent = "újra ügynökhöz";

// Verifikáló kapu: nem oszlop, hanem két sáv közötti átjáró. A felirat a vonal
// mentén, elforgatva áll, hogy ne érjen bele a szomszéd oszlopba.
const kapuG = el("g", { class: "kapu" }, svg);
el("line", { x1: KAPU_X, y1: SOR_Y + 12, x2: KAPU_X, y2: SOR_Y + SOR_H - 12 }, kapuG);
const kapuFelirat = el("text", {
  x: KAPU_X - 6, y: SOR_Y + SOR_H / 2, "text-anchor": "middle",
  transform: `rotate(-90 ${KAPU_X - 6} ${SOR_Y + SOR_H / 2})`,
}, kapuG);
kapuFelirat.textContent = "verifikáló";

// Ügynöksáv a színpad tetején: ez a mondat a modell lényege, ezért olvassa a
// szem elsőként — és itt nem ütközik a visszavezető ív feliratával.
const ugynokG = el("g", { class: "ugynok-sav" }, svg);
el("circle", { class: "pont", cx: 20, cy: 22, r: 4 }, ugynokG);
const ugynokSzoveg = el("text", { x: 32, y: 26 }, ugynokG);
const ugynokNev = el("tspan", { class: "nev" }, ugynokSzoveg);
ugynokNev.textContent = "implementáló ügynökök";
const ugynokAllapot = el("tspan", {}, ugynokSzoveg);

// Bírálati keret sávja.
const keretG = el("g", {}, svg);
el("text", { class: "keretsav-szoveg", x: 16, y: 536 }, keretG).textContent = "Bírálati keret";
el("rect", { class: "keretsav-hatter", x: 16, y: 544, width: 1008, height: 12 }, keretG);
const keretToltes = el("rect", { class: "keretsav-toltes", x: 16, y: 544, width: 0, height: 12 }, keretG);
const keretSzoveg = el("text", { class: "keretsav-szoveg", x: 16, y: 574 }, keretG);

// Biztonsági lánc: csak a lánc eseményeinél jelenik meg.
const lancG = el("g", { class: "lanc rejtett" }, svg);
el("rect", { class: "doboz", x: LANC.x, y: LANC.y, width: LANC.w, height: LANC.h }, lancG);
const lancCim = el("text", { class: "cim", x: LANC.x + 16, y: LANC.y + 22 }, lancG);
const lancMagyarazat = el("text", { class: "magyarazat", x: LANC.x + 16, y: LANC.y + 88 }, lancG);
const lancTalalatok = el("g", {}, lancG);

// --- Kártyák: elemenként egy állandó csoport ------------------------------------

const kartyak = {};
for (const [id, adat] of Object.entries(elemek)) {
  const g = el("g", { class: "kartya rejtett" }, svg);
  const test = el("rect", { class: "test", x: 0, y: 0, width: 148, height: REKESZ_H }, g);
  const cimke = el("text", { class: "cimke", x: 8, y: 14 }, g);
  cimke.textContent = id;
  const alcim = el("text", { class: "alcim", x: 8, y: 26 }, g);
  alcim.textContent = rovidit(adat.cim, 24);
  const jelolo = el("circle", { class: "jelolo", cx: 138, cy: 10, r: 3.5 }, g);
  if (adat.magas_kockazat) g.classList.add("kockazatos");
  kartyak[id] = { g, test, alcim, jelolo };
}

// --- Egy kocka kirajzolása -------------------------------------------------------

const SAV_OSZTALY = {
  "Kész a kezdésre": "sav-keszen",
  "Megvalósítás alatt": "sav-megvalositas",
  "Bírálatra vár": "sav-biralatra",
  "Bírálat alatt": "sav-biralat",
  "Javítás alatt": "sav-javitas",
  "Beolvadt": "sav-beolvadt",
};

function kartyaHelye(sav, sorszam, kocka, id) {
  const o = OSZLOPOK[sav];
  if (sav === "Javítás alatt") {
    return { x: JAVITAS.x + 12 + sorszam * 136, y: JAVITAS.y + 34, w: JAVITAS.kartya, h: REKESZ_H };
  }
  if (sav === "Beolvadt") {
    // A beolvadt elemek apró jelvényként gyűlnek: a szám a lényeg, nem a cím.
    const oszlop = sorszam % 3, sorIdx = Math.floor(sorszam / 3);
    return { x: o.x + 10 + oszlop * 58, y: ELSO_REKESZ + sorIdx * 20, w: o.kartya, h: 16 };
  }
  if (sav === "Bírálat alatt") {
    const biralo = kocka.biralok[id] || "";
    const idx = Math.max(0, szeniorok.indexOf(biralo));
    return { x: o.x + 10 + idx * 116, y: ELSO_REKESZ, w: o.kartya, h: REKESZ_H };
  }
  const korlat = korlatok[sav];
  // A korlát fölötti elem a rekeszsor FÖLÉ kerül, kilógva az oszlopból —
  // ez maga a torlódás képe: nincs hova betenni.
  const tullepo = korlat !== undefined && sorszam >= korlat;
  return {
    x: o.x + 10,
    y: tullepo ? SOR_Y - 42 : ELSO_REKESZ + sorszam * REKESZ_LEPES,
    w: o.kartya,
    h: REKESZ_H,
    tullepo,
  };
}

function lancotFrissit(i) {
  const k = kockak[i];
  const lancEsemenyek = ["biztonsagi_talalat", "talalat_cafolva", "talalat_elfogadva"];
  if (!lancEsemenyek.includes(k.esemeny)) {
    lancG.classList.add("rejtett");
    return;
  }
  // Visszafelé keressük meg, hány találattal indult a lánc, és mennyi esett ki.
  let osszes = 0, kiejtve = 0;
  for (let j = i; j >= 0; j--) {
    if (kockak[j].esemeny === "biztonsagi_talalat" && kockak[j].talalat_szam !== null) {
      osszes = kockak[j].talalat_szam;
      break;
    }
  }
  for (let j = i; j >= 0; j--) {
    if (kockak[j].esemeny === "biztonsagi_talalat") break;
    if (kockak[j].esemeny === "talalat_cafolva" && kockak[j].talalat_szam !== null) {
      kiejtve = kockak[j].talalat_szam;
    }
  }

  lancG.classList.remove("rejtett");
  lancCim.textContent = "Biztonsági lánc — " + k.elem_id;
  lancMagyarazat.textContent = rovidit(k.reszlet, 78);
  lancTalalatok.replaceChildren();
  for (let n = 0; n < osszes; n++) {
    // A kiejtett találat üres kerettel marad ott: látszódjon, mennyit szűrt a
    // cáfoló, és mennyi jutott valóban emberi figyelem elé.
    const kiesett = n < kiejtve;
    el("rect", {
      class: "talalat" + (kiesett ? " kiejtve" : ""),
      x: LANC.x + 16 + n * 34, y: LANC.y + 36, width: 26, height: 26,
    }, lancTalalatok);
  }
  el("text", { class: "magyarazat", x: LANC.x + 16 + osszes * 34 + 8, y: LANC.y + 54 }, lancTalalatok)
    .textContent = osszes ? `${osszes} találatból ${osszes - kiejtve} marad emberi döntésre` : "";
}

function rajzol(i) {
  mutato = korlatoz(i, 0, kockak.length - 1);
  const k = kockak[mutato];

  // Fejléc
  document.getElementById("ora").textContent = k.idopont.slice(0, 16);
  document.getElementById("iteracio").textContent =
    `${k.iteracio}. iteráció — ${(forgatokonyv.iteraciok.find((it) => it.id === k.iteracio) || {}).nev || ""}`;

  const szereplo = forgatokonyv.szereplok.find((s) => s.azonosito === k.szereplo) || {};
  const sor = document.getElementById("esemeny");
  sor.className = "esemeny-sor " + (szereplo.tipus || "") + (k.forras === "levezetett" ? " levezetett" : "");
  sor.innerHTML =
    `<b>${k.szereplo}</b> · ${(window.ESEMENY_CIMKE || {})[k.esemeny] || k.esemeny}${k.elem_id ? " · " + k.elem_id : ""}` +
    (k.forras === "levezetett"
      ? ' <span class="reszlet">— levezetett lépés: a modell szerint minden elem áthalad a verifikálón, a napló csak a bukást rögzíti</span>'
      : k.reszlet ? ` <span class="reszlet">— ${k.reszlet}</span>` : "");

  // Kártyák
  const holVan = {};
  for (const [sav, idk] of Object.entries(k.tabla)) {
    idk.forEach((id, sorszam) => { holVan[id] = { sav, sorszam }; });
  }

  for (const [id, kartya] of Object.entries(kartyak)) {
    const hely = holVan[id];
    if (!hely || !SAV_OSZTALY[hely.sav]) {
      kartya.g.classList.add("rejtett");
      continue;
    }
    const p = kartyaHelye(hely.sav, hely.sorszam, k, id);
    kartya.g.classList.remove("rejtett");
    kartya.g.setAttribute("transform", `translate(${p.x}, ${p.y})`);
    kartya.test.setAttribute("width", p.w);
    kartya.test.setAttribute("height", p.h);
    kartya.jelolo.setAttribute("cx", p.w - 10);
    kartya.alcim.style.opacity = p.h < 24 ? 0 : 1;
    // A cím hossza a sávtól függ: a keskeny bírálati alsávban kevesebb fér ki.
    kartya.alcim.textContent = rovidit(elemek[id].cim, Math.max(6, Math.floor((p.w - 16) / 5.2)));

    kartya.g.classList.remove(...Object.values(SAV_OSZTALY), "tullepo");
    kartya.g.classList.add(SAV_OSZTALY[hely.sav]);
    // Pirosan jelöljük, ami kilóg a korlátból, és azt is, ami a méretkorlátot lépi túl.
    const meretes = hely.sav === "Bírálatra vár"
      && elemek[id].meret_sor > forgatokonyv.konfig.meretkorlat_sor;
    if (p.tullepo || meretes) kartya.g.classList.add("tullepo");
  }

  // Oszlopállapot
  oszlopCsoportok["Bírálatra vár"].classList.toggle("tele", k.torlodas);

  // Verifikáló kapu
  kapuG.classList.toggle("aktiv", k.esemeny === "verifikalo_atengedte");
  kapuG.classList.toggle("bukott", k.esemeny === "kapu_bukott");
  kapuFelirat.textContent =
    k.esemeny === "kapu_bukott" ? "verifikáló: bukott" : "verifikáló";

  // Ügynöksáv: a torlódás a szabály állapota, nem külön esemény.
  ugynokG.classList.toggle("all", k.torlodas);
  ugynokAllapot.textContent = k.torlodas
    ? " — állnak: a bírálati sor betelt, új feladat nem indul"
    : " — dolgoznak";

  // Bírálati keret
  const arany = k.keret.osszes ? Math.min(k.keret.elhasznalt / k.keret.osszes, 1) : 0;
  keretToltes.setAttribute("width", Math.round(arany * 1008));
  keretSzoveg.textContent =
    `${k.keret.elhasznalt} bírálati esemény a becsült ${k.keret.osszes}-ból — ` +
    "minden, ami emberi szemet igényel, ugyanebből fogy";

  lancotFrissit(mutato);

  document.getElementById("kurzor").value = mutato;
  document.getElementById("allas").textContent = `${mutato + 1}. / ${kockak.length} lépés`;
}

// --- Lejátszás -------------------------------------------------------------------

function kovetkezoKesleltetes() {
  const k = kockak[mutato];
  const kov = kockak[mutato + 1];
  if (!kov) return 0;
  // A levezetett lépés nem kap saját időbélyeget, ezért fix, látható ideig áll.
  const alap = k.forras === "levezetett"
    ? 450
    : korlatoz((idopontra(kov.idopont) - idopontra(k.idopont)) / 3600000 * 1000, 140, 2400);
  return Math.max(alap / sebesseg, 55);
}

function lep() {
  if (!jatszik) return;
  if (mutato >= kockak.length - 1) { szunet(); return; }
  rajzol(mutato + 1);
  idozito = setTimeout(lep, kovetkezoKesleltetes());
}

function indit() {
  if (mutato >= kockak.length - 1) rajzol(0);
  jatszik = true;
  document.getElementById("jatszas").textContent = "Szünet";
  idozito = setTimeout(lep, kovetkezoKesleltetes());
}

function szunet() {
  jatszik = false;
  clearTimeout(idozito);
  document.getElementById("jatszas").textContent = "Lejátszás";
}

function ugras(idx) {
  szunet();
  rajzol(idx);
}

// --- Vezérlők bekötése -----------------------------------------------------------

document.getElementById("jatszas").addEventListener("click", () => (jatszik ? szunet() : indit()));
document.getElementById("kurzor").addEventListener("input", (e) => ugras(Number(e.target.value)));

// Egyesével léptetés: gombbal, vagy a nyilakkal, ha a színpadon van a fókusz. Az időkurzor
// csúszkája fókuszban maga is lép a nyilakra, ezért ott nem kezeljük kétszer.
document.getElementById("elozo").addEventListener("click", () => ugras(mutato - 1));
document.getElementById("kovetkezo").addEventListener("click", () => ugras(mutato + 1));
document.addEventListener("keydown", (e) => {
  if (e.target.id === "kurzor" || e.altKey || e.ctrlKey || e.metaKey) return;
  if (e.key === "ArrowLeft") { e.preventDefault(); ugras(mutato - 1); }
  if (e.key === "ArrowRight") { e.preventDefault(); ugras(mutato + 1); }
});

document.querySelectorAll("[data-sebesseg]").forEach((gomb) => {
  gomb.addEventListener("click", () => {
    sebesseg = Number(gomb.dataset.sebesseg);
    document.querySelectorAll("[data-sebesseg]").forEach((g) =>
      g.setAttribute("aria-pressed", String(g === gomb))
    );
  });
});

const fejezetSav = document.getElementById("fejezetek");
forgatokonyv.fejezetek.forEach((f) => {
  const gomb = document.createElement("button");
  gomb.textContent = f.cimke;
  gomb.addEventListener("click", () => ugras(f.idx));
  fejezetSav.appendChild(gomb);
});

// --- Külső felület: a képernyőkép-készítés és a hivatkozható pillanat miatt ------

window.animacio = { ugras, indit, szunet, kockaSzam: kockak.length };

const kurzor = document.getElementById("kurzor");
kurzor.max = kockak.length - 1;

const horgony = location.hash.match(/kocka=(\d+)/);
rajzol(horgony ? Number(horgony[1]) : 0);
