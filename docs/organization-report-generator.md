# Szervezeti riportgenerátor

A `scripts/generate_organization_report.py` a repository helyi `data/*-discovery.json` állományaiból készít dátumozott Markdown riportot.

## Futtatás

A repository gyökérkönyvtárából, Python 3-mal:

```bash
python scripts/generate_organization_report.py --self-test
python scripts/generate_organization_report.py
```

Alapértelmezett kimenet: `reports/organization-report-latest.md`.

Egyedi útvonalak:

```bash
python scripts/generate_organization_report.py --data-dir data --output reports/pilot-report.md
```

## Biztonságos státuszkezelés

- Csak az explicit `open-and-current` / támogatott nyitott státusz kerül a „kifejezetten nyitott” részbe.
- A hivatalos nyilvántartás aktuális időablakát jelző rekord külön, ellenőrzendő jelöltként jelenik meg.
- A discovery-only, ismeretlen, nem ellenőrzött, lejárt, lezárt és visszavont rekord nem jelenik meg lehetőségként.
- A határidő lejárta esetén a rekord kimarad akkor is, ha a státuszmező még nyitottnak látszik.
- A riport nem igazol jogosultságot, nem helyettesíti az eredeti kiírást, és nem ígér támogatást.

## Fontos működési korlátok

Ez jelenleg kézzel futtatható riportgenerátor. Nem tölt le új adatot, nem küld e-mailt, nem fogad megrendelést és nem kezel fizetést. Automatikus ütemezést vagy kereskedelmi szolgáltatást csak külön adatminőségi, tárhely-, jogi és tulajdonosi jóváhagyás után szabad bekapcsolni. A projekt 0 Ft indulási elve változatlan.
