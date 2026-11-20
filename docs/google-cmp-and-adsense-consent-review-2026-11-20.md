# Google AdSense és EGT hozzájáruláskezelés – ellenőrzés

Dátum: 2026-11-20  
Projekt: Global Support Radar  
Státusz: belső megfelelőségi munkadokumentum; nem jogi tanács és nem publikálható adatvédelmi tájékoztató.

## 1. Google követelmény

A Google AdSense hivatalos tájékoztatója szerint az EGT-ben, az Egyesült Királyságban és Svájcban személyre szabott hirdetéseket kiszolgáló AdSense-partnereknek Google által tanúsított, az IAB Europe Transparency and Consent Framework (TCF) keretrendszerébe integrált CMP-t kell használniuk. Az EGT és az Egyesült Királyság esetében ez 2024. január 16. óta, Svájc esetében 2024. július 31. óta követelmény.

A Google által biztosított Privacy & Messaging európai szabályozási üzenete tanúsított megoldásként szerepel a Google tájékoztatójában. Alternatívaként más, az aktuális Google-listán szereplő tanúsított CMP is választható.

A Google szerint a nem tanúsított CMP-vel érkező forgalom bizonyos esetekben jogosult lehet nem személyre szabott vagy korlátozott hirdetésekre, de ez nem jelenti azt, hogy a webhely automatikusan megfelel az adatvédelmi és ePrivacy jogszabályoknak.

## 2. Projektállapot

- Az AdSense betöltő kódja korábban bekerült a weboldalba.
- A tényleges AdSense-fiókbeállításokhoz és a Privacy & Messaging felülethez a fióktulajdonos bejelentkezése szükséges.
- A CMP konfigurációját, a megjelenő üzenetet, a nyelveket és a hozzájárulási jelzések működését még nem ellenőriztük.
- Nem igazolt, hogy az AdSense-fiók jóváhagyta a webhelyet.
- Nem igazolt, hogy a jelenlegi látogatók felé már megjelenik megfelelő hozzájárulási üzenet.
- A forráskód puszta vizsgálata nem mutatja meg a böngészőben ténylegesen létrejövő harmadik fél sütiket, hálózati kéréseket vagy tárolási műveleteket.

## 3. Kötelező következő ellenőrzések

1. AdSense-fiókban a Privacy & Messaging menüpont ellenőrzése.
2. Európai szabályozási üzenet létrehozása vagy meglévő beállítás felülvizsgálata.
3. A Google által tanúsított CMP és TCF-integráció státuszának ellenőrzése.
4. A hirdetéstechnológiai szolgáltatók listájának áttekintése és a látogatók felé történő megfelelő tájékoztatás ellenőrzése.
5. A hozzájárulás elutasítási és visszavonási útvonalának tesztelése.
6. Tiszta böngészőprofilban, EGT-régióból végzett teszt: az első oldalbetöltés előtti és utáni hálózati kérések, sütik és localStorage/sessionStorage változások rögzítése.
7. A végleges adatvédelmi tájékoztató csak a tényleges adatfolyamok, adatfeldolgozók, megőrzési idők, jogalapok és üzemeltetői adatok tisztázása után készülhet el.

## 4. Biztonságos átmeneti álláspont

Amíg a hozzájáruláskezelés nincs beállítva és tesztelve, ne tekintsük a webhelyet EGT-hirdetéskiszolgálásra késznek. Ne állítsuk, hogy a cookie/hozzájárulási megfelelőség megvalósult, és ne adjunk hozzá saját, nem tanúsított „cookie bannert” úgy, mintha az önmagában teljesítené a Google CMP-követelményeit.

A Google AdSense-kód jelenléte önmagában nem igazolja sem a hirdetésmegjelenítést, sem a jóváhagyást, sem a jogszerű hozzájáruláskezelést.

## 5. Hivatalos Google-források

- Google AdSense – Consent management requirements for serving ads in the EEA, UK and Switzerland (publishers): https://support.google.com/adsense/answer/13554116
- Google AdSense – Set up and manage your Consent Management Platform (CMP): https://support.google.com/adsense/answer/7670013
- Google AdSense – Publisher integration with the IAB Europe TCF: https://support.google.com/adsense/answer/9804260
- Google AdSense – Commonly asked questions about European regulations messages: https://support.google.com/adsense/answer/11546682

## 6. Korlátozások

Ez a dokumentum a Google közzétett hirdetési követelményeit foglalja össze. Nem minősül jogi szakvéleménynek, nem helyettesíti a GDPR/ePrivacy megfelelőség teljes vizsgálatát, és nem igazolja az AdSense-fiók aktuális beállításait.
