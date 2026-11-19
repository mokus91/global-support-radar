# Global Support Radar — adatfolyam és ellenőrzési architektúra

## 1. Adatrétegek

1. **Forrásregiszter** — a hivatalos közzétevő, joghatóság, forrástípus, URL, hozzáférési mód és korlátozások.
2. **Forrásnavigátor** — nemzeti portálok, szociális védelmi útmutatók, tematikus adatbázisok. A portálhivatkozás önmagában nem egy konkrét támogatási program.
3. **Felfedezési adapterek** — dokumentált API-k, RSS-feedek és engedélyezett nyilvános oldalak lekérdezése. Az eredmény alapértelmezés szerint ellenőrizetlen jelölt.
4. **Normalizálás** — csak a forrás által ténylegesen közölt adatok kerülnek a rekordba; az eredeti cím, nyelv, URL, dátum és pénznem megőrzendő.
5. **Ellenőrzés** — az eredeti hivatalos programoldal, a jelentkezési időszak, jogosultak, összeg és benyújtási útvonal ellenőrzése.
6. **Közzététel** — csak a bizonyítékkal alátámasztott állapot jeleníthető meg. A lejárt és visszavont rekordokat ki kell venni az aktív találatokból.
7. **Monitoring** — időbélyegzett frissítés, URL-elérhetőség és adapterhibák naplózása.

## 2. Státuszok

- `unverified` — felfedezett rekord, az eredeti felhívás még nincs ellenőrizve.
- `official-page-checked` — a hivatalos oldal meg lett nézve, de a jelenlegi nyitottság nem bizonyított.
- `open-and-current` — az eredeti hivatalos oldal bizonyítja, hogy a program jelenleg fogad jelentkezést.
- `closed`, `expired`, `withdrawn` — nem fogad új jelentkezést.

A történeti portálhivatkozások külön `historical-directory-lead` státuszúak. Az elérhetőségi ellenőrzés csak azt jelzi, hogy egy URL válaszolt; nem bizonyítja a pályázat létezését, nyitottságát vagy a jogosultságot.

## 3. Jelenlegi automatizált források

A `.github/workflows/source-discovery.yml` napi, 04:17 UTC-s futása az alábbiakat frissíti:

- data.europa.eu nyíltadat-katalógus.
- Európai Bizottság Funding & Tenders kereső: a lekérés a legkésőbbi határidők felől halad, hogy a régi, lejárt rekordok ne töltsék ki az első oldalakat; a lejárt dátumú rekordok kiszűrésre kerülnek. A státusz továbbra is ellenőrizetlen jelölt, amíg az eredeti felhívásoldalt nem vizsgáltuk meg.
- EU CAP Network mezőgazdasági és vidéki innovációs lehetőségek.
- 27 EU nemzeti finanszírozási portál mezőgazdasági és egyéb ágazati linkjei.
- Grants.gov amerikai szövetségi pályázatok.
- UKRI brit kutatásfinanszírozási lehetőségek.
- Japan JGrants nyilvános API: aktív jelentkezési időszakú támogatások kulcsszavas keresése.
- Chile CORFO Start-Up Chile Growth 13: a hivatalos felhívásoldal státuszának, határidejének és maximális társfinanszírozásának napi ellenőrzése.
- Australian ARC kutatási támogatási rekordok.
- Canadian CIHR egészségkutatási RSS.
- Magyar nyíltadat-katalógus, pályázati közlemény RSS-próba és NKFIH RSS.
- UN DESA 193 tagállami történeti portáljegyzék építése és a 46 ország-specifikus forráslink URL-elérhetőségének ellenőrzése.

A CORFO-adapter csak az általa ellenőrzött Start-Up Chile oldalt fedi le; nem általános chilei pályázatgyűjtő. A Sercotec-adatok jelenleg külön, rögzített hivatalos pillanatfelvételként szerepelnek, nem napi automatizált feedként. A CIHR és ARC külön panelen jelenik meg, nem a fő kereső teljes körű országos kínálataként.

## 4. Globális lefedettség pontos jelentése

Az országválasztó és a forrásnavigátor globális. A 193 ENSZ-tagállami portálhivatkozás történeti UN DESA jegyzékből származik; az URL-eket 2013-ban ellenőrizték. Ezek nem tekinthetők jelenleg ellenőrzött támogatáskeresőnek. A 66 ország-specifikus hivatkozás 46 országra ad dedikáltabb hivatalos forrást. Az automatikus egyedi pályázati feedek ennél is szűkebb körűek.

A kezelőfelület jelenleg magyar és angol nyelvű. Az eredeti programcímeket és forrásnyelvet meg kell őrizni; gépi fordítás nem írhatja felül a hivatalos feltételeket.

## 5. Adapter-követelmények

Minden új adapternek:
- dokumentált API-t, RSS-t vagy jogszerűen elérhető hivatalos oldalt kell használnia;
- be kell tartania a sebességkorlátokat és az újrafelhasználási feltételeket;
- meg kell őriznie az eredeti hivatalos URL-t és nyelvet;
- nem találgathat dátumot, összeget, pénznemet vagy jogosultságot;
- mentenie kell a lekérés idejét, hibáját és a rekordok számát;
- nem emelhet egy rekordot nyitott státuszba pusztán cím, keresési kivonat vagy katalógus-metaadat alapján;
- üres vagy hibás lekérés esetén nem helyettesíthet adatot kitalált rekorddal.

## 6. Biztonság, adatvédelem és üzleti szabályok

- A kliensoldali eligazító nem küld és nem tárol személyes válaszokat.
- A rendszer jelenleg nem nyújt be pályázatot és nem hoz jogosultsági döntést.
- Érzékeny személyes adat csak szigorúan indokolt esetben gyűjthető.
- Hirdetés vagy szponzorált találat egyértelműen jelölendő, és nem befolyásolhatja az ellenőrzési státuszt.
- A hivatalos kiírás az irányadó; a weboldal nem garantál támogatást.

## 7. Validáció és üzemeltetés

A napi workflow a JSON-adatokat, a Python adapterek szintaxisát és a beágyazott JavaScriptet ellenőrzi. A `scripts/validate_project.py` hibával leáll duplikált forrásazonosító, hibás HTTPS URL, hibás rekordlista vagy JSON/JavaScript szintaktikai hiba esetén. A GitHub Actions futás sikeressége külön ellenőrizendő; a commit önmagában nem bizonyít sikeres adatfrissítést vagy Pages-deployt.
