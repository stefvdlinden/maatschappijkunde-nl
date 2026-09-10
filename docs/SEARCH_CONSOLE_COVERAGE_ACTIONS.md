# Search Console: beoordeling en acties

Bekeken op 10 september 2026 via de ingelogde browser voor de domeinproperty maatschappijkunde.nl. Indexeringsrapport bijgewerkt tot 4 september 2026: 88 geïndexeerd, 199 niet geïndexeerd. Deze aantallen zijn Google's momentopname, geen live-testuitslag.

## Beoordeling per categorie

| Categorie | Aantal | Bevinding en actie |
|---|---:|---|
| Ongeautoriseerd verzoek (401) | 61 | Alle 61 voorbeelden horen bij de oude ontwikkelhost. Geen aangetoonde productie-401. Oude host afhandelen in de hostingconfiguratie. |
| Pagina met omleiding | 21 | Vooral HTTP/www-varianten, feeds en begrippen. Bewuste omleidingen hoeven niet zelf geïndexeerd te worden. |
| Niet gevonden (404) | 11 | Concrete productie-URL's; hieronder opgenomen. Redirectafhandeling hersteld in de middleware en live-audit uitgebreid. |
| Serverfout (5xx) | 4 | Alle vier op de oude ontwikkelhost: multiculturele-samenleving-overzicht, criminaliteit kerndoel 4, verzorgingsstaat kerndoel 2 en examenstofarchief. |
| Alternatieve pagina met correcte canonieke tag | 4 | Twee homepage-queryvarianten, oude tagpaginering en een begrip. Tagpaginering krijgt een redirect naar het volledige tagoverzicht. |
| Soft 404 | 1 | Zoektemplate-query `?s={search_term_string}` op de oude ontwikkelhost; geen van de vijf korte productieoverzichten. |
| Gecrawld, momenteel niet geïndexeerd | 81 | Mix van lesstof, overzichten, PDF's, queryvarianten, begrippen en oude paden. Bekende legacy-paden toegevoegd aan redirects; overige inhoud behouden. |
| Gevonden, momenteel niet geïndexeerd | 15 | Productiepagina's zoals categorieën, tags, contact, websites en enkele lesstofpagina's. Herkennen en crawlen door Google afwachten; geen bewijs van verwijdernoodzaak. |
| Uitgesloten door noindex | 1 | `/multiculturelemsamenleving-kerndoel-1/feed/`; feed moet naar de bestaande pagina redirecten. Validatie stond al op Gestart. |
| Dubbel zonder gekozen canonical | 0 | Geen open voorbeelden. |

## Elf 404-voorbeelden

| Gemeld pad | Hostvariant | Doel |
|---|---|---|
| `/begrippen/maatschappelijke-positie` | HTTP www | Schoolwoorden-begrip maatschappelijke positie |
| `/planning/` | HTTPS apex | `/examenstof/` |
| `/ciminaliteitenrechtsstaat-kerndoel1/` | HTTP www | `/examenstof/criminaliteitenrechtsstaat-kerndoel1/` |
| `/begrippen/sociale-mobiliteit/` | HTTPS www | Schoolwoorden-begrip sociale mobiliteit |
| `/planning/leerjaar3/` | HTTPS apex | `/examenstof/` |
| `/kerndoelen/` | HTTPS apex | `/examenstof/` |
| `/planning/leerjaar4/` | HTTPS apex | `/examenstof/` |
| `/kerndoel-tags/` | HTTPS apex | `/examenstof/` |
| `/examenstof/politiekenbeleid-kerndoel1-2/feed/` | HTTPS apex | Bovenliggende artikelpagina |
| `/examenstof/criminaliteitenrechtsstaat-kerndoel2/feed/` | HTTPS apex | Bovenliggende artikelpagina |
| `/examenstof/multiculturelemsamenleving-kerndoel-1/feed/` | HTTPS apex | Bovenliggende artikelpagina |

## Canonicals en sitemap

De vier canonical-voorbeelden zijn `/?post_type=question`, `/?ajax=1&ht-kb-search=1&s=`, `/kerndoel-tags/se/page/2/` en `/begrippen/sociale-mobiliteit/`. Homepage-queryvarianten gebruiken de productiecanonical. De oude tweede tagpagina verwijst voortaan naar `/kerndoel-tags/se/`; het begrip behoudt de Schoolwoorden-redirect.

Search Console meldde voor `https://maatschappijkunde.nl/sitemap.xml`: **Succesvol**, ingediend op 15 juni 2026, laatst gelezen op 31 augustus 2026, 106 ontdekte pagina's. De vernieuwde sitemap bevat 105 URL's omdat `/home/` een redirect is en niet als indexeerbare pagina hoort te worden ingediend.

## Technische achtergrond

De root-middleware draaide voor inkomende requests, maar voerde alleen de www-normalisatie uit. Cloudflare past `_redirects` niet toe op door Pages Functions afgehandelde requests. De middleware leest nu de migratieredirects en de gedeelde SEO-regels. Ook slashloze legacy-URL's en feeds worden verwerkt. Het interne bestand `/_redirects` hoort zelf 404 te geven. Zie [Cloudflare Pages redirects](https://developers.cloudflare.com/pages/configuration/redirects/).

## Vervolg

1. Na geslaagde deployment alle live-audits uitvoeren.
2. De vernieuwde sitemap opnieuw indienen.
3. De 404-validatie opnieuw starten nadat de gemelde URL's correct reageren.
4. De reeds lopende noindex-validatie laten afronden.
5. Ontwikkelhost afzonderlijk afhandelen; op 10 september gaf de root een configuratieplaceholder (200) en een gecontroleerd oud artikel 404. Geen publieke sitecontent gevonden op die twee requests.
6. Na hercrawl het rapport opnieuw beoordelen. Een gestarte validatie of geslaagde deploy betekent niet dat Google alle pagina's al opnieuw heeft verwerkt.
