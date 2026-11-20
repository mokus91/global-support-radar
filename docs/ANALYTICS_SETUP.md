# Global Support Radar — látogatottságmérés

## Állapot
A webhelybe beépítettük a GoatCounter-alapú, adatvédelmi szempontból kímélő analitikai betöltőt. **A mérés jelenleg KI van kapcsolva**, mert még nincs a tulajdonos által létrehozott ingyenes GoatCounter webhelyazonosító. A kód addig nem tölt be külső mérőszkriptet és nem küld látogatói adatot.

## Bekapcsolás
1. Hozz létre egy ingyenes fiókot a https://www.goatcounter.com/ oldalon.
2. Regisztráld a webhelyet ezzel a címmel: https://mokus91.github.io/global-support-radar/
3. A választott webhelyazonosítót írd be az `analytics-config.js` fájlban a `siteCode` mezőbe (csak az azonosító, ne URL).
4. Mentsd a fájlt a GitHub `main` ágába. A telepítés után a látogatások a GoatCounter irányítópultján jelennek meg.

## Mit mér?
Összesített oldalmegtekintéseket és hivatkozó oldalakat; a részletes kimutatások elérhetősége a szolgáltató beállításaitól függ. Ez a kód nem kér nevet, e-mail-címet, pontos helyadatot, és nem használ saját sütit vagy eszköz-ujjlenyomatot.

## Fontos
- A mérés jelenleg nem aktív, ezért a dashboard még nem fog valós adatot mutatni.
- A szolgáltató saját adatkezelési feltételeit és a vonatkozó jogi tájékoztatási kötelezettségeket a bekapcsolás előtt ellenőrizni kell.
- Ez nem Google Analytics és nem Google Search Console; a keresőből érkező teljesítményadatokat továbbra is a Search Console mutatja.
