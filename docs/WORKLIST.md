# Werklijst

Bijgewerkt: 17 september 2026.

## Hercontrole indexering — gepubliceerd op 17 september 2026

- [x] Rapport van 14 september beoordeeld: 88 geïndexeerd, 160 uitgesloten; alle 60 401-, 42 gecrawlde, 16 gevonden en 11 404-voorbeelden bekeken.
- [x] Alle 105 live sitemap-URL's gecontroleerd; HTTP 200, juiste canonical, geen aangetroffen noindex.
- [x] Sitemapverwerking bevestigd: Succesvol, 105 pagina's, laatst gelezen 10 september.
- [x] Bestaande live-audits en zeven dev-redirectcontroles geslaagd.
- [x] Kapotte/omleidende broodkruimellinks vervangen door directe bestaande bovenliggende pagina's.
- [x] Dertien onderwijs-overzichten via Examenstof ontsloten; Leertips en Websites via footer.
- [x] Tests, build, sitemapdekking en controle van alle gerenderde interne links geslaagd; preview visueel bekeken.
- [x] Navigatiewijzigingen gepubliceerd in commit `88dd830`; Cloudflare Pages geslaagd, 44 live-checks geslaagd en nieuwe navigatie live bevestigd.
- [x] Herindexering van `/examenstof/` aangevraagd en sitemap opnieuw ingediend; beide door Search Console bevestigd.

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

De runtimecorrectie uit commit `10f7d71` is gepubliceerd. De Cloudflare Pages-check is geslaagd. De eerste poging faalde doordat Wrangler 3.114.17 de JSON-importsyntax `with` niet kon verwerken; de compatibele import en gedeelde handler zijn daarna ook lokaal met exact die bundelaar getest.

- [x] Cloudflare-buildlogs gelezen, concrete oorzaak opgelost en opnieuw gepubliceerd.
- [x] Live smoke-audit: 17 checks, nul fouten.
- [x] Live redirectaudit: 21 checks, nul fouten.
- [x] Live headeraudit: zes checks, nul waarschuwingen.
- [x] Alle 105 URL's uit de live sitemap gecontroleerd: HTTP 200 en de juiste canonical; `/home/` is uitgesloten.
- [x] Sitemap opnieuw ingediend op 10 september; Google toont **Sitemap ingediend**.
- [x] 404-validatie opnieuw gestart op 10 september: elf URL's in behandeling, nul mislukt bij aanvang.

- [x] Oude ontwikkelhost na expliciete toestemming doorverwezen naar productie: proxied A-record voor subdomein `dev` naar 80.69.67.10, met actieve Cloudflare-regel **Retire old development host**. De 301 behoudt pad en queryparameters. HTTP en HTTPS live gecontroleerd; de vier oude serverfoutpaden, een artikel en de zoektemplate-query komen uit op HTTP 200.
- [x] Validaties voor 401, serverfouten en soft 404 gestart op 10 september; Search Console bevestigt voor alle drie **Validatie Gestart**.

## Open externe acties
- [ ] Na Google's hercrawl de 401-, 404-, serverfout- en soft-404-categorie opnieuw bekijken. De noindex-validatie is op 17 september Voltooid. Indexering is niet direct na deployment afgerond.
- [ ] De 42 gecrawlde en 16 gevonden maar niet geïndexeerde URL's volgen. De groep bevat historische varianten, downloads en bestaande inhoud; geen algemene verwijder- of herschrijfopdracht.
- [ ] Enkele oude paden zonder bewezen vervanger inhoudelijk beoordelen, waaronder `/vraag/verzorgingsstaat/`, `/vraag/downloads/`, `/featured/politiekenbeleid/`, `/glossary-categories/criminaliteitenrechtsstaat/` en het afgebroken pad `/examenstof/politiekenbeleid-`. Geen generieke redirect naar de homepage toevoegen.

## Verificatie

`npm test`, `npm run build` en `npm run audit:sitemap-urls` slagen. De oorspronkelijke sitemapinventaris bevat 100 URL's: 97 pagina's, drie bewuste redirects, nul ontbrekend. De live sitemap bevat 105 URL's; alle URL's en canonicals zijn gecontroleerd.

## Nieuw onderhoudspunt uit de buildlog

- [ ] Astro en transitieve afhankelijkheden actualiseren. `npm audit` meldt op 10 september acht dependencybevindingen: één kritisch, zes hoog en één laag. npm noemt een Astro-major-upgrade als volledige oplossing. Dit is afzonderlijk onderhoud met migratie- en buildtests; er is geen ongecontroleerde `npm audit fix --force` uitgevoerd. De site wordt statisch gepubliceerd, maar de ontwikkel- en buildketen moet ook worden onderhouden.
