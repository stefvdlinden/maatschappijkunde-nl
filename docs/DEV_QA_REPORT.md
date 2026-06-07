# Dev QA rapport - maatschappijkunde.nl

Datum: 2026-06-07

## 1. Dev-deploy

Laatste GitHub Actions run:

- Run: `27087535473`
- Commit: `d3aee9e Link legacy archive overviews`
- Workflow: `Deploy dev site to TransIP`
- Status: success
- Build: success
- Deploy via SFTP: success
- Duur: 13m54s

`https://dev.maatschappijkunde.nl/` reageert met Basic Auth realm `omzetten hosting`.
Met de dev-credentials is de live dev-site bereikbaar.

Recente succesvolle runs:

| Run | Commit | Status |
|---|---|---|
| `27087535473` | `Link legacy archive overviews` | success |
| `27087154418` | `Clear content fidelity audit` | success |
| `27085775546` | `Fill static overview pages` | success |
| `27075312197` | `Skip empty content wrapper` | success |
| `27074933184` | `Clean public conversion artifacts` | success |

Bekende workflow-waarschuwing:

- GitHub Actions meldt een Node.js 20 deprecation warning voor `actions/checkout@v4` en `actions/setup-node@v4`.
- Dit is geen deploy-failure. De workflow slaagt en de site wordt gedeployed.

## 2. Automatische audits

Automatische audits op de huidige statische conversie:

| Audit | Resultaat |
|---|---:|
| URL coverage | 110 pagina's, 242 redirects |
| Redirect audit | 242 redirects, 0 issues |
| Asset audit | 47 upload references, 0 missing |
| HTML conversion audit | 0 issues |
| Visible artifact audit | 0 issues |
| Content fidelity audit | 0 issues |
| Internal link audit | 704 links, 0 missing |
| External reference audit | 0 issues |
| URL gap report | 0 investigate URLs |
| Unresolved shortcodes | 0 |

Veilige media:

| Extensie | Aantal |
|---|---:|
| `.png` | 1022 |
| `.jpg` | 234 |
| `.jpeg` | 25 |
| `.pdf` | 14 |

## 3. Kernpagina QA

Gecontroleerd op basis van de gegenereerde statische build, `data/site/pages.json` en live dev met Basic Auth.

| URL | Bevinding |
|---|---|
| `/` | Pagina aanwezig, geen ruwe shortcodes of handmatige code-notices. |
| `/examenstof/` | Overzicht gevuld met onderwerp- en kerndoellinks. |
| `/kerndoelen/` | Overzicht gevuld met kerndoeloverzichten. |
| `/examenstof/mens-en-werk/` | Oude lege pagina gevuld vanuit het corresponderende kerndoeloverzicht. |
| `/category/amv/` | Legacy categorie-URL behouden en aangevuld met link naar `/kerndoelen/amv/` plus AMV-kerndoellinks. |
| `/kerndoel-tags/leerjaar-3/` | Legacy tag-URL behouden en aangevuld met kerndoeloverzichten. |
| `/kerndoelen/domein-c-parlementaire-democratie/` | Korte lege taxonomiepagina aangevuld met statische context. |
| `/planning/` | Tabellen aanwezig en gevuld. |
| `/planning/leerjaar3/` | Tabellen aanwezig en gevuld. |
| `/planning/leerjaar4/` | Tabellen aanwezig en gevuld. |
| `/begrippen/` | Overzichtspagina aanwezig; individuele begrippen blijven redirects. |

Visuele desktop/mobile QA is uitgevoerd op 1280x720 en 390x844 voor de kernroutes. Resultaat:

- Geen console-errors gevonden.
- Hoofdnavigatie staat op alle gecontroleerde routes in de DOM.
- Geen horizontale overflow op de gecontroleerde routes na de table-overflow fix.
- `/planning/` bevat 4 tabellen en is specifiek mobiel gecontroleerd.
- Examenstofpagina's met embeds blijven binnen de viewport.

## 4. Redirectoplossing

Redirects zijn server-side werkend gemaakt voor TransIP door naast `_redirects` ook `.htaccess` te genereren uit `data/site/redirects.json`.

Live redirectbevindingen:

- `https://dev.maatschappijkunde.nl/_redirects` is live bereikbaar met status `200`, maar Netlify-style `_redirects` wordt niet door TransIP/nginx toegepast.
- `/begrippen/tweede-kamer/` geeft `301` naar `https://schoolwoorden.nl/begrip/tweede-kamer/`.
- `/begrippen/parlement/` volgt door naar `https://schoolwoorden.nl/begrip/parlement`.
- `/begrippen/reageerakkoord/` geeft `301` naar `https://schoolwoorden.nl/begrip/regeerakkoord/`.
- Extra legacy examenstofredirects zijn toegevoegd voor:
  - `/politiekenbeleid-kerndoel1-1/`
  - `/amv-kerndoel1/`
  - `/ciminaliteitenrechtsstaat-kerndoel1/`
- `https://dev.maatschappijkunde.nl/.htaccess` geeft `403`, dus het bestand wordt niet publiek als tekst geserveerd.

## 5. Headers en cache

Live header-audit op dev:

| Pad | Status | Bevinding |
|---|---:|---|
| `/` | 200 | HTML mist `Strict-Transport-Security` en `X-Content-Type-Options`. |
| `/examenstof/` | 200 | HTML mist `Strict-Transport-Security` en `X-Content-Type-Options`. |
| `/sitemap-index.xml` | 200 | OK. |
| `/_redirects` | 200 | Bestand is publiek leesbaar; functioneel onschadelijk op TransIP, maar niet nodig voor Apache. |
| `/.htaccess` | 403 | OK, niet publiek leesbaar. |
| `/wp-content/uploads/2016/12/Analyse-Maatschappelijk-Vraagstuk-212x300.png` | 200 | Asset mist `Cache-Control`. |

Deze punten zijn opgenomen in `docs/PRODUCTION_CUTOVER.md`.

## 6. Legacy oefenmodules

De oude `uhe_style1` oefenmodules zijn omgezet naar statische linklijsten. Er wordt geen oude WordPress-plugin of runtime-code uitgevoerd.

| URL | Categorie | Status |
|---|---|---|
| `/examenstof/analyse-maatschappelijk-vraagstuk/` | `amv` | Statische oefenlinks aanwezig. |
| `/examenstof/criminaliteit-en-rechtsstaat/` | `criminaliteit` | Statische oefenlinks aanwezig. |
| `/examenstof/politiekenbeleid/` | `politiek` | Statische oefenlinks aanwezig. |

## 7. Aanbevolen vervolgstappen

1. Rerun live redirect-audit na deploy van de extra legacy examenstofredirects.
2. Productieheaders met TransIP/Apache testen voordat ze live worden afgedwongen.
3. Productie-cutover voorbereiden volgens `docs/PRODUCTION_CUTOVER.md`.
4. Inhoudelijk reviewen of algemene legacy archive-teksten voldoende zijn of per pagina specifieker moeten worden gemaakt.
