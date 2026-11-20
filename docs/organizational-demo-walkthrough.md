# Szervezeti bemutató – 5 perces demó és visszajelzési lap

**Verzió:** 2026-11-20  
**Státusz:** belső bemutatóanyag; nem kereskedelmi ajánlat, nem ügyfélnek elküldött dokumentum.

## A demó célja

Nem azt kell bizonyítani, hogy a rendszer minden ország minden támogatását ismeri. Azt kell tesztelni, hogy egy szervezet számára hasznos-e egy olyan, dátumozott összefoglaló, amely:
- több ország hivatalos forrásait egy riportba rendezi;
- megkülönbözteti a hivatalos oldalon ellenőrzött nyitott felhívást az adatbázis-időablak szerinti jelölttől;
- megőrzi az eredeti forráslinket, az adatpillanatot és az ellenőrzési korlátokat;
- nem állít jogosultságot, ha azt a kiírás teljes feltételrendszere nem igazolja.

## 5 perces bemutató menete

### 0:00–0:45 – A probléma

„A több országban dolgozó szervezeteknek sokszor különböző nyelvű hivatalos oldalakon kell keresniük. A célunk annak tesztelése, hogy egy egységes, forráslinkekkel és ellenőrzési státusszal ellátott riport csökkenti-e az első körös tájékozódás idejét.”

### 0:45–1:30 – A termék határai

Mutassuk meg a Global Support Radar főoldalát és a keresőt. Mondjuk el egyértelműen:
- ez fejlesztés alatt álló MVP;
- a globális országválasztó nem jelent teljes globális pályázati lefedettséget;
- a találatok egy része ellenőrizendő jelölt, nem igazoltan nyitott pályázat;
- a rendszer nem végez jogosultsági döntést és nem nyújt be kérelmet.

### 1:30–3:30 – A riportminta

Nyissuk meg a [2026-11-20-i minta szervezeti riportot](sample-organization-report-2026-11-20.md).

Mutassuk be:
1. A szűrési célt: vállalkozás/startup, Chile és Spanyolország.
2. A chilei CORFO-rekordot: a hivatalos felhívásoldal nyitottként jelzett státusza és a feltüntetett határidő.
3. A spanyol rekordot: hivatalos nyilvántartási API szerinti időablak-jelölt, amelynél az eredeti kiírás további ellenőrzést igényel.
4. A kétféle státusz közötti különbséget.
5. A forrásnaplót, a dátumozást és a korlátokat.

### 3:30–4:30 – A szervezet munkafolyamata

Kérdezzük meg:
- Ki használná a riportot a szervezetnél?
- Milyen országokat és témaköröket kellene figyelni?
- Milyen gyakoriság lenne hasznos?
- Melyik adat nélkül nem hoznának döntést?
- Mi az a hiba vagy hiányosság, ami miatt nem használnák?

### 4:30–5:00 – Következő lépés

„A következő lépés nem automatikus előfizetés vagy szerződés. Először egy pontosan körülhatárolt, kézi mintát szeretnénk a visszajelzésük alapján javítani. Csak akkor érdemes pilotról beszélni, ha a riport ténylegesen hasznos és a működési feltételek rendezettek.”

## Visszajelzési pontozólap

Minden pont 0–2 értéket kapjon: **0 = nem hasznos / hiányzik; 1 = részben hasznos / javítandó; 2 = egyértelműen hasznos.**

| Szempont | Pont (0–2) | Megjegyzés |
|---|---:|---|
| Ország- és témakörválasztás illeszkedése |  |  |
| Hivatalos források megbízhatósága |  |  |
| Nyitott és ellenőrizendő jelöltek elkülönítése |  |  |
| Határidők és összegek érthetősége |  |  |
| Riport formátuma és áttekinthetősége |  |  |
| Frissítési gyakoriság |  |  |
| Időmegtakarítás a jelenlegi folyamathoz képest |  |  |

**Összpontszám:** /14

### Döntési szabály a visszajelzés után

- **0–5 pont:** a termékérték jelenleg nem igazolt; a problémát és a célcsoportot újra kell vizsgálni.
- **6–10 pont:** célzott javítás és újabb minta szükséges.
- **11–14 pont:** érdemes egy szűk, kézi pilotot megtervezni; ez még nem jelent fizetési hajlandóságot vagy ügyfél-elköteleződést.

A pontszám mellett legalább egy konkrét, valós munkafolyamatot és egy ténylegesen hiányzó funkciót is rögzíteni kell. Udvarias dicséret vagy általános érdeklődés nem minősül vásárlási szándéknak.

## Belső státusznapló

| Mutató | Jelenlegi érték |
|---|---:|
| Kutatott szervezeti célpont | 20 |
| Elküldött megkeresés | 0 |
| Megtartott bemutató | 0 |
| Beérkezett visszajelzés | 0 |
| Igazolt érdeklődő | 0 |
| Pilot | 0 |
| Fizető ügyfél | 0 |
| Tényleges bevétel | 0 Ft |

A státuszokat csak megtörtént, dokumentálható esemény után szabad módosítani.

## 0 Ft-os és tulajdonosi korlátok

- A demó előkészítése és a kézi bemutató nem igényel fizetett hirdetést vagy előfizetést.
- Külső megkeresést, e-mailt vagy bemutató-időpontkérést csak külön tulajdonosi jóváhagyás után szabad küldeni.
- Nem ígérhető teljes országos/globális lefedettség, támogatási jogosultság, nyertes pályázat vagy garantált időmegtakarítás.
- Fizetős pilot előtt rendezni kell a kereskedelmi tárhelyet, adatvédelmet, szerződési, számlázási és adózási feltételeket.
- A GitHub Pages nem használható ingyenes kereskedelmi SaaS- vagy tranzakciós tárhelyként; a kereskedelmi indulás külön tárhelykapuhoz kötött.
- Minden kiadás előzetes tulajdonosi jóváhagyást igényel. A projekt továbbra is 0 Ft saját tőkéből indul.

## A demó után rögzítendő adatok

Csak a szükséges üzleti kapcsolattartási adatokat rögzítsük, megfelelő jogalappal és tájékoztatással. A visszajelzés lehet név nélkül is. Ne kérjünk érzékeny személyes adatot, ügyféladatot vagy bizalmas pályázati anyagot.
