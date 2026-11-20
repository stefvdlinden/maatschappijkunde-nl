# I4: oude paden en templatepagina's, voorstel per URL

Datum: 20 november 2026. Status: **I4.1–I4.6 doorgevoerd op 20 november 2026** (akkoord van de eigenaar). De vier pagina's zijn verwijderd uit `pages.json` en geven nu een 301 naar `/examenstof/`; `/examenstof/` linkt nu naar de drie overzichten (kaart per onderwerp, badge "Overzicht"). Live status gemeten op 20 november.

## A. Pagina's die bestaan en in de sitemap staan

| # | URL | Wat het is | Inkomende links | Voorstel | Reden |
|---|---|---|---|---|---|
| I4.1 | `/contact-support/` | Engelse WordPress-template ("This is an example page where your customers could reach out to support"), daaronder een navigatielijst. Staat in sitemap. | 0 | **301 naar `/examenstof/`** en uit sitemap | Geen eigen inhoud, Engelstalig voorbeeld. `/contact/` bestaat niet, dus de examenstofpagina is de dichtstbijzijnde bruikbare bestemming. Alternatief: 410. |
| I4.2 | `/examenstof-2/` | "Knowledge Base Archive", 517 tekens, alleen een lijst met kerndoel-overzichten. | 0 | **301 naar `/examenstof/`** | Dubbel met `/examenstof/`, dat dezelfde kerndoelen beter ontsluit. |
| I4.3 | `/category/featured/` | "Featured Category", lijst met uitgelichte links. Is al uit de navigatie gehaald. | Alleen vanuit het archief | **301 naar `/examenstof/`**, maar pas na I4.6 (zie onder) | Deze pagina is nu de enige bron voor twee van de drie examenstofoverzichten. |
| I4.4 | `/leerjaar-3-versneld/` | Planning uit 2017 voor klas X11 media en vormgeving (data 2017). | 0 | **301 naar `/examenstof/`**, consistent met de bestaande redirects van `/planning/…` | Verouderd, klasspecifiek, geen waarde voor nieuwe bezoekers. Alternatief: laten staan met `noindex`. |

## B. Oude paden die al een 404 geven

| # | URL | Live | Voorstel |
|---|---|---|---|
| I4.5 | `/vraag/verzorgingsstaat/`, `/vraag/downloads/`, `/featured/politiekenbeleid/`, `/glossary-categories/criminaliteitenrechtsstaat/`, `/examenstof/politiekenbeleid-` | 404 | **Laten staan als 404.** Geen inhoud meer in de site-data en geen bewezen vervanger. Een redirect naar de homepage of examenstof zou Google een soft-404 geven. Het laatste pad is een afgebroken URL. |

## C. Zwakke interne routering

| # | Pagina's | Probleem | Voorstel |
|---|---|---|---|
| I4.6 | `/examenstof/criminaliteit-en-rechtsstaat/`, `/examenstof/mens-en-werk/`, `/examenstof/politiekenbeleid/` | Werden alleen gelinkt vanaf `/category/featured/` en `/contact-support/`. Zonder die twee pagina's zijn het weesjes. | **Eerst een link toevoegen op `/examenstof/`** (dat linkt nu alleen naar de losse kerndoelpagina's, niet naar deze overzichten) en eventueel op de drie `/kerndoelen/…`-overzichten, daarna pas I4.1 en I4.3 doorvoeren. Alternatief: deze drie ook als duplicaat van hun kerndoelenpagina beschouwen en een canonical zetten (eerst inhoud vergelijken). |

## Volgorde bij akkoord

1. I4.6: links toevoegen.
2. I4.1, I4.2, I4.3, I4.4: redirects in `lib/seo-redirects.js` en uit de sitemap.
3. Tests, push, live controle van redirects en sitemap.
