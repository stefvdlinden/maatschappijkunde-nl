# Volgende taak voor Codex

De statische conversiepijplijn voor maatschappijkunde.nl staat lokaal, is gekoppeld aan GitHub en deployt naar `https://dev.maatschappijkunde.nl/`.

## Huidige status

- Architectuur: Astro static build.
- Bron: `data/generated/content-inventory.json` en SQL/taxonomiegegevens.
- Output: 110 statische pagina's en 239 redirects.
- Redirectbestanden: `_redirects` en `.htaccess`.
- Safe media: 1295 bestanden uit uploads, zonder PHP/pluginresten.
- Unresolved shortcodes: 0.
- Content fidelity audit: 0 issues.
- URL gap report: 0 investigate URLs.
- Laatste dev-deploy: `d3aee9e Link legacy archive overviews`, run `27087535473`, success.

## Harde grenzen

- Bouw nog geen redesign.
- Wijzig geen bestaande URL zonder redirect.
- Verwijder geen content zonder expliciete keuze.
- Publiceer geen ongeschoonde WordPress uploads.
- Deploy geen PHP-bestanden uit uploads.
- Houd dev Basic Auth actief tot productie-cutover expliciet wordt voorbereid.

## Eerstvolgende activiteiten

1. Voer visuele QA uit op desktop en mobiel voor de kernroutes:
   - `/`
   - `/examenstof/`
   - `/kerndoelen/`
   - `/begrippen/`
   - `/planning/`
   - `/examenstof/amv-kerndoel1/`
   - `/examenstof/criminaliteitenrechtsstaat-kerndoel1/`
   - `/category/amv/`
   - `/kerndoel-tags/leerjaar-3/`
2. Leg visuele QA-bevindingen vast in `docs/DEV_QA_REPORT.md`.
3. Controleer redirects live op dev voor een representatieve set begrippen en oude URL's.
4. Bereid productie-cutover voor:
   - hosting/doelpad bevestigen;
   - Basic Auth alleen op dev houden;
   - cacheheaders en sitemap controleren;
   - rollbackroute bepalen.
5. Los de GitHub Actions Node.js 20 warning op zodra de workflow naar Node 24 moet of kan.

## Nuttige commando's

```bash
npm test
npm run build
gh run list --workflow deploy-dev.yml --limit 5
```

Live dev is afgeschermd met Basic Auth.
