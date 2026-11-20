# Szervezeti pilot – végrehajtási és minőségellenőrzési munkalap

**Verzió:** 1.0  
**Dátum:** 2026-11-20  
**Státusz:** belső munkalap; pilot még nem indult.

## 1. A pilot célja

Egyetlen, jól körülhatárolt szervezeti igényen ellenőrizni, hogy a Global Support Radar riportja valóban releváns, pontos, visszakövethető és időtakarékos-e. A pilot nem értékesítési ígéret, és nem bizonyítja a teljes ország- vagy programlefedettséget.

## 2. Pilot hatóköre

Az első próba szűk legyen:
- **ország:** a tesztelő által kiválasztott 1 ország;
- **témakör:** 1 kategória;
- **szervezettípus:** 1 pontosan megadott típus;
- **időablak:** a kézi ellenőrzés napja és az eredeti kiírás aktuális beadási időszaka;
- **kimenet:** egy dátumozott, forráslinkekkel ellátott riport.

Ne vállaljunk előre olyan országot vagy kategóriát, amelyhez nincs ellenőrizhető, naprakész hivatalos adatforrás.

## 3. Kötelező ellenőrzési kapu minden rekordhoz

Minden riportba kerülő rekordnál töltsük ki:

| Ellenőrzési pont | Eredmény |
|---|---|
| Az eredeti kiíró/hatóság azonosítható | Igen / Nem |
| Az eredeti hivatalos oldal HTTPS | Igen / Nem |
| Az eredeti felhívás közvetlenül megnyitható | Igen / Nem |
| Jelentkezési státusz az eredeti oldalon ellenőrizve | Nyitott / Lezárt / Nem egyértelmű |
| Határidő és időzóna rögzítve | Igen / Nem / Nincs megadva |
| Jogosultak köre az eredeti szabályzatban megtalálható | Igen / Nem |
| Támogatási összeg és pénznem jelentése tisztázott | Igen / Nem / Nincs megadva |
| Utolsó ellenőrzés időpontja rögzítve | Igen / Nem |
| Fordítás/összefoglalás visszaellenőrizve | Igen / Nem / Nem releváns |

**Közzétételi szabály:** ha az eredeti forrás nem támasztja alá a nyitott státuszt, a rekord nem jelenhet meg nyitottként. Ha a kiírás nem elérhető, vagy a határidő ellentmondásos, a rekordot ki kell hagyni vagy egyértelműen „ellenőrizendő” jelöltként kell jelölni. A nyilvántartási API időablaka önmagában nem bizonyítja a nyitott jelentkezést.

## 4. Riport előállításának sorrendje

1. Rögzítsük a szervezeti igényt ország, témakör és szervezettípus szerint.
2. Csak a meglévő hivatalos adatfolyamokban és hivatalos forrásregiszterben keressünk.
3. Nyissuk meg az eredeti forrást minden lehetséges találatnál.
4. Töltsük ki a 3. szakasz ellenőrzési táblázatát.
5. Távolítsuk el a duplikátumokat, lezárt és lejárt rekordokat.
6. Különítsük el a hivatalosan nyitottként ellenőrzött rekordokat az ellenőrizendő jelöltektől.
7. Generáljuk a riportot, majd emberi ellenőrzéssel olvassuk át.
8. Rögzítsük a tényleges munkaidőt, a hibákat és a hiányzó adatokat.
9. A riportot csak a tulajdonos által jóváhagyott tesztelővel osszuk meg, a szükséges adatvédelmi tájékoztatás mellett.

## 5. Pilot utáni mérőlap

| Mutató | Mérés |
|---|---|
| Átvizsgált nyers rekordok | |
| Eredeti forrásoldalon ellenőrzött rekordok | |
| Nyitottként igazolt rekordok | |
| Csak jelöltként megmaradt rekordok | |
| Kizárt lejárt/lezárt rekordok | |
| Duplikátumok | |
| Hibás vagy elérhetetlen források | |
| Riport elkészítésére fordított idő (perc) | |
| Tesztelő által becsült jelenlegi kézi munka (perc) | |
| Tesztelő által jelzett tényleges hasznosság | |
| Ismételt használati szándék | Igen / Nem / Nem tudja |
| Fizetési hajlandóság | Csak külön, egyértelmű árteszt esetén |

A kézi munka becsült csökkenését nem szabad tényként vagy garantált időmegtakarításként kommunikálni. A pilot során mért értékeket dátummal és módszerrel együtt rögzítsük.

## 6. Döntési kapu

**Folytatásra alkalmas**, ha:
- az eredeti források visszakövethetők;
- nincs félrevezető nyitott státusz;
- a tesztelő legalább egy konkrét, releváns felhasználási esetet azonosít;
- a riport formátuma érthető;
- a teljesítés kézi munkával megismételhető.

**Javítás szükséges**, ha:
- túl sok a nem ellenőrzött jelölt;
- a forráslinkek vagy határidők hiányosak;
- a tesztelő nem tudja felhasználni az eredményt;
- a riport elkészítése aránytalanul sok kézi munkát igényel.

**Leállítás vagy újratervezés szükséges**, ha:
- nincs releváns találat a kiválasztott szegmensben;
- az adatok nem ellenőrizhetők megbízhatóan;
- a tesztelői probléma nem valós vagy nem ismétlődő.

Egy pozitív visszajelzés önmagában nem jelent szerződést vagy fizetési hajlandóságot.

## 7. Pénzügyi és jogi korlátok

- Jelenlegi induló saját tőke: 0 Ft.
- A belső pilot előkészítése nem járhat fizetős szolgáltatás, API, hirdetés vagy előfizetés aktiválásával.
- Külső megkeresés és riportküldés csak külön tulajdonosi jóváhagyással történhet.
- Fizetős pilot előtt rendezni kell a kereskedelmi tárhelyet, a szerződési feltételeket, az adatvédelmi tájékoztatást, a számlázást és az adózást.
- A GitHub Pages nem megfelelő ingyenes kereskedelmi SaaS- vagy tranzakciós tárhely; kereskedelmi indulás előtt megfelelő platformra kell költözni.
- Nincs fizetési szolgáltató, banki hozzáférés vagy automatikus átutalás beállítva.
- Minden költség és szerződés előzetes tulajdonosi jóváhagyást igényel.

## 8. Jelenlegi állapot

| Esemény | Státusz |
|---|---:|
| Pilot specifikáció | Elkészült |
| Bemutatóanyag | Elkészült |
| Minőségellenőrzési munkalap | Elkészült |
| Külső megkeresés | 0 |
| Pilot | 0 |
| Fizető ügyfél | 0 |
| Bevétel | 0 Ft |

Ez a munkalap előkészítés, nem végrehajtott pilot.
