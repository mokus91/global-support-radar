# A Global Support Radar önépítő működése

## Mit épít fel automatikusan?

A `.github/workflows/source-discovery.yml` naponta négyszer (01:23, 07:23, 13:23 és 19:23 UTC) elindítja a hivatalos források felderítését. A folyamat többek között:

1. újraépíti a 193 ENSZ-tagállam nemzeti portáljegyzékét;
2. frissíti a támogatási adatforrásokból származó keresési pillanatképeket;
3. ellenőrzi a JSON-adatokat és a forráskimeneteket;
4. frissíti a forrásállapotot, a változásnaplót és a minőségi jelentést;
5. a `scripts/build_country_pages.py` segítségével automatikusan létrehozza az országoldalakat;
6. frissíti a webhelytérképet, és az új országoldalakra mutató hivatkozásokat helyez el az országjegyzékben;
7. ellenőrzés után visszamenti a generált adatokat és oldalakat a projektbe.

A forrásfelderítő workflow sikeres futása után a GitHub Pages közzétételi folyamata publikálja a repository tartalmát.

## Adatbiztonsági korlátok

- Az automatikusan felfedezett link nem válik automatikusan igazolt támogatássá.
- A történeti nemzeti portálhivatkozás történeti/ellenőrizetlen jelölést kap.
- A generátor nem talál ki támogatási összeget, határidőt vagy jogosultságot.
- A forrásrekordok nyitottságát kizárólag külön ellenőrzés igazolhatja.
- Ha az adatgyűjtés vagy validáció hibázik, a folyamat nem tekinti sikeres frissítésnek a hibás kimenetet.

## Mit nem csinál önállóan?

A rendszer nem módosítja saját programkódját korlátlanul, nem telepít fizetős szolgáltatást, nem vállal költséget, nem kezel banki adatot, és nem küld felhasználói adatot harmadik félnek. A kódmódosítások tesztelést és verziókezelést igényelnek.

## Ellenőrzés

A futások állapota a GitHub Actions felületén követhető. A generált országoldalak és a webhelytérkép csak a sikeres adatgyűjtés és commit után tekinthetők frissítettnek.
