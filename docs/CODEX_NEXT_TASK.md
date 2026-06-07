# Volgende taak voor Codex

De statische conversiepijplijn voor maatschappijkunde.nl staat lokaal, is gekoppeld aan GitHub en deployt naar `https://dev.maatschappijkunde.nl/`.

## Huidige status

- Architectuur: Astro static build.
- Bron: `data/generated/content-inventory.json` en SQL/taxonomiegegevens.
- Output: 110 statische pagina's en 242 redirects.
- Redirectbestanden: `_redirects` en `.htaccess`.
- Safe media: 1295 bestanden uit uploads, zonder PHP/pluginresten.
- Unresolved shortcodes: 0.
- Content fidelity audit: 0 issues.
- URL gap report: 0 investigate URLs.
- Laatste afgeronde dev-deploy voor deze notitie: zie `docs/DEV_QA_REPORT.md`.

## Harde grenzen

- Bouw nog geen redesign.
- Wijzig geen bestaande URL zonder redirect.
- Verwijder geen content zonder expliciete keuze.
- Publiceer geen ongeschoonde WordPress uploads.
- Deploy geen PHP-bestanden uit uploads.
- Houd dev Basic Auth actief tot productie-cutover expliciet wordt voorbereid.

## Eerstvolgende activiteiten

1. Rerun live redirect-audit na deploy:
   - `MK_DEV_AUTH='...' npm run audit:live:redirects`
2. Rerun live header-audit:
   - `MK_DEV_AUTH='...' npm run audit:live:headers`
3. Werk `docs/DEV_QA_REPORT.md` bij met de nieuwste run-id en live redirect/header-uitkomst.
4. Bereid productie-cutover voor volgens `docs/PRODUCTION_CUTOVER.md`.
5. Test productieheaders eerst op dev of staging voordat ze op productie worden afgedwongen.

## Nuttige commando's

```bash
npm test
npm run build
MK_DEV_AUTH='user:password' npm run audit:live:redirects
MK_DEV_AUTH='user:password' npm run audit:live:headers
gh run list --workflow deploy-dev.yml --limit 5
```

Live dev is afgeschermd met Basic Auth.
