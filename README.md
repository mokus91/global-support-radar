# Global Support Radar

**Élő oldal:** https://mokus91.github.io/global-support-radar/

A Global Support Radar mobilbarát, magyar és angol nyelvű kereső és hivatalos forrásgyűjtemény állami támogatásokhoz, pályázatokhoz és szociális ellátásokhoz.

## Tulajdonosi, jogi és biztonsági dokumentáció

- [Tulajdonosi és szellemi tulajdon nyilvántartása](docs/ownership-and-ip.md)
- [Jogosultsági bizonyítékok naplója](docs/rights-evidence-log.md)
- [Külső anyagok és licencek](THIRD_PARTY_NOTICES.md)
- [Ikonok és grafikai elemek eredetnyilvántartása](docs/asset-provenance-register.md)
- [Üzemeltetési biztonság és tulajdonosi ellenőrzőlista](docs/production-security-checklist.md)
- [Privát forráskód és telepítés célarchitektúrája](docs/owner-control-and-deployment-plan.md)
- [0 Ft-os indulás, önfinanszírozás és tulajdonosi nyereség terve](docs/zero-budget-self-funding-plan.md)
- [Bevételi motor, szervezeti pilot és értékesítési terv](docs/revenue-engine-roadmap.md)
- [Személyre szabott érdeklődői kérdésvázlatok](docs/prospect-interview-guides.md)
- [Második 10 szervezeti célpont kutatása](docs/next-10-organizational-prospects.md)
- [Fizetőképes ügyféljelöltek – harmadik kutatási hullám](docs/revenue-prospects-wave-3.md)
- [Három személyre szabott üzleti bemutatóvázlat](docs/three-prospect-demo-briefs.md)
- [Magyarország / innováció és K+F – ellenőrzött szervezeti riportminta](docs/sample-organization-report-2026-11-20.md)
- [Partnerhálózat-építési rendszer és megkeresési folyamat](docs/partner-growth-engine.md)
- [Nemzetközi partnerkutatás – 6. hullám (Afrika, Ázsia, Latin-Amerika)](docs/global-partner-collection-wave-6.md)
- [Második hullámos partnerhálózati térkép](docs/partner-network-map-wave-2.md)
- [Kereshető partnerjelölt-adatbázis](partner-network.html)
- [Adatbesorolási és ellenőrzési szabvány](docs/data-classification-standard.md)
- [Szervezeti riportgenerátor – használat és szűrés](docs/organization-report-generator.md)

## Első fizetős riportpilot – belső előkészítés

- [Első fizetős riportpilot ajánlati kerete és sikerfeltételei](docs/first-paid-report-pilot.md)

## Automatikus riportgyártás

- [Automatikus szervezeti riportgyártás](docs/automated-organization-report-production.md)

## Önálló bevételi működés\n\n- [Önálló bevételi működés és élesítési kapuk](docs/autonomous-revenue-operations.md)\n\n## Bevételfogadás és tulajdonosi kifizetés

- [Fizetési elszámolás és tulajdonosi kifizetés előkészítési terve](docs/payment-and-owner-payout-readiness.md)

## Nyilvános bétaindítás – 0 Ft-os terv

- [0 Ft-os nyilvános bétaindítás és ingyenes tárhely-migrációs ellenőrzőlista](docs/free-launch-readiness.md)

## Mi működik jelenleg?

