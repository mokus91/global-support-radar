# Automatikus szervezeti riportgyártás

A `.github/workflows/organization-report-production.yml` workflow napi ütemezéssel, kézi indítással, illetve sikeres hivatalos adatforrás-frissítés után készít szervezeti támogatásfigyelő riportot.

## Folyamat

1. A workflow az aktuális alapértelmezett ágat tölti le.
2. Lefuttatja a projektadatok és a frontend validációját.
3. Lefuttatja a riportgenerátor regressziós tesztjeit.
4. Elkészíti a `reports/organization-report-latest.md` fájlt.
5. A riportot 14 napig elérhető GitHub Actions artifactként őrzi meg.

## Fontos korlátok

- A riport a repositoryban található adatpillanatképből készül; nem garantál teljes ország- vagy témakörlefedettséget.
- A riport nem jogosultsági döntés és nem pályázati tanácsadás.
- A workflow nem küld riportot ügyfélnek, nem tesz közzé személyes adatot, és nem vállal költséget.
- A külső ügyfélnek történő átadás, ajánlat és számlázás tulajdonosi jóváhagyást igényel.
- A GitHub Actions artifact belső ellenőrzési kimenet, nem fizetős ügyfélportál.

## Ellenőrzés

A futások a GitHub repository Actions lapján követhetők. A GitHub ütemezett workflow-jai nagy terhelés esetén késhetnek; ezért a tényleges futási naplót kell ellenőrizni.

## Többprofilos riportcsomag

A `config/report-profiles.json` négy mintaprofilt tartalmaz: magyar általános, magyar vállalkozásfejlesztési, magyar mezőgazdasági és globális összesített nézetet. A `scripts/build_report_portfolio.py` minden profilhoz külön Markdown-riportot készít, ugyanazzal a szigorú státusz- és adatminőségi szűréssel. A szűrők pontos egyezést használnak; ha egy profilhoz nincs megfelelő rekord, a riport ezt jelzi, nem talál ki lehetőséget. A profilok szerkeszthetők, új ország/témakör csak akkor adható hozzá, ha az adatállomány ténylegesen tartalmaz ilyen címkéket.

A CI külön regressziós tesztet futtat a profilgenerátorra. Az alapriport és a profilriportok egyaránt belső, 14 napos Actions artifactként kerülnek megőrzésre; nem publikáljuk és nem küldjük ki ügyfeleknek.
