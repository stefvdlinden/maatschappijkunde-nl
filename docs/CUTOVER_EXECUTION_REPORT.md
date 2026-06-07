# Cutover-uitvoeringsrapport - maatschappijkunde.nl

Datum: 2026-06-07

## Uitgevoerde activiteiten 1 t/m 5

| Activiteit | Status | Bevinding |
|---|---|---|
| 1. Productiepad, DNS-route en rollbackroute bevestigen | Deels uitgevoerd | DNS voor `maatschappijkunde.nl` en `dev.maatschappijkunde.nl` wijst naar `80.69.67.10`. GitHub bevat alleen generieke SFTP-secrets, geen aparte productie-workflow of aparte productie-secrets. Productiepad en rollbackroute zijn niet vanuit deze workspace te bevestigen. |
| 2. Productie-cutover uitvoeren | Geblokkeerd | Er is geen productie-workflow en het concrete productiepad/rollbackpad is niet bevestigd. Daarom is er geen productie-deploy of DNS-wijziging uitgevoerd. |
| 3. Directe preflight voor cutover | Uitgevoerd | `npm test`, `npm run build`, dev redirect-audit, dev header-audit en dev smoke-audit zijn groen. |
| 4. Productie-livechecks uitvoeren | Uitgevoerd als verificatie | Productie is nog niet gelijk aan dev: header-audit heeft 4 warning rows, redirect-audit heeft 1 issue, smoke-audit heeft 2 issues. |
| 5. Serverlogs/Search Console/analytics nalopen | Geblokkeerd | Deze databronnen zijn niet beschikbaar in de workspace. Productie-auditbestanden zijn wel vastgelegd als externe controle. |

## Preflightresultaat dev

- `npm test`: groen.
- `npm run build`: groen.
- Dev live redirect-audit: 6 checks, 0 issues.
- Dev live header-audit: 6 checks, 0 warnings.
- Dev live smoke-audit: 16 checks, 0 issues.

## Productieresultaat

Productie-origin: `https://maatschappijkunde.nl`

| Audit | Resultaat |
|---|---:|
| Productie header-audit | 6 checks, 4 warning rows |
| Productie redirect-audit | 6 checks, 1 issue |
| Productie smoke-audit | 16 checks, 2 issues |

Belangrijkste productieverschillen:

- `/sitemap-index.xml` geeft op productie `404`.
- `/_redirects` geeft op productie `404`.
- `/ciminaliteitenrechtsstaat-kerndoel1/` geeft op productie `404` in plaats van een redirect naar `/examenstof/criminaliteitenrechtsstaat-kerndoel1/`.
- Productie-HTML mist HSTS en `X-Content-Type-Options`.

De productie-auditoutput staat in:

- `data/site/production-header-audit.csv`
- `data/site/production-redirect-audit.csv`
- `data/site/production-smoke-audit.csv`

## Conclusie

Dev is klaar voor productie-cutover, maar de cutover zelf is niet veilig uitvoerbaar zonder bevestigd productiepad en rollbackroute. De huidige productiechecks tonen dat productie nog niet de statische dev-build serveert.
