# maatschappijkunde.nl - statische herbouw

## Doel
Maatschappijkunde.nl wordt omgezet van WordPress naar een snelle, statische website.

## Doelgroep
Primaire doelgroep: leerlingen.

## Positionering
De website blijft voorlopig zelfstandig. Geen commerciële funnel naar Methode M of NEO.

## Eigenaarschap
De site was oorspronkelijk van Wessel Peeters en is nu omgezet/beheerd door Stef van der Linden.

## Contentbeleid
- Bestaande teksten blijven in eerste instantie behouden.
- Niet herschrijven naar vmbo-niveau zonder expliciete keuze.
- Geen commerciële verwijzingen toevoegen zonder expliciete keuze.

## URL-beleid
- Oude URL's behouden waar mogelijk.
- Als een URL niet behouden kan worden, moet er een 301-redirect komen.
- Bestaande redirects uit `.htaccess` moeten worden meegenomen.

## SEO/AEO-beleid
- Eerst veilig migreren en bestaande structuur behouden.
- SEO/AEO-optimalisatie doen op basis van database, sitemap, redirects en analytics/Search Console.
- Pagina's niet verwijderen op basis van beperkte data; markeer zulke pagina's eerst als `mogelijk verwijderen / later beoordelen`.

## Bronnen
- `data/source/maatsk_nkhniy67.sql` - WordPress database-export.
- `data/source/uploads.zip` - WordPress uploads/media.
- `data/source/sitemap-data.txt` - bestaande sitemap-URL's.
- `data/source/htaccess.txt` - bestaande WordPress/serverregels en redirects.
- `data/source/analytics-pages.pdf` - beperkte GA4-export, periode 1 jan 2024 t/m 5 jun 2025.

## Niet doen zonder expliciete toestemming
- Content herschrijven.
- Pagina's verwijderen.
- URL's wijzigen zonder redirect.
- Begrippen opnieuw publiceren als ze bewust extern redirecten naar schoolwoorden.nl.
- Uploads-map ongeschoond publiceren, zeker niet met PHP-bestanden.
