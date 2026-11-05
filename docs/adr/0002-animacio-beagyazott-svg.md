# 0002 — Az animáció beágyazott SVG, nem külön backend

## Státusz

Elfogadva, 2026-09-15.

## Kontextus

A prototípus négy táblázatos nézete pontos, de csak annak mond valamit, aki a folyamatban dolgozik. A projekt központi állítása — hogy nem az ügynökök sebessége a szűk keresztmetszet, hanem az emberi bírálat kapacitása — ellentmond a józan észnek, és ráadásul időbeli, mennyiségi állítás: gyors termelő, lassú fogyasztó, korlátos sor. Egy táblázat ezt rosszul adja át, egy mozgó ábra jól.

A kérdés az volt, milyen technológiával készüljön, és hogy a megjelenítő honnan vegye az állapotot.

## Döntés

Az animáció **beágyazott SVG + sima JavaScript**, az adat JSON-ként a fájlba írva. A kimenet önálló HTML-dokumentum, amelyet két úton használunk: a Streamlit ötödik nézete `streamlit.components.v1.html` hívással ágyazza be, az exportáló pedig ugyanezt írja ki szerver nélkül megnyitható fájlba.

A **tábla állapotát a Python számolja**, nem a böngésző: a `modell/animacio.py` minden kockához eltárolja a teljes sávállapotot, a meglévő `allapot.pillanat()` hívásával.

## Alternatívák, amiket elvetettünk

- **Külön FastAPI + React (vagy Svelte) alkalmazás.** Egy demóanimációért node-toolchaint, build-lépést, második portot és második üzemeltetendő szolgáltatást hozna be. A gép szabályai és a projekt mérete ellene szólnak. Ha ebből valaha termék lesz, ez a döntés újranyitható.
- **Streamlit-natív animáció** (`st.rerun` ciklusban újrarajzolt diagram). Képkockánként szerverfordulót igényelne, akadozna, és a Streamlit újrafuttatási modellje ellen dolgozna.
- **Az állapotgép újraírása JavaScriptben.** Ez lett volna a kézenfekvő, de így az állapotgépnek két megvalósítása lenne, amelyek némán elcsúszhatnának egymástól — az animáció mást mutatna, mint a négy táblázatos nézet. Ezt a `test_a_tabla_egyezik_az_allapot_modullal` teszt őrzi.
- **Előre renderelt videó vagy GIF.** Nem interaktív, és nem tudná később egy élő szimuláció eseményeit lejátszani.

## Következmény

A megjelenítő **eseményfolyamot fogyaszt**, nem CSV-t. Ez szándékos: a tervezett szimulációs fázis ugyanezt a színpadot tudja majd használni, ha a saját eseményeit ugyanebbe a forgatókönyv-szerződésbe tölti.

Egy fejlesztési kényelmetlenséggel jár: az oldal a `@st.cache_data` miatt egyszer építi fel a HTML-t, így a CSS vagy a JS módosítása **nem látszik a futó szerveren újraindítás nélkül**. Ez a fejlesztés közben már egyszer megtévesztett.
