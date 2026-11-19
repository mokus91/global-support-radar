# Global Support Radar – közös támogatási adatstandard

A különböző országok hivatalos adatforrásai eltérő mezőket és fogalmakat használnak. A rendszer megőrzi az eredeti mezőket, és ahol a jelentés egyértelmű, egységes mezőket tesz melléjük.

## Alapmezők

- `country_code`: ISO 3166-1 alpha-2 országkód.
- `id`: forráson belüli stabil rekordazonosító.
- `title_original`: eredeti nyelvű hivatalos cím.
- `source_language`: a rekord eredeti nyelve, ha ismert.
- `official_url`: az eredeti hivatalos felhívás vagy program oldala.
- `application_url`: közvetlen jelentkezési oldal, ha a forrás megadja.
- `deadline`: jelentkezési határidő ISO 8601 formátumban.
- `verification_status`: a forrásellenőrzés tényleges szintje.

## Pénzügyi mezők

- `amount_currency`: hárombetűs ISO 4217 pénznemkód (például EUR, JPY, CLP).
- `amount_maximum`: egy pályázó/projekt számára elérhető, forrás által közölt felső összeg – csak egyértelmű jelentés esetén.
- `total_call_budget`: a teljes felhívás keretösszege; soha nem jeleníthető meg egyéni támogatásként.
- `amount_type`: az összeg jelentése, például `maximum_co_funding_per_project` vagy `total_call_budget_not_individual_award`.
- `amount_status`: `published`, `not_published`, `not_published_or_zero_in_api` vagy `source_field_untyped`.

A régi mezők – például `amount_max`, `currency`, `budget` és `maximum_amount_jpy` – kompatibilitási okból megmaradhatnak. A kanonikus mezőket csak bizonyítható jelentés esetén töltjük ki. Nem váltunk át pénznemet becsült árfolyamon; az összegek mindig a forrás pénznemében jelennek meg.

## Jogosultság és nyitottság

A jogosulti kategória felsorolása nem bizonyítja az egyéni jogosultságot. Az `eligibility_verified` csak akkor lehet igaz, ha a részletes hivatalos feltételek alapján tényleges ellenőrzés történt. A portál API-szűrője önmagában nem bizonyítja, hogy a felhívás még nyitott. A bizonytalan vagy hiányzó mezőket nem találgatjuk.

## Adatminőség

A `scripts/validate_project.py` ellenőrzi a kanonikus pénzügyi mezők pénznemkódját, engedélyezett státuszait és a számszerű összegek érvényességét. Az automatikus validálás nem helyettesíti a kiírás emberi ellenőrzését.
