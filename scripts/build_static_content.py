#!/usr/bin/env python3
import base64
import csv
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from inventory import get_columns, iter_insert_rows, clean_text, rel_url  # noqa: E402

SRC = ROOT / "data" / "source"
GENERATED = ROOT / "data" / "generated"
SITE = ROOT / "data" / "site"
PUBLIC = ROOT / "public"
SQL = SRC / "maatsk_nkhniy67.sql"
SCHOOLWOORDEN_SITEMAP = GENERATED / "schoolwoorden-sitemap.xml"

PUBLIC_TYPES = {"page", "post", "ht_kb", "glossary"}
TYPE_LABELS = {
    "page": "Pagina",
    "post": "Bericht",
    "ht_kb": "Examenstof",
    "glossary": "Begrip"
}
INTERNAL_URL_REWRITES = {
    "/examenstof/kerndoel-1-2/": "/examenstof/politiekenbeleid-kerndoel1-2/",
    "/politiekenbeleid-kerndoel1-1/": "/examenstof/politiekenbeleid-kerndoel1-1/",
    "/politiekenbeleid-kerndoel1-2/": "/examenstof/politiekenbeleid-kerndoel1-2/",
    "/politiekenbeleid-kerndoel1-3/": "/examenstof/politiekenbeleid-kerndoel1-3/",
    "/politiekenbeleid-kerndoel1-4/": "/examenstof/politiekenbeleid-kerndoel1-4/",
    "/politiekenbeleid-kerndoel2/": "/examenstof/politiekenbeleid-kerndoel2/",
    "/politiekenbeleid-kerndoel3/": "/examenstof/politiekenbeleid-kerndoel3/",
    "/politiekenbeleid-kerndoel4/": "/examenstof/politiekenbeleid-kerndoel4/",
    "/politiekenbeleid-kerndoel5/": "/examenstof/politiekenbeleid-kerndoel5/",
    "/amv-kerndoel1/": "/examenstof/amv-kerndoel1/",
    "/amv-kerndoel2/": "/examenstof/amv-kerndoel2/",
    "/amv-kerndoel3/": "/examenstof/amv-kerndoel3/",
    "/ciminaliteitenrechtsstaat-kerndoel1/": "/examenstof/criminaliteitenrechtsstaat-kerndoel1/",
    "/ciminaliteitenrechtsstaat-kerndoel2/": "/examenstof/criminaliteitenrechtsstaat-kerndoel2/",
    "/ciminaliteitenrechtsstaat-kerndoel3/": "/examenstof/criminaliteitenrechtsstat-kerndoel3/",
    "/criminaliteitenrechtsstaat-kerndoel4/": "/examenstof/criminaliteitenrechtsstaat-kerndoel4/",
    "/criminaliteitenrechtsstaat-kerndoel5/": "/examenstof/criminaliteitenrechtsstaat-kerndoel5/"
}
TAXONOMY_PREFIXES = {
    "ht_kb_category": "/kerndoelen/",
    "ht_kb_tag": "/kerndoel-tags/",
    "category": "/category/"
}
EXTRA_REDIRECTS = [
    {
        "line": "extra:legacy-examenstof",
        "status": "301",
        "source": "/politiekenbeleid-kerndoel1-1/",
        "target": "/examenstof/politiekenbeleid-kerndoel1-1/"
    },
    {
        "line": "extra:legacy-examenstof",
        "status": "301",
        "source": "/amv-kerndoel1/",
        "target": "/examenstof/amv-kerndoel1/"
    },
    {
        "line": "extra:legacy-examenstof",
        "status": "301",
        "source": "/ciminaliteitenrechtsstaat-kerndoel1/",
        "target": "/examenstof/criminaliteitenrechtsstaat-kerndoel1/"
    },
    {
        "line": "extra:removed-planning",
        "status": "301",
        "source": "/planning/",
        "target": "/examenstof/"
    },
    {
        "line": "extra:removed-planning",
        "status": "301",
        "source": "/planning/leerjaar3/",
        "target": "/examenstof/"
    },
    {
        "line": "extra:removed-planning",
        "status": "301",
        "source": "/planning/leerjaar4/",
        "target": "/examenstof/"
    }
]
LEGACY_MODULES = {}
TITLE_REWRITES = {
    ("1029", "???? Analyse Maatschappelijk Vraagstuk"): "Analyse Maatschappelijk Vraagstuk"
}
SCHOOLWOORDEN_CANONICAL_SLUGS = {
    "agenda-functie": "agendafunctie",
    "commentaar-functie": "commentaarfunctie",
    "controlerende-functie": "controle-of-waakhondfunctie",
    "europese-parlement": "europees-parlement",
    "immateriele-schade": "immateriele-gevolgen",
    "informerende-functie": "informatiefunctie",
    "materiele-schade": "materiele-gevolgen",
    "misdrijven": "misdrijf",
    "multi-step-flow-theorie": "multistepflowtheorie",
    "overtredingen": "overtreding",
    "terbeschikkingstelling-tbs": "tbs",
    "theorie-van-selectieve-perceptie": "theorie-van-de-selectieve-perceptie",
    "volksverzekeringen": "volksverzekering",
    "wet-economische-delicten": "wet-op-de-economische-delicten",
    "zwevende-kiezer": "zwevende-kiezers",
}
DOWNLOAD_ITEMS = [
    ("Mens en Werk - leertekst", "PDF", "/wp-content/uploads/2016/12/Mens-en-Werk-Kerndoel-1-tm-6-leertekst.pdf"),
    ("Multiculturele Samenleving - leertekst", "PDF", "/wp-content/uploads/2016/12/Multiculturele-Samenleving-Kerndoel-1-tm-5-leertekst.pdf"),
    ("Massamedia - leertekst", "PDF", "/wp-content/uploads/2017/06/Massamedia-Kerndoel-1-tm-4-leertekst.pdf"),
    ("Politiek en Beleid - leertekst", "PDF", "/wp-content/uploads/2018/04/Politiek-en-Beleid-Kerndoel-1-tm-5-leertekst.pdf"),
    ("Criminaliteit en Rechtsstaat - leertekst", "PDF", "/wp-content/uploads/2017/06/Criminaliteit-en-Rechtsstaat-Kerndoel-1-tm-5-leertekst.pdf"),
    ("Analyse Maatschappelijk Vraagstuk - leertekst", "PDF", "/wp-content/uploads/2016/12/Analyse-Maatschappelijk-Vraagstuk-AMV-Kerndoel-1-tm-3.pdf"),
    ("Schema parlementaire democratie", "JPG", "/wp-content/uploads/2016/02/Nederlandse-Parlementaire-Democratie-A3.jpg"),
    ("Checklist CSE Maatschappijkunde 2018", "PDF", "/wp-content/uploads/2019/04/Checklist-CSE-Maatschappijkunde-2018.pdf"),
    ("Check CSE Maatschappijleer 2 2017", "PDF", "/wp-content/uploads/2017/04/Check-CSE-Maatschappijleer-2-2017.pdf"),
    ("Massamedia - leertekst 2020", "PDF", "/wp-content/uploads/2020/03/3_Massamedia.pdf"),
    ("Multiculturele Samenleving - leertekst 2018", "PDF", "/wp-content/uploads/2018/12/Multiculturele-Samenleving-Kerndoel-1-tm-5-leertekst.pdf"),
    ("Mens en Werk - leertekst 2018", "PDF", "/wp-content/uploads/2018/12/Mens-en-Werk-Kerndoel-1-tm-6-leertekst.pdf"),
    ("Analyse Maatschappelijk Vraagstuk - leertekst 2016", "PDF", "/wp-content/uploads/2016/03/Analyse-Maatschappelijk-Vraagstuk-AMV-Kerndoel-1-tm-3-leertekst.pdf"),
    ("Criminaliteit en Rechtsstaat - leertekst 2016", "PDF", "/wp-content/uploads/2016/02/Criminaliteit-en-Rechtsstaat-Leertekst-Maatschappijkunde.nl_.pdf"),
]
EXAMENSTOF_GROUPS = [
    ("Maatschappijkunde", [
        "/kerndoelen/mensenwerk/",
        "/kerndoelen/multiculturelesamenleving/",
        "/kerndoelen/massamedia/",
        "/kerndoelen/politiekenbeleid/",
        "/kerndoelen/criminaliteit-en-rechtsstaat/",
        "/kerndoelen/amv/",
    ]),
    ("Maatschappijleer", [
        "/kerndoelen/maatschappijleer-vmbo/",
        "/kerndoelen/maatschappijleer/",
        "/kerndoelen/domein-b-rechtsstaat/",
        "/kerndoelen/domein-c-parlementaire-democratie/",
        "/kerndoelen/domein-d-verzorgingsstaat/",
        "/kerndoelen/domien-e-pluriforme-samenleving/",
    ]),
    ("Maatschappijwetenschappen", [
        "/kerndoelen/cultuur-en-socialisatie/",
        "/kerndoelen/beeldvorming-en-stereotypering/",
        "/kerndoelen/macht-en-zeggenschap/",
        "/kerndoelen/sociale-verschillen/",
    ]),
]


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def attrs_to_dict(raw):
    attrs = {}
    for key, _, value1, value2, value3 in re.findall(r'([a-zA-Z0-9_:-]+)\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s\]]+))', raw or ""):
        attrs[key] = html.unescape(value1.strip("\"'") if value1 else value2 or value3)
    return attrs


