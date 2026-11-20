# Global Support Radar – licencelési keretrendszer

**Verzió:** 1.0  
**Előkészítés dátuma:** 2026-11-20  
**Státusz:** belső előkészítő dokumentum; nem aláírt szerződés és nem jogi szakvélemény.

## 1. Cél és tulajdonosi modell

A projekt célja nem a teljes tulajdonjog eladása, hanem az eredeti, igazoltan licencelhető szoftverelemek nem kizárólagos licencelése. A jogszerű jogosult megtartja a szerzői jogokat, továbbfejlesztési lehetőséget és a további licencek kiadásának jogát.

**Alapelv:** egy vevő licencének megadása nem adhat neki kizárólagosságot, és nem ruházhatja át a teljes projekt tulajdonjogát.

A tulajdonosi szándékot a `docs/ownership-and-ip.md` rögzíti, de az önmagában nem bizonyítja a jogláncot. A licenc kiadása előtt minden közreműködői és eszköz-eredetet igazolni kell.

## 2. Licencelhető tárgy – csak ellenőrzés után

Lehetséges licenc tárgya:
- az eredeti, saját fejlesztésű alkalmazáskód és adatfeldolgozó/automatizáló szkriptek;
- a saját fejlesztésű felület, keresési logika és riport-előállítási megoldás;
- az eredeti dokumentáció és saját grafikai elemek, amennyiben eredetük igazolt;
- a projekt összeállításának és szerkezetének olyan részei, amelyekre a jogosultnak valóban van joga.

Nem része automatikusan a licencnek:
- kormányzati, EU-s, ENSZ-es vagy más harmadik féltől származó adat, rekord, szöveg, logó, név és adatbázis;
- külső API-k, szolgáltatások, csomagok, betűkészletek, ikonok és képek;
- a GitHub, tárhely, domain, piactér vagy más szolgáltató fiókja;
- felhasználói adat, ügyfélkör, bevétel, vállalkozás vagy jövőbeni eredmény;
- olyan fájl, amelynek jogi eredete vagy továbbengedélyezhetősége nincs igazolva.

A harmadik fél anyagai a saját licencük, adatbázis-joguk, forrásfeltételeik és szolgáltatási feltételeik szerint használhatók. A licencvevőnek szükség esetén saját hozzáférést és API-kulcsot kell szereznie.

## 3. Javasolt licencmodell

A piactérre szánt modell: **nem kizárólagos, világméretű, időben határozatlan felhasználási, módosítási és telepítési engedély**, kizárólag a piactér aktuális szerződéses feltételei és a vevő által megvásárolt licenc keretei között.

A Zero to Hundred jelenlegi standard feltételei alapján a vevő a forráskódot fizetés után megkapja, saját személyes vagy kereskedelmi célra használhatja, módosíthatja és telepítheti; a vevő nem értékesítheti tovább, nem listázhatja újra, nem adhat allicencet és nem terjesztheti tovább a szoftvert termékként. A jogosult megtartja a szerzői jogot, és más vevőknek is adhat licencet. A piactér feltételei változhatnak; közzététel előtt újra ellenőrizendők.

**Nem ígérünk** kizárólagosságot, tulajdonjog-átruházást, garantált bevételt, ügyfeleket, támogatási adatpontosságot vagy jövőbeni karbantartást.

## 4. Nyilvános GitHub-forrás – kritikus korlátozás

A repository jelenleg nyilvános. A nyilvános GitHub-tárhely felhasználói a kódot megtekinthetik és fork-olhatják a GitHub feltételei szerint. A saját jogi fenntartás nem vonja vissza a platform által biztosított hozzáférési lehetőségeket.

Ezért:
1. A nyilvános repository nem tekinthető titkos vagy csak fizetés után hozzáférhető forráscsomagnak.
2. A piactéri vevőnek átadott csomag értékét, teljességét és a nyilvános változattól való különbségét őszintén kell leírni.
3. Ne állítsuk, hogy a forráskód kizárólag a fizető vevő számára érhető el.
4. A repository-t nem szabad egyszerűen privátra állítani, amíg a jelenlegi GitHub Pages oldal erre támaszkodik. Előbb mentés, külön telepítési cél, staging és visszaállítási terv kell.
5. A licenc piactéri közzététele előtt vizsgáljuk meg, hogy a platform elfogadja-e a jelenleg nyilvános forráskódú projektet és az abból származó átadási csomagot.

