# Adatbesorolási és ellenőrzési szabvány

**Cél:** a Global Support Radar ne keverje össze a támogatási programot, a hivatalos portált, a hírt és a puszta adatbázis-találatot. Ez a dokumentum a kereső, a riportgenerátor és a jövőbeli adatimport közös besorolási alapja.

## 1. Támogatási kategóriák

| Kód | Magyar megnevezés | Ide tartozik |
|---|---|---|
| `housing` | Lakhatás | lakásvásárlás, bérlakás, felújítás, lakhatási támogatás |
| `family` | Család | gyermeknevelés, családi ellátás, szülői támogatás |
| `agriculture` | Mezőgazdaság | gazdálkodók, állattartás, vidékfejlesztés |
| `business` | Vállalkozás | KKV, startup, beruházás, innováció |
| `education` | Oktatás | ösztöndíj, képzés, tanulmányi támogatás |
| `healthcare` | Egészségügy | egészségügyi ellátás, megelőzés, egészségügyi szervezetek támogatása |
| `energy` | Energia | energiahatékonyság, megújuló energia, rezsitámogatás |
| `employment` | Foglalkoztatás | munkahelyteremtés, bértámogatás, álláskeresési program |
| `social` | Szociális | jövedelempótló, fogyatékossági és egyéb szociális ellátás |
| `transport` | Közlekedés | mobilitási, jármű- és közlekedési támogatás |
| `other` | Egyéb | csak akkor, ha egyik fenti kategória sem megfelelő |

A rekordnak egy elsődleges kategóriája legyen. Több célcsoport esetén a `beneficiary_types` mező használatos; nem kell ugyanazt a programot mesterségesen több rekordra bontani.

## 2. Rekordtípusok – nem minden találat támogatás

A `record_type` mező lehetséges értékei:

- `programme`: hosszabb távú támogatási program vagy ellátási konstrukció.
- `call`: konkrét, meghirdetett pályázati felhívás.
- `benefit`: jogszabály vagy hivatalos tájékoztató alapján működő ellátás/juttatás.
- `portal`: hivatalos kereső- vagy ügyintézési portál; önmagában nem támogatási ajánlat.
- `announcement`: hír, közlemény vagy módosítás; nem feltétlenül jelent új pályázatot.
- `dataset-discovery`: adatbázis vagy adatkészlet felfedezett hivatkozása; nem igazolt támogatási lehetőség.
- `directory-entry`: országos vagy intézményi forrásjegyzék egy bejegyzése.

A portál, közlemény, adatbázis és címtár nem jelenhet meg konkrét, nyitott támogatásként.

## 3. Jelentkezési állapot

Az `application_status` mező:

- `open`: a hivatalos forrásból ellenőrzött, aktuálisan nyitott jelentkezési időszak.
- `upcoming`: hivatalosan meghirdetett, de még el nem kezdődött beadási időszak.
- `closed`: a jelentkezés lezárult.
- `unknown`: nem áll rendelkezésre elég bizonyíték az állapot megállapításához.
- `not-applicable`: folyamatos ellátás, tájékoztató vagy portál, amelynél nincs klasszikus pályázati időablak.

**Biztonsági szabály:** hiányzó vagy bizonytalan állapot soha nem alakítható automatikusan `open` értékké. A határidő nélküli rekord sem tekinthető automatikusan nyitottnak.

## 4. Ellenőrzési dimenziók

A `verification_dimensions` mezőben külön kell jelölni:

- `official_source_checked`: az eredeti hivatalos forrás megnyitható és a rekordhoz tartozik.
- `application_window_checked`: a beadási időszak és a határidő ellenőrizve.
- `eligibility_checked`: célcsoport és fő jogosultsági feltételek ellenőrizve.
- `amount_checked`: egyéni támogatási összeg és pénznem ellenőrizve.
- `latest_amendments_checked`: a legfrissebb módosítások és közlemények ellenőrizve.

Egyetlen igaz dimenzió nem teszi a teljes rekordot minden szempontból ellenőrzötté. A felhasználói felületen és a szervezeti riportban a hiányzó ellenőrzéseket világosan jelezni kell.

## 5. Megjelenítési és minőségi szabályok

1. Minden rekordhoz HTTPS hivatalos forráslink szükséges.
2. A forrás utolsó ellenőrzésének időpontja kötelező és időzónás ISO 8601 formátumú.
3. A program egyéni támogatási maximuma és a teljes pályázati keret két külön adat.
4. A lezárt, visszavont vagy lejárt állapot minden nyitott jelzést felülír.
5. Hibás dátum, hibás összeg, hibás JSON vagy nem biztonságos URL esetén a rekordot ki kell zárni a nyitott ajánlatok közül.
6. A gépi fordítást fordításként, az automatizált adatbázis-találatot jelöltként kell megnevezni.
7. A látogató mindig az eredeti kiírásban ellenőrizze a jogosultságot, a beadási módot és a feltételeket.

## 6. Jelenlegi adatminőségi pillanatkép

A 2026. november 20-i minőségi jelentés 18 adatfolyamot és 2 199 rekordot vizsgált. A jelentésben 1 rekord szerepelt ellenőrzött nyitottként, 212 API-időablak jelöltként, 1 907 hivatalos listából származó jelöltként, 74 ellenőrizetlenként és 5 egyébként. A 2 199-es ellenőrzött rekordszám a jelentés kategóriaösszesítéseinek összege; ez nem 2 199 igazolt támogatási ajánlat.

A pillanatkép idővel változik. A weboldalnak mindig a legutóbb sikeresen előállított minőségi jelentést kell használnia, és nem szabad a régi adatot frissként feltüntetnie.

## 7. Kapcsolódó technikai fájlok

- `data/programme.schema.json`: közös rekordmezők és megengedett értékek.
- `scripts/audit_opportunity_quality.py`: adatminőségi összesítés.
- `scripts/validate_project.py`: JSON-, URL- és adatfolyam-integritás.
- `scripts/generate_organization_report.py`: szervezeti riportok státuszérzékeny előállítása.
