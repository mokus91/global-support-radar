# Böngészős tárolás és közzétételi audit — 2026-11-20

**Projekt:** Global Support Radar  
**Állapot:** belső technikai ellenőrzés, nem jogi megfelelőségi tanúsítvány.

## 1. Forráskód alapján azonosított helyi tárolás

A főoldal `index.html` fájljában három `localStorage` kulcs szerepel:

| Kulcs | Mentett adat | Cél |
|---|---|---|
| `gsr_saved_opportunities_v1` | mentett támogatási rekordok azonosítói | kedvencek / mentett lehetőségek |
| `gsr_seen_change_events_v1` | legfeljebb 500 megtekintett változási eseményazonosító | ismétlődő változásjelzések elkerülése |
| `gsr_support_profile_v1` | ország, pályázótípus, kategória, státusz, rendezés, nyelv és mentés ideje | keresési profil helyi mentése |

A fenti adatok a főoldal JavaScriptje szerint a látogató böngészőjében tárolódnak. Ez nem bizonyítja, hogy más, beágyazott vagy később hozzáadott szolgáltatás nem kezel adatot.

## 2. Egyéb technikai adatfolyamok

A kódvizsgálatban azonosított elemek:
- Google AdSense JavaScript betöltése a `pagead2.googlesyndication.com` címről.
- A saját webhelyről JSON adatfájlok betöltése `fetch()` használatával.
- Külső hivatalos támogatási portálokra mutató hivatkozások.
- A visszajelzési folyamat GitHub Issues oldalra irányít.
- Keresési/szűrési paraméterek az URL-be kerülhetnek a `history.replaceState` használatával.
- A profil mentésekor mentési időbélyeg is rögzül.

A statikus forráskód önmagában nem mutatja meg a ténylegesen beállított sütiket, harmadik fél hálózati kéréseit, IP-naplózását, böngésző-ujjlenyomatát vagy az AdSense fiókbeállításait.

## 3. Amit nem igazoltunk

- Tiszta böngészőprofilban a sütik, IndexedDB, sessionStorage és teljes hálózati kérések vizsgálata.
- Google AdSense jóváhagyás és tényleges hirdetésmegjelenítés.
- EGT látogatókhoz szükséges Google által elfogadott CMP tényleges működése.
- A tárhelyszolgáltató naplóinak pontos adattartalma és megőrzési ideje.
- Az adatkezelő személyazonossága, jogalapok, megőrzési idők és érintetti kapcsolattartási csatorna.

Ezért jelenleg nem szabad azt állítani, hogy a weboldal sütimentes, teljes GDPR-megfelelőséggel működik, vagy hogy a látogatói adatok semmilyen külső szolgáltatóhoz nem jutnak el.

## 4. Kiadási és publikálási ellenőrzés

A forrásrepo legutóbbi belső dokumentációs commitjaihoz tartozó GitHub Pages buildjei sikeresek:
- `2fdd08b3` — legal checklist: success
- `2a02f237` — operator details template: success
- `314acfb4` — privacy draft: success
- `e1806693` — address-options review: success

A gyökérdomain telepítő workflow legutóbbi ellenőrzött sikeres futása még korábbi forrásverzióra készült (`6d060faa`, 2026-11-20 21:23 UTC). A workflow óránként, 17 perckor ütemezett, ezért az újabb dokumentációs commitok gyökérdomainre történő szinkronizálása a lekérdezés pillanatában még nem volt igazolt. A forrásrepo saját Pages buildje ettől külön fut.

## 5. Következő kötelező vizsgálatok

1. Böngésző DevTools / tiszta profil: Network, Application/Storage, Cookies, Local Storage, IndexedDB.
2. AdSense fiók: webhely státusz, Auto ads, CMP állapot és EU/EGT beállítások.
3. GitHub Pages/GitHub adatfeldolgozási feltételek és naplózási tájékoztatók ellenőrzése.
4. A végleges adatkezelési tájékoztató összehangolása a tényleges működéssel.
5. Csak ezután jogi szakértői ellenőrzés és nyilvános jogi oldalak publikálása.

**Közzétételi szabály:** a belső audit nem kerül a látogatók elé. Adatvédelmi tájékoztatót, cookie panelt vagy impresszumot nem szabad hiányos vagy kitalált adatokkal publikálni.