- Reszponzív weboldal magyar és angol kezelőfelülettel.
- Helyi könyvjelzők: a látogató elmentheti a számára érdekes lehetőségeket; a mentések kizárólag az adott böngésző eszközén, localStorage-ban maradnak.
- A szűrt keresési találatok CSV-fájlba exportálhatók, táblázatkezelőben megnyitható formátumban.
- A keresések megoszthatók egyedi URL-lel: a keresőszó, ország, kategória és nyelv a hivatkozásban marad; a személyes mentések nem kerülnek bele.
- Telepíthető webalkalmazás (PWA): Androidon a böngésző „Hozzáadás a kezdőképernyőhöz / Telepítés” lehetőségével indítható.
- A telepített alkalmazás gyorsműveleteket kínál a világszintű forráskeresőhöz és a magyar támogatási portálokhoz; a PWA stabil alkalmazásazonosítót és kategóriákat is deklarál.
- A telepíthetőséghez külön 192×192 pixeles általános PNG-ikon, 512×512 pixeles Android maskable ikon és Apple kezdőképernyő-ikon is tartozik; a fő grafika a maszk biztonságos középső zónájában marad.
- Offline módban a felület gyorsítótárazott váza megnyitható, és figyelmeztetés jelzi, hogy az élő adatok nem frissülnek. A pályázati JSON-adatokat a service worker szándékosan nem tárolja, így nem tüntet fel régi adatot aktuálisként.
- A mentett, határidővel rendelkező lehetőségek iCalendar (ICS) fájlba exportálhatók; a naptárbejegyzés 7 nappal korábbi emlékeztetőt tartalmaz. Az emlékeztető a felhasználó saját naptáralkalmazásától függ.
- Nagy találati listáknál fokozatos betöltés működik, így mobilon sem jelenik meg egyszerre több ezer kártya.
- Országválasztó az ISO országkód-lista alapján, lokalizált országnevekkel.
- Tíz támogatási kategória: lakhatás, család, mezőgazdaság, vállalkozás, oktatás, egészségügy, energia, foglalkoztatás, szociális támogatás és közlekedés.
- Világszintű forrásnavigátor: az ENSZ 193 tagállamának nemzeti e-kormányzati portáljegyzéke, az ILO szociális védelmi országprofiljai és a Világbank ASPIRE adatbázisa.
- 71 ország-specifikus hivatalos forráslink 46 országra, köztük a francia Aides-territoires helyi támogatáskereső és a brit Find a Grant hivatalos portálja. A többi ENSZ-tagállamnál külön megjelölt, történeti UN DESA portálhivatkozás jelenik meg; ezek URL-jeit 2013-ban ellenőrizték, ezért nem tekinthetők friss vagy ellenőrzött támogatáskeresőnek.
- 27 EU-tagállam nemzeti EU-finanszírozási portálja és 27 országra vonatkozó Európai Bizottság/MISSOC szociális védelmi tájékoztató.
- A 27 nemzeti EU-finanszírozási portál mezőgazdasági és hat további kategóriájú linkfelderítése átmeneti hálózati hibák esetén legfeljebb két, 9 másodperces időkorlátú próbálkozással fut; a találatok továbbra is ellenőrizendő forráslinkek, nem automatikusan nyitott támogatások.
- Hat uniós kategória- és finanszírozási gyűjtőoldal, valamint hivatalos francia és német vállalkozásfinanszírozási adatbázisok. A francia Aides-territoires API-ból napi katalógusimport készül; a katalógusrekord nem igazolja a beadási határidőt vagy a nyitott jelentkezést.
- Egységes nemzetközi támogatási adatstandard: az egyéni maximális támogatási összeg és a teljes pályázati keret külön mezőben szerepel; a pénznem és az összeg jelentése is megőrződik. A kereső ezeket a közös mezőket használja, és a teljes keretet nem nevezi egyéni támogatásnak.
- A fő kereső hét automatikus hivatalos adatkapcsolatból jelenít meg jelölteket: Japan JGrants (Japán), CORFO (Chile), SNPSAP/BDNS (Spanyolország), Grants.gov (USA), UKRI (Egyesült Királyság), NKFIH (Magyarország) és EU Funding & Tenders (Európai Unió). A rekordok státusza és ellenőrzöttsége forrásonként eltér; a kereső nem állítja, hogy minden jelölt nyitott pályázat.
- Japán JGrants: napi lekérdezés a japán Digitális Ügynökség nyilvános API-jából, aktív jelentkezési időszakra szűrve. A címek japánul maradnak; a lekérdezés nem teljes körű.
- Chile CORFO: napi ellenőrzés a Start-Up Chile Growth 13 hivatalos felhívásoldalán.
- Spanyolország SNPSAP/BDNS: napi nyilvános REST API-lekérdezés; az utolsó 50 regisztrált felhívás részletes jelentkezési időszakát ellenőrzi, és csak aktív vagy határozatlan jelentkezési ablakot mutat. Nem teljes katalógus. A nyitott státusz, határidő és maximális társfinanszírozás csak a hivatalos oldal alapján kerül be; a részletes jogosultságot továbbra is a jogszabályi feltételek határozzák meg.
- Chile Sercotec: hivatalos felhívásoldalról rögzített, külön jelölt pillanatfelvétel; jelenleg nem automatikus napi adatkapcsolat.
- Külön ausztrál ARC kutatási támogatási panel (archív/felfedezési adatok, nem általános nyitott pályázati lista) és kanadai CIHR RSS-panel (szűk, egészségkutatási terület; üres lekérés nem jelenti azt, hogy Kanadában nincs támogatás).
- Magyar hivatalos kiindulópontok családtámogatáshoz, lakhatáshoz, mezőgazdasághoz, vállalkozáshoz, civil/kulturális támogatáshoz és kutatás-fejlesztéshez.
- Nyolc hivatalos magyar háztartástámogatási tájékoztató és böngészőben futó, előzetes eligazító. Az eligazító válaszai helyben maradnak, nem kerülnek szerverre és nem tárolódnak.
- Automatikus NKFIH RSS-hírgyűjtés; a hírek ellenőrizetlen pályázati jelöltek, nem garantáltan nyitott felhívások.
- 125 bejegyzés az ellenőrzött hivatalos forrásregiszterben.
- Automatikus forrásfrissítés naponta négyszer (01:23, 07:23, 13:23 és 19:23 UTC) GitHub Actions segítségével; kézi workflow-indítás is be van állítva. A sikertelen külső lekérések külön hibastátuszt kapnak, és ahol biztonságos, az előző adatpillanatkép megmarad.
- A források elérhetőségét külön napi ellenőrzés vizsgálja. A weboldalon külön adatfrissítési állapotpanel mutatja a 18 automatikusan vizsgált adatfolyam legutóbbi ellenőrzési idejét és eredményét; az ellenőrzés nem jelent támogatási jogosultságot vagy nyitott pályázatot. A 401/403/429 vagy hálózati hiba nem feltétlenül jelent megszűnt oldalt.

