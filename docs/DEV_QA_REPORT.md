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

`https://dev.maatschappijkunde.nl/` reageert met `401` en Basic Auth realm `omzetten hosting`. Daardoor is publieke visuele controle op de dev-URL zonder credentials niet mogelijk. De deploy zelf is wel succesvol afgerond.

Recente runs na de concurrency-wijziging:

| Run | Commit | Status |
|---|---|---|
| `27069922947` | `Prevent parallel dev deployments` | success |
| `27069783606` | `Audit redirect integrity` | success |
| `27069711100` | `Audit external references` | success |

## 2. Kernpagina QA

Gecontroleerd op basis van de gegenereerde statische build en `data/site/pages.json`.

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
