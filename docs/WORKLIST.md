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

- [ ] Gewijzigde site publiceren en Cloudflare-check verifiëren.
- [ ] Live smoke-, redirect- en headeraudits uitvoeren op de nieuwe productieversie.
- [ ] Sitemap opnieuw indienen en 404-validatie starten nadat de live controles slagen.

## Open externe acties

- [ ] Oude ontwikkelhost afhandelen via Cloudflare/hosting: de root toont een configuratieplaceholder (200), een gecontroleerde oude lesstof-URL geeft 404. De 61 historische 401's, vier 5xx'en en één soft 404 horen bij deze host. Dashboardtoegang vereist een gebruikerslogin. Definitieve keuze: de vervallen host naar productie laten verwijzen of de oude omgeving consistent uitfaseren; geen beveiliging uitschakelen om Google toegang te geven.
- [ ] Na Google's hercrawl de 404- en noindex-categorie opnieuw bekijken. Indexering is niet direct na deployment afgerond.
- [ ] De 81 gecrawlde en 15 gevonden maar niet geïndexeerde URL's volgen. De groep bevat historische varianten, downloads en bestaande inhoud; geen algemene verwijder- of herschrijfopdracht.
- [ ] Enkele oude paden zonder bewezen vervanger inhoudelijk beoordelen, waaronder `/vraag/verzorgingsstaat/`, `/vraag/downloads/`, `/featured/politiekenbeleid/`, `/glossary-categories/criminaliteitenrechtsstaat/` en het afgebroken pad `/examenstof/politiekenbeleid-`. Geen generieke redirect naar de homepage toevoegen.

## Verificatie

`npm test`, `npm run build` en `npm run audit:sitemap-urls` slagen. De oorspronkelijke sitemapinventaris bevat 100 URL's: 97 pagina's, drie bewuste redirects, nul ontbrekend. De actuele productiesitemap bevat na deze wijziging 105 URL's.
