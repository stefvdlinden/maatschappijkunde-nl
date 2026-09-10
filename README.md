# Maatschappijkunde.nl

Statische Astro-site met bestaande lesstof, gebouwd uit een WordPress-export en gepubliceerd via Cloudflare Pages.

## Projectdocumentatie

- [Werklijst](docs/WORKLIST.md): actuele status, controles en open acties.
- [Projectafspraken](PROJECT_BRIEF.md): doelgroep, inhoud, eigenaarschap en URL-beleid.
- [Search Console](docs/SEARCH_CONSOLE_COVERAGE_ACTIONS.md): beoordeling van de indexeringsmeldingen.
- [Broninventarisatie](docs/INVENTORY_REPORT.md): historische uitgangssituatie vóór de migratie.
- [Cleanup-audit](docs/REFACTOR_CLEANUP_AUDIT.md): historische refactorinventarisatie.

## Ontwikkelen en controleren

Getest met Node.js 20.20.2, npm 10.8.2 en Python 3.

```bash
npm ci
npm test
npm run build
npm run audit:sitemap-urls
npm run dev
```

`npm test` bereidt content voor en controleert URL-dekking, redirects, de Pages-middleware, media, HTML-conversie, inhoud, interne links en repositoryhygiëne. De build schrijft `dist/`.

Na publicatie:

```bash
npm run audit:live:smoke
npm run audit:live:redirects
npm run audit:live:headers
```

De live-audits gebruiken standaard de productie-origin. Stel `MK_LIVE_ORIGIN` in voor een preview. Lokale live-rapporten staan in `data/site/live-*-audit.*` en zijn genegeerd door Git.

## Git en hosting

Repository: [stefvdlinden/maatschappijkunde-nl](https://github.com/stefvdlinden/maatschappijkunde-nl). Productie: [maatschappijkunde.nl](https://maatschappijkunde.nl).

De `main`-branch is gekoppeld aan Cloudflare Pages. Een push start een deployment; controleer de GitHub-check **Cloudflare Pages** en voer daarna de live-audits uit. Er zijn momenteel geen actieve GitHub Actions-workflows. Historische TransIP-runs horen bij de vorige hostingopzet.

## Bronnen en gegenereerde bestanden

- `data/source/maatsk_nkhniy67.sql` en `data/source/uploads.zip` zijn alleen lokaal beschikbaar en bewust uitgesloten van Git.
- `scripts/inventory.py` maakt de oorspronkelijke inventarisatie in `data/generated/`; opnieuw uitvoeren is alleen nodig bij gewijzigde brondata.
- `scripts/extract_safe_media.py` extraheert toegestane media naar `public/wp-content/uploads/`.
- `scripts/build_static_content.py` genereert onder andere `data/site/pages.json`, `redirects.json`, `_redirects` en `_headers`.
- Zonder SQL/ZIP gebruikt de build de bijgehouden site-data en publieke media. Daarom moeten wijzigingen aan de generator samen met de opnieuw gegenereerde output worden vastgelegd.
- `src/pages/[...slug].astro` publiceert de contentpagina's; `src/layouts/BaseLayout.astro` verzorgt de gedeelde vormgeving en metadata.
- `scripts/postbuild-seo.mjs` schrijft de definitieve sitemap, robots.txt, redirects en headers in `dist/`.

## Redirects

`functions/_middleware.js` gebruikt de handler uit `lib/redirect-middleware.js` en voert de regels uit `data/site/redirects.json` uit, inclusief varianten zonder eindslash. De SEO-regels uit `lib/seo-redirects.js` worden gedeeld met de postbuild. Feeds verwijzen naar hun bovenliggende pagina; `www` verwijst naar HTTPS zonder `www`. Queryparameters blijven behouden.

Dit is noodzakelijk omdat Cloudflare `_redirects` niet toepast op requests die door Pages Functions worden afgehandeld. Het bestand `/_redirects` hoort zelf niet publiek bereikbaar te zijn. Zie de [Cloudflare-documentatie](https://developers.cloudflare.com/pages/configuration/redirects/).

Bestaande Schoolwoorden-redirects blijven behouden. Het compatibiliteitspad `/wp-content/uploads/` bevat statische media en is geen actieve WordPress-installatie.

## Gecontroleerde lokale status — 10 september 2026

- 106 contentpagina's; daarnaast een echte 404-pagina.
- 264 migratieredirects, plus gedeelde SEO-regels.
- 1.295 veilige media-assets en 59 gecontroleerde uploadverwijzingen, niets ontbreekt.
- 776 interne links, niets ontbreekt.
- Geen onopgeloste shortcodes, conversiefouten of ongedekte inventaris-URL's.
- Vier lichte inhoudssignalen: korte maar functionele kerndoeloverzichten met links naar de lesstof; beoordeeld en behouden.
- De sitemap sluit `/home/` uit omdat dit pad naar `/` redirectt: 105 indexeerbare URL's.
