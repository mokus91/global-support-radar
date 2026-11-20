# Önálló bevételi működés – következő kiépítési szakasz

Frissítve: 2026-11-20

## Cél

A rendszer automatikusan végezze el a bevétel-előkészítés ismétlődő munkáját: friss forrásadatokból riportot készít, ellenőrzi a riportot, naplózza a hiányokat, és előkészíti a szervezeti pilot anyagait. A tulajdonosnak a döntéseket, jóváhagyásokat és a tényleges nettó nyereség ellenőrzését kelljen végeznie.

## Automatikus folyamat

1. Hivatalos források adatfrissítése a meglévő source-discovery workflow-val.
2. Adatminőségi és forrásfrissességi audit a meglévő quality workflow-val.
3. Szervezeti riport előállítása a meglévő riportgenerátorral.
4. A bevételi készenlét napi ellenőrzése a `.github/workflows/revenue-readiness.yml` workflow-val.
5. A futás eredményének rövid ideig elérhető GitHub Actions artifactként történő megőrzése.
6. Hibás vagy hiányzó termékeszköz esetén a jelentés nyitott akadályként jelzi.

## Nettó nyereség elve

Csak ténylegesen beérkezett bevételt szabad bevételként számolni. A tulajdonoshoz kerülő összeg alapja:

**Nettó rendelkezésre álló nyereség = beérkezett bevétel – visszatérítések – fizetési díjak – működési költségek – adótartalék.**

A rendszer jelenleg nem fér hozzá bankszámlához, nem fogad fizetést, nem számláz és nem utal. Ezekhez később külön, biztonságos szolgáltatói beállítás, jogi/adózási ellenőrzés és tulajdonosi jóváhagyás kell.

## Korlátok

- Nincs ügyfélnek küldött automatikus e-mail vagy ajánlat.
- Nincs automatikus hirdetésvásárlás, fizetős API vagy előfizetés.
- Nincs automatikus tárhely- vagy DNS-módosítás.
- Nincs automatikus pénzmozgás.
- A GitHub Actions időzített futása késhet vagy kimaradhat; ezért a futásnapló ellenőrzése szükséges.
- A GitHub Pages jelenlegi helyzetét kereskedelmi élesítés előtt külön felül kell vizsgálni.

## Kötelező élesítési kapuk

1. Legalább egy kézzel ellenőrzött és elfogadott pilotriport.
2. Tulajdonosi jóváhagyás a megkereséshez és az ajánlati árhoz.
3. Ügyfél által elfogadott pilot és jogszerű számlázás.
4. Kereskedelmi célra megfelelő tárhely és adatvédelmi tájékoztatás.
5. Fizetési szolgáltató, visszatérítés és chargeback folyamat tesztje.
6. A tényleges nettó nyereség havi egyeztetése és a tulajdonosi kifizetés jóváhagyása.

**A cél az automatizált működés, nem a kontroll nélküli pénzügyi vagy jogi döntéshozatal.**