def normalize_legacy_url(url):
    text = normalize_internal_urls(url.strip())
    try:
        path = re.sub(r"^https?://(?:www\.)?maatschappijkunde\.nl", "", text, flags=re.I)
    except Exception:
        path = text
    for source, target in INTERNAL_URL_REWRITES.items():
        if path == source:
            return target
    return path


def extract_serialized_value(raw, key):
    match = re.search(rf's:\d+:"{re.escape(key)}";s:\d+:"(.*?)";', raw, flags=re.S)
    return html.unescape(match.group(1)) if match else ""


def extract_legacy_modules(meta_by_post):
    modules = {}
    for values in meta_by_post.values():
        side = values.get("sidemeta", "")
        info = values.get("infosmeta", "")
        category = extract_serialized_value(side, "category")
        if not category or not info:
            continue
        items = []
        for item_match in re.finditer(r"i:\d+;a:\d+:\{(.*?)\}", info, flags=re.S):
            raw_item = item_match.group(1)
            image = normalize_internal_urls(extract_serialized_value(raw_item, "style1_image"))
            description = clean_text(extract_serialized_value(raw_item, "style1_description"))
            link = normalize_legacy_url(extract_serialized_value(raw_item, "style1_link"))
            if image or description or link:
                items.append({"image": image, "description": description, "link": link})
        if items:
            modules[category] = items
    return modules


def render_legacy_module(category):
    items = LEGACY_MODULES.get(category, [])
    if not items:
        return f'<div class="shortcode-panel" data-legacy-module="uhe_style1" data-category="{html.escape(category)}">Oude oefenmodule: {html.escape(category)}</div>'
    links = []
    for item in items:
        image = f'<img src="{html.escape(item["image"])}" alt="" loading="lazy">' if item.get("image") else ""
        description = f'<span>{html.escape(item.get("description", ""))}</span>' if item.get("description") else ""
        href = html.escape(item.get("link") or "#")
        links.append(f'<li><a href="{href}">{image}{description}</a></li>')
    return f'<ul class="legacy-module-list" data-legacy-module="uhe_style1" data-category="{html.escape(category)}">{"".join(links)}</ul>'


def normalize_title(post):
    title = clean_text(post.get("post_title") or "")
    return TITLE_REWRITES.get((str(post.get("ID")), title), title) or "Zonder titel"


def convert_table(match):
    inner = match.group(1)
    rows = []
    for heading in re.findall(r"\[gt_table_heading[^\]]*\](.*?)\[/gt_table_heading\]", inner, flags=re.S | re.I):
        cells = [f"<th>{cell.strip()}</th>" for cell in heading.split("||")]
        if cells:
            rows.append(f"<tr>{''.join(cells)}</tr>")
    for body in re.findall(r"\[gt_table_body[^\]]*\](.*?)\[/gt_table_body\]", inner, flags=re.S | re.I):
        for raw_attrs, body_content in re.findall(r"\[gt_table_data([^\]]*)\](.*?)\[/gt_table_data\]", body, flags=re.S | re.I):
            attrs = attrs_to_dict(raw_attrs)
            content = attrs.get("data", "").strip() or body_content.strip()
            cells = [f"<td>{cell.strip()}</td>" for cell in content.split("||")]
            if cells:
                rows.append(f"<tr>{''.join(cells)}</tr>")
    return f"<table><tbody>{''.join(rows)}</tbody></table>" if rows else ""


def strip_wrapping_shortcode(name, css_class, text):
    pattern = re.compile(rf"\[{name}[^\]]*\](.*?)\[/{name}\]", re.S | re.I)
    while pattern.search(text):
        text = pattern.sub(rf'<div class="{css_class}">\1</div>', text)
    text = re.sub(rf"\[{name}[^\]]*/?\]", f'<div class="{css_class}">', text, flags=re.I)
    return text


def convert_fusion_code(match, notes):
    raw = html.unescape(match.group(1)).strip()
    decoded = ""
    try:
        decoded = base64.b64decode(raw, validate=True).decode("utf-8", errors="replace").strip()
    except Exception:
        pass

    shortcode = decoded or raw
    notes.append(f"fusion_code gedecodeerd: {shortcode}")

    if re.fullmatch(r"\[wpdreams_ajaxsearchpro\s+id=['\"]?\d+['\"]?\s*\]", shortcode, flags=re.I):
        return ""

    uhe_match = re.fullmatch(r"\[uhe_style1\s+category=['\"]?([a-z0-9_-]+)['\"]?\s*\]", shortcode, flags=re.I)
    if uhe_match:
        return render_legacy_module(uhe_match.group(1))

    notes.append("Onbekende fusion_code moet handmatig worden beoordeeld.")
    return '<div class="notice">Ingesloten code moet handmatig worden beoordeeld.</div>'


