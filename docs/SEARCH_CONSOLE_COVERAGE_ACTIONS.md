# Search Console: beoordeling en acties

## Hercontrole — 17 september 2026

Rapportdatum 14 september 2026: **88 geïndexeerd, 160 niet geïndexeerd**. Op 4 september waren dat 88 en 199. De daling van 39 uitgesloten URL's is geen bewijs van 39 extra geïndexeerde pagina's: het geïndexeerde aantal bleef gelijk.

| Reden | Aantal | Beoordeling op 17 september |
|---|---:|---|
| Pagina met omleiding | 21 | Bewuste redirects mogen uitgesloten blijven. Live redirectaudit: 21 checks geslaagd. |
| Alternatief met correcte canonical | 4 | Geen nieuwe canonicalfout aangetoond; juiste voorkeurs-URL laten indexeren. |
| Gecrawld, niet geïndexeerd | 42 | Was 81. Alle 42 voorbeelden bekeken: mix van PDFs, www/HTTP-varianten, begrippenredirects, feed, queryvarianten en inhoudspagina's. |
| Gevonden, niet geïndexeerd | 16 | Alle voorbeelden bekeken. Daarvan missen vier categorieën, vijf tagoverzichten en Websites inkomende links; navigatie lokaal verbeterd. |
| 401 | 60 | Alle 60 voorbeelden op dev.maatschappijkunde.nl; oude crawldatums. Validatie sinds 10 september loopt nog. |
| 404 | 11 | Dezelfde elf oude URL's als hieronder; bestaande redirectoplossingen werken. Validatie loopt nog. |
| 5xx | 4 | Validatie loopt nog; vier eerder vastgelegde dev-paden opnieuw getest: 301 naar productie, eindstatus 200. |
| Soft 404 | 1 | Validatie loopt nog; oude dev-zoektemplate verwijst naar productie en eindigt op 200. |
| noindex | 1 | Validatie staat nu op **Voltooid**. Het rapport toont nog één historische URL. |
| Dubbel zonder gekozen canonical | 0 | Geen actie. |

### Live verificatie

- Sitemap in Search Console: **Succesvol**, ingediend én laatst gelezen op 10 september, **105 ontdekte pagina's**. Opnieuw indienen is nu niet nodig.
- Alle 105 live sitemap-URL's gecontroleerd: HTTP 200 zonder redirect, juiste canonical, geen aangetroffen robots-meta/header met noindex.
- Smoke-, redirect- en headeraudits: respectievelijk 17, 21 en 6 checks, geen fouten/waarschuwingen.
- Zeven HTTPS-dev-URL's gecontroleerd, waaronder de vier historische serverfoutpaden en de zoektemplate: 301 naar productie en eindstatus 200.
- Lopende validaties niet opnieuw gestart. Google's historische foutgroepen lopen achter op de actuele HTTP-responses.

### Lokaal aangebrachte verbeteringen (nog niet gepubliceerd)

- Broodkruimels van categorie-, tag- en kerndoeloverzichten wijzen rechtstreeks naar `/examenstof/`. Hiermee verdwijnt onder andere de kapotte link naar `/category/` en vervallen omleidingen via de oude indexpaden. Gestructureerde broodkruimeldata gebruikt dezelfde links.
- Examenstof linkt nu naar zes bestaande onderwerpcategorieën en zeven niveau-/examenoverzichten. Deze dertien overzichten hadden geen inkomende contentlinks.
- Leertips en Websites opgenomen in de footer; beide waren niet intern bereikbaar.
- De generieke support-template, de oude planning uit 2017, `/category/featured/` en `/examenstof-2/` niet extra gepromoot. Inhoudelijk beoordelen voordat deze actief worden aangeboden of geconsolideerd. Geen pagina's verwijderd.
- `npm test`, `npm run build` en `npm run audit:sitemap-urls` slagen. Alle interne links in de gerenderde 106 contentpagina's gecontroleerd: nul ontbrekende doelen. Nieuwe navigatie visueel gecontroleerd in lokale preview.

De navigatieverbeteringen maken pagina's beter bereikbaar, maar bewijzen niet dat ontbrekende interne links de enige oorzaak van uitsluiting zijn. Indexering blijft een keuze van Google; zie [Google: pagina-indexeringsrapport](https://support.google.com/webmasters/answer/7440203?hl=nl).

## Historische controle — 10 september 2026

Bekeken op 10 september 2026 via de ingelogde browser voor de domeinproperty maatschappijkunde.nl. Indexeringsrapport bijgewerkt tot 4 september 2026: 88 geïndexeerd, 199 niet geïndexeerd. Deze aantallen zijn Google's momentopname, geen live-testuitslag.

## Beoordeling per categorie

| Categorie | Aantal | Bevinding en actie |
|---|---:|---|
| Ongeautoriseerd verzoek (401) | 61 | Alle 61 voorbeelden horen bij de oude ontwikkelhost. Geen aangetoonde productie-401. Oude host verwijst nu via Cloudflare naar productie; validatie gestart op 10 september. |
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

Commit `10f7d71` is succesvol gepubliceerd. De eerste poging faalde op JSON-importsyntax die de oudere Cloudflare-bundelaar niet ondersteunde; dit is opgelost en met Wrangler 3.114.17 gecontroleerd.

- Alle 105 live sitemap-URL's geven HTTP 200 met de juiste canonical.
- Live smoke-, redirect- en headeraudits slagen met respectievelijk 17, 21 en zes checks.
- De sitemap is opnieuw ingediend op 10 september 2026; de browser bevestigde **Sitemap ingediend**. Het weergegeven oude aantal ontdekte pagina's wordt pas bij verwerking bijgewerkt.
- De 404-validatie staat op **Gestart, 10-09-2026**, met elf URL's in behandeling en nul mislukt bij aanvang.
- De noindex-validatie liep al en is niet opnieuw gestart.
- De oude ontwikkelhost verwijst na expliciete toestemming via een actieve 301 naar productie, met behoud van pad en queryparameters. Het proxied A-record voor subdomein `dev` gebruikt het bestaande adres 80.69.67.10. De wildcardrecords zijn behouden.
- Cloudflare-regel **Retire old development host**, ID `c9471ff380af42a6a8a23c126ce15cb4`, geldt alleen voor de oude ontwikkelhost en gebruikt als dynamisch doel `concat("https://maatschappijkunde.nl", http.request.uri.path)` met querybehoud ingeschakeld. Deze zoneconfiguratie staat buiten de Pages-repository.
- HTTP en HTTPS zijn live gecontroleerd. De homepage, een artikel met queryparameters, alle vier oude serverfoutpaden en de zoektemplate-query verwijzen naar productie en eindigen op HTTP 200.
- De 401-, 5xx- en soft-404-validaties staan alle drie op **Gestart, 10-09-2026**. Dit bevestigt de aanvraag; Google moet de oude foutmeldingen nog opnieuw beoordelen.
- Na hercrawl het rapport opnieuw beoordelen. Een gestarte validatie betekent niet dat Google alle pagina's al opnieuw heeft verwerkt.
