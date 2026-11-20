# Bevételi pipeline – működési szabályok

Frissítve: 2026-11-20

A `data/revenue-pipeline.json` belső, konzervatív állapotnyilvántartás. A kutatott célpont nem érdeklődő, partner vagy ügyfél; a státusz előrelépése csak tényleges, ellenőrizhető esemény alapján történhet.

## Státuszok
- `researched`: nyilvános információ alapján kutatott célpont.
- `outreach_approved`: a tulajdonos az adott megkeresést kifejezetten jóváhagyta.
- `contacted`: a jóváhagyott megkeresés ténylegesen elküldésre került.
- `replied`: tényleges válasz érkezett.
- `pilot`: dokumentált pilot indult.
- `paid_customer`: ténylegesen fizető ügyfél, igazolt beérkezett összeggel.

## Kötelező korlátok
1. Megkeresés csak tulajdonosi jóváhagyás után küldhető.
2. Kutatott célpontot nem szabad érdeklődőként vagy partnerként feltüntetni.
3. Válasz csak tényleges kapcsolatfelvétel után rögzíthető.
4. Fizető ügyfél státuszhoz pilot és ténylegesen beérkezett fizetés szükséges.
5. Bevétel csak fizető ügyfélhez rendelhető; becsült vagy várható összeg nem bevétel.
6. A pipeline nem tárolhat banki, kártya- vagy belépési adatokat.
7. A napi bevételi készenléti workflow ellenőrzi az ellentmondásokat.

## Induló állapot
7 kutatott szervezeti célpont, 0 jóváhagyott megkeresés, 0 elküldött megkeresés, 0 válasz, 0 pilot, 0 fizető ügyfél, 0 Ft igazolt bevétel.

A pipeline nem indít külső kapcsolatfelvételt.


## Automatikus tulajdonosi teendősor

A `scripts/build_revenue_readiness_report.py` a pipeline státuszaiból legfeljebb tíz következő lépést állít elő. A sorrend a tényleges előrehaladást követi: válasz érkezett, kapcsolatfelvétel megtörtént, jóváhagyott megkeresés, kutatott célpont, pilot, fizető ügyfél. A sor minden rekordnál feltünteti a következő kézi feladatot és a szükséges jóváhagyási kaput.

A teendősor kizárólag belső döntéstámogató kimenet. Nem küld üzenetet, nem módosítja a CRM-státuszt, nem indít hirdetést, nem foglal időpontot és nem vállal költséget. A kutatott célpontnál a kapcsolatfelvétel továbbra is tiltott tulajdonosi jóváhagyás nélkül.