def convert_shortcodes(content):
    notes = []
    text = content or ""
    text = re.sub(r"\[gt_table[^\]]*\](.*?)\[/gt_table\]", convert_table, text, flags=re.S | re.I)
    text = re.sub(r"\[icon[^\]]*\]", '<span class="legacy-icon" aria-hidden="true"></span>', text, flags=re.I)

    wrappers = {
        "vc_row": "wp-row",
        "vc_column": "wp-column",
        "vc_column_text": "wp-column-text",
        "fusion_text": "wp-column-text",
        "fullwidth": "wp-row",
        "one_fifth": "wp-column",
        "three_fifth": "wp-column",
        "content_boxes": "wp-row",
        "content_box": "wp-column",
        "vc_message": "shortcode-panel",
        "ultimate_modal": "shortcode-panel"
    }
    for name, css_class in wrappers.items():
        text = strip_wrapping_shortcode(name, css_class, text)
        text = re.sub(rf"\[/{name}\]", "</div>", text, flags=re.I)

    text = re.sub(r"\[toggle([^\]]*)\](.*?)\[/toggle\]", r'<section class="toggle"><div>\2</div></section>', text, flags=re.S | re.I)
    text = re.sub(r"\[vc_tta_tabs[^\]]*\](.*?)\[/vc_tta_tabs\]", r'<section class="tab-section">\1</section>', text, flags=re.S | re.I)
    text = re.sub(r"\[vc_tta_section([^\]]*)\](.*?)\[/vc_tta_section\]", r'<section class="tab-section">\2</section>', text, flags=re.S | re.I)
    text = re.sub(r"\[gt_tab([^\]]*)\](.*?)\[/gt_tab\]", r'<section class="tab-section">\2</section>', text, flags=re.S | re.I)

    text = re.sub(
        r"\[fusion_code[^\]]*\](.*?)\[/fusion_code\]",
        lambda match: convert_fusion_code(match, notes),
        text,
        flags=re.S | re.I
    )

    text = re.sub(r"\[/?(?:gt_table_heading|gt_table_body|gt_table_data|button|separator|glossary_exclude|glossary|usquare|ht_message)[^\]]*\]", "", text, flags=re.I)
    unresolved = sorted(set(re.findall(r"\[/?([a-zA-Z0-9_:-]+)(?:\s|\]|/)", text)))
    if unresolved:
        notes.append("Onopgeloste shortcode(s): " + ", ".join(unresolved))
    return text, notes


def normalize_internal_urls(content):
    text = content or ""
    text = re.sub(r"https?://(?:www\.)?maatschappijkunde\.nl/wp-content/uploads/", "/wp-content/uploads/", text, flags=re.I)
    text = re.sub(r"https?://(?:www\.)?maatschappijkunde\.nl/", "/", text, flags=re.I)
    for source, target in INTERNAL_URL_REWRITES.items():
        text = text.replace(f'href="{source}"', f'href="{target}"')
        text = text.replace(f"href='{source}'", f"href='{target}'")
    return text


def canonicalize_schoolwoorden_url(url):
    text = url or ""
    for old_slug, new_slug in SCHOOLWOORDEN_CANONICAL_SLUGS.items():
        text = re.sub(
            rf"(?P<prefix>https://schoolwoorden\.nl/begrip/|/begrip/){re.escape(old_slug)}(?P<suffix>/?)(?=$|[\"'<\s])",
            rf"\g<prefix>{new_slug}\g<suffix>",
            text,
            flags=re.I
        )
    return text


def canonicalize_schoolwoorden_links(content):
    return canonicalize_schoolwoorden_url(content or "")


def clean_wordpress_blocks(content):
    text = content or ""
    text = re.sub(r"<!--\s*/?wp:[^>]*-->", "", text, flags=re.I)
    text = text.replace("<!--more-->", "").replace("<!--noteaser-->", "")
    text = re.sub(r'<div class="embed-container embed-responsive embed-responsive-4by3">\s*</div>', "", text)
    return text


def remove_youtube(content):
    text = content or ""
    text = re.sub(
        r"<figure\b[^>]*\b(?:is-provider-youtube|wp-block-embed-youtube|is-type-video)[^>]*>.*?</figure>",
        "",
        text,
        flags=re.I | re.S
    )
    text = re.sub(
        r"<iframe\b[^>]*\bsrc=[\"'][^\"']*(?:youtube\.com|youtube-nocookie\.com|youtu\.be)[^\"']*[\"'][^>]*>\s*</iframe>",
        "",
        text,
        flags=re.I
    )
    text = re.sub(
        r"<a\b[^>]*\bhref=[\"'][^\"']*(?:youtube\.com|youtube-nocookie\.com|youtu\.be)[^\"']*[\"'][^>]*>.*?</a>",
        "",
        text,
        flags=re.I | re.S
    )
    text = re.sub(r"(?<![\"'=])https?://(?:www\.)?(?:youtube\.com|youtube-nocookie\.com|youtu\.be)/[^<\s]+", "", text, flags=re.I)
    text = re.sub(r'<div class="embed-container embed-responsive embed-responsive-4by3">\s*</div>', "", text, flags=re.I)
    return text


