# Globális méretezhetőség és terhelhetőségi terv

**Döntés:** a jelenlegi statikus oldal jó induló felület egy fokozatosan bővülő, elsősorban olvasási forgalmú partnerkatalógushoz. A jelenlegi állapot alapján azonban nem állítható, hogy a rendszer nagy forgalomra terheléses teszttel igazoltan felkészült.

## Rövid válasz: bírni fogja?

- A partnerjelöltek számának növekedése önmagában nem terheli meg arányosan a szervert, ha az adatokat statikus fájlokban tároljuk és CDN szolgálja ki őket.
- A böngésző terhelése viszont nőhet, ha több ezer rekordot egyszerre töltünk be és jelenítünk meg.
- A GitHub Pages hivatalos dokumentációja 1 GB-os publikált oldalmaximumot, 100 GB/hó puha sávszélességi limitet és 429-es korlátozás lehetőségét írja le. GitHub Pages nem használható ingyenes kereskedelmi hostingként online üzlet vagy elsődlegesen SaaS működtetésére. Üzleti bevételszerzés előtt ezért külön, kereskedelmi használatra alkalmas hostingot kell választani és ellenőrizni.
- Cloudflare Pages lehetséges későbbi alternatíva: a Free csomag 20 000 fájlt enged projektenként, egy fájl legfeljebb 25 MiB lehet. A statikus assetkérések díjmentesek, a Functions viszont külön Workers-kvótához tartozik. Ez nem beállított vagy jóváhagyott migráció.

## Javasolt architektúra – 0 Ft-os fejlesztési szakasz

### 1. Statikus frontend, külön adatfájlok
A HTML/CSS/JavaScript maradjon könnyű. A partnerrekordokat ne egyetlen óriási HTML- vagy JavaScript-tömbbe írjuk. Külön JSON-adatfájlokban tároljuk őket.

### 2. Ország- és régióalapú adatdarabolás
Javasolt könyvtárszerkezet:
- `data/partners/index.json` – metaadatok, régiók és országok jegyzéke;
- `data/partners/europe/<ISO2>.json`;
- `data/partners/africa/<ISO2>.json`;
- `data/partners/asia/<ISO2>.json`;
- `data/partners/north-america/<ISO2>.json`;
- `data/partners/south-america/<ISO2>.json`;
- `data/partners/oceania/<ISO2>.json`.

Csak a kiválasztott ország vagy régió adatát töltsük le. A teljes katalógus ne töltődjön le minden látogatónál.

### 3. Keresés és megjelenítés
- ország- és kategóriaszűrő;
- kezdetben böngészőoldali szűrés az éppen betöltött ország/régió adatán;
- lapozás vagy „továbbiak betöltése”;
- kis méretű JSON;
- ne rajzoljunk ki több ezer kártyát egyszerre;
- ne töltsünk le minden ország rekordját a kezdőoldal betöltésekor.

### 4. Gyorsítótárazás és frissesség
A statikus fájlok CDN-gyorsítótárazása jó teljesítményt adhat. Az adatfájlok verziózott fájlnévvel vagy ellenőrzött cache-szabállyal frissüljenek. A támogatási státuszoknál a frissesség fontosabb, mint a maximális cache-idő: minden rekord őrizze meg az ellenőrzés dátumát és a hivatalos forrást.

### 5. Backend csak akkor, amikor tényleg szükséges
A felhasználói fiók, előfizetés, fizetés, jogosultságkezelés, személyre szabott értesítés és partner CRM később külön backend/API és biztonsági ellenőrzés feladata. Ezeket nem szabad pusztán statikus HTML-ben vagy nyilvános JSON-ban megvalósítani.

## Kapacitási kapuk

Nem ígérünk előre konkrét egyidejű látogatószámot mérés nélkül. A következő kapukon kell átmenni:

1. Adatminőség: duplikációk, hibás URL-ek, hiányzó országkódok, ellenőrzési dátumok tesztelése.
2. Frontend: 100, 1 000 és 10 000 szintetikus rekordkal betöltési és keresési teszt; ez szintetikus teszt, nem valódi forgalmi ígéret.
3. Hálózat: mobilhálózati teszt, lassú kapcsolat, nagy JSON és hibás/hiányzó adatfájl kezelése.
4. Terhelés: fokozatos, engedélyezett teszt az éles hostingon, 429/5xx hibák, válaszidő és cache-találati arány mérése.
5. Élesítés: kereskedelmi használatra megfelelő hosting, adatvédelmi és biztonsági felülvizsgálat, visszaállítási terv.

## Mit ne tegyünk?

- Ne töltsük az összes világadatot egyetlen HTML-fájlba.
- Ne kérjünk minden oldalletöltésnél külső API-adatot.
- Ne építsünk ingyenes, korlátlan automatikus lekérdezést más weboldalakra.
- Ne használjunk tömeges e-mailt vagy agresszív adatgyűjtést.
- Ne állítsunk be fizetős tárhelyet, domaint, API-t vagy adatbázist tulajdonosi jóváhagyás nélkül.
- Ne tekintsük a GitHub Pages jelenlegi ingyenes tárhelyét a későbbi kereskedelmi szolgáltatás végleges hosztolásának.

## Jelenlegi mérési állapot

- A projekt statikus GitHub Pages frontend.
- A partnerkatalógus első áttekintő oldala létrejött.
- Valódi látogatottsági, sávszélességi, válaszidő- és egyidejű felhasználói mérési adatot ebben a fejlesztési körben nem szereztünk.
- Terheléses teszt nem futott; ezért konkrét felhasználószám vagy garantált teljesítmény nem adható meg.

## Hivatalos műszaki források

- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- GitHub Pages terms: https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features
- Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/
- Cloudflare Pages Functions pricing: https://developers.cloudflare.com/pages/functions/pricing/

## Következő fejlesztési sorrend

1. Partneradatok külön JSON-fájlokba rendezése.
2. Régió/ország szerinti betöltés és lapozás.
3. Adatminőségi és duplikációs tesztek.
4. 100/1 000/10 000 rekordos szintetikus böngészőteszt.
5. Hostingdöntés csak akkor, amikor a kereskedelmi funkciók ténylegesen szükségesek és a költség/üzleti feltételek ellenőrizhetők.
