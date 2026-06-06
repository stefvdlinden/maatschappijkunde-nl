# Eerste taak voor Codex

Analyseer dit repo als voorbereiding op een statische herbouw van maatschappijkunde.nl.

## Context
Lees eerst:

1. `PROJECT_BRIEF.md`
2. `docs/INVENTORY_REPORT.md`
3. `data/generated/summary.json`
4. `data/generated/url-inventory.csv`
5. `data/generated/shortcode-counts.csv`

## Taak
Maak nog geen redesign en verwijder geen content. Bouw eerst een eerste statische conversiepijplijn.

## Gewenste output

1. Kies een eenvoudige statische architectuur, bij voorkeur Astro.
2. Maak een extractor die publieke content uit `data/generated/content-inventory.json` kan gebruiken als bron.
3. Maak contentcollecties voor:
   - pagina's;
   - examenstof / kennisbankartikelen;
   - begrippen of redirectregels voor begrippen;
   - kerndoel/taxonomie-overzichten indien haalbaar.
4. Maak conversieregels voor de meest voorkomende shortcodes:
   - `gt_table`, `gt_table_heading`, `gt_table_body`, `gt_table_data` -> HTML table;
   - `icon` -> verwijderen of decoratief span-element;
   - `vc_row`, `vc_column`, `vc_column_text` -> neutrale HTML containers;
   - `toggle`, `gt_tab`, `vc_tta_tabs` -> later behandelen, voorlopig semantisch en leesbaar houden;
   - `fusion_code` -> onderzoeken, niet blind renderen.
5. Maak een eerste statische build met behoud van URL's.
6. Maak een redirectbestand op basis van `data/generated/redirects.csv`.
7. Voeg een test toe die controleert dat top-analytics-URL's, sitemap-URL's en redirects niet onbedoeld verdwijnen.

## Harde grenzen

- Geen bestaande URL wijzigen zonder redirect.
- Geen pagina's verwijderen.
- Geen commerciële verwijzingen toevoegen.
- Geen uploads.zip ongeschoond publiceren.
- Geen PHP-bestanden uit uploads deployen.