def apply_text_corrections(content):
    text = content or ""
    replacements = [
        (r"\bTesktboekjes\b", "Tekstboekjes"),
        (r"\bwerplekken\b", "werkplekken"),
        (r"\bopzoek\b", "op zoek"),
        (r"\bVrijwilligers werk\b", "Vrijwilligerswerk"),
        (r"\bvrijwilligers werk\b", "vrijwilligerswerk"),
        (r"\blichamelijk of geestelijk inspanning\b", "lichamelijke of geestelijke inspanning"),
        (r"\bWerkt geeft\b", "Werk geeft"),
        (r"\bhet regering\b", "de regering"),
        (r"\bwordt door het regering\b", "wordt door de regering"),
        (r"\bcoalitieparijten\b", "coalitiepartijen"),
        (r"\bvoortellen\b", "voorstellen"),
        (r"\bMinisters President\b", "minister-president"),
        (r"\bMinisters-president\b", "minister-president"),
        (r"\bmeerheid\b", "meerderheid"),
        (r"\bbepaald, medewerkers\b", "bepaalt, medewerkers"),
        (r"\bde de\b", "de"),
        (r"\bPressiemidelen\b", "Pressiemiddelen"),
        (r"\bpressiemidelen\b", "pressiemiddelen"),
        (r"\bHerstvakantie\b", "Herfstvakantie"),
        (r"\bben\.t\b", "bent"),
        (r"\bwerkelozen\b", "werklozen"),
        (r"\bwerkeloze\b", "werkloze"),
        (r"\bverlichtingen\b", "verplichtingen"),
        (r"\bde vasten lasten\b", "de vaste lasten"),
        (r"\bvasten lasten\b", "vaste lasten"),
        (r"\bslechter Nederlandse spreken\b", "slechter Nederlands spreken"),
        (r"\bhun goed aan een baan\b", "hen goed aan een baan"),
        (r"\bOudere werknemer zijn\b", "Oudere werknemers zijn"),
        (r"\bVrouwen werkte\b", "Vrouwen werkten"),
        (r"\bAl hoewel\b", "Alhoewel"),
        (r"\bal hoewel\b", "alhoewel"),
        (r"\btegen over\b", "tegenover"),
        (r"\ber voor kiezen\b", "ervoor kiezen"),
        (r"\ber voor zorgen\b", "ervoor zorgen"),
        (r"\bhet zelfde\b", "hetzelfde"),
        (r"\beindexamen onderwerp\b", "eindexamenonderwerp"),
        (r"\bexamen onderwerp\b", "examenonderwerp"),
        (r"\bMaatschappelijk vraagstuk\b", "Maatschappelijk Vraagstuk"),
        (r"\b/Beinvloedingstheorieen\b", "/ Beinvloedingstheorieen"),
        (r"Geschreven uitleg,\s*video(?:'|&#x27;|’)?s,\s*slides", "Geschreven uitleg, slides"),
        (r"geschreven uitleg,\s*video(?:'|&#x27;|’)?s,\s*slides", "geschreven uitleg, slides"),
        (r"uitleg,\s*video(?:'|&#x27;|’)?s,\s*slides", "uitleg, slides"),
        (r"Uitleg,\s*Video(?:'|&#x27;|’)?s,\s*Slides", "Uitleg, slides"),
        (r"Geschreven uitleg,\s*Video(?:'|&#x27;|’)?s,\s*Slides", "Geschreven uitleg, slides"),
        (r"Alle Geschreven uitleg,\s*Video(?:'|&#x27;|’)?s,\s*Slides", "Alle geschreven uitleg, slides"),
        (r"met per onderwerp geschreven uitleg,\s*video(?:'|&#x27;|’)?s,\s*slides", "met per onderwerp geschreven uitleg, slides"),
        (r"met per kerndoel\s*uitleg,\s*video(?:'|&#x27;|’)?s,\s*slides", "met per kerndoel uitleg, slides"),
        (r":\s*Geschreven uitleg,\s*Video(?:'|&#x27;|’)?s,\s*Oefenvragen,\s*Slides", ": Geschreven uitleg, oefenvragen, slides")
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


def convert_strong_lists(content):
    def split_strong_markers(inner, marker_re, ordered=False):
        matches = list(marker_re.finditer(inner))
        if len(matches) < 2:
            return None
        prefix = inner[:matches[0].start()].strip()
        if prefix and len(clean_text(prefix).split()) > 18:
            return None
        items = []
        for index, match in enumerate(matches):
            title = clean_text(match.group("title")).strip(" :")
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(inner)
            body = inner[start:end].strip()
            body = re.sub(r"^\s*[:.)-]\s*", "", body)
            if not title or not clean_text(body):
                return None
            items.append((title, body))
        before = f"<p>{prefix}</p>" if prefix else ""
        tag = "ol" if ordered else "ul"
        list_items = "".join(
            f"<li><strong>{html.escape(title)}</strong> {body}</li>"
            for title, body in items
        )
        return f'{before}<{tag} class="content-list">{list_items}</{tag}>'

    numbered_re = re.compile(r"<strong>\s*(?:\d+)\.\s*(?P<title>[^<]+?)\s*</strong>", re.I)
    colon_re = re.compile(r"<strong>\s*(?P<title>[^<:]{3,70}?):\s*</strong>", re.I)

    def convert_paragraph(match):
        inner = match.group(1)
        converted = split_strong_markers(inner, numbered_re, ordered=True)
        if converted:
            return converted
        converted = split_strong_markers(inner, colon_re, ordered=False)
        return converted or match.group(0)

    return re.sub(r"<p>(.*?)</p>", convert_paragraph, content or "", flags=re.I | re.S)


def improve_readability(content):
    text = content or ""
    text = re.sub(r"<p([^>]*)>\s*(?:&nbsp;|\s)*</p>", "", text, flags=re.I)
    text = re.sub(r"<span[^>]*>(.*?)</span>", r"\1", text, flags=re.I | re.S)
    text = re.sub(r'\sstyle="[^"]*"', "", text, flags=re.I)
    text = re.sub(r"\r\n\r\n+", "\n\n", text)
    text = re.sub(r"(?<!>)\n{2,}(?!<)", "</p><p>", text)
    text = re.sub(r"<p>\s*</p>", "", text, flags=re.I)
    return text.strip()


def clean_empty_legacy_wrappers(content):
    text = content or ""
    empty_wrapper = re.compile(r'<div class="(?:wp-row|wp-column|wp-column-text|shortcode-panel|tab-section|toggle)">\s*</div>', re.I)
    empty_section = re.compile(r'<section class="(?:tab-section|toggle)">\s*</section>', re.I)
    previous = None
    while previous != text:
        previous = text
        text = empty_wrapper.sub("", text)
        text = empty_section.sub("", text)
    return text.strip()


def slug_segments(url):
    path = url.strip("/")
    return None if path == "" else path.split("/")


def slug_param(url):
    path = url.strip("/")
    return None if path == "" else path


def html_link_list(items):
    if not items:
        return "<p>Voor dit overzicht zijn nog geen gekoppelde artikelen gevonden.</p>"
    links = []
    for item in sorted_pages(items):
        links.append(f'<li><a href="{html.escape(item["url"])}">{html.escape(item["title"])}</a></li>')
    return f"<ul>{''.join(links)}</ul>"


def sorted_pages(items):
    return sorted(items, key=lambda p: (p["title"].lower(), p["url"]))


def slugify_text(value):
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    return ascii_text.strip("-")


def read_schoolwoorden_urls():
    if not SCHOOLWOORDEN_SITEMAP.exists():
        return {}
    xml = SCHOOLWOORDEN_SITEMAP.read_text(encoding="utf-8", errors="replace")
    urls = re.findall(r"<loc>\s*(https://schoolwoorden\.nl/begrip/[^<\s]+)\s*</loc>", xml, flags=re.I)
    by_slug = {}
    for url in urls:
        clean_url = html.unescape(url).rstrip("/")
        slug = clean_url.rsplit("/", 1)[-1].lower()
        by_slug[slug] = clean_url
    return by_slug


def build_glossary_terms(posts, posts_by_id, redirect_by_source, schoolwoorden_urls):
    terms = []
    for post in posts:
        if post.get("post_status") != "publish" or post.get("post_type") != "glossary":
            continue
        title = normalize_title(post)
        legacy_url = rel_url(post, posts_by_id)
        legacy_slug = legacy_url.strip("/").split("/")[-1]
        redirect_target = (redirect_by_source.get(legacy_url) or "").rstrip("/")
        redirect_target = canonicalize_schoolwoorden_url(redirect_target)
        redirect_slug = redirect_target.rsplit("/", 1)[-1].lower() if "schoolwoorden.nl/begrip/" in redirect_target else ""
        title_slug = slugify_text(title)
        sitemap_url = (
            schoolwoorden_urls.get(redirect_slug)
            or schoolwoorden_urls.get(legacy_slug)
            or schoolwoorden_urls.get(title_slug)
        )
        schoolwoorden_url = sitemap_url or redirect_target
        schoolwoorden_url = canonicalize_schoolwoorden_url(schoolwoorden_url)
        raw_definition, _ = convert_shortcodes(post.get("post_content") or "")
        raw_definition = normalize_internal_urls(raw_definition)
        raw_definition = clean_wordpress_blocks(raw_definition)
        raw_definition = remove_youtube(raw_definition)
        raw_definition = apply_text_corrections(raw_definition)
        definition = clean_text(raw_definition)
        terms.append({
            "title": title,
            "legacyUrl": legacy_url,
            "definition": definition,
            "schoolwoordenUrl": schoolwoorden_url or "",
            "matchedSitemap": bool(sitemap_url)
        })
    return sorted(terms, key=lambda item: (item["title"].lower(), item["legacyUrl"]))


def build_glossary_page(glossary_terms):
    grouped = {}
    for term in glossary_terms:
        first = slugify_text(term["title"])[:1].upper() or "#"
        if not first.isdigit() and not ("A" <= first <= "Z"):
            first = "#"
        grouped.setdefault(first, []).append(term)

    nav_letters = "".join(
        f'<a href="#begrippen-{html.escape(letter.lower())}">{html.escape(letter)}</a>'
        for letter in sorted(grouped)
    )
    sections = []
    for letter in sorted(grouped):
        rows = []
        for term in grouped[letter]:
            title = html.escape(term["title"])
            definition = html.escape(term["definition"])
            if term["schoolwoordenUrl"]:
                link = f'<a href="{html.escape(term["schoolwoordenUrl"])}">{title}</a>'
            else:
                link = title
            definition_html = f'<p>{definition}</p>' if definition else '<p>Geen definitie beschikbaar.</p>'
            rows.append(
                '<article class="glossary-item">'
                f'<h3>{link}</h3>'
                f'{definition_html}'
                '</article>'
            )
        sections.append(
            f'<section class="glossary-section" id="begrippen-{html.escape(letter.lower())}">'
            f'<h2>{html.escape(letter)}</h2>'
            f'<div class="glossary-grid">{"".join(rows)}</div>'
            '</section>'
        )
    linked = sum(1 for term in glossary_terms if term.get("schoolwoordenUrl"))
    matched = sum(1 for term in glossary_terms if term.get("matchedSitemap"))
    fallback_terms = [term for term in glossary_terms if term.get("schoolwoordenUrl") and not term.get("matchedSitemap")]
    fallback_list = "".join(
        f'<li>{html.escape(term["title"])} - <a href="{html.escape(term["schoolwoordenUrl"])}">{html.escape(term["schoolwoordenUrl"])}</a></li>'
        for term in fallback_terms
    )
    fallback_details = (
        '<details class="glossary-fallbacks">'
        f'<summary>{len(fallback_terms)} koppelingen niet exact in de sitemap bevestigd</summary>'
        f'<ul>{fallback_list}</ul>'
        '</details>'
    ) if fallback_terms else ""
    return (
        '<p>Hieronder staan de begrippen uit de lesstof. Elk gekoppeld begrip verwijst naar Schoolwoorden.nl.</p>'
        f'<p class="notice">Begrippen gekoppeld aan Schoolwoorden.nl: {linked} van {len(glossary_terms)}. Daarvan zijn {matched} koppelingen exact bevestigd in de sitemap.</p>'
        f'{fallback_details}'
        f'<nav class="glossary-index" aria-label="Begrippen op letter">{nav_letters}</nav>'
        f'{"".join(sections)}'
    )


def build_over_page():
    return (
        '<p>Maatschappijkunde.nl bewaart examenstof, kerndoelen, begrippen en downloads voor leerlingen en docenten.</p>'
        '<p>De oorspronkelijke inhoud is gemaakt door Wessel Peeters. Stef van der Linden heeft de inhoud overgenomen om deze beschikbaar te houden.</p>'
    )


def build_downloads_page():
    cards = []
    missing = []
    for title, file_type, url in DOWNLOAD_ITEMS:
        file_path = PUBLIC / url.lstrip("/")
        if not file_path.exists():
            missing.append(url)
        cards.append(
            '<article class="download-card">'
            f'<h2>{html.escape(title)}</h2>'
            f'<p class="download-meta">{html.escape(file_type)}</p>'
            f'<a class="download-button" href="{html.escape(url)}" download>Download</a>'
            '</article>'
        )
    if missing:
        raise FileNotFoundError("Downloadbestand ontbreekt in public: " + ", ".join(missing))
    return (
        '<p>Alle beschikbare bestanden staan hieronder bij elkaar.</p>'
        f'<div class="download-grid">{"".join(cards)}</div>'
    )


def build_examenstof_page(kb_overviews, pages_by_url):
    used = set()
    sections = []
    for group_title, urls in EXAMENSTOF_GROUPS:
        cards = []
        for url in urls:
            page = pages_by_url.get(url)
            if not page:
                continue
            used.add(url)
            links = re.findall(r'<li><a href="([^"]+)">([^<]+)</a></li>', page.get("html") or "")
            child_links = "".join(
                f'<li><a href="{html.escape(href)}">{html.escape(clean_text(label))}</a></li>'
                for href, label in links
            )
            cards.append(
                '<article class="subject-card">'
                f'<h2><a href="{html.escape(url)}">{html.escape(page["title"])}</a></h2>'
                f'<ul>{child_links}</ul>'
                '</article>'
            )
        if cards:
            sections.append(
                f'<section class="subject-group"><h2>{html.escape(group_title)}</h2>'
                f'<div class="subject-grid">{"".join(cards)}</div></section>'
            )
    remaining = [page for page in kb_overviews if page["url"] not in used]
    if remaining:
        sections.append(
            '<section class="subject-group"><h2>Overige onderwerpen</h2>'
            f'{html_link_list(remaining)}</section>'
        )
    return "".join(sections)


def build_homepage(kb_overviews, pages_by_url):
    featured_urls = [
        "/kerndoelen/mensenwerk/",
        "/kerndoelen/multiculturelesamenleving/",
        "/kerndoelen/massamedia/",
        "/kerndoelen/politiekenbeleid/",
        "/kerndoelen/criminaliteit-en-rechtsstaat/",
        "/kerndoelen/amv/"
    ]
    topic_cards = []
    for url in featured_urls:
        page = pages_by_url.get(url)
        if not page:
            continue
        children = re.findall(r'<li><a href="([^"]+)">([^<]+)</a></li>', page.get("html") or "")
        child_links = "".join(
            f'<li><a href="{html.escape(href)}">{html.escape(clean_text(label))}</a></li>'
            for href, label in children[:3]
        )
        if not child_links:
            child_links = '<li><a href="/examenstof/">Bekijk de gekoppelde examenstof</a></li>'
        topic_cards.append(
            '<section class="topic-card">'
            f'<a href="{html.escape(url)}">{html.escape(page["title"])}</a>'
            f'<ul>{child_links}</ul>'
            '</section>'
        )

    if len(topic_cards) < 6:
        for page in kb_overviews:
            if page["url"] in featured_urls:
                continue
            topic_cards.append(
                '<section class="topic-card">'
                f'<a href="{html.escape(page["url"])}">{html.escape(page["title"])}</a>'
                '</section>'
            )
            if len(topic_cards) >= 6:
                break

    quick_cards = [
        ("/examenstof/", "Examenstof"),
        ("/kerndoelen/", "Kerndoelen"),
        ("/begrippen/", "Begrippen"),
        ("/downloads/", "Downloads")
    ]
    quick_html = "".join(
        '<section class="quick-card">'
        f'<a href="{html.escape(url)}">{html.escape(title)}</a>'
        '</section>'
        for url, title in quick_cards
    )

    return (
        '<section class="home-hero">'
        '<div class="home-hero__copy">'
        '<p class="home-eyebrow">VMBO maatschappijleer 2</p>'
        '<h1>Maatschappijkunde.nl</h1>'
        '<p>Examenstof, kerndoelen, begrippen en downloads voor maatschappijkunde en maatschappijleer.</p>'
        '<div class="home-actions">'
        '<a class="button-link" href="/examenstof/">Naar examenstof</a>'
        '<a class="button-link secondary" href="/begrippen/">Begrippen zoeken</a>'
        '</div>'
        '</div>'
        '<aside class="home-hero__panel" aria-label="Snel starten">'
        '<h2>Snel starten</h2>'
        '<ul>'
        '<li><a href="/kerndoelen/mensenwerk/">Mens en Werk</a></li>'
        '<li><a href="/kerndoelen/multiculturelesamenleving/">Multiculturele Samenleving</a></li>'
        '<li><a href="/kerndoelen/massamedia/">Massamedia</a></li>'
        '<li><a href="/kerndoelen/politiekenbeleid/">Politiek en Beleid</a></li>'
        '<li><a href="/kerndoelen/criminaliteit-en-rechtsstaat/">Criminaliteit en Rechtsstaat</a></li>'
        '</ul>'
        '</aside>'
        '</section>'
        '<section class="home-section">'
        '<div class="section-heading"><div><h2>Belangrijkste onderwerpen</h2></div><a href="/kerndoelen/">Alle kerndoelen</a></div>'
        f'<div class="topic-grid">{"".join(topic_cards)}</div>'
        '</section>'
        '<section class="home-section">'
        '<div class="section-heading"><div><h2>Verder op de site</h2></div></div>'
        f'<div class="quick-grid">{quick_html}</div>'
        '</section>'
    )


def write_redirect_files(redirects):
    netlify_lines = [f'{r["source"]} {r["target"]} {r["status"]}' for r in redirects]
    apache_lines = [
        "# Generated from data/site/redirects.json. Do not edit by hand.",
        "RewriteEngine On",
        *[f'Redirect {r["status"]} {r["source"]} {r["target"]}' for r in redirects],
        "",
        "<IfModule mod_headers.c>",
        '  Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"',
        '  Header set X-Content-Type-Options "nosniff"',
        '  Header set Referrer-Policy "strict-origin-when-cross-origin"',
        '  <FilesMatch "\\.(png|jpg|jpeg|gif|webp|svg|css|js|woff2?)$">',
        '    Header set Cache-Control "public, max-age=31536000, immutable"',
        "  </FilesMatch>",
        '  <FilesMatch "\\.(html|xml)$">',
        '    Header set Cache-Control "public, max-age=300"',
        "  </FilesMatch>",
        "</IfModule>",
        ""
    ]
    (SITE / "_redirects").write_text("\n".join(netlify_lines) + "\n", encoding="utf-8")
    (SITE / ".htaccess").write_text("\n".join(apache_lines), encoding="utf-8")
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "_redirects").write_text("\n".join(netlify_lines) + "\n", encoding="utf-8")
    (PUBLIC / ".htaccess").write_text("\n".join(apache_lines), encoding="utf-8")


