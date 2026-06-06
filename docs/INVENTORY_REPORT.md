# Inventarisatierapport - maatschappijkunde.nl

## Samenvatting

De huidige bronnen zijn voldoende om te starten met een statische herbouw. De eerste inventarisatie geeft dit beeld:

| Onderdeel | Aantal |
|---|---:|
| SQL-tabellen | 87 |
| Publieke content-items | 317 |
| Gepubliceerde pagina's | 18 |
| Gepubliceerde posts | 5 |
| Gepubliceerde `ht_kb` kennisbankartikelen | 55 |
| Gepubliceerde `glossary` begrippen | 239 |
| Attachments in database | 121 |
| Bestanden in uploads.zip | 3.084 |
| Bestaande redirects uit `.htaccess` | 239 |
| Sitemap-URL's | 100 |
| Analytics-URL's automatisch gelezen | 84 |
| Content-items met shortcodes | 70 |

## Belangrijke observaties

### 1. Examenstof lijkt vooral in `ht_kb` te zitten
De 55 gepubliceerde `ht_kb`-items zijn waarschijnlijk de kern van de examenstof. De sitemap gebruikt hiervoor URL's onder `/examenstof/.../`.

### 2. Begrippen zijn dubbel belangrijk
Er zijn 239 gepubliceerde `glossary`-items. Tegelijkertijd bevat `.htaccess` 239 redirects van `/begrippen/...` naar `schoolwoorden.nl`. Dit moet bewust worden ingericht:

- bestaande redirects behouden als ze bedoeld zijn;
- geen redirect overschrijven met een lokale statische pagina zonder keuze;
- analytics meenemen, want sommige begrippen krijgen nog verkeer.

### 3. Shortcodes zijn de grootste conversieklus
Veel content bevat WordPress/plugin-shortcodes. De belangrijkste gevonden shortcodes zijn:

| Shortcode | Aantal |
|---|---:|
| `gt_table_data` | 356 |
| `icon` | 240 |
| `one_fifth` | 44 |
| `ultimate_modal` | 36 |
| `vc_column_text` | 32 |
| `vc_column` | 26 |
| `vc_row` | 24 |
| `vc_tta_section` | 22 |
| `gt_table` | 22 |
| `gt_table_heading` | 22 |
| `gt_table_body` | 22 |
| `fusion_code` | 16 |

Conclusie: we moeten conversieregels maken voor tabellen, iconen, tabs/toggles/modals en Visual Composer/Avada-layoutshortcodes.

### 4. Uploads.zip mag niet ongeschoond live
De zip bevat naast afbeeldingen en PDF's ook PHP-bestanden, cache/pluginbestanden en andere WordPress-restanten. De 121 attachments uit de database lijken wel allemaal een origineel bestand in de uploads.zip te hebben. Voor deploy moet er een schone assets-map komen.

### 5. Analytics is nuttig, maar beperkt
De GA4-export loopt van 1 jan 2024 t/m 5 jun 2025. Top URL's zijn onder andere `/`, `/examenstof/amv-kerndoel1/`, `/kerndoelen/politiekenbeleid/`, `/examenstof/criminaliteitenrechtsstaat-kerndoel1/` en `/examenstof/criminaliteitenrechtsstat-kerndoel3/`.

Gebruik analytics nu als prioriteitssignaal, niet als harde basis om content te verwijderen.

## Aanbevolen migratieadvies

Werk met vier URL-categorieen:

1. `preserve as static page` - content bestaat en moet statisch worden opgebouwd.
2. `keep redirect` - bestaande redirect behouden.
3. `investigate - sitemap URL not matched to extracted content` - sitemap noemt URL maar extractie matcht niet direct.
4. `investigate - analytics URL not matched to extracted content` - analytics noemt URL maar extractie matcht niet direct.

Zie `data/generated/url-inventory.csv`.
