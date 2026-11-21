# E-mailes értesítések — bevezetési terv

**Állapot: ELŐKÉSZÍTÉS, NINCS FELIRATKOZÓGYŰJTÉS ÉS NINCS KÜLDÉS.**

A projekt üzemeltetője jóváhagyta, hogy később legyen lehetőség új támogatásokról szóló e-mailes értesítésre. Ez a döntés önmagában nem jelent hozzájárulást látogatói e-mail-címek gyűjtéséhez, és nem jogosít fel e-mailek küldésére.

## Javasolt első változat
- Külön, önkéntes feliratkozás az „Új támogatásokról kérek értesítést” célra.
- Csak e-mail-cím szükséges; név ne legyen kötelező.
- A checkbox alapértelmezetten üres legyen.
- A feliratkozás ne legyen feltétele az oldal használatának.
- Külön és világos tájékoztató: milyen témákról, milyen gyakran érkezik üzenet.
- Kettős megerősítés (double opt-in) ajánlott; a feliratkozási kérelem és megerősítés bizonyítékát biztonságosan dokumentálni kell.
- Minden levélben jól látható, ingyenes leiratkozás.
- Marketing/szponzorált ajánlat csak külön, különálló hozzájárulással; az alapértesítéstől elkülönítve.
- A hozzájárulás visszavonása után a küldést le kell állítani; csak a jogszerűen szükséges minimális tiltólista-adat maradhat meg, ha annak jogalapja és ideje igazolt.

## Technikai kapu
A jelenlegi GitHub Pages statikus oldal önmagában nem biztosít biztonságos, adatvédelmi szempontból megfelelő feliratkozói adatbázist, double opt-in folyamatot, törlési/leiratkozási kezelést és naplózást. Ne tároljunk e-mail-címeket localStorage-ban, GitHub issue-ban, URL-paraméterben vagy nyilvános repository-ban.

Feliratkozó űrlap csak megfelelő szolgáltató kiválasztása, adatfeldolgozói feltételeinek és adattovábbításainak ellenőrzése, adatkezelési tájékoztató frissítése, hozzájárulási szöveg véglegesítése és biztonsági teszt után építhető be. Fizetős szolgáltatás nem kapcsolható be külön jóváhagyás nélkül.

## Nyitott kérdések
- Értesítés csak új támogatásokról és státuszváltozásokról szóljon, vagy legyen külön marketing/szponzorációs levél? Alapértelmezett döntés: csak szolgáltatási értesítés; marketing külön opt-in.
- Mely országok/nyelvek legyenek választhatók?
- Milyen gyakoriság: azonnali, heti összefoglaló vagy mindkettő?
- Melyik szolgáltató biztosít ingyenes induló szintet, megfelelő adatfeldolgozási szerződést, double opt-int, leiratkozást és export/törlést? Ezt a bevezetés előtt ellenőrizni kell.

## Jogi kiindulópontok
- E-mailes reklám természetes személynek előzetes, egyértelmű és kifejezett hozzájárulást igényel; a leiratkozásnak egyszerűnek és ingyenesnek kell lennie.
- A hozzájárulásnak önkéntesnek, tájékozottnak, konkrétnak és visszavonhatónak kell lennie.
- Az értesítési cél és a marketingcél külön kezelendő.

Források:
- NMHH: https://english.nmhh.hu/electronic-advertising
- Európai Bizottság — hozzájárulás: https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data_en
- NAIH határozat a hírlevelekről: https://www.naih.hu/hatarozatok-vegzesek?download=590%3Ahirlevekkel-kapcsolatos-adatkezeles