## Fontos korlátok — mit nem állít a rendszer?

Ez egy működő MVP, nem teljes világméretű támogatási adatbázis. Az országválasztó globális, de az automatikus pályázati adatkapcsolatok jelenleg csak néhány országra és programcsoportra terjednek ki. Sok ország esetében a rendszer hivatalos portálra irányít, nem pedig egyenként feldolgozott aktuális támogatásokat mutat.

A felismert pályázati rekordok többsége **ellenőrizetlen jelölt**. A keresőtalálat vagy adatbázis-bejegyzés önmagában nem bizonyítja, hogy a felhívás még nyitott, az összeg igényelhető, vagy a látogató jogosult. A felhasználónak mindig meg kell nyitnia az eredeti hivatalos kiírást, és ellenőriznie kell a határidőt, a jogosultságot, az összeget és a benyújtás módját.

A kezelőfelület jelenleg magyar és angol nyelvű; a programok eredeti címeit és forrásnyelvét megőrizzük. Nem állítjuk, hogy minden ország saját nyelvén teljes fordítás érhető el.

A történeti támogatási adatbázisok, odaítélt támogatások nyilvántartásai, forrásjegyzékek és aktuális pályázati felhívások külön vannak kezelve. A korábbi támogatás vagy egy általános adatbázis-bejegyzés nem jelent most igényelhető támogatást.