def main():
    global LEGACY_MODULES
    SITE.mkdir(parents=True, exist_ok=True)
    if not SQL.exists():
        existing_pages = SITE / "pages.json"
        existing_redirects = SITE / "redirects.json"
        if existing_pages.exists() and existing_redirects.exists():
            pages = json.loads(existing_pages.read_text(encoding="utf-8"))
            redirects = json.loads(existing_redirects.read_text(encoding="utf-8"))
            PUBLIC.mkdir(parents=True, exist_ok=True)
            redirects_file = SITE / "_redirects"
            if redirects_file.exists():
                (PUBLIC / "_redirects").write_text(redirects_file.read_text(encoding="utf-8"), encoding="utf-8")
            htaccess_file = SITE / ".htaccess"
            if htaccess_file.exists():
                (PUBLIC / ".htaccess").write_text(htaccess_file.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                write_redirect_files(redirects)
            print(json.dumps({
                "pages": len(pages),
                "redirects": len(redirects),
                "source": "existing-site-data",
                "note": "SQL-export ontbreekt; bestaande data/site gebruikt."
            }, ensure_ascii=False))
            return
        raise FileNotFoundError(f"SQL-export ontbreekt en {existing_pages} bestaat niet.")

    sql_text = SQL.read_text(encoding="utf-8", errors="replace")
    post_cols = get_columns(sql_text, "wp_posts")
    meta_cols = get_columns(sql_text, "wp_postmeta")
    term_cols = get_columns(sql_text, "wp_terms")
    term_taxonomy_cols = get_columns(sql_text, "wp_term_taxonomy")
    relationship_cols = get_columns(sql_text, "wp_term_relationships")
    posts = list(iter_insert_rows(SQL, "wp_posts", post_cols))
    posts_by_id = {str(p["ID"]): p for p in posts}

    meta_keys = {"_yoast_wpseo_title", "_yoast_wpseo_metadesc", "infosmeta", "sidemeta"}
    meta_by_post = {}
    for row in iter_insert_rows(SQL, "wp_postmeta", meta_cols):
        if row.get("meta_key") in meta_keys:
            meta_by_post.setdefault(str(row.get("post_id")), {})[row.get("meta_key")] = row.get("meta_value") or ""
    LEGACY_MODULES = extract_legacy_modules(meta_by_post)

    redirects = read_csv(GENERATED / "redirects.csv")
    for redirect in redirects:
        redirect["target"] = canonicalize_schoolwoorden_url(redirect.get("target") or "")
    known_redirect_sources = {redirect["source"] for redirect in redirects}
    redirects.extend(
        redirect for redirect in EXTRA_REDIRECTS
        if redirect["source"] not in known_redirect_sources
    )
    redirect_by_source = {redirect["source"]: redirect["target"] for redirect in redirects}
    schoolwoorden_urls = read_schoolwoorden_urls()
    glossary_terms = build_glossary_terms(posts, posts_by_id, redirect_by_source, schoolwoorden_urls)
    redirect_sources = {r["source"] for r in redirects}
    pages = []
    pages_by_id = {}

    for post in posts:
        if post.get("post_status") != "publish" or post.get("post_type") not in PUBLIC_TYPES:
            continue
        url = rel_url(post, posts_by_id)
        if url in redirect_sources:
            continue
        meta = meta_by_post.get(str(post.get("ID")), {})
        converted, notes = convert_shortcodes(post.get("post_content") or "")
        converted = normalize_internal_urls(converted)
        converted = canonicalize_schoolwoorden_links(converted)
        converted = clean_wordpress_blocks(converted)
        converted = remove_youtube(converted)
        converted = apply_text_corrections(converted)
        converted = improve_readability(converted)
        converted = convert_strong_lists(converted)
        converted = clean_empty_legacy_wrappers(converted)
        title = normalize_title(post)
        page = {
            "id": str(post.get("ID")),
            "type": post.get("post_type"),
            "typeLabel": TYPE_LABELS.get(post.get("post_type"), post.get("post_type")),
            "title": title,
            "url": url,
            "slugSegments": slug_segments(url),
            "slugParam": slug_param(url),
            "date": post.get("post_date") or "",
            "modified": post.get("post_modified") or "",
            "seoTitle": meta.get("_yoast_wpseo_title") or title,
            "description": meta.get("_yoast_wpseo_metadesc") or "",
            "html": converted,
            "plainText": clean_text(converted),
            "conversionNotes": notes
        }
        pages.append(page)
        pages_by_id[page["id"]] = page

    home = next((p for p in pages if p["url"] == "/home/"), None)
    if home and not any(p["url"] == "/" for p in pages):
        root = dict(home)
        root["url"] = "/"
        root["slugSegments"] = None
        root["slugParam"] = None
        pages.insert(0, root)

    terms = {r["term_id"]: r for r in iter_insert_rows(SQL, "wp_terms", term_cols)}
    taxonomies = list(iter_insert_rows(SQL, "wp_term_taxonomy", term_taxonomy_cols))
    relationships = list(iter_insert_rows(SQL, "wp_term_relationships", relationship_cols))
    related_ids_by_taxonomy = {}
    for relationship in relationships:
        related_ids_by_taxonomy.setdefault(relationship["term_taxonomy_id"], set()).add(str(relationship["object_id"]))

    taxonomies_by_id = {t["term_taxonomy_id"]: t for t in taxonomies}
    children_by_parent = {}
    for taxonomy in taxonomies:
        children_by_parent.setdefault(taxonomy.get("parent") or "0", []).append(taxonomy)

    def collect_related_pages(taxonomy_id, seen=None):
        seen = seen or set()
        if taxonomy_id in seen:
            return []
        seen.add(taxonomy_id)
        related = [pages_by_id[post_id] for post_id in related_ids_by_taxonomy.get(taxonomy_id, set()) if post_id in pages_by_id]
        for child in children_by_parent.get(taxonomy_id, []):
            related.extend(collect_related_pages(child["term_taxonomy_id"], seen))
        by_url = {page["url"]: page for page in related}
        return sorted_pages(by_url.values())

    existing_urls = {page["url"] for page in pages}
    for taxonomy in taxonomies:
        taxonomy_name = taxonomy.get("taxonomy")
        if taxonomy_name not in TAXONOMY_PREFIXES:
            continue
        term = terms.get(taxonomy.get("term_id"))
        if not term:
            continue
        url = f'{TAXONOMY_PREFIXES[taxonomy_name]}{term["slug"]}/'
        if url in existing_urls or url in redirect_sources:
            continue
        related_pages = collect_related_pages(taxonomy["term_taxonomy_id"])
        child_terms = [
            terms[child["term_id"]]
            for child in children_by_parent.get(taxonomy["term_taxonomy_id"], [])
            if child.get("term_id") in terms
        ]
        child_links = ""
        if child_terms:
            child_links = "<h2>Onderliggende overzichten</h2><ul>" + "".join(
                f'<li><a href="{html.escape(TAXONOMY_PREFIXES[taxonomy_name] + child["slug"] + "/")}">{html.escape(child["name"])}</a></li>'
                for child in sorted(child_terms, key=lambda t: t["name"].lower())
            ) + "</ul>"
        description = taxonomy.get("description") or ""
        if description:
            intro_text = description
        else:
            intro_text = (
                f"Overzicht van examenstof en kerndoelen voor {term['name']}."
            )
        intro = f"<p>{html.escape(intro_text)}</p>"
        plain_text = clean_text(" ".join([intro_text, " ".join(p["title"] for p in related_pages)]))
        page = {
            "id": f'taxonomy:{taxonomy["term_taxonomy_id"]}',
            "type": taxonomy_name,
            "typeLabel": "Overzicht",
            "title": term["name"],
            "url": url,
            "slugSegments": slug_segments(url),
            "slugParam": slug_param(url),
            "date": "",
            "modified": "",
            "seoTitle": term["name"],
            "description": clean_text(description),
            "html": f"{intro}{child_links}<h2>Examenstof</h2>{html_link_list(related_pages)}",
            "plainText": plain_text,
            "conversionNotes": []
        }
        pages.append(page)
        existing_urls.add(url)

    pages_by_url = {page["url"]: page for page in pages}
    kb_overviews = sorted_pages(page for page in pages if page.get("type") == "ht_kb_category")

    root_page = pages_by_url.get("/")
    if root_page:
        root_page["title"] = "Maatschappijkunde.nl"
        root_page["seoTitle"] = "Maatschappijkunde.nl"
        root_page["description"] = "Examenstof, kerndoelen, begrippen en downloads voor maatschappijkunde en maatschappijleer."
        root_page["html"] = build_homepage(kb_overviews, pages_by_url)
        root_page["plainText"] = clean_text(root_page["html"])

    over_page = pages_by_url.get("/over/")
    if over_page:
        over_page["description"] = "Herkomst van de inhoud op Maatschappijkunde.nl."
        over_page["html"] = build_over_page()
        over_page["plainText"] = clean_text(over_page["html"])

    glossary_page = pages_by_url.get("/begrippen/")
    if glossary_page:
        glossary_page["description"] = "Alle begrippen uit de lesstof, gekoppeld aan Schoolwoorden.nl."
        glossary_page["html"] = build_glossary_page(glossary_terms)
        glossary_page["plainText"] = clean_text(glossary_page["html"])

    downloads_page = pages_by_url.get("/downloads/")
    if downloads_page:
        downloads_page["description"] = "Downloads voor maatschappijkunde en maatschappijleer."
        downloads_page["html"] = build_downloads_page()
        downloads_page["plainText"] = clean_text(downloads_page["html"])

    def fill_existing_page(url, html_content, plain_text=None):
        page = pages_by_url.get(url)
        if not page or (page.get("html") or "").strip():
            return
        page["html"] = html_content
        page["plainText"] = plain_text if plain_text is not None else clean_text(html_content)

    def word_count(page):
        text = (page.get("plainText") or clean_text(page.get("html") or "")).strip()
        return len(text.split()) if text else 0

    def enhance_short_page(url, html_content, plain_text=None, force=False):
        page = pages_by_url.get(url)
        if not page or (not force and word_count(page) >= 30):
            return
        existing_html = (page.get("html") or "").strip()
        if force:
            existing_html = re.sub(
                r"<h2>Examenstof</h2><p>Voor dit overzicht zijn nog geen gekoppelde artikelen gevonden\.</p>",
                "",
                existing_html
            )
        page["html"] = f"{existing_html}{html_content}" if existing_html else html_content
        page["plainText"] = plain_text if plain_text is not None else clean_text(page["html"])

    def pages_matching(*needles):
        matched = []
        for page in pages:
            haystack = f'{page.get("url", "")} {page.get("title", "")}'.lower()
            if any(needle in haystack for needle in needles):
                matched.append(page)
        return sorted_pages(matched)

    overview_links = html_link_list(kb_overviews)
    examenstof_page = pages_by_url.get("/examenstof/")
    if examenstof_page:
        examenstof_page["description"] = "Examenstof gegroepeerd per vak en onderwerp."
        examenstof_page["html"] = build_examenstof_page(kb_overviews, pages_by_url)
        examenstof_page["plainText"] = clean_text(examenstof_page["html"])
    fill_existing_page(
        "/kerndoelen/",
        "<p>Alle kerndoelen en examenonderwerpen zijn hieronder als overzicht beschikbaar.</p>"
        "<h2>Kerndoeloverzichten</h2>"
        f"{overview_links}"
    )

    mens_en_werk = pages_by_url.get("/kerndoelen/mensenwerk/")
    if mens_en_werk:
        fill_existing_page(
            "/examenstof/mens-en-werk/",
            mens_en_werk.get("html") or "",
            mens_en_werk.get("plainText") or ""
        )

    category_fallbacks = {
        "/category/amv/": ("/kerndoelen/amv/", "Analyse Maatschappelijk Vraagstuk"),
        "/category/criminaliteitenrechtsstaat/": ("/kerndoelen/criminaliteit-en-rechtsstaat/", "Criminaliteit en Rechtsstaat"),
        "/category/massamedia/": ("/kerndoelen/massamedia/", "Massamedia"),
        "/category/mens-en-werk/": ("/kerndoelen/mensenwerk/", "Mens en Werk"),
        "/category/politiekenbeleid/": ("/kerndoelen/politiekenbeleid/", "Politiek en Beleid"),
    }
    for category_url, (overview_url, title) in category_fallbacks.items():
        overview = pages_by_url.get(overview_url)
        if not overview:
            continue
        enhance_short_page(
            category_url,
            f"<p>Examenstof en kerndoelen voor {html.escape(title)}.</p>"
            f'<p><a href="{html.escape(overview_url)}">Bekijk het volledige kerndoeloverzicht voor {html.escape(title)}</a>.</p>'
            f"{overview.get('html') or ''}",
            clean_text(f"{title} categorie overzicht {overview.get('plainText') or ''}"),
            force=True
        )

    enhance_short_page(
        "/category/examenstof/",
        "<p>Archief met verwijzingen rond examenstof.</p>"
        f"{overview_links}",
        force=True
    )
    enhance_short_page(
        "/category/multiculti/",
        "<p>Examenstof over de multiculturele samenleving.</p>"
        f"{pages_by_url.get('/kerndoelen/multiculturelesamenleving/', {}).get('html') or ''}",
        force=True
    )
    enhance_short_page(
        "/category/featured/",
        "<p>Uitgelichte verwijzingen naar examenstof, kerndoelen, begrippen en downloads.</p>"
        f"{html_link_list(pages_matching('/examenstof/', '/kerndoelen/', '/begrippen/', '/downloads/'))}",
        force=True
    )

    for tag_url, label in {
        "/kerndoel-tags/leerjaar-3/": "leerjaar 3",
        "/kerndoel-tags/leerjaar-4/": "leerjaar 4",
    }.items():
        enhance_short_page(
            tag_url,
            f"<p>Examenstof voor {html.escape(label)}.</p>"
            f"{overview_links}",
            force=True
        )

    enhance_short_page(
        "/examenstof-2/",
        "<p>Kennisbankarchief voor examenstof.</p>"
        f"{overview_links}"
    )
    enhance_short_page(
        "/contact-support/",
        "<p>Inhoudelijke navigatie naar examenstof, kerndoelen, begrippen en overige informatiepagina's.</p>"
        f"{html_link_list(pages_matching('/examenstof/', '/kerndoelen/', '/begrippen/', '/over/'))}"
    )
    enhance_short_page(
        "/leertips/",
        "<p>Leertips en hulpmiddelen voor maatschappijleer en maatschappijkunde.</p>"
        f"{overview_links}"
    )
    enhance_short_page(
        "/websites/",
        "<p>Handige websites en verwijzingen voor maatschappijleer en maatschappijkunde.</p>"
        f"{html_link_list(pages_matching('/examenstof/', '/kerndoelen/', '/begrippen/'))}"
    )

    for page in pages:
        page["html"] = clean_empty_legacy_wrappers(canonicalize_schoolwoorden_links(convert_strong_lists(improve_readability(apply_text_corrections(remove_youtube(page.get("html") or ""))))))
        page["description"] = clean_text(apply_text_corrections(page.get("description") or ""))
        page["plainText"] = clean_text(page["html"])

    pages.sort(key=lambda p: (p["url"] != "/", p["url"]))
    (SITE / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / "redirects.json").write_text(json.dumps(redirects, ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / "schoolwoorden-glossary-match-summary.json").write_text(json.dumps({
        "glossary_terms": len(glossary_terms),
        "linked_schoolwoorden_urls": sum(1 for term in glossary_terms if term.get("schoolwoordenUrl")),
        "matched_schoolwoorden_sitemap_urls": sum(1 for term in glossary_terms if term.get("matchedSitemap")),
        "unmatched_terms": [
            {"title": term["title"], "legacyUrl": term["legacyUrl"]}
            for term in glossary_terms
            if not term.get("schoolwoordenUrl")
        ],
        "linked_from_existing_redirect": [
            {"title": term["title"], "legacyUrl": term["legacyUrl"], "schoolwoordenUrl": term["schoolwoordenUrl"]}
            for term in glossary_terms
            if term.get("schoolwoordenUrl") and not term.get("matchedSitemap")
        ]
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_redirect_files(redirects)
    print(json.dumps({"pages": len(pages), "redirects": len(redirects)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
