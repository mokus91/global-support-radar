# Global Support Radar

**Élő szolgáltatás:** https://mokus91.github.io/global-support-radar/  
**Rendeltetés:** nemzetközi, többnyelvű hivatalos támogatási és pályázati forráskereső  
**Üzemeltetés:** GitHub Pages és automatizált GitHub Actions munkafolyamatok  
**Költségkeret:** 0 Ft; fizetős szolgáltatás vagy költés nincs engedélyezve.

## A rendszer célja

A Global Support Radar állami támogatásokhoz, pályázatokhoz, juttatásokhoz és közszolgáltatásokhoz kapcsolódó hivatalos információforrásokat gyűjt és tesz kereshetővé ország és témakör szerint. Nem hatóság és nem pályázatkezelő: tájékoztató és forrásnavigációs szolgáltatás.

A támogatáskeresés és az alapvető tájékoztatás ingyenes marad; nincs kötelező regisztráció vagy fizetős hozzáférési fal. A bevételszerzés előkészítése folyamatban van: az AdSense-kód a főoldalba be van illesztve, a webhely Google-felülvizsgálata folyamatban van, ezért tényleges hirdetésmegjelenítés vagy bevétel még nem tekinthető igazoltnak. A szponzorált megjelenések, partnerjutalékok és prémium kiegészítő szolgáltatások csak külön fejlesztés, egyértelmű jelölés és tulajdonosi jóváhagyás után indulhatnak el. A projekt később külön tulajdonosi döntéssel licencelhető vagy értékesíthető; a külső adatforrások és licencek jogai ettől nem szállnak át automatikusan.

## Nyilvánosan elérhető funkciók

- **Országkereső:** 194 országot tartalmazó országjegyzék.
- **Témakörök:** család, lakhatás, energia, mezőgazdaság, vállalkozás, oktatás, foglalkoztatás, egészségügy, szociális ellátások, közlekedés és egyéb támogatások.
- **Többnyelvű felület:** magyar, angol, spanyol, francia, német, olasz, portugál, arab, hindi, orosz és egyszerűsített kínai.
- **Országoldalak:** hivatalos forrásgyűjtemények és közvetlen hivatkozások.
- **Keresés és szűrés:** a rendelkezésre álló rekordok ország, kategória és keresőkifejezés szerint szűrhetők.
- **Mentés:** könyvjelzők helyi böngészőtárolóban.
- **Export és megosztás:** CSV-export és megosztható keresési hivatkozások.
- **Határidőnaptár:** a mentett határidők naptárba exportálhatók, ha a rekord dátumot tartalmaz.
- **Telepíthető webalkalmazás:** PWA-támogatás és korlátozott offline felület.
- **Automatizált adatfeldolgozás:** ütemezett munkafolyamatok vizsgálják és dolgozzák fel a csatlakoztatott forrásokat.

## Adatminőség és megbízhatóság

A rendszer megkülönbözteti a konkrét támogatási programot, pályázati felhívást, ellátást, hivatalos portált, hírt, adatbázis-találatot és történeti címtárbejegyzést. Egy hivatalos portálra mutató link önmagában nem bizonyítja, hogy ott jelenleg nyitott pályázat érhető el.

A rekordok állapota és ellenőrzöttsége forrásonként eltér. Ahol az aktuális beadási időszak, jogosultság, összeg vagy határidő nincs ellenőrizve, a rendszer nem tekintheti automatikusan nyitott támogatásnak. A történeti nemzetközi portáljegyzékek kiindulópontként, nem aktuális támogatási katalógusként vannak megjelölve.

A Global Support Radar nem hoz jogosultsági döntést, nem garantál támogatást, és nem nyújt be kérelmet a látogató helyett. A feltételeket és határidőket mindig az eredeti hivatalos kiírásban kell ellenőrizni.

## Automatizált működés

A nyilvános tárhely GitHub Pages. A GitHub Actions ellenőrzéseket, adatforrás-feldolgozást, országoldal-építést és telepítést végez. Az automatizmusok csak a beállított forrásokból és a rendelkezésre álló hozzáférésekkel tudnak dolgozni. Külső API-hiba, hozzáférés-változás vagy forrásoldali módosítás esetén emberi felülvizsgálat válhat szükségessé.

Az automatizált ellenőrzés nem azonos az összes ország és minden támogatási program folyamatos, teljes körű ellenőrzésével. A frissesség és a részletesség országonként, forrásonként változik.

## Minőségbiztosítás

- JSON-adatok, forrásazonosítók, országkódok és HTTPS-hivatkozások automatikus ellenőrzése.
- A történeti, nem ellenőrzött portálhivatkozások elkülönítése az aktuális hivatalos forrásoktól.
- Bizonytalan rekord nem jelenhet meg ellenőrzötten nyitottként.
- A frissítési és telepítési munkafolyamatok eredményének ellenőrzése.
- Új külső szolgáltatás, adatlicenc, fizetési rendszer vagy költség csak külön tulajdonosi jóváhagyással kapcsolható be.
- A hirdetések és partneri tartalmak jól láthatóan szponzoráltként jelölendők; nem befolyásolhatják a támogatások szakmai sorrendjét.
- A látogatók személyes vagy pályázati adatait nem értékesítjük, és nem kérünk be hivatalos belépési adatokat.

