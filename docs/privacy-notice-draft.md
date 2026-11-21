# Adatvédelmi tájékoztató — munkavázlat

**Global Support Radar — magánszemély által üzemeltetett független információs projekt**

**Állapot: NEM KÖZZÉTEHETŐ.** Belső munkavázlat. A hiányzó adatokat ki kell tölteni, az adatfolyamokat és külső szolgáltatók aktuális feltételeit ellenőrizni kell, majd a végleges szöveget szakértővel felül kell vizsgáltatni.

## 1. Adatkezelő
- Adatkezelő neve: Tóth Csaba Mihály (az üzemeltető kifejezetten engedélyezte a nyilvános feltüntetést).
- Közzéteendő cím: cím privát csatornán megadva; nyilvános közzétételének szükségessége és jogszerűsége még vizsgálandó.
- Adatvédelmi megkeresések e-mail-címe: csabikatoth25@gmail.com (az üzemeltető kifejezetten engedélyezte a nyilvános közzétételt); a cím működését és rendszeres figyelését még ellenőrizni kell.
- Adatvédelmi tisztviselő: [KIJELÖLÉS SZÜKSÉGESSÉGÉNEK JOGI ELEMZÉSE SZÜKSÉGES]

## 2. A szolgáltatás jellege
A Global Support Radar független tájékoztató és keresőfelület. Nem állami szerv, nem pályázatkezelő, nem dönt jogosultságról, nem nyújt jogi vagy pénzügyi tanácsadást, és nem nyújt be kérelmet a látogató nevében. A támogatások feltételeit, határidejét és elérhetőségét minden esetben az eredeti kiíró hivatalos oldalán kell ellenőrizni.

## 3. A forráskódban eddig azonosított működés (2026-11-20)
- A látogató által kiválasztott támogatások és egyes keresési / szűrési profilbeállítások a böngésző localStorage tárhelyén menthetők. A főoldal kódja ezeknél nem küld automatikusan személyes profilt a szerverre.
- A felület böngészőértesítést kérhet; az engedélyezést a böngésző kezeli.
- A keresési feltételek egy része az URL paramétereibe kerülhet, ezért az URL megosztásakor ezek is megoszthatók.
- A főoldal Google AdSense JavaScriptet tölt be (publisher ID: ca-pub-7022315203746196). Ez önmagában nem bizonyítja a hirdetésmegjelenítést vagy a fiók jóváhagyását.
- A visszajelzési / partneri folyamat GitHub Issues oldalra irányíthatja a látogatót. A GitHubon megadott adatokra a GitHub saját adatkezelési feltételei vonatkoznak; nyilvános issue-ban megadott adatok mások számára is láthatók lehetnek.
- A GitHub Pages tárhelyszolgáltató szervernaplóinak és biztonsági adatainak részleteit a szolgáltató dokumentációjából kell ellenőrizni.
- A főoldal forrásában nem találtunk Google Analytics / gtag kódot vagy közvetlen document.cookie hívást. Ez nem zárja ki, hogy külső hirdetési kód vagy későbbi szolgáltatás sütit / eszközazonosítót használjon.

## 4. Adatkezelési célok és jogalapok
A végleges tájékoztatóban célonként kell rögzíteni az adatokat, a célt, a GDPR szerinti jogalapot, a megőrzési időt, a címzetteket és az esetleges harmadik országbeli adattovábbítást. Ezeket nem szabad feltételezésből kitölteni. Ellenőrizendő területek: webhelybiztonság és szervernaplók; helyi böngészős mentések; böngészőértesítések; hirdetési technológiák; a látogató által önkéntesen kezdeményezett kapcsolatfelvétel.

## 5. Sütik és hirdetési technológiák
Nem szabad azt állítani, hogy a weboldal sütimentes, amíg a böngészőben a tényleges hálózati és tárolási működést nem teszteltük. Nem szükséges sütik vagy hasonló végberendezés-hozzáférések esetén előzetes, megfelelő hozzájárulásra lehet szükség. A hozzájárulás legyen célonként külön, visszautasítható és később visszavonható.
Az EGT-re vonatkozó hirdetési beállításokat, a Google által megkövetelt CMP-t és a hirdetések személyre szabását a tényleges AdSense-fiókállapot alapján kell dokumentálni. A kód jelenléte nem jelent jóváhagyást vagy bevételt.

## 6. Külső szolgáltatók
Előzetesen azonosított szolgáltatók: GitHub Pages / GitHub (tárhely és visszajelzési felület); Google (AdSense kód, amennyiben aktív); a támogatási programok hivatalos weboldalai (külső hivatkozások). A pontos szerepeket, adatfeldolgozói feltételeket, adatközpontokat, adattovábbítási garanciákat és megőrzési időket a szolgáltatói dokumentumokból kell ellenőrizni.

## 7. Érintetti jogok és panasz
A végleges tájékoztatóban ismertetni kell a GDPR szerinti hozzáférés, helyesbítés, törlés, korlátozás, tiltakozás, adathordozhatóság és hozzájárulás-visszavonás feltételeit, továbbá a NAIH-hoz fordulás lehetőségét. A joggyakorlásra szolgáló kapcsolattartó e-mail-cím még hiányzik.

## 8. Közzététel előtti ellenőrzőlista
- [x] Üzemeltető teljes jogi neve és nyilvános feltüntetésének engedélye rögzítve.
- [ ] Közzéteendő cím jogszerűsége és szükségessége tisztázva; a lakcím nincs engedélyezve nyilvános közzétételre.
- [x] Kapcsolattartási e-mail nyilvános közzétételét az üzemeltető engedélyezte.
- [ ] Kapcsolattartási e-mail működése és rendszeres figyelése ellenőrizve.
- [ ] Teljes localStorage-kulcslista és pontos tartalom dokumentálva.
- [ ] Böngészőértesítések működésének vizsgálata.
- [ ] Tiszta böngészőprofilban sütik, localStorage, sessionStorage, IndexedDB és külső hálózati kérések vizsgálata.
- [ ] Google AdSense / CMP tényleges beállítások ellenőrizve.
- [ ] GitHub Pages és GitHub adatkezelési / adatfeldolgozási szerepek ellenőrizve.
- [ ] Megőrzési idők, jogalapok, címzettek és nemzetközi adattovábbítások kitöltve.
- [ ] Magyar/EU adatvédelmi szakértő átnézte a végleges szöveget.

## Hivatalos tájékozódási források
- GDPR: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- Európai Bizottság — adatvédelem online: https://europa.eu/youreurope/citizens/consumers/internet-telecoms/data-protection-online-privacy/index_en.htm
- NAIH: https://www.naih.hu/
- NMHH — elektronikus reklám: https://english.nmhh.hu/electronic-advertising

Ez a munkavázlat nem jogi tanácsadás és nem helyettesíti az adatkezelési folyamatok tényleges auditját.