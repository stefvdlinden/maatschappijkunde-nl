# Refactor Cleanup Audit

Inventarisatie voor de cleanup na de WordPress-naar-Astro-migratie.

## 1. Veilig verwijderen

- `.DS_Store` en `data/.DS_Store`: lokale macOS-bestanden, al genegeerd door `.gitignore`.
- `data/site/live-*-audit.*` en `data/site/production-*-audit.*`: momentopnames van live-audits. De scripts blijven bestaan; actuele resultaten kunnen opnieuw worden gegenereerd.
- `data/site/.htaccess`: gegenereerd Apache-tussenbestand uit de eerdere TransIP-fase. De site draait nu op Cloudflare Pages; `_redirects` en `_headers` zijn de runtime-artefacten.
- `docs/DEV_QA_REPORT.md`, `docs/PRODUCTION_CUTOVER.md`, `docs/CUTOVER_EXECUTION_REPORT.md` en `docs/CODEX_NEXT_TASK.md`: historische cutover/dev-documenten zonder blijvende operationele waarde.

## 2. Veilig hernoemen/refactoren

- CSS/HTML-klassen:
  - `legacy-content` -> `article-content`
  - `legacy-module-list` -> `module-list`
  - `wp-row` -> `content-row`
  - `wp-column` -> `content-column`
  - `wp-column-text` -> `content-column-text`
  - `shortcode-panel` -> `content-panel`
- `clean_empty_legacy_wrappers` kan neutraal worden hernoemd naar `clean_empty_content_wrappers`.
- De Astro sitemap-integratie overlapt met `scripts/postbuild-seo.mjs`. Postbuild kan de enige eigenaar blijven van `sitemap.xml`, `sitemap-index.xml`, `robots.txt`, `dist/_redirects` en `dist/_headers`.

## 3. Bewust behouden voor compatibiliteit

- `public/wp-content/uploads/`: bewust legacy assetpad. Dit is geen actieve WordPress-installatie; het pad blijft bestaan omdat content, downloads, afbeeldingen, Google en externe links deze URL's kunnen kennen.
- `data/source/maatsk_nkhniy67.sql`, `data/source/uploads.zip` en `data/source/htaccess.txt`: bronmateriaal voor reproduceerbare migratie en inventarisatie.
- WordPress- en shortcode-termen in `scripts/inventory.py` en `scripts/build_static_content.py`: nodig voor de contentconversie vanuit SQL, niet voor runtime.
- Redirects vanaf WordPress-achtige paden zoals `/wp-sitemap.xml`: bewust SEO-compatibel.
- `functions/_middleware.js`: Cloudflare runtimeconfiguratie, geen WordPress-runtime.

## 4. Nader beoordelen

- Auditrapporten in `data/site/*-audit.*`: lokale test-audits zijn reproduceerbaar. Alleen blijvende projectstatus hoort in `docs/`.
- Oude migratiedocumenten in de root, zoals `PROJECT_BRIEF.md`, zijn historisch maar kunnen nuttig blijven als projectcontext.
- Functie- en variabelenamen met `legacy` in migratiescripts kunnen later verder worden geneutraliseerd, zolang duidelijk blijft dat ze broncompatibiliteit modelleren.

## Generator-eigenaarschap

- Contentvoorbereiding: `npm run prepare:content`
  - `scripts/extract_safe_media.py`: schrijft veilige assets naar `public/wp-content/uploads/` en media-auditdata naar `data/site/`.
  - `scripts/build_static_content.py`: schrijft `pages.json`, `redirects.json`, `_redirects` en `_headers`.
- Buildfase: `astro build`
  - bouwt statische HTML en kopieert publieke assets.
- Postbuildfase: `scripts/postbuild-seo.mjs`
  - schrijft de definitieve productievarianten van `sitemap.xml`, `sitemap-index.xml`, `robots.txt`, `dist/_redirects` en `dist/_headers`.

## Baseline voor wijziging

- `data/site/pages.json`: 106 contentpagina's.
- `data/site/redirects.json`: 246 redirects.
- `dist/sitemap.xml`: 106 URL's.
- `data/site/safe-media.csv`: 1.295 veilige media-assets.
- Geen merge-conflictmarkers gevonden met line-start scan op `<<<<<<<`, `=======` en `>>>>>>>`.
- Geen oude dev-host in bronbestanden gevonden.