## Tulajdonosi, jogi és biztonsági dokumentáció

- [Ingyenes használat és átláthatósági alapelvek](https://mokus91.github.io/global-support-radar/free-policy.html)
- [Adatminőségi módszertan](https://mokus91.github.io/global-support-radar/methodology.html)
- [Minőség és ellenőrzési állapot](https://mokus91.github.io/global-support-radar/quality.html)
- [Frissítések és változásnapló](https://mokus91.github.io/global-support-radar/updates.html)
- [Tulajdonosi és szellemi tulajdon nyilvántartása](docs/ownership-and-ip.md)
- [AI-közreműködéssel készült fejlesztés átláthatósága](docs/ai-assisted-development-disclosure.md)
- [Előzetes jogi és licencelési audit](docs/preliminary-rights-and-licensing-audit-2026-11-20.md)
- [Adatforrások kereskedelmi újrafelhasználási előauditja](docs/source-data-commercial-reuse-audit-2026-11-20.md)
- [Jogosultsági bizonyítékok naplója](docs/rights-evidence-log.md)
- [Külső anyagok és licencek](THIRD_PARTY_NOTICES.md)
- [Üzemeltetési biztonsági ellenőrzőlista](docs/production-security-checklist.md)
- [Adatbesorolási és ellenőrzési szabvány](docs/data-classification-standard.md)

## Licencelhetőség

A szoftver licencelési és átadási dokumentációja előkészítés alatt áll. Ez nem jelenti azt, hogy minden beépített adat, külső szolgáltatás, grafikai elem vagy harmadik féltől származó tartalom szabadon továbbértékesíthető. Minden ilyen elemre külön jog- és licencellenőrzés szükséges.

- [Licencelési tájékoztató](https://mokus91.github.io/global-support-radar/licensing.html)
- [Licencelési keretrendszer](docs/licensing-framework-hu.md)
- [Licencelt csomag átadási ellenőrzőlista](docs/licensing-delivery-checklist.md)

## Bevételszerzés – jelenlegi állapot

A bevételszerzés fokozatosan, az ingyenes alapfunkciók megőrzésével készül. Az AdSense webhely-ellenőrzése még folyamatban van. Partnerprogram, fizetős kiemelés, előfizetés és online fizetés jelenleg nem tekinthető éles, működő szolgáltatásnak. Ezeket csak megfelelő szerződési, adatvédelmi, fogyasztóvédelmi és technikai feltételek mellett szabad elindítani.

## Következő szakmai fejlesztési szakasz

1. Az országoldalak hivatalos forrásainak egyenkénti ellenőrzése és bővítése.
2. Egységes forrásdátum, ellenőrzési státusz, jogosultsági feltétel és beadási időszak rögzítése.
3. Hibás vagy elérhetetlen adatforrások jelzése és javítási folyamata.
4. Automatizált tesztek bővítése a keresésre, szűrésre, exportokra és adatfrissítésre.
5. Üzemeltetési mentés, visszaállítás és biztonsági felülvizsgálat dokumentált ellenőrzése.

A cél egy megbízható, hosszú távon fenntartható nemzetközi információs szolgáltatás. A rendszer nem állít teljes körű ország- vagy programlefedettséget; a nyilvános funkciók és az ellenőrzött adatlefedettség fokozatosan bővül.

## Napi forrásfigyelés és új minőségellenőrzések (2026-11-22)

A napi GitHub Actions munkafolyamat a beállított katalógusrekordok hivatalos URL-jeit ellenőrzi, összehasonlít egy legfeljebb 64 KB-os oldalmintát az előző futással, és a megváltozott mintákat külön emberi felülvizsgálati sorba teszi. A beállított RSS/Atom hírcsatornákból lehetséges támogatási híreket is gyűjt, de ezek nem kerülnek automatikusan igazolt támogatásként a katalógusba.

- [Napi forrásállapot](https://mokus91.github.io/global-support-radar/source-status.html)
- [Megváltozott hivatalos oldalak – felülvizsgálati lista](https://mokus91.github.io/global-support-radar/content-review.html)
- [Új hivatalos közlemények – felülvizsgálati lista](https://mokus91.github.io/global-support-radar/announcements.html)

A napi munkafolyamat új katalógus-integritási ellenőrzést is futtat (scripts/validate_catalogue.py): vizsgálja a kötelező mezőket, az egyedi azonosítókat, az országkódok formátumát és a HTTPS-forráscímeket. A hibás katalógus megállítja az ellenőrzési folyamatot.

**Korlát:** a napi URL- és oldalminta-ellenőrzés nem olvassa ki megbízhatóan a támogatások aktuális összegét, jogosultságát, határidejét vagy nyitottságát. A változásjelzés nem automatikus tényfrissítés; a támogatási adatokat hivatalos közleményből embernek kell ellenőriznie. A hírcsatornák jelenlegi lefedettsége csak a konfigurációban felsorolt országokra terjed ki, nem a világ összes országára.