## 5. Piactéri közzététel feltételei

Közzététel előtt mindegyik pontot teljesíteni kell:
- [ ] A jogosult személyazonosságát és jogláncát privát, aláírt dokumentum igazolja.
- [ ] Minden korábbi közreműködő hozzájárulása vagy jogátruházása ellenőrzött.
- [ ] A `THIRD_PARTY_NOTICES.md` minden csomagja és adatforrása áttekintett.
- [ ] A nem igazolt PNG/SVG ikonok cserélve vagy igazolva vannak.
- [ ] A licencbe kerülő fájlok listája és ellenőrzőösszege rögzített.
- [ ] Titkok, tokenek, személyes adatok, privát tesztadatok és belső jegyzetek nincsenek a csomagban.
- [ ] A build és a fő funkciók tiszta környezetben ellenőrizve vannak.
- [ ] Készült aktuális, valósághű képernyőfelvétel vagy működő bemutató.
- [ ] A korlátok, adatforrások és nem teljes funkcionalitások a hirdetésben szerepelnek.
- [ ] A piactér aktuális feltételei, díjai, KYC- és Stripe-követelményei ellenőrizve vannak.
- [ ] Az ár és a nettó bevétel számítása a tulajdonos által jóváhagyott.
- [ ] Magyar adózási és számlázási kötelezettségek tisztázva vannak könyvelővel.

## 6. Díjazás és pénzmozgás

A licencár még nincs jóváhagyva. A piactér díja a jelenlegi tájékoztatás szerint:
- saját, érvényes megosztási hivatkozással érkező közvetlen vásárlás: 8% + 0,50 USD;
- piactéri felfedezésből érkező vásárlás: 25%;
- a listázás ingyenes, havi díj nélkül.

A kifizetés Stripe Connecten keresztül történik; a piactér legalább 72 órás visszatartást alkalmazhat, és személyazonosság-ellenőrzést kérhet. A Stripe-fiók, azonosítás, bankszámla/payout-adatok és adózási adatok megadása kizárólag a tulajdonos saját felületén történhet. Jelszót, banki adatot vagy ellenőrző kódot senkinek ne küldjön el.

A platformdíjakon felül fizetési feldolgozási, devizaátváltási és adóterhek is felmerülhetnek. A piactér nem intézi automatikusan a tulajdonos összes magyar adó- és számlázási kötelezettségét.

## 7. Vevői átadási csomag

Minden tranzakcióhoz külön, verziózott csomag készüljön:
1. a licencbe bevont fájlok;
2. telepítési és futtatási útmutató;
3. függőségek és licenceik listája;
4. adatforrások és API-k korlátozásai;
5. ismert hibák és korlátok;
6. verzióazonosító és SHA-256 ellenőrzőösszeg;
7. a piactéri licenc feltételeinek hivatkozása.

A csomag nem tartalmazhat személyes titkot, fiókhozzáférést, API-kulcsot, GitHub-tokeneket, felhasználói adatot vagy más ügyfél bizalmas információját.

## 8. Felelősségi és működési határok

A jelenlegi projekt korai MVP/béta. Nem igazolt a bevétel, a felhasználószám, a rendelkezésre állás vagy a kereskedelmi eredmény. A támogatási rekordok egy része felfedezési jelölt vagy hivatalos forrásra mutató link, nem feltétlenül aktív pályázat. A jogosultsági és beadási feltételeket a vevőnek az eredeti hivatalos forrásban kell ellenőriznie.

Folyamatos frissítés, SLA, hibajavítás, ügyféltámogatás, egyedi fejlesztés és tárhely csak külön, írásos megállapodással vállalható.

## 9. Kötelező emberi jóváhagyási kapuk

A rendszer és az előkészítő dokumentumok nem adhatnak ki automatikusan licencet, nem publikálhatnak hirdetést, nem fogadhatnak el szerződést, nem módosíthatnak bankszámlát, és nem indíthatnak kifizetést. Minden ilyen lépéshez a tulajdonos külön jóváhagyása kell.

**Jogi figyelmeztetés:** ez működési és értékesítési előkészítő dokumentum. A tényleges licencszerződést magyar szerzői jogban és adózásban jártas ügyvéd/könyvelő ellenőrizze.
