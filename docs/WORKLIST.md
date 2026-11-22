# Werklijst

Bijgewerkt: 20 november 2026, op basis van de projectchats en lokale documentatie.

## Geconsolideerde open werklijst

Deze lijst bundelt de nog openstaande punten uit de drie gevonden projectchats. De oorspronkelijke septembercontroles hieronder blijven als historie behouden. De live website, Cloudflare, Analytics en Search Console zijn bij deze inventarisatie niet opnieuw gecontroleerd; historische aantallen zijn dus geen actuele meetresultaten. De volgorde is een voorgestelde prioritering.

| Nr. | Prioriteit | Open actie | Gereed wanneer | Bron / laatst bekende status |
|---|---|---|---|---|
| 1 | Hoog | Livegang en werking van de cookiebanner controleren. Controleer zonder keuze, na weigeren, na akkoord, na herladen en na intrekken via “Cookie-instellingen”; controleer ook de privacyverklaring. | Cloudflare-publicatie van `6869bc3` of een opvolgende versie bevestigd; vóór akkoord geen Analytics-verzoeken; na akkoord een collect-verzoek met `gcs=G101`; na intrekken geen meting, beide GA-cookies op het echte domein verwijderd en keuze bewaard. | Chat “Werk cookiebanner en GA4-toestemming”: commit en push afgerond, alleen lokaal browseronderzoek; livegang expliciet niet gecontroleerd. |
| 2 | Hoog | De eerdere GA4-melding “0% toestemming, 100% geweigerd” opnieuw bekijken. | Vastgelegd op welk signaal de melding betrekking heeft. Na akkoord moet `analytics_storage` toegestaan zijn; advertentietoestemmingen blijven bewust geweigerd. Bij blijvende statistiekweigering de oorzaak onderzoeken. | Dezelfde chat: hercontrole na 48–72 uur en nieuwe metingen genoemd; geen latere afronding gevonden. |
| 3 | Hoog | Astro en transitieve afhankelijkheden actualiseren na een nieuwe afhankelijkhedencontrole. | Actuele bevindingen beoordeeld, passende update uitgevoerd en migratie, tests en build gecontroleerd. | Bestaande werklijst: op 10 september acht bevindingen (één kritisch, zes hoog, één laag); actuele aantallen niet vastgesteld. |
| 4 | Normaal | De mislukte repositorycontrole uit de cookiebannerchat oplossen. | Historische verwijzingen in documentatie en ongewenste ontwikkelverwijzingen passend onderscheiden; de volledige `npm test` slaagt zonder de controle algemeen uit te schakelen. | Cookiebannerchat: laatste teststap struikelde over een bestaande ontwikkelhostverwijzing in `docs/SEARCH_CONSOLE_COVERAGE_ACTIONS.md`; die verwijzing en de brede controle zijn lokaal nog aanwezig. |
| 5 | Normaal | Search Console-validaties voor 401, 404, serverfouten en soft 404 opnieuw beoordelen. | Recente rapportdatum, validatie-uitkomst en resterende voorbeelden vastgelegd; alleen nog werkelijk falende URL’s krijgen vervolgwerk. | Chats “Controleer Git en projectdocs” en “Verbeter pagina niet geïndexeerd”: validaties gestart op 10 september; op 17 september nog lopend. Noindex was toen voltooid. |
| 6 | Normaal | Indexering van bestaande inhoud en effect van de nieuwe navigatie volgen. | Actuele sitemapverwerking en indexering vergeleken met 17 september; echte inhoudspagina’s gescheiden van redirects, downloads en historische varianten; gerichte vervolgacties bepaald. | Laatste rapport: 88 geïndexeerd, 42 gecrawld maar niet geïndexeerd en 16 gevonden maar niet geïndexeerd. Navigatie gepubliceerd, Examenstof-herindexering aangevraagd en sitemap opnieuw ingediend op 17 september. |
| 7 | Normaal | Oude paden zonder bewezen vervanger inhoudelijk beoordelen: `/vraag/verzorgingsstaat/`, `/vraag/downloads/`, `/featured/politiekenbeleid/`, `/glossary-categories/criminaliteitenrechtsstaat/` en `/examenstof/politiekenbeleid-`. | Per pad een onderbouwd besluit over behouden, een passende redirect of een bewuste foutstatus vastgelegd. | Bestaande open werklijst; geen generieke homepage-redirect toevoegen. |
| 8 | Later | De generieke support-template, planning uit 2017, `/category/featured/` en `/examenstof-2/` inhoudelijk beoordelen. | Vastgelegd of deze pagina’s bruikbaar zijn en moeten worden ontsloten, aangepast of geconsolideerd. Verwijderen of herschrijven vereist een expliciete inhoudelijke keuze. | Search Console-documentatie van 17 september: bewust niet extra gepromoot, beoordeling nog open. |
| 9 | Normaal | De reeds aanwezige lokale sitemapwijziging beoordelen en afronden. | Toevoeging van `/privacyverklaring/` in `scripts/postbuild-seo.mjs` gecontroleerd op datum en sitemapdekking; bij een volgende publicatieronde vastgelegd en gepubliceerd. | Aanvullende lokale bevinding op 19 november: dit bestand was bij aanvang al gewijzigd en staat nog niet in een commit. Tijdens deze inventarisatie niet aangepast. |

