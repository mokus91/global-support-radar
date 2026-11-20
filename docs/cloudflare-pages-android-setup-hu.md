# Cloudflare Pages beállítása Android telefonról – 0 Ft-os útmutató

**Cél:** a Global Support Radar statikus bemutatóoldalának díjmentes teszttelepítése úgy, hogy a jelenlegi GitHub Pages oldal közben változatlanul elérhető maradjon.

**Fontos:** ez előkészítő útmutató. A Cloudflare-fiók, a GitHub-engedélyezés és a Pages-projekt létrehozása tulajdonosi művelet. A projektet még nem kapcsoltuk össze, és nem történt telepítés.

## 0. Költségvédelmi szabály – ezt tartsd be

- Csak akkor folytasd, ha a felületen egyértelműen a Free / 0 Ft csomag szerepel.
- Ha bankkártyát, fizetési módot, fizetős próbaidőszakot, csomagfrissítést vagy díjköteles funkciót kér, állj meg; ne add meg az adatokat.
- Ne válassz Workers fizetős funkciót, fizetős analitikát, domaint vagy más fizetős kiegészítőt.
- Jelszót, egyszer használatos kódot, recovery kódot és API-tokent ne küldj chatben.
- Ne töröld és ne kapcsold ki a GitHub Pages oldalt.

## 1. Előkészítés telefonon

1. Nyisd meg a Cloudflare hivatalos oldalát: https://dash.cloudflare.com/sign-up
2. Hozz létre fiókot a saját e-mail címeddel, vagy lépj be a meglévő fiókba.
3. Ellenőrizd, hogy a fiókban nincs bekapcsolva fizetős csomag vagy fizetős kiegészítő.
4. Nyisd meg a Workers & Pages részt.

## 2. Pages projekt indítása

1. Válaszd a Create application / Create project lehetőséget.
2. Válaszd a Pages, majd a Connect to Git lehetőséget.
3. Kapcsold össze a saját GitHub-fiókoddal a hivatalos engedélyező képernyőn.
4. Ha lehet, csak a `mokus91/global-support-radar` repositoryhoz adj hozzáférést.
5. Válaszd ki a `global-support-radar` repositoryt és a `main` ágat.

## 3. Build-beállítások

A repository jelenleg statikus HTML/CSS/JavaScript oldalt tartalmaz. A teszttelepítéshez:

- Project name: `global-support-radar` (ha még szabad)
- Production branch: `main`
- Framework preset: `None`
- Build command: hagyd üresen
- Build output directory: `/` vagy `.` – a Cloudflare felületén elfogadott root értéket használd
- Root directory: hagyd alapértelmezetten, ha a felület nem kéri külön

Ha a felület kötelező build parancsot kér, vagy a root könyvtár beállítása nem egyértelmű, ne találgass: állj meg és kérj segítséget.

## 4. Első telepítés ellenőrzése

1. Indítsd el a deployt kizárólag Free beállítással.
2. Várd meg, amíg a Cloudflare sikeres telepítést jelez.
3. Nyisd meg a kiosztott `*.pages.dev` címet.
4. Ellenőrizd telefonon:
   - a főoldal betöltődik;
   - a magyar és angol nyelvváltás működik;
   - ország- és kategóriaszűrés működik;
   - a keresési találatok és hivatalos forráslinkek megnyílnak;
   - a változásnapló és a partneroldalak betöltődnek;
   - a PWA kezdőképernyőre telepíthető;
   - nincs fizetési űrlap vagy fizetős regisztráció.
5. Próbáld ki asztali böngészőben is, ha elérhető.

## 5. Átállási tilalom

A `pages.dev` cím egyelőre csak tesztcím. Ne változtasd meg a főoldali címet, DNS-t, egyéni domaint, GitHub Pages beállítást vagy repository láthatóságát. A jelenlegi GitHub Pages oldal maradjon elérhető.

Az átállás csak akkor mérlegelhető, ha:
- a Cloudflare telepítés sikeres;
- a teljes ellenőrzőlista hibamentes;
- a mobilos és asztali ellenőrzés megtörtént;
- a tulajdonos külön jóváhagyta az új elsődleges címet;
- az aktuális szolgáltatási feltételek és a tervezett felhasználás összeegyeztethetők.

A Free csomag nem jelent korlátlan vagy SLA-val garantált működést. A későbbi üzleti/pénzforgalmi használhatóságot külön kell ellenőrizni.

## 6. Hivatalos kiindulópontok

- Cloudflare regisztráció: https://dash.cloudflare.com/sign-up
- Cloudflare Pages: https://pages.cloudflare.com/
- Pages Git-integráció: https://developers.cloudflare.com/pages/get-started/git-integration/
- Pages build konfiguráció: https://developers.cloudflare.com/pages/configuration/build-configuration/

## Jelenlegi státusz

- [x] Útmutató elkészült.
- [ ] Cloudflare-fiók tulajdonosi ellenőrzése.
- [ ] GitHub repository összekapcsolása.
- [ ] Ingyenes Pages teszttelepítés.
- [ ] Mobilos és asztali ellenőrzés.
- [ ] Tulajdonosi jóváhagyás az átállásra.

**Igazolt bevétel:** 0 Ft. **Fizetős funkció:** nincs bekapcsolva.
