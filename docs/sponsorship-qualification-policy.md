# Hirdetői és szponzori minősítési szabályzat

Frissítve: 2026-11-20

## Cél

A hirdetési bevétel csak olyan szolgáltatótól származhat, amely releváns a támogatáskereső közönség számára, és nem veszélyezteti a független tájékoztatást. A `data/sponsorship-inventory.json` külön nyilvántartja a lehetséges kategóriákat és a tényleges partnerkapcsolatokat.

## Jelenlegi állapot

- Kutatott hirdető: 0
- Jóváhagyott megkeresés: 0
- Elküdött megkeresés: 0
- Aktív szponzor: 0
- Igazolt hirdetési bevétel: 0 Ft
- Külső hirdetési kód: nincs bekapcsolva

Ezek a számok a nyilvántartás induló állapotát tükrözik; nem jelentenek piaci felmérést.

## Elfogadható kategóriák

1. Pályázati tanácsadók, könyvelők és KKV-fejlesztési szolgáltatók.
2. Civil és közösségi szervezetek releváns programjai.
3. Oktatási, kutatási és innovációs szolgáltatók.

A kategória önmagában nem jelent jóváhagyást. Minden egyes hirdetőt külön kell minősíteni.

## Kötelező minősítési ellenőrzőpontok

- Valós, beazonosítható szervezet és ellenőrizhető nyilvános webes jelenlét.
- A szolgáltatás releváns a látogatók számára.
- Nincs hamis támogatási ígéret, garantált nyerés, megtévesztő sürgetés vagy jogosulatlan állami/hatósági látszat.
- Nincs tiltott, jogellenes, diszkriminatív vagy kifejezetten káros termék/szolgáltatás.
- A szponzor nem befolyásolhatja a támogatási rekordok forrásminőségét, jogosultsági státuszát vagy rangsorolását.
- Az ellenszolgáltatás, időtartam, díj, lemondás és számlázás írásban tisztázott.
- A hirdetés egyértelműen „Hirdetés” vagy „Szponzorált” címkét kap.

## Státuszok és átmenetek

- `researched`: csak belső kutatási jelölt.
- `outreach_approved`: a tulajdonos az adott megkeresést kifejezetten jóváhagyta.
- `contacted`: a jóváhagyott megkeresést ténylegesen elküldték.
- `negotiating`: dokumentált válasz és egyeztetés van.
- `approved_sponsor`: a partner és a megjelenés tartalma ellenőrzött, a feltételek írásban elfogadottak.
- `active`: a jóváhagyott hirdetés ténylegesen megjelent az egyeztetett időszakban.
- `completed`: a megjelenés lezárult.

A státusz nem léphet előre pusztán automatikus becslés alapján. A kutatási jelölt nem jelenhet meg partnerként.

## Pénzügyi kontroll

- A szerződéses díj nem bevétel, amíg ténylegesen be nem érkezik.
- A bevétel rögzítéséhez összeg, dátum és bizonylathivatkozás szükséges.
- A bruttó bevételt nem szabad automatikusan elkölthető pénznek tekinteni; adó, visszatérítés, szolgáltatói költség és tartalék levonása szükséges.
- Fizetős kampányt vagy eszközt a 0 Ft-os indulási szabály miatt nem indítunk.
- Banki vagy kártyaadatot a nyilvántartás nem tárolhat.

## Automatizálás határai

A rendszer később segíthet a nyilvános céges információk rendszerezésében, a minősítési ellenőrzőlista előkészítésében és a bevételi riportban. Nem küldhet megkeresést, nem fogadhat el ajánlatot, nem köthet szerződést, nem kapcsolhat be hirdetési kódot és nem költhet pénzt tulajdonosi jóváhagyás nélkül.
