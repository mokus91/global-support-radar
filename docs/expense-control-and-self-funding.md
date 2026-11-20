# Kiadási nyilvántartás és önfinanszírozási szabályzat

Frissítve: 2026-11-20

## Alapelv

A Global Support Radar semmilyen költséget nem vállalhat addig, amíg annak teljes fedezete ténylegesen be nem érkezett, és a tulajdonos az adott kiadást külön jóvá nem hagyta. **Bevétel nélkül a költési keret 0 Ft.** Várható bevétel, ajánlat, érdeklődő vagy pipeline-érték nem fedezet.

## Minden nyilvántartandó költség

A `data/financial-ledger.json` külön tervezett kiadási kategóriákban tartja nyilván:

- tárhely, forgalom, túllépés és extra kapacitás;
- domain, DNS és megújítás;
- e-mail, hírlevél, SMS és push értesítés;
- fizetős API, adatlicenc, fordítás és külső adatforrás;
- automatizálás, CI/CD, worker, szerver, adatbázis és futtatási kvóta;
- fizetési szolgáltató, bank, tranzakció, devizaváltás, visszaterhelés;
- könyvelés, számlázás és adminisztráció;
- adók, járulékok és kötelező terhek;
- jogi, fogyasztóvédelmi és adatvédelmi megfelelés;
- biztonság, mentés és monitorozás;
- marketing, hirdetés és ügyfélszerzés;
- ügyfélszolgálat, telefon, külső munka és alvállalkozó;
- visszatérítés, reklamáció és chargeback;
- hardver, szoftverlicenc és egyéb beszerzés;
- egyéb, váratlan kiadás.

A lista nem jelenti azt, hogy ezeket most meg kell venni. Induláskor minden tervezett összeg 0 Ft és blokkolt.

## Kötelező pénzügyi kapu

A csak olvasási ellenőrző a következő képletet használja:

`szabad pénz = nyitó egyenleg + igazoltan beérkezett bevétel - bizonylatos kiadások - elkülönített adó/visszatérítési tartalék`

`jóváhagyható költési plafon = a szabad pénz és a tulajdonos által jóváhagyott plafon közül az alacsonyabb`

Egy tervezett kiadás csak akkor megy át az ellenőrzésen, ha:
1. tényleges, igazolt szabad pénz fedezi;
2. a tulajdonos által jóváhagyott költési plafonba belefér;
3. az adott tételre külön tulajdonosi jóváhagyás is van.

A keretellenőrzés **nem fizetési engedély**. A tényleges megrendelést és fizetést minden esetben a tulajdonos végzi a szolgáltató saját felületén. A rendszer nem tárol banki adatot, nem kezdeményez tranzakciót, nem változtatja meg a jóváhagyott plafont.

## Bizonylatok és nyilvántartás

Minden bevételhez és kiadáshoz egyedi azonosító, HUF összeg, státusz és bizonylat-/elszámolási hivatkozás kell. A személyes és banki adatok nem kerülhetnek nyilvános GitHub-fájlba; a hivatkozás lehet belső, nem érzékeny bizonylatazonosító. A tényleges könyvelést és adóbevallást nem helyettesíti ez az egyszerű nyilvántartás.

## Jelenlegi induló állapot

- Nyitó egyenleg: 0 Ft.
- Igazolt bevétel: 0 Ft.
- Rögzített tényleges kiadás: 0 Ft.
- Elkülönített tartalék: 0 Ft.
- Tulajdonos által jóváhagyott költési plafon: 0 Ft.
- Jelenleg elkölthető keret: **0 Ft**.
- Minden tervezett költség blokkolt; nincs automatikus feltöltés, fizetős csomag, bankkártya vagy automatikus megújítás.

## Korlátok

A modul költségvetési ellenőrzés, nem könyvelőprogram, nem banki kapcsolat, nem fizetési rendszer és nem garantálja a szolgáltatók jövőbeli díjait. Minden szolgáltatás díját a megrendelés előtt az aktuális hivatalos feltételek alapján kell ellenőrizni. Adózási és jogi kötelezettségekhez könyvelő vagy megfelelő szakember szükséges.
