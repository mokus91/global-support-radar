# 0 Ft-os nyilvános indulás – ellenőrzőlista

## Cél

A Global Support Radar jelenlegi, információs MVP-jének nyilvános bétaindítása úgy, hogy a tulajdonosnak ne kelljen saját pénzt befizetnie. A rendszer nem ígér teljes ország-lefedettséget, támogatási jogosultságot vagy garantált bevételt.

## Költségvédelmi szabályok

- Tervezett induló készpénzkiadás: **0 Ft**.
- Nincs fizetős domain, tárhely, API, hirdetés, e-mailküldő vagy prémium bővítmény.
- Nincs automatikus fizetős csomagra váltás, próbaidőszakból fizetős előfizetés vagy használatalapú szolgáltatás engedélyezése.
- Nincs bankkártyaadat-, bankszámla-, jelszó- vagy fizetési adatgyűjtés a weboldalon.
- Nincs fizetési űrlap, checkout, fizetős regisztráció vagy automatikus pénzmozgás.
- Minden olyan szolgáltatást, amely díjat, hitelkártya-terhelést, fizetős kvótát vagy domainvásárlást eredményezhet, a tulajdonos előzetes jóváhagyása nélkül tilos bekapcsolni.
- A GitHub Actions ingyenes kvótája és a külső hivatalos adatforrások elérhetősége korlátozott lehet; az ingyenesség nem jelent korlátlan, garantált rendelkezésre állást.

## Közzétételi platform

A GitHub Pages jelenleg működő fejlesztési/nyilvános bemutatóhely, de a GitHub hivatalos szabályzata szerint nem használható ingyenes tárhelyként online üzlet, e-kereskedelmi oldal vagy kereskedelmi SaaS működtetésére. Emiatt a kereskedelmi szolgáltatás elindítása előtt külön tárhely-ellenőrzés és migráció szükséges.

Első vizsgálandó, díjmentes statikus tárhely a Cloudflare Pages. A hivatalos dokumentáció a Free kerethez 500 buildet/hó, egyidejűleg 1 buildet, legfeljebb 20 000 fájlt projektenként és 25 MiB maximális fájlméretet sorol fel. A statikus oldal kiszolgálására használjuk; dinamikus funkciókat és fizetős kvótát nem kapcsolunk be.

**Fontos korlát:** a Cloudflare Free csomag bemutatása személyes/hobbi, nem üzletkritikus projektekre szól. A Developer Platform feltételei lehetővé teszik a tartalom hosztolását, de a Free csomag kereskedelmi használhatóságát nem tekintjük automatikusan, minden üzleti modellre garantáltnak. Üzleti/pénzforgalmi funkció élesítése előtt a mindenkori szerződési feltételeket külön ellenőrizni kell. A Free csomag nem üzletkritikus, SLA-val garantált infrastruktúra.

## Migrációs lépések – tulajdonosi fiók szükséges

1. A tulajdonos saját maga megnyitja a Cloudflare hivatalos regisztrációs oldalát, és ellenőrzi, hogy a kiválasztott Free szolgáltatás valóban 0 Ft-os, nem kér fizetési módot és nem indít automatikus fizetős szolgáltatást.
2. A tulajdonos engedélyezi a GitHub-repository olvasását a Cloudflare Git-integráció számára. Csak a szükséges jogosultságokat adja meg.
3. Pages projekt létrehozása a `mokus91/global-support-radar` repóból, `main` ágról.
4. Statikus oldal beállítása: framework preset = None; build command = üres; output directory = repository root ( `.` ).
5. A rendszer által kiosztott `pages.dev` címen ellenőrizni kell a főoldalt, keresőt, partneroldalakat, adatfrissítési állapotot, változásnaplót, PWA-t, sitemapet és a mobilos megjelenést.
6. A nyilvános Cloudflare URL csak akkor válik elsődleges címmé, ha minden ellenőrzés sikeres. Egyéni domain vásárlása nem része a 0 Ft-os indulásnak.
7. A GitHub Pages beállítását addig nem kapcsoljuk ki, amíg az új oldal teljesen nem ellenőrzött és a tulajdonos nem hagyta jóvá az átállást.

A fiók létrehozását, OAuth-jóváhagyást, hozzáférési engedélyt és végső élesítést a tulajdonosnak kell elvégeznie. Jelszót, API-tokent, recovery kódot vagy banki adatot nem szabad chatben megadni.

## Bétaindítási minőségi kapuk

- [ ] Staging validáció sikeres.
- [ ] Minden Python regressziós teszt sikeres.
- [ ] Frontend JavaScript szintaktikai ellenőrzése sikeres.
- [ ] Főoldal és összes belső navigáció működik.
- [ ] A változásnapló üres adatállapotban és hibás adatforrásnál is érthető.
- [ ] A források státusza, ellenőrzési dátuma és korlátai láthatók.
- [ ] Mobilnézet ellenőrizve.
- [ ] Adatvédelmi és kapcsolatfelvételi felületek áttekintve.
- [ ] Nincs fizetési adatgyűjtés, fizetős szolgáltatás vagy automatikus költség.
- [ ] Tulajdonosi jóváhagyás a végleges nyilvános címre.

## Bevételi funkciók – külön, későbbi szakasz

Az első bétaindítás ingyenes tájékoztató termék. Fizetős szervezeti riport, előfizetés, partnerjutalék, szponzorált megjelenés vagy fizetési szolgáltató csak külön jogi/adózási ellenőrzés, megfelelő kereskedelmi tárhely, szolgáltatói feltételek és tulajdonosi jóváhagyás után indulhat. Az első tényleges bevétel előtt a rendszer nem állíthatja, hogy önfenntartó vagy nyereséges.

## Hivatalos hivatkozások

- GitHub Pages korlátozások: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- Cloudflare Pages limitek: https://developers.cloudflare.com/pages/platform/limits/
- Cloudflare Developer Platform feltételek: https://www.cloudflare.com/service-specific-terms-developer-platform/
- Cloudflare Pages indítás: https://pages.cloudflare.com/

## Jelenlegi állapot

**Ellenőrzési frissítés: 2026-11-20**

- A GitHub Pages bemutatóoldal a jelenlegi nyilvános változat; a Cloudflare-migráció nincs elvégezve.
- A GitHub-repository és a meglévő staging-validációs workflow rendelkezésre áll.
- A bétaindítás nem tekinthető lezártnak, amíg a tulajdonos nem kapcsolja össze a saját Cloudflare-fiókját, és a `pages.dev` címen a teljes ellenőrzőlista nem teljesül.
- A felhasználó jelenlegi döntése: minden induló szolgáltatás és fejlesztési lépés maradjon 0 Ft-os; fizetési módot vagy fizetős csomagot nem adunk meg.


- A weboldal jelenleg GitHub Pages címen érhető el.
- Cloudflare-fiók nincs összekötve, Pages-projekt nincs létrehozva, migráció nem történt.
- A dokumentum előkészíti a díjmentes bétaindítást, de nem állítja, hogy a Cloudflare-telepítés már megtörtént.
- Jelenlegi igazolt bevétel: 0 Ft.
