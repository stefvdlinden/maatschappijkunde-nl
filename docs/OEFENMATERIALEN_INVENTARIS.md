# Oefenvragen en externe lesmaterialen: inventaris (taak I2)

Datum: 19 november 2026. Methode: alle `iframe`- en formulierlinks uit `data/site/pages.json` verzameld en per bestemming met een gewone GET-aanvraag opgehaald. Er is niets ingevuld of verzonden. Gecontroleerd is alleen bereikbaarheid en titel/structuur; de inhoud van de dia's is niet beoordeeld.

Omvang: 29 unieke Google Presentaties (op ~45 pagina's, vaak met meerdere dia-startpunten) en 1 Google Formulier.

## Bevindingen

| # | Onderdeel | Pagina's | Bevinding | Status |
|---|---|---|---|---|
| 1 | Google Formulier "Politiek en Beleid: Kerndoel 3" | `/examenstof/politiekenbeleid-kerndoel3/` | Bereikbaar. Verplichte velden **Naam** en **Wachtwoord**, daarna een verplichte keuze "Welke versie wil je maken? Versie A". Vragen 1–10 zijn niet verplicht. Het formulier staat dus niet op kerndoel 1.1 (zoals vermeld in de aanvullende lijst) maar op kerndoel 3. Het "Wachtwoord"-veld is onduidelijk voor leerlingen. Of de labels "Jennifer"/"x11" ergens anders vandaan komen is niet gevonden. Er is geen antwoordfeedback of score zichtbaar zonder inzending te doen. | **Herstellen** na overleg met beheerder |
| 2 | Presentatie `1QXp1TIEyLK7…` | Mens en Werk kerndoel 5 en 6 (twee pagina's, drie embeds) | **HTTP 403**: niet openbaar of verwijderd. Leerlingen zien een geblokkeerde dia. | **Herstellen** (deelinstelling of vervangen) |
| 3 | Presentatie `1DlW_-Pr4kUa…` | Multiculturele samenleving kerndoel 4 (+ `/ml2-k-6-4-culturele-differentiatie/`) | Bereikbaar, maar de titel van de presentatie is **"Verwijderd"**. Controleer of de inhoud nog klopt. | **Controleren** |
| 4 | Presentatie `1WOWsjtGTijg…` | Politiek en Beleid kerndoel 5 | Titel **"engels liedje"**: lijkt een verkeerde presentatie. | **Controleren, waarschijnlijk vervangen** |
| 5 | Presentatie `1kGq1apM0Vi1…` | Politiek en Beleid kerndoel 3 | Titel **"Interculturele communicatie"**: past niet bij het onderwerp. | **Controleren** |
| 6 | Presentatie `1QTmu5_LYOHV…` | Criminaliteit en Rechtsstaat kerndoel 5 | Titel **"Naamloze presentatie"**. Inhoud controleren. | Controleren |
| 7 | Presentatie `14LfemDfGahK…` | Criminaliteit en Rechtsstaat kerndoel 1 | Titel **"Stelling nl"**: lijkt niet de kerndoel-1-presentatie. | Controleren |
| 8 | Presentatie `1OcjlGw1M8fY…` | Politiek en Beleid kerndoel 1.1 | Titel "Democratie, Rechtsstaat". Bereikbaar; steekproef eerder werkte. | Werkt |
| 9 | Overige 22 presentaties | zie hieronder | HTTP 200, titel past bij het onderwerp. | Werkt (inhoud niet beoordeeld) |

Werkend en passend: AMV kerndoel 1, 2 en 3 (twee decks), Massamedia kerndoel 2 en 3, Criminaliteit en Rechtsstaat kerndoel 2, 3 en 4, Mens en Werk kerndoel 1–4 en 6 (kerndoel 6 zelf, `13zJK2nG…`), Multiculturele samenleving kerndoel 1, 2, 3 en 5, Politiek en Beleid kerndoel 1.2, 1.3, 1.4, 2 en 4.

Opmerking: Mens en Werk kerndoel 6 gebruikt naast zijn eigen presentatie ook twee dia's uit de 403-presentatie van kerndoel 5.

## Niet gecontroleerd

- Of leerlingen zonder Google-account de presentaties zien (alleen anoniem opgehaald: 200 betekent wel openbaar bereikbaar).
- Of de dia's inhoudelijk aansluiten op de lesstof, en of oefenvragen antwoordfeedback hebben. Dat vereist een lees- en vergelijkronde per kerndoel, en hoort bij I1.
- Scores/feedback van het formulier: dat vraagt een testinzending. Doe dit alleen met een bewust testdoel en bij voorkeur nadat de beheerder is geraadpleegd.
- Andere externe lesmaterialen dan Google (YouTube, quiz-sites): de zoekactie had geen treffers, maar de lijst trefwoorden is niet uitputtend.

## Vervolgacties

1. **Jij**: vaststellen wie eigenaar is van het formulier en de 403-presentatie (waarschijnlijk jouw eigen Google-account of dat van een oud collega-account).
2. Na akkoord: voor de 403-presentatie een nieuw openbaar deelbare kopie of vervanging aanwijzen en de embed vervangen.
3. Verkeerde presentaties (4, 5, 7) per pagina aanwijzen; ik zoek de juiste ID's niet zelf: de correcte presentatie moet jij aanleveren.

## Hercontrole en voorstel (22 november 2026)

### I2: oefenvragen en externe materialen

- De presentatie `1QXp1TIEyLK7sV8jfVoHiX_xjlmCccuyK_q88wcR5Td0` (Mens en Werk kerndoel 5 en 6) geeft nog steeds **HTTP 403**. Een controlevoorbeeld, de AMV-presentatie, geeft 200.
- Herstel vraagt de eigenaar van het Google-account. Zonder toegang kan ik de deelinstelling niet wijzigen. Voorstel: deel de presentatie met "iedereen met de link" of maak een nieuwe kopie en geef me het nieuwe id; ik vervang dan de drie embeds.
- Het formulier "Politiek en Beleid: Kerndoel 3" blijft een besluit voor de eigenaar: verplichte velden Naam en Wachtwoord horen niet bij een oefenformulier. Voorstel: velden niet-verplicht maken, "Wachtwoord" schrappen of het formulier vervangen door een link naar de oefenvragen op de pagina zelf.
- Niets is ingevuld of gewijzigd.

### I3: downloads

- Alle 14 downloadlinks op `/downloads/` geven live HTTP 200 (13 bestanden plus het schema van de parlementaire democratie).
- Inhoudelijk zijn de PDF's momentopnamen uit 2016 tot 2020 en lopen ze achter op de webpagina's:
  - Mens en Werk (2016 en 2018), Multiculturele samenleving (2016 en 2018): bevatten "allochtonen" (4, 33) en "niet-westers" (3, 15), de oude terminologie.
  - Politiek en Beleid (2018): noemt 2015 en 2016 als recente jaren.
  - Checklists "Check CSE Maatschappijleer 2017" en "Checklist CSE Maatschappijkunde 2018": titels verwijzen naar een oud examenjaar.
- Er zijn dubbele versies per thema (Mens en Werk, Multiculturele samenleving, Analyse maatschappelijk vraagstuk, Criminaliteit en Rechtsstaat, Massamedia): de oudere en de nieuwere staan allebei op de pagina.
- Voorstel, op akkoord: (1) de oudere duplicaten van de downloadpagina halen en de 2016-bestanden laten staan voor bestaande links; (2) boven de lijst een zin "Deze leerteksten zijn momentopnamen; de webpagina's zijn actueler"; (3) de leerteksten opnieuw genereren kan alleen met de bronbestanden, die ik niet heb.

### Besluiten van 23 november 2026

- **403-presentatie:** embeds verwijderd (5 op Mens en Werk kerndoel 5 en 6).
- **Formulier Politiek en Beleid kerndoel 3:** blok met formulierlink verwijderd (4 keer op de pagina).
- **Downloads:** alle leerteksten van `/downloads/` gehaald; schema en checklists blijven.
- **Aanvulling na review:** de inventaris telde alleen `docs.google.com/forms`-links. Daarnaast staan er 5 verschillende `goo.gl/forms/...`-links (30 vermeldingen op Politiek en beleid 1.1 t/m 1.4 en kerndoel 2). Ze geven alle vijf live HTTP 200 en wijzen naar werkende Google Formulieren. Ze zijn niet verwijderd: het besluit van 23 november ging over het formulier met de verplichte velden Naam en Wachtwoord.
