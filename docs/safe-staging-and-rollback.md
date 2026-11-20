# Biztonságos fejlesztési tesztkörnyezet

A Global Support Radar fejlesztési folyamata három elkülönített szakaszt használ:

1. **Ellenőrzés:** a GitHub Actions ideiglenes futtatókörnyezetében lefut a Python-szintaxisellenőrzés, a projektvalidátor és az összes regressziós teszt.
2. **Bizonyíték:** a futás összefoglalója letölthető CI-artifactként megőrződik. A tesztkörnyezet nem kap írási jogosultságot a repóhoz.
3. **Kiadás:** csak a sikeres ellenőrzés után, külön felülvizsgálattal kerülhet módosítás az éles `main` ágra.

## Visszaállítás

- Minden kiadás egyedi Git commit azonosítóval rendelkezik.
- Hiba esetén a korábbi stabil commitra lehet visszaállni GitHubon.
- Az adatgyűjtési futás hibája nem jogosítja fel a rendszert arra, hogy a pályázatokat automatikusan lezártnak vagy nem létezőnek jelölje.
- A tesztfolyamat nem módosíthat titkokat, jogosultságokat, DNS-t, tárhelybeállításokat vagy éles adatokat.

## Fontos korlát

A GitHub Actions futtatókörnyezete ideiglenes CI-tesztkörnyezet, nem teljes értékű külön staging weboldal. A jelenlegi statikus GitHub Pages oldal változatlanul az éles bemutatófelület. Külön előnézeti tárhely és szerveroldali szolgáltatás későbbi infrastruktúra-fejlesztést igényel.
