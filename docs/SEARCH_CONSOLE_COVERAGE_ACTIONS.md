# Search Console coverage acties

Datum: 2026-07-10

## Waarschijnlijk opgelost door technische productie-fixes

- Verwijzingen naar de oude dev-host zijn uit bronbestanden, live-audits en gegenereerde live-rapporten verwijderd.
- Astro gebruikt `https://maatschappijkunde.nl` als site-origin.
- Canonical URL's en sitemap-URL's worden in de build en postbuild op `https://maatschappijkunde.nl` gezet.
- `robots.txt` verwijst na de postbuild naar `https://maatschappijkunde.nl/sitemap.xml`.
- Cloudflare `_headers` wordt gegenereerd met HSTS en `X-Content-Type-Options`.
- `.htaccess` wordt niet meer naar `public` of `dist` gekopieerd.
- Legacy interne URLs krijgen forced Cloudflare redirects, zodat bestaande statische bestanden de redirect niet overschrijven.

## Normale of verwachte Search Console meldingen

- `Pagina met omleiding` is normaal voor oude URLs die bewust met 301 naar de nieuwe URL of naar Schoolwoorden.nl verwijzen.
- `Alternatieve pagina met correcte canonieke tag` kan normaal zijn wanneer Google dezelfde inhoud via een variant kent en de canonical naar de productie-URL wijst.
- Individuele begrippen-URLs die naar Schoolwoorden.nl redirecten horen niet als indexeerbare maatschappijkunde.nl-pagina te eindigen.

## Handmatig op URL-niveau uit Search Console exporteren

Deze groepen moeten na deploy opnieuw uit Search Console worden bekeken, omdat de exacte URLs in de samenvatting ontbreken:

- `Serverfout (5xx)` - exporteer alle 4 URLs en controleer of ze na deploy nog 5xx geven.
- `Niet gevonden (404)` - exporteer alle 7 URLs en bepaal per URL of een 301 redirect nodig is of dat 404 terecht is.
- `Geblokkeerd wegens ongeautoriseerd verzoek (401)` - exporteer de 62 URLs als dit na productie-deploy blijft bestaan; 401 hoort niet op de publieke productie-origin.
- `Dubbele pagina zonder door gebruiker geselecteerde canonieke versie` - exporteer de 4 URLs en controleer canonical tags.
- `Gecrawld - momenteel niet geïndexeerd` en `Gevonden - momenteel niet geïndexeerd` - hercontroleer na sitemap/canonical/deploy-validatie; dit kan ook normale Google-selectie zijn.
- `Uitgesloten door tag noindex` - exporteer de URL en controleer of noindex gewenst is.

## Na deploy valideren

1. Dien `https://maatschappijkunde.nl/sitemap.xml` opnieuw in of laat Google de bestaande sitemap opnieuw ophalen.
2. Start in Search Console validatie voor 401, 5xx, 404, canonicals en noindex.
3. Controleer live minimaal:
   - `https://maatschappijkunde.nl/examenstof/`
   - `https://maatschappijkunde.nl/begrippen/`
   - `https://maatschappijkunde.nl/downloads/`
   - `https://maatschappijkunde.nl/sitemap.xml`
   - `https://maatschappijkunde.nl/sitemap-index.xml`
4. Controleer de legacy redirects:
   - `/politiekenbeleid-kerndoel1-1/`
   - `/amv-kerndoel1/`
   - `/ciminaliteitenrechtsstaat-kerndoel1/`
