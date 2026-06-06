# maatschappijkunde-static

Codex-ready startpakket voor de statische herbouw van maatschappijkunde.nl.

## Eerste stap
Voer de inventarisatie uit:

```bash
python3 scripts/inventory.py
```

De resultaten verschijnen in `data/generated/`.

## Belangrijkste output
- `summary.json` - kernsamenvatting.
- `content-inventory.csv` - publieke pagina's, berichten, kennisbankartikelen en begrippen.
- `url-inventory.csv` - gecombineerde URL-lijst uit content, sitemap, redirects en analytics.
- `redirects.csv` - redirects uit `.htaccess`.
- `shortcode-report.csv` en `shortcode-counts.csv` - WordPress/plugin-shortcodes die geconverteerd moeten worden.
- `media-files.csv` en `db-attachments.csv` - media in uploads en database.
- `analytics-top-pages.csv` - top URL's uit de GA4 PDF voor zover automatisch leesbaar.

## Aanbevolen volgende fase
1. Kies framework: Astro heeft de voorkeur voor deze contentwebsite.
2. Maak content-extractor naar Markdown/JSON.
3. Maak templates voor pagina's, examenstof, kerndoelen en eventueel begrippen/redirects.
4. Bouw statische site.
5. Test URL's en redirects.
6. Optimaliseer SEO/AEO.

## Eerste statische conversiepijplijn

Deze repo bevat nu een minimale Astro-build zonder redesign. De build gebruikt de WordPress SQL-export en de gegenereerde inventaris als bron.

```bash
npm install
npm run prepare:content
npm test
npm run build
```

Belangrijke bestanden:

- `scripts/build_static_content.py` - haalt gepubliceerde content uit de SQL-export, converteert bekende shortcodes naar veilige HTML en schrijft `data/site/pages.json`.
- `scripts/extract_safe_media.py` - extraheert alleen veilige media uit jaar/maandmappen van `uploads.zip` naar `public/wp-content/uploads/`.
- `scripts/audit-static-migration.mjs` - controleert lokale uploadverwijzingen en onopgeloste shortcodes.
- `scripts/audit-converted-html.mjs` - controleert geconverteerde HTML op shortcode-resten, WordPress block-comments, lege embeds en PHP-verwijzingen.
- `scripts/audit-internal-links.mjs` - controleert interne links tegen gegenereerde pagina's en redirects.
- `scripts/report-url-gaps.mjs` - schrijft URL's met `investigate`-status naar `data/site/url-gaps.csv`.
- `data/site/redirects.json` en `public/_redirects` - redirects uit `data/generated/redirects.csv`.
- `data/site/safe-media.csv` - overzicht van veilig geëxtraheerde media.
- `data/site/asset-audit.csv` - controle van uploadverwijzingen in geconverteerde content.
- `data/site/html-conversion-audit.csv` - rapport met resterende conversiepunten.
- `data/site/internal-link-audit.csv` - rapport met interne links en status (`page`, `redirect`, `missing`).
- `data/site/url-gaps.csv` - sitemap/analytics-URL's die nog gematcht of als redirect ingericht moeten worden.
- `src/pages/[...slug].astro` - genereert alle statische URL's met behoud van paden.
- `scripts/test-url-coverage.mjs` - controleert dat preserve/redirect-URL's uit de inventaris afgedekt blijven.

Begrippenpagina's waarvoor een bestaande 301 naar schoolwoorden.nl bestaat, worden niet lokaal gepubliceerd. Die redirectregels krijgen voorrang.

Huidige status van de migratie-audit:

- 1.295 veilige mediafiles geëxtraheerd (`.png`, `.jpg`, `.jpeg`, `.pdf`).
- 31 uploadverwijzingen in geconverteerde content gecontroleerd, 0 ontbrekend.
- 0 onopgeloste shortcode-types in de huidige geconverteerde HTML.
- 211 interne links gecontroleerd, 0 ontbrekend.
- 6 medium conversiepunten over voor handmatige beoordeling van `fusion_code`-achtige ingesloten code, 0 high issues.
- 110 statische pagina's gegenereerd, inclusief kerndoel-, tag- en categorie-overzichten.
- 0 URL's hebben nog `investigate`-status na dekking van taxonomie-overzichten.

Bekende interne link-normalisaties:

- `/examenstof/kerndoel-1-2/` -> `/examenstof/politiekenbeleid-kerndoel1-2/`
- `/politiekenbeleid-kerndoel1-2/` -> `/examenstof/politiekenbeleid-kerndoel1-2/`