### Gecombineerde lijst met codes (stand 19 november 2026, avond)

Dit is de samenvoeging van bovenstaande tabel met `WORKLIST_AANVULLING.md` (A01–A09). Codes: I inhoud, B begrippen, S Search Console en SEO, M meting en kwaliteit, O onderhoud, P projectafspraken, A administratie. Details van B1 en I2 staan in [BEGRIPPENLIJST_REVIEW.md](BEGRIPPENLIJST_REVIEW.md) en [OEFENMATERIALEN_INVENTARIS.md](OEFENMATERIALEN_INVENTARIS.md).

| Code | Taak | Stand |
|---|---|---|
| S1 | Search Console-foutcategorieën opnieuw bekijken (401, 404, 5xx, soft 404) | **Gedaan 19 nov** (rapport 16 nov: 91 geïndexeerd, 132 niet). 404-validatie **Mislukt** door `/begrippen/maatschap` (de andere acht URL's redirecten). 401 (52) en 5xx (4) staan op Gestart; Google heeft de dev-URL's nog niet opnieuw gecrawld. noindex en soft 404 Voltooid. Zie `SEARCH_CONSOLE_COVERAGE_ACTIONS.md`. |
| S2 | Gecrawld/gevonden maar niet geïndexeerd volgen | **Onderzocht 19 nov** (21 + 18 URL's, alle 200, geen noindex). Overwegend verwacht gedrag (PDF's, redirects, dunne overzichten). Twee concrete problemen: vijf dubbele pagina's (zie S4) en twee weesjes in de sitemap. Details in `SEARCH_CONSOLE_COVERAGE_ACTIONS.md`. |
| S4 | Vijf dubbele WordPress-berichten naast hun examenstofpagina | **Opgelost in code (19 nov), nog te publiceren**: canonical naar de examenstofversie, uit de sitemap (nu 101 URL's), regressietest toegevoegd. Daarna live controleren. |
| S3 | Sitemapmetadata | **Gedaan**, commit `ea9fb67`: privacyverklaring toegevoegd (lastmod 2026-10-14). Besluit: homepage-lastmod blijft de WordPress-datum (2016). |
| B1 | Begrippenlijst actualiseren | **Gedaan** (commits `7145bb9`, `3d35c44`, `d5856d8`, live bevestigd): alle vijf secties van het review doorgevoerd. Spellingronde gedaan op 20 november 2026 (macOS-spellingcontrole plus handmatige beoordeling; negen fouten verbeterd) en 50+ gecontroleerd: 50PLUS zit sinds november 2025 weer in de Tweede Kamer (2 zetels), naam nu "50PLUS". Rest: tekstuele afstemming met Schoolwoorden niet vergeleken. |
| B2 | Begrippen koppelen aan Schoolwoorden (termenlinker) | Aangehouden tot B1 en I1 klaar zijn. |
| I1 | Examenstof actualiseren (dekkingsmatrix, syllabus 2027) | I1b gedaan (2014-zetelafbeelding vervangen door tekst). I1a doorgevoerd: kerndoel 1.1 aangevuld volgens `docs/I1A_DEKKINGSMATRIX_KERNDOEL1-1.md` (legaliteitsbeginsel aangehouden tot het niveau bekend is). Matrices voor kerndoel 1.2–1.4 en de overige kerndoelen nog niet gestart. De vier verouderde feiten (28/27 lidstaten, 751/720 zetels, tuchtschool/jeugddetentie, beroepsbevolking) zijn wel gecorrigeerd in `politiekenbeleid-kerndoel2`, `criminaliteitenrechtsstaat-kerndoel2` en `mensenwerk-kerndoel6`. De afbeelding `zetelverdeling2014.png` is nog van 2014. I1c: matrices voor kerndoel 1.2–1.4 en 2–5 staan in `docs/I1C_DEKKINGSMATRIX_POLITIEKENBELEID.md`, I1c volledig doorgevoerd (onjuistheden, kerndoel 5 en overige aanvullingen); alleen de partij-indeling onder Nationalistisch ter controle door de eigenaar. I1d deel 1–2 (Mens en werk, Multiculturele samenleving): stap 1 en 2 doorgevoerd (`docs/I1D_DEKKINGSMATRIX_MENSENWERK_MULTICULTUREEL.md`); stap 3 (I1d-5) doorgevoerd, en MC5 (beleid 2024–2026) doorgevoerd op 20 november 2026. Let op: K/5, K/6 en K/7 zijn schoolexamen-onderdelen zonder syllabus. I1d deel 3–4 (Criminaliteit en rechtsstaat, Massamedia, AMV): matrix in `docs/I1D_DEKKINGSMATRIX_CRIMINALITEIT_MASSAMEDIA_AMV.md`: onjuistheden en restanten (3a, 4a) en aanvullen (3b, 4b) doorgevoerd; actualiseren (3c, 4c) doorgevoerd en de labels "(tot 2022)" verwijderd; dubbele tekst AMV 3 blijft staan, CR6 (voorlopige hechtenis) wacht op bron. |
| I1e | Oude domeinen (Maatschappijleer HAVO B–E, Maatschappijleer VMBO, Maatschappijwetenschappen) | Matrix opgesteld in `docs/I1E_DEKKINGSMATRIX_OUDE_DOMEINEN.md` (20 nov). Deze domeinen staan niet in de syllabus 2027. Voorstel: kleine correctieronde (VZ1–3, VZ5, PL3–5, MV1, MV2); PL1/PL2 zijn een keuze (herschrijven of schrappen). **Correctieronde doorgevoerd 22 nov**: VZ1 (AOW-leeftijd), VZ2, VZ3, VZ5, PL3, PL4 (EU 1993, gedoogvoorbeeld), PL5 (typefouten, tekst bij burgers herschreven), MV1 (PowNed vervangen), MV2 (eigen inleiding). Open: PL1 en PL2 (keuze eigenaar), VZ4 (wacht op I1c-Q), I1e-Q2 (welke niveaus). |
| I5 | Vakvernieuwing (SLO-startnotitie juni 2025) | Pagina `/vakvernieuwing/` staat live (22 nov) en is gelinkt vanaf de homepage (knop) en Examenstof (regel bovenaan). Dekking en stappen in `docs/VAKVERNIEUWING_DEKKING.md`. K3/V3 gecontroleerd: zie `docs/I1F_DEKKINGSMATRIX_K3_V3.md`. Open: voorstel een pagina "Leervaardigheden" (K/3) en een zin over de politieke agenda bij AMV kerndoel 1 (V/3 heeft geen uitwerking in de syllabus). |
| B3 | Begrippen en Schoolwoorden | **Doorgevoerd 22 nov**: `volksvertegenwoordigers`, `recidiveren` en `liberale-stroming` (bron- en redirectlinks) wijzen nu naar `volksvertegenwoordiger`, `recidive` en `liberalisme`. Alle 238 begrippen linken daarmee naar een bestaande Schoolwoorden-pagina. In de lopende tekst van de examenstof staan geen links naar Schoolwoorden (B2). |
| I2 | Oefenvragen en externe materialen | **Inventaris klaar.** Herstel wacht op eigenaar van formulier (politiekenbeleid-kerndoel3) en 403-presentatie (mensenwerk kerndoel 5/6); vijf presentaties met verdachte titel. |
| I3 | Downloads beoordelen | Aangehouden tot I1. Alle 13 downloadlinks geven HTTP 200. |
| I-redir | Redirectketen oude begrippen-URL's | **Doorgevoerd 20 nov**: 232 doelen op schoolwoorden.nl verwezen zelf door naar de variant zonder eindslash; de doelen wijzen nu direct naar het eindadres (3 doelen met een tweede doorverwijzing ook). Het doel `/begrip/liberale-stroming` geeft 404 op schoolwoorden.nl (bron `/begrippen/liberale-stroming/`) en is nog open. Wacht op live controle. |
| I4 | Oude paden en templatepagina's (vraag/…, featured, contact-support, examenstof-2, planning) | Doorgevoerd (`docs/I4_OPRUIMVOORSTEL.md`): vier pagina's naar 301, drie overzichten gelinkt vanaf `/examenstof/`, vijf oude 404-paden bewust 404 gelaten. Wacht op live controle na publicatie. |
| S6 | Hercontrole indexering in Search Console | Gepland rond 10 december 2026: lezen of de vijf dubbele pagina's (S4), de vier verwijderde pagina's en de drie overzichten (I4) zijn opgepakt. |
| M1 | Gebruiks- en Analytics-controle | **Grotendeels gedaan** op de live site: geen keuze/weigeren = geen verzoeken of cookies; toestemming = één collect met `gcs=G101` en twee GA-cookies; intrekken verwijdert cookies. Mobiel geen horizontale overflow. Tablet (768 px) en Tab-toets op de homepage ook gecontroleerd: geen horizontale overflow en zichtbare focus. Open: GA4-rapportage (M2). |
| M2 | GA4-melding "0% toestemming, 100% geweigerd" opnieuw bekijken | Open; alleen in GA4 te beoordelen. |
| O1 | Astro en dependencies actualiseren | Open; aparte branch met tests en preview. |
| O2 | Cleanup uit de refactor-audit | Aangehouden. |
| O3 | Mislukte repositorycontrole (dev-hostverwijzing in docs) | **Gedaan.** De controle slaat `docs/` over voor de dev-hostcheck; `npm test` slaagt volledig. |
| P1 | Footer (Methode M) en `PROJECT_BRIEF.md` gelijk trekken | Beslissing van de eigenaar nog open. |
| A1 | Werklijst bijwerken | Gedaan met deze sectie. |

Momentopnames: Search Console op 7 november (rapport tot 23 oktober): 89 geïndexeerd, 139 uitgesloten, 22 gecrawld, 19 gevonden; sitemap op 3 november gelezen met 105 pagina's. Dit zijn historische meetwaarden, geen meting van 19 november.

### Bronnen van de chatcontrole

- “Controleer Git en projectdocs” — 10 september 2026, chat-ID `01a08b35-c500-7e50-a206-9a04b2803857`.
- “Verbeter pagina niet geïndexeerd” — 17 september 2026, chat-ID `01a0adfa-2d51-7441-a5c0-9413cb825da5`.
- “Werk cookiebanner en GA4-toestemming” — 14 oktober 2026, chat-ID `01a13983-1fb7-72e2-9d46-d43838ae28c4`.

Latere antwoorden in dezelfde chats zijn meegewogen: de oude ontwikkelhost, redirectreparaties, septemberpublicatie, sitemapindiening en oktobercommit/push zijn afgerond. Die staan daarom niet opnieuw als uitvoerwerk open. De actieve en gearchiveerde Codex-chatlijsten zijn doorzocht op dit project en deze werkmap.


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

## Verificatie

`npm test`, `npm run build` en `npm run audit:sitemap-urls` slagen. De oorspronkelijke sitemapinventaris bevat 100 URL's: 97 pagina's, drie bewuste redirects, nul ontbrekend. De live sitemap bevat 105 URL's; alle URL's en canonicals zijn gecontroleerd.

## Historische onderhoudsbevinding

De afhankelijkhedenbevinding van 10 september is opgenomen als open actie 3. De toenmalige tests en buildresultaten hierboven dateren van september; de cookiebannerchat meldde later de mislukte repositorycontrole uit actie 4.
