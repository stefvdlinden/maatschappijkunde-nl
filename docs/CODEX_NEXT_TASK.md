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
- Laatste afgeronde dev-deploy voor deze notitie: run `27089016118`, commit `54ef20f Prepare production QA checks`.
- Live redirect-audit op dev: 6 checks, 0 issues.
- Live header-audit op dev: 6 checks, 3 bekende waarschuwingen voor productieheaders/cache.

## Harde grenzen

- Bouw nog geen redesign.
- Wijzig geen bestaande URL zonder redirect.
- Verwijder geen content zonder expliciete keuze.
- Publiceer geen ongeschoonde WordPress uploads.
- Deploy geen PHP-bestanden uit uploads.
- Houd dev Basic Auth actief tot productie-cutover expliciet wordt voorbereid.

## Eerstvolgende activiteiten

1. Beslis of de productieheaders/cache-regels uit `docs/PRODUCTION_CUTOVER.md` op dev getest mogen worden.
2. Bereid productie-cutover voor volgens `docs/PRODUCTION_CUTOVER.md`.
3. Bevestig productiepad, DNS-route en rollbackroute bij TransIP.
4. Draai direct voor cutover nogmaals:
   - `npm test`
   - `npm run build`
   - `MK_DEV_AUTH='...' npm run audit:live:redirects`
   - `MK_DEV_AUTH='...' npm run audit:live:headers`
5. Na productie-cutover dezelfde redirect/header smoke tests op productie uitvoeren.

## Nuttige commando's

```bash
npm test
npm run build
MK_DEV_AUTH='user:password' npm run audit:live:redirects
MK_DEV_AUTH='user:password' npm run audit:live:headers
gh run list --workflow deploy-dev.yml --limit 5
```

Live dev is afgeschermd met Basic Auth.