A weboldal nem nyújt be kérelmet, nem hoz jogosultsági döntést, nem kér érzékeny személyes adatot, és nem garantál támogatást.

## Adatforrások és automatizálás

A napi GitHub Actions folyamat a következő fő adaptereket futtatja:

| Forrás | Mit gyűjt? | Korlát |
| --- | --- | --- |
| data.europa.eu | EU-s közadatkatalógus-metaadatok | Nem egyedi pályázati jogosultság |
| EU Funding & Tenders | EU-s felhívásjelöltek | A hivatalos témalapon ellenőrizendő |
| EU CAP Network | Mezőgazdasági és vidéki innovációs felhívásjelöltek | A forrásoldalon ellenőrizendő |
| 27 EU nemzeti portál | Mezőgazdasági és több ágazati hivatkozás | Linkfelderítés, nem nyitott pályázat-ellenőrzés |
| Grants.gov | Amerikai szövetségi pályázatok | Előre jelzett vagy szervezeteknek szóló lehetőségek is lehetnek |
| UKRI | Brit kutatásfinanszírozási lehetőségek | Nem teljes brit támogatási katalógus |
| Japan JGrants | Aktív jelentkezési időszakú japán támogatások | Kulcsszavas API-lekérdezés, nem teljes leltár |
| Spain SNPSAP/BDNS | Legutóbbi 50 regisztrált felhívás jelentkezési időszakának ellenőrzése | Nem teljes katalógus; csak API szerinti aktív időszakok |
| Chile CORFO | Start-Up Chile Growth 13 | Egy hivatalos felhívásoldal napi ellenőrzése |
| Australian ARC | Kutatásfinanszírozási rekordok | Külön archív/felfedezési panel |
| Canadian CIHR | Egészségkutatási RSS-hírek | Szűk terület, külön panel |
| New Zealand Funding Explorer | Hivatalos üzleti támogatási katalógus | Programlistázás; nincs automatikusan igazolt nyitott státusz vagy határidő |
| Magyar nyíltadat- és RSS-források | Adatkatalógusok és pályázati hírek | A hírek nem automatikusan nyitott kiírások |

## Adatstruktúra

- `index.html` — felhasználói felület és keresési logika.
- `data/source-registry.json` — hivatalos forrásregiszter (125 rekord).
- `data/worldwide-national-support-sources.json` — 71 ország-specifikus forrás 46 országból.
- `data/un-national-portals.json` — 193 ENSZ-tagállam történeti nemzeti portáljegyzéke.
- `data/global-support-directory.json` — globális hivatalos és szociális védelmi hivatkozások.
- `data/europe-national-portals.json` — EU-tagállami finanszírozási portálok.
- `data/eu-social-protection-country-pages.json` — 27 EU-tagállam MISSOC tájékoztatója.
- `data/hu-household-support.json` — magyar háztartástámogatási tájékoztatók.
- `data/*-discovery.json` — automatikusan vagy kézzel frissített felfedezési rekordok.
- `scripts/` — adatforrás-adapterek, országportál-építők és ellenőrzések.
- `.github/workflows/source-discovery.yml` — napi adatfrissítő folyamat.
- `docs/architecture.md` — adatfolyam és ellenőrzési szabályok.
- `docs/data-standard.md` — országokon átívelő közös rekord-, pénzügyi és jogosultsági adatstandard.

## Helyi futtatás

A napi workflow Python 3.12-t használ. A fő ellenőrzés:

```bash
python -m pip install certifi pycountry
python -m compileall -q scripts
python scripts/validate_project.py
```

Az egyes adapterek külön is futtathatók a `scripts/` mappából.

## Ellenőrzési szabály

Egy rekord csak akkor kaphat „open-and-current” státuszt, ha az eredeti hivatalos felhívásoldal igazolja a nyitott állapotot, a határidőt, a jogosultak körét, a támogatás feltételeit és a jelentkezési útvonalat. A jelenlegi automatikus adapterek többsége felfedezést végez, nem teljes körű jogosultsági ellenőrzést; ezért az eredmények ellenőrizetlen jelöltként jelennek meg.

