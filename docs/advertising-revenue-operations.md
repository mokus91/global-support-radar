# Hirdetési bevételi működés – biztonságos előkészítés

**Állapot: előkészítés, nincs aktív hirdetés vagy bevétel.** A nyilvántartás és a jelentés nem jelent ügyfélszerzést, külső kapcsolatfelvételt vagy automatikus monetizációt.

## Mi készült el?

- `data/advertising-inventory.json`: a hirdetési helyek, hirdetők és bevételi események géppel olvasható nyilvántartása.
- `scripts/build_advertising_readiness_report.py`: csak olvasási ellenőrzés és Markdown-jelentés.
- `scripts/test_build_advertising_readiness_report.py`: szabályellenőrző tesztek.

## Kötelező indulási kapuk

1. A kereskedelmi célú tárhely és a szolgáltatói feltételek ellenőrzése.
2. Hirdető vagy partner tényleges jóváhagyása, írásos feltételekkel.
3. Adatvédelmi, sütikezelési és hozzájárulási felülvizsgálat, ha külső hirdetési technológia adatot kezel.
4. Minden fizetett megjelenés jól látható jelölése.
5. Tulajdonosi jóváhagyás a hirdetési hely bekapcsolása, külső kód vagy bármilyen költség előtt.
6. A bevétel csak tényleges beérkezés és bizonylathivatkozás esetén kerülhet a pénzügyi jelentésbe.

## Tiltások

- Nem történik automatikus partnermegkeresés vagy e-mail-küldés.
- Nem kerül be külső reklámkód vagy követőscript.
- Nincs automatikus előfizetés, banki hozzáférés, utalás vagy költés.
- A hirdető nem befolyásolhatja a támogatási rekordok jogosultsági, hitelességi vagy rangsorolási státuszát.
- A jelentés nem kapcsolja le a tájékoztató oldalt; csak a hirdetési lehetőségek indulását blokkolja.

## Jelentés futtatása

A repository gyökeréből:

```bash
python scripts/build_advertising_readiness_report.py
python -m unittest scripts.test_build_advertising_readiness_report -v
```

A jelentés helyben az `advertising-readiness-report.md` fájlba készül. A generátor nem küld adatot sehova.
