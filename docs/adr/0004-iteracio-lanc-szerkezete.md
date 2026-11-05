# 0004 — Az iterációlánc szerkezete a szimulációban

## Státusz

Elfogadva, 2026-09-16.

## Kontextus

A szimuláció első változata egyetlen iterációt játszott le. Emiatt a visszatekintési döntésnek — hogy szabályt írunk-e a hibaosztályra, gépi kaput építünk-e köré, vagy nem lépünk — nem volt megfigyelhető következménye: a döntés az iteráció legvégén született, és a szimuláció rögtön utána véget ért.

A koncepció központi állítása viszont éppen az, hogy a tanulási hurok bizonyítéka nem az ügynök ígérete, hanem az, hogy a hibaosztály **eltűnik** (S-26, `koncepcio/03-esemenyek-es-tanulas.md`). Ez definíció szerint két iteráció összehasonlítása. Amíg a szimuláció egy iterációnál megállt, a modell legfontosabb állítását nem lehetett rajta megnézni.

A láncoláshoz el kellett dönteni, mi megy át a következő iterációba és mi nem.

## Döntés

**Átmegy:** a szabályfájl és a gépi kapuk, a teljes eseménynapló, az át nem adott munka, valamint a mért `R`, `t`, `r` paraméterek. A következő iteráció bírálati kerete innentől a **mért** paraméterekből számol, nem a kiinduló feltevésből.

**Nem megy át:** a napi bírálati keret, a WIP-állapot, a szeniorok félbehagyott bírálata, az iteráció szabályszegései és naplósorai. Ezek az iterációval együtt lezárulnak, és a mérleg pillanatképként megőrzi őket (`Allas.lezart_merlegek`).

**Az átcsúszott elem újrakezdődik.** A következő iteráció elején `athozva` eseménnyel visszakerül a tábla első oszlopába, és az ügynök elölről megcsinálja. A méret és a rejtett hibák újra keletkeznek — már az érvényes szabály- és kapukészlettel.

**A visszatekintés csak a saját iterációját nézi.** Az ismétlődő hibaosztályok számlálása az iteráció időablakára szűkül, nem a teljes láncra.

## Alternatívák, amiket elvetettünk

- **A félkész munka folytatása ott, ahol abbamaradt.** Élethűbb volna, de két dolgot rontana el. Egyrészt új állapotátmenetek kellenének a bírálati sorba és a javítás alá való visszatéréshez, ami a folyamat fogalomkészletét bővítené — a koncepció 08. dokumentuma szerint a felület nem vezethet be új fogalmat. Másrészt a félbehagyott elem rejtett hibái még a **régi** szabálykészlettel keletkeztek, tehát egy áthozott elem visszahozhatná a gépi kapu mögé zárt hibaosztályt. Pontosan azt a bizonyítékot rontaná el, amiért a lánc készült.
- **Az iterációk számának megadása az indítópanelen.** Elvetve: azt a döntést, hogy folytatod-e, a mérleg elolvasása után kell meghozni, nem előtte. A gomb ezért a zárómérleg alatt van.
- **A napló iterációnkénti nullázása.** Elvetve: az elemzőréteg (`kapacitas`, `allapot`, `jelzesek`, `tanulas`) eleve időablakkal dolgozik, tehát az összefűzött naplóból minden iterációnkénti mérőszám külön is kiszámolható — a keresztiterációs kimutatás viszont csak összefűzött naplóból lehetséges.
- **Az új keret a kiinduló feltevésből.** Elvetve: akkor a mérésnek nem volna következménye, és a szimuláció nem mutatná meg a modell visszacsatolását.

## Következmény

Az iterációablakok nem érnek össze: az új iteráció az előző utáni első munkanap reggelén kezdődik, így minden esemény pontosan egy iterációhoz tartozik. Erre teszt is van, mert ezen múlik minden iterációnkénti mérőszám.

A backlog véges (`prototipus/adatok/szimulacio/backlog.csv`, 36 tétel). Ha elfogy, a lánc véget ér, és a felület ezt kimondja. Hosszabb lánchoz a CSV-t kell bővíteni — szándékosan kézzel szerkeszthető adat marad, nem generált.

A túlvállalás ára láthatóvá vált: az átcsúszott elem a következő iteráció keretéből megy el, és a munkája elölről kezdődik.
