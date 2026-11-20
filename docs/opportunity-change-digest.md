# Változásfigyelő digest

A scripts/track_opportunity_changes.py a korábbi és az új hivatalos adatforrás-pillanatképek közötti eltéréseket rögzíti a data/opportunity-changes.json fájlban. A scripts/build_opportunity_change_digest.py ebből ember által gyorsan áttekinthető Markdown-összefoglalót készít.

## Megjelenített változások
- Új rekord az adatforrásban.
- Figyelt mezők változása: státusz, beadási határidő, támogatási összeg/keret és jogosultsági státusz.
- Adatforrásból eltűnt rekord, kifejezett figyelmeztetéssel: az eltűnés nem bizonyít lezárást.
- Az EU Funding & Tenders Portal ismert státuszkódjai olvasható címkét kapnak: 31094501 = Forthcoming, 31094502 = Open, 31094503 = Closed. Ismeretlen kódot nem fordítunk le találgatással.

## Korlátok
A változásnapló nem ellenőrzi önmagában a kiírói oldalt és nem állapít meg jogosultságot. A digest belső ellenőrzési anyag, nem publikált értesítés és nem ügyfélkommunikáció. Az EU státuszkódok feloldása az Európai Bizottság hivatalos API-leírásán alapul: https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/support/apis
