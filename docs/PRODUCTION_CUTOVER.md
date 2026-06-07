# Productie-cutover checklist - maatschappijkunde.nl

Deze checklist hoort bij de statische conversie van maatschappijkunde.nl. De site is eerst op dev gevalideerd; productie volgt pas na expliciete keuze.

## Voorwaarden

- `npm test` is groen.
- `npm run build` is groen.
- Laatste dev-deploy is groen.
- Live redirect-audit is groen.
- Live header-audit is groen op dev.
- Live smoke-audit is groen op dev.
- Dev Basic Auth blijft actief; productie krijgt geen Basic Auth tenzij expliciet gewenst.

## Hosting en deploy

1. Bevestig het productiepad bij TransIP.
2. Bevestig of productie dezelfde `.htaccess`-redirects gebruikt als dev.
3. Deploy alleen de inhoud van `dist/`.
4. Publiceer geen brondata, SQL-export, scripts of ongeschoonde uploads.
5. Controleer dat `.htaccess` niet als tekst publiek leesbaar is.

## DNS

1. Noteer huidige DNS-records en TTL.
2. Verlaag TTL ruim voor cutover als dat nog niet is gedaan.
3. Zet productie-DNS pas om na groene smoke tests op het productiepad.
4. Bewaar de oude hostingroute tot rollback niet meer nodig is.

## Smoke tests direct na livegang

Controleer minimaal:

- `/`
- `/examenstof/`
- `/kerndoelen/`
- `/begrippen/`
- `/planning/`
- `/examenstof/amv-kerndoel1/`
- `/examenstof/criminaliteitenrechtsstaat-kerndoel1/`
- `/category/amv/`
- `/kerndoel-tags/leerjaar-3/`
- `/sitemap-index.xml`
- `/robots.txt` als die wordt toegevoegd

Controleer redirects:

- `/begrippen/tweede-kamer/`
- `/begrippen/parlement/`
- `/begrippen/reageerakkoord/`
- `/politiekenbeleid-kerndoel1-1/`
- `/amv-kerndoel1/`
- `/ciminaliteitenrechtsstaat-kerndoel1/`

## Headers en cache

Dev-audit heeft deze productie-aandachtspunten gevonden:

- Headers/cache zijn op dev getest via `.htaccess` en geven 0 live header-waarschuwingen.
- Controleer bij productie-cutover dat dezelfde Apache-configuratie actief is op het productiepad.

Aanbevolen productieheaders:

```apache
Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header set X-Content-Type-Options "nosniff"
Header set Referrer-Policy "strict-origin-when-cross-origin"
<FilesMatch "\\.(png|jpg|jpeg|gif|webp|svg|css|js|woff2?)$">
  Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
<FilesMatch "\\.(html|xml)$">
  Header set Cache-Control "public, max-age=300"
</FilesMatch>
```

Deze regels zijn op dev toegepast. Test na productie-cutover opnieuw met:

```bash
MK_LIVE_ORIGIN='https://maatschappijkunde.nl' npm run audit:live:headers
MK_LIVE_ORIGIN='https://maatschappijkunde.nl' npm run audit:live:redirects
MK_LIVE_ORIGIN='https://maatschappijkunde.nl' npm run audit:live:smoke
```

## Rollback

1. Laat oude productiehosting tijdelijk intact.
2. Bewaar laatste werkende deploy-artifact of commit SHA.
3. Rollbackroute:
   - DNS terugzetten naar oude hosting, of
   - vorige `dist/` terugdeployen, afhankelijk van de gekozen cutover.
4. Controleer na rollback minimaal homepage, examenstof, begrippenredirects en sitemap.

## Na livegang

1. Controleer serverlogs op 404's.
2. Controleer Search Console zodra beschikbaar.
3. Controleer analytics op onverwachte daling of redirectproblemen.
4. Plan pas daarna redesign- of templateverbeteringen.

## Huidige cutoverstatus

- Dev is technisch groen voor cutover.
- Productie-cutover is nog niet uitgevoerd vanuit deze workspace.
- Nog extern te bevestigen: productiepad, DNS-route, TTL en rollbackroute bij TransIP.
