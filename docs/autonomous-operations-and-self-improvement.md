# Önálló működési és önfejlesztési terv

Frissítve: 2026-11-20

## Cél
A Global Support Radar a lehető legtöbb ismétlődő technikai és adatfrissítési feladatot automatikusan végezze. A tulajdonosnak elsősorban az üzleti döntésekkel, a jóváhagyásokkal és a jogszerűen realizált nyereséggel kelljen foglalkoznia.

Ez fokozatos automatizálási terv, nem annak állítása, hogy a rendszer már teljesen önálló vagy bevételt termel.

## Automatizált folyamatok

| Terület | Automatizálás | Ütemezés / indítás | Biztonsági korlát |
|---|---|---|---|
| Hivatalos támogatási források | Ország- és forrásfelderítő adapterek futtatása, adatok frissítése | naponta többször | csak engedélyezett, nyilvános hivatalos források |
| Adatminőség | séma-, forrás-, dátum-, státusz- és duplikációellenőrzés | adatfrissítés után és ütemezve | hibás rekord nem kerülhet publikálásra |
| Változásfigyelés | új, módosult és lejárt lehetőségek követése | minden adatfrissítés után | forrásbizonyíték és ellenőrzési időpont megőrzése |
| Weboldal egészsége | publikus oldal, JSON feedek és frissesség ellenőrzése | 6 óránként | hiba esetén GitHub-riasztás |
| Visszajelzések | visszajelzések címkézése és anonimizált statisztika | beérkezéskor és naponta | személyes adatok nem kerülnek nyilvános statisztikába |
| Folyamatos fejlesztés | kódellenőrzés, regressziós tesztek, fejlesztési backlog | naponta | automatikus javaslat igen, éles kódmódosítás csak tesztelt és ellenőrzött módon |
| Közzététel | Pages build/deploy | jóváhagyott main commit után | sikertelen validáció esetén ne tekintsük késznek |

## Önfejlesztési ciklus

1. **Észlelés:** hibák, elavult források, hiányzó országok, rossz rekordok és felhasználói visszajelzések gyűjtése.
2. **Elemzés:** a rendszer prioritást rendel a problémákhoz: biztonság, adatpontosság, működés, lefedettség, használhatóság, bevételi lehetőség.
3. **Javaslat:** automatikus, bizonyítékokra épülő fejlesztési backlog készül.
4. **Teszt:** minden kódváltozás előtt fordítási, séma- és regressziós teszt szükséges.
5. **Ellenőrzés:** a staging és a publikus oldal állapotát külön ellenőrizni kell.
6. **Jóváhagyás:** a kockázatos vagy üzleti hatású változás tulajdonosi jóváhagyást igényel.
7. **Tanulás:** a hibák és visszajelzések alapján frissülnek a tesztek, ellenőrzési szabályok és prioritások.

## Mit végezhet automatikusan?

- Nyilvános hivatalos források ellenőrzése és adatfrissítése.
- Rekordok normalizálása, duplikációk kiszűrése, lejárati státuszok felülvizsgálata.
- Minőségjelentés, változásnapló, fejlesztési backlog és hibajegy frissítése.
- Tesztek és build futtatása.
- Hiba esetén riasztás és újrapróbálkozás a beállított keretek között.

## Mihez kell tulajdonosi jóváhagyás?

- Ügyfeleknek vagy partnereknek küldött e-mail, üzenet, ajánlat vagy szerződés.
- Hirdetésvásárlás, fizetős API, előfizetés, tárhelyváltás, domain/DNS-módosítás.
- Fizetési szolgáltató, számlázás, banki adat vagy pénzmozgás beállítása.
- Árazás, szerződéses feltételek és jogi/adózási állítások módosítása.
- Olyan automatikus kódmódosítás, amely fizetést, hozzáférést, biztonságot vagy adatvédelmet érint.

## Bevétel és nyereség

A rendszer készíthet riportmintát, termékbemutatót, célpontlistát és mérheti az érdeklődést. Nem küldhet ki automatikusan értékesítési megkeresést jóváhagyás nélkül, nem állíthat be önállóan fizetést, és nem utalhat pénzt.

A nyereség csak ténylegesen beérkezett bevételből számolható: bevétel mínusz visszatérítések, szolgáltatói díjak, működési költségek és adótartalék. A tulajdonosi kifizetés a tulajdonos által jóváhagyott bankszámlára, jogszerű számlázási és adózási háttér mellett történhet.

## 0 Ft-os működési szabály

- Először a rendelkezésre álló ingyenes eszközök és kvóták használhatók.
- Fizetős szolgáltatás vagy költségvállalás nem indulhat előzetes jóváhagyás nélkül.
- Ha egy ingyenes szolgáltatás korlátja elérhetővé válik, a rendszer jelezze; ne váltson automatikusan fizetős csomagra.
- A GitHub Pages jelenlegi statikus bemutatófelület. Kereskedelmi szolgáltatás élesítése előtt a tárhely és a platform feltételeit újra ellenőrizni, és szükség esetén megfelelő tárhelyre migrálni kell.

## Jelenlegi érettségi állapot

Már létező automatizmusok: forrásfelderítés, adatminőség-ellenőrzés, változáskövetés, minőségriport, oldal-egészségfigyelés, visszajelzés-triázs, fejlesztési backlog, staging teszt és Pages deploy.

Még nem kész: teljes világméretű forráslefedettség, teljesen automatikus és hibamentes országonkénti frissítés, önálló ügyfélszerzés, ügyfélfiók, előfizetés, fizetés, számlázás, jogi/adózási folyamat, tulajdonosi kifizetés és terheléses kapacitásbizonyítás.

**Alapelv:** automatizáljuk a munkát, de ne automatizáljuk el a tulajdonosi kontrollt, a jogszerűséget és a pénzügyi biztonságot.
