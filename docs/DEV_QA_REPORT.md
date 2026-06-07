# Dev QA rapport - maatschappijkunde.nl

Datum: 2026-06-07

## 1. Dev-deploy

Laatste GitHub Actions run:

- Run: `27089769954`
- Commit: `058fc66 Test production headers on dev`
- Workflow: `Deploy dev site to TransIP`
- Status: success
- Build: success
- Deploy via SFTP: success
- Duur: 12m26s

`https://dev.maatschappijkunde.nl/` reageert met Basic Auth realm `omzetten hosting`.
Met de dev-credentials is de live dev-site bereikbaar.

Recente succesvolle runs:

| Run | Commit | Status |
|---|---|---|
| `27089769954` | `Test production headers on dev` | success |
| `27089243137` | `Record live QA audit results` | success |
| `27089016118` | `Prepare production QA checks` | success |
| `27088147576` | `Update dev QA handoff` | success |
| `27087535473` | `Link legacy archive overviews` | success |

Workflow-onderhoud:

- Dev-deploys gebruiken `concurrency` met `cancel-in-progress: true`, zodat deployments naar `dev.maatschappijkunde.nl` niet parallel lopen.
- De workflow zet `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true`.
- GitHub toont nog een informatieve annotatie dat `actions/checkout@v4` en `actions/setup-node@v4` Node.js 20 targeten, maar forced op Node.js 24 draaien.
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
| Sitemap URL coverage | 100 sitemap-URL's, 100 pagina's, 0 redirects, 0 missing |
| Unresolved shortcodes | 0 |
| Live smoke audit op dev | 16 checks, 0 issues |

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
- Live redirect-audit na deploy `27089769954`: 6 checks, 0 issues.
- `https://dev.maatschappijkunde.nl/.htaccess` geeft `403`, dus het bestand wordt niet publiek als tekst geserveerd.

## 5. Headers en cache

Live header-audit op dev na deploy `27089769954`:

| Pad | Status | Bevinding |
|---|---:|---|
| `/` | 200 | OK: HSTS, `X-Content-Type-Options`, `Referrer-Policy` en korte HTML-cache aanwezig. |
| `/examenstof/` | 200 | OK: HSTS, `X-Content-Type-Options`, `Referrer-Policy` en korte HTML-cache aanwezig. |
| `/sitemap-index.xml` | 200 | OK: XML-cache aanwezig. |
| `/_redirects` | 200 | Bestand is publiek leesbaar; functioneel onschadelijk op TransIP, maar niet nodig voor Apache. |
| `/.htaccess` | 403 | OK, niet publiek leesbaar. |
| `/wp-content/uploads/2016/12/Analyse-Maatschappelijk-Vraagstuk-212x300.png` | 200 | OK: lange immutable asset-cache aanwezig. |

De header-audit geeft nu 0 warning rows.

## 6. Legacy oefenmodules

De oude `uhe_style1` oefenmodules zijn omgezet naar statische linklijsten. Er wordt geen oude WordPress-plugin of runtime-code uitgevoerd.

| URL | Categorie | Status |
|---|---|---|
| `/examenstof/analyse-maatschappelijk-vraagstuk/` | `amv` | Statische oefenlinks aanwezig. |
| `/examenstof/criminaliteit-en-rechtsstaat/` | `criminaliteit` | Statische oefenlinks aanwezig. |
| `/examenstof/politiekenbeleid/` | `politiek` | Statische oefenlinks aanwezig. |

## 7. Aanbevolen vervolgstappen

1. Productiepad, DNS-route en rollbackroute bij TransIP bevestigen.
2. Productie-cutover uitvoeren volgens `docs/PRODUCTION_CUTOVER.md`.
3. Na productie-cutover dezelfde live redirect/header/smoke-audits opnieuw draaien op productie.
4. Inhoudelijk reviewen of algemene legacy archive-teksten voldoende zijn of per pagina specifieker moeten worden gemaakt.