## Adatvédelem és későbbi bevételszerzés

A jelenlegi MVP nem igényel felhasználói fiókot, és nem tárol személyes jogosultsági profilokat. Érzékeny adatot nem szabad gyűjteni, ha az nem feltétlenül szükséges. A személyes adatokat nem szabad értékesíteni. A későbbi hirdetések vagy szponzorált megjelenések egyértelműen jelölendők, és nem befolyásolhatják a források ellenőrzését vagy az organikus találati sorrendet.


## Keresőoptimalizálás és felfedezhetőség

A weboldal magyar nyelvű alapértelmezett címet és leírást, Open Graph megosztási metaadatokat, Schema.org WebSite/SearchAction strukturált adatot, robots.txt fájlt és XML oldaltérképet használ. Az oldaltérkép kizárólag a stabil kezdőoldalt tartalmazza; az automatikusan felfedezett támogatásjelöltek nem kapnak külön indexelhető URL-t, amíg nincs hozzájuk ellenőrzött, önálló részletes oldal. Ez segít elkerülni a vékony vagy félrevezető keresőtalálatokat.

## Globális méretezhetőség és terhelhetőség

- [Globális skálázási és terhelhetőségi terv](docs/global-scale-architecture.md)

## Bevételi modell és termékfejlesztési irány

- [Bevételi pipeline és státuszszabályok](docs/revenue-pipeline-operations.md)

A bevételszerzéshez külön, egyértelműen jelölt hirdetési és szponzorált felületek, opcionális prémium értesítések, mentett keresések és szervezeti/partneri csomagok tervezhetők. A jelenlegi GitHub Pages kiadás statikus frontend: önmagában nem biztosít biztonságos felhasználói fiókot, előfizetés-kezelést, fizetést vagy szerveroldali jogosultság-ellenőrzést. Ezeket csak külön backenddel, adatvédelmi és fizetési folyamatokkal szabad élesíteni. A fizetős funkciók nem befolyásolhatják a hivatalos források minősítését vagy a természetes találati sorrendet.


## Tulajdonosi és jogi dokumentáció

- [Proprietary rights notice](LICENSE)
- [Ownership and intellectual-property record](docs/ownership-and-ip.md)
- [Rights and development evidence log](docs/rights-evidence-log.md)
- [Third-party materials and source obligations](THIRD_PARTY_NOTICES.md)

Ezek a dokumentumok a projekt eredeti anyagainak védelmi szándékát és a fejlesztési nyomvonalat rögzítik. Nem helyettesítik az aláírt jogátruházási megállapodásokat, és nem teszik a külső adatokat vagy szoftvereket a projekt tulajdonává. A nyilvános GitHub-tárhely továbbra is nyilvános, a GitHub feltételei szerint megtekinthető és fork-olható.

- Tulajdonosi és üzemeltetési kontrollterv: `docs/owner-control-and-deployment-plan.md` (technikai terv, nem jogi igazolás).

- [Szervezeti bemutató és visszajelzési lap](docs/organizational-demo-walkthrough.md)

- [Szervezeti pilot végrehajtási és minőségellenőrzési munkalap](docs/organizational-pilot-execution-checklist.md)


### Többprofilos szervezeti riportok

- Profilbeállítások: `config/report-profiles.json`
- Többprofilos riportgenerátor: `scripts/build_report_portfolio.py`
- Automatizált gyártás és tesztek: `docs/automated-organization-report-production.md`


### Támogatási lehetőségek változásfigyelése

- Változásnapló olvasható összefoglalója: `scripts/build_opportunity_change_digest.py`
- Szabályok és korlátok: `docs/opportunity-change-digest.md`


- [Nyilvános adatváltozási napló](updates.html)
