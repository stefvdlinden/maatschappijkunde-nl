# Werklijst

Bijgewerkt: 10 september 2026.

## Uitgevoerd en lokaal gecontroleerd

- [x] GitHub-authenticatie, remote, branch en Cloudflare-koppeling gecontroleerd.
- [x] Oorzaak van ontbrekende runtime-redirects aangepakt: Pages Functions voert de redirectregels nu zelf uit.
- [x] Planning, kerndoelindex, tagindex, oude lesstofpaden, feeds en slashloze begrippen-URL's meegenomen.
- [x] Bestaande interne URL-normalisaties ook als publieke redirects vastgelegd.
- [x] Runtime-regressietests toegevoegd voor alle 264 regels op beide hosts, met en zonder eindslash en met queryparameters.
- [x] Redirectaudit controleert ook of interne doelen als pagina bestaan.
- [x] Headeraudit verwacht terecht 404 voor het interne bestand `/_redirects`.
- [x] Leeg overzicht Parlementaire Democratie gekoppeld aan bestaande relevante lesstof.
- [x] Vier andere korte overzichten beoordeeld: Beeldvorming en stereotypering, Cultuur en Socialisatie, Macht en zeggenschap, Sociale verschillen. Deze bevatten 3–4 artikelverwijzingen en blijven behouden; geen tekst opgevuld om alleen een woorddrempel te halen.
- [x] README vernieuwd en historische documenten onderscheiden van actuele acties.
- [x] Search Console-browser onderzocht: alle categorieën en de ingediende sitemap bekeken.
- [x] Sitemap sluit de omleidende `/home/`-pagina uit.

## Afronding productie

Productie draait op commit `10f7d71`. De Cloudflare Pages-check is geslaagd. De eerste poging faalde doordat Wrangler 3.114.17 de JSON-importsyntax `with` niet kon verwerken; de compatibele import en gedeelde handler zijn daarna ook lokaal met exact die bundelaar getest.

- [x] Cloudflare-buildlogs gelezen, concrete oorzaak opgelost en opnieuw gepubliceerd.
- [x] Live smoke-audit: 17 checks, nul fouten.
- [x] Live redirectaudit: 21 checks, nul fouten.
- [x] Live headeraudit: zes checks, nul waarschuwingen.
- [x] Alle 105 URL's uit de live sitemap gecontroleerd: HTTP 200 en de juiste canonical; `/home/` is uitgesloten.
- [x] Sitemap opnieuw ingediend op 10 september; Google toont **Sitemap ingediend**.
- [x] 404-validatie opnieuw gestart op 10 september: elf URL's in behandeling, nul mislukt bij aanvang.

## Open externe acties

- [ ] Oude ontwikkelhost doorverwijzen naar productie. Een gericht proxied A-record naar het bestaande adres 80.69.67.10 en een 301 met pad- en querybehoud zijn in Cloudflare voorbereid. Automatische goedkeuringscontrole heeft de DNS-wijziging geblokkeerd wegens ontbrekende expliciete toestemming; goedkeuring is gevraagd. De wildcardrecords en overige domeininstellingen zijn niet gewijzigd.
- [ ] Na Google's hercrawl de 404- en noindex-categorie opnieuw bekijken. Indexering is niet direct na deployment afgerond.
- [ ] De 81 gecrawlde en 15 gevonden maar niet geïndexeerde URL's volgen. De groep bevat historische varianten, downloads en bestaande inhoud; geen algemene verwijder- of herschrijfopdracht.
- [ ] Enkele oude paden zonder bewezen vervanger inhoudelijk beoordelen, waaronder `/vraag/verzorgingsstaat/`, `/vraag/downloads/`, `/featured/politiekenbeleid/`, `/glossary-categories/criminaliteitenrechtsstaat/` en het afgebroken pad `/examenstof/politiekenbeleid-`. Geen generieke redirect naar de homepage toevoegen.

## Verificatie

`npm test`, `npm run build` en `npm run audit:sitemap-urls` slagen. De oorspronkelijke sitemapinventaris bevat 100 URL's: 97 pagina's, drie bewuste redirects, nul ontbrekend. De live sitemap bevat 105 URL's; alle URL's en canonicals zijn gecontroleerd.

## Nieuw onderhoudspunt uit de buildlog

- [ ] Astro en transitieve afhankelijkheden actualiseren. `npm audit` meldt op 10 september acht dependencybevindingen: één kritisch, zes hoog en één laag. npm noemt een Astro-major-upgrade als volledige oplossing. Dit is afzonderlijk onderhoud met migratie- en buildtests; er is geen ongecontroleerde `npm audit fix --force` uitgevoerd. De site wordt statisch gepubliceerd, maar de ontwikkel- en buildketen moet ook worden onderhouden.
