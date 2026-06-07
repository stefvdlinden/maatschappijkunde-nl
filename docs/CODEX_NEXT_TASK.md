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
- Laatste afgeronde dev-deploy voor deze notitie: run `27089769954`, commit `058fc66 Test production headers on dev`.
- Live redirect-audit op dev: 6 checks, 0 issues.
- Live header-audit op dev: 6 checks, 0 waarschuwingen.
- Live smoke-audit op dev: 16 checks, 0 issues.
- Productie-cutover is nog niet uitgevoerd vanuit deze workspace: productiepad en rollbackroute moeten extern bij TransIP bevestigd worden.
- Laatste cutover-uitvoeringspoging: zie `docs/CUTOVER_EXECUTION_REPORT.md`.

## Harde grenzen

- Bouw nog geen redesign.
- Wijzig geen bestaande URL zonder redirect.
- Verwijder geen content zonder expliciete keuze.
- Publiceer geen ongeschoonde WordPress uploads.
- Deploy geen PHP-bestanden uit uploads.
- Houd dev Basic Auth actief tot productie-cutover expliciet wordt voorbereid.

## Eerstvolgende activiteiten

1. Bevestig bij TransIP welk SFTP-pad productie is en welk pad/route rollback is.
2. Voeg een expliciete productie-deployroute toe of bevestig dat de bestaande SFTP-secrets tijdelijk naar productie wijzen.
3. Voer productie-cutover uit volgens `docs/PRODUCTION_CUTOVER.md`.
4. Draai direct voor cutover nogmaals:
   - `npm test`
   - `npm run build`
   - `MK_DEV_AUTH='...' npm run audit:live:redirects`
   - `MK_DEV_AUTH='...' npm run audit:live:headers`
   - `MK_DEV_AUTH='...' npm run audit:live:smoke`
5. Na productie-cutover dezelfde live checks op productie uitvoeren met `MK_LIVE_ORIGIN=https://maatschappijkunde.nl`.
6. Daarna serverlogs/Search Console/analytics nalopen op 404's of redirectproblemen.

## Nuttige commando's

```bash
npm test
npm run build
MK_DEV_AUTH='user:password' npm run audit:live:redirects
MK_DEV_AUTH='user:password' npm run audit:live:headers
MK_DEV_AUTH='user:password' npm run audit:live:smoke
MK_LIVE_ORIGIN='https://maatschappijkunde.nl' npm run audit:live:smoke
gh run list --workflow deploy-dev.yml --limit 5
```

Live dev is afgeschermd met Basic Auth.
