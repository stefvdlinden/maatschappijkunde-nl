# Dev QA rapport - maatschappijkunde.nl

Datum: 2026-06-06

## 1. Dev-deploy

Laatste GitHub Actions run:

- Run: `27069922947`
- Commit: `e028878 Prevent parallel dev deployments`
- Workflow: `Deploy dev site to TransIP`
- Status: success
- Build: success
- Deploy via SFTP: success
- Duur: 15m 6s

`https://dev.maatschappijkunde.nl/` reageert met Basic Auth realm `omzetten hosting`. Met credentials is de live dev-site bereikbaar.

Recente runs na de concurrency-wijziging:

| Run | Commit | Status |
|---|---|---|
| `27069922947` | `Prevent parallel dev deployments` | success |
| `27069783606` | `Audit redirect integrity` | success |
| `27069711100` | `Audit external references` | success |

## 2. Kernpagina QA

Gecontroleerd op basis van de gegenereerde statische build, `data/site/pages.json` en live dev met Basic Auth.

| URL | Bevinding |
|---|---|
| `/` | Pagina aanwezig, geen ruwe shortcodes of handmatige code-notices. |
| `/examenstof/` | Pagina aanwezig; oude zoekmodule is veilig verwijderd uit output. |
| `/examenstof/amv-kerndoel1/` | Content aanwezig, 2 embeds, geen conversie-issues. |
| `/examenstof/criminaliteitenrechtsstaat-kerndoel1/` | Content aanwezig, 10 embeds, geen conversie-issues. |
| `/kerndoelen/politiekenbeleid/` | Taxonomie-overzicht aanwezig en gevuld. |
| `/planning/` | 4 tabellen aanwezig en gevuld. |
| `/planning/leerjaar3/` | 4 tabellen aanwezig en gevuld. |
| `/planning/leerjaar4/` | 1 tabel aanwezig en gevuld. |
| `/begrippen/` | Overzichtspagina aanwezig; individuele begrippen blijven redirects. |

Live dev statuschecks:

| URL | Status |
|---|---:|
| `/` | 200 |
| `/examenstof/` | 200 |
| `/examenstof/amv-kerndoel1/` | 200 |
| `/examenstof/criminaliteitenrechtsstaat-kerndoel1/` | 200 |
| `/kerndoelen/politiekenbeleid/` | 200 |
| `/planning/` | 200 |
| `/planning/leerjaar3/` | 200 |
| `/planning/leerjaar4/` | 200 |
| `/begrippen/` | 200 |

Live redirectbevinding:

- `https://dev.maatschappijkunde.nl/_redirects` is live bereikbaar met status `200`, maar Netlify-style `_redirects` wordt niet door TransIP/nginx toegepast.
- Er wordt daarom ook een Apache `.htaccess` gegenereerd en gedeployed.
- `/begrippen/tweede-kamer/` geeft nu `301` naar `https://schoolwoorden.nl/begrip/tweede-kamer/`.
- `/begrippen/parlement/` volgt door naar `https://schoolwoorden.nl/begrip/parlement`.
- `/begrippen/reageerakkoord/` geeft `301` naar `https://schoolwoorden.nl/begrip/regeerakkoord/`.
- `https://dev.maatschappijkunde.nl/.htaccess` geeft `403`, dus het bestand wordt niet publiek als tekst geserveerd.

Automatische audits blijven groen:

- URL coverage: 110 pagina's, 239 redirects
- Redirect audit: 239 redirects, 0 issues
- Asset audit: 0 missing assets
- HTML conversion audit: 0 issues
- Internal link audit: 295 links, 0 missing
- External reference audit: 0 issues
- URL gap report: 0 investigate URLs

## 3. Legacy oefenmodules

Er zijn drie oude `uhe_style1` oefenmodules gevonden. Deze zijn veilig als legacy-placeholder gemarkeerd en worden niet als plugin/runtime-code uitgevoerd.

| URL | Categorie | Beoordeling |
|---|---|---|
| `/examenstof/analyse-maatschappelijk-vraagstuk/` | `amv` | Later vervangen door statische oefenlinks of archiefmelding. |
| `/examenstof/criminaliteit-en-rechtsstaat/` | `criminaliteit` | Later vervangen door statische oefenlinks of archiefmelding. |
| `/examenstof/politiekenbeleid/` | `politiek` | Later vervangen door statische oefenlinks of archiefmelding. |

Aanbevolen vervolg: bepaal per legacy oefenmodule of er nog bruikbare oefenvragen/formulieren zijn. Zo ja: statisch opnemen als gewone links/content. Zo nee: markeren als verouderd of verwijderen na expliciete contentkeuze.

## Redirectoplossing

Redirects zijn server-side werkend gemaakt voor TransIP door naast `_redirects` ook `.htaccess` te genereren uit `data/site/redirects.json`.
