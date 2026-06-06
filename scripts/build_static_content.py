#!/usr/bin/env python3
import csv
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from inventory import get_columns, iter_insert_rows, clean_text, rel_url  # noqa: E402

SRC = ROOT / "data" / "source"
GENERATED = ROOT / "data" / "generated"
SITE = ROOT / "data" / "site"
PUBLIC = ROOT / "public"
SQL = SRC / "maatsk_nkhniy67.sql"

PUBLIC_TYPES = {"page", "post", "ht_kb", "glossary"}
TYPE_LABELS = {
    "page": "Pagina",
    "post": "Bericht",
    "ht_kb": "Examenstof",
    "glossary": "Begrip"
}
INTERNAL_URL_REWRITES = {
    "/examenstof/kerndoel-1-2/": "/examenstof/politiekenbeleid-kerndoel1-2/",
    "/politiekenbeleid-kerndoel1-2/": "/examenstof/politiekenbeleid-kerndoel1-2/"
}
TAXONOMY_PREFIXES = {
    "ht_kb_category": "/kerndoelen/",
    "ht_kb_tag": "/kerndoel-tags/",
    "category": "/category/"
}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def attrs_to_dict(raw):
    attrs = {}
    for key, _, value1, value2, value3 in re.findall(r'([a-zA-Z0-9_:-]+)\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s\]]+))', raw or ""):
        attrs[key] = html.unescape(value1.strip("\"'") if value1 else value2 or value3)
    return attrs


def convert_table(match):
    inner = match.group(1)
    rows = []
    for section_name, tag in (("gt_table_heading", "th"), ("gt_table_body", "td")):
        for section in re.findall(rf"\[{section_name}[^\]]*\](.*?)\[/{section_name}\]", inner, flags=re.S | re.I):
            cells = []
            for raw_attrs in re.findall(r"\[gt_table_data([^\]]*)\]", section, flags=re.I):
                attrs = attrs_to_dict(raw_attrs)
                cells.append(f"<{tag}>{html.escape(attrs.get('data', '').strip())}</{tag}>")
            if cells:
                rows.append(f"<tr>{''.join(cells)}</tr>")
    return f"<table><tbody>{''.join(rows)}</tbody></table>" if rows else ""


def strip_wrapping_shortcode(name, css_class, text):
    pattern = re.compile(rf"\[{name}[^\]]*\](.*?)\[/{name}\]", re.S | re.I)
    while pattern.search(text):
        text = pattern.sub(rf'<div class="{css_class}">\1</div>', text)
    text = re.sub(rf"\[{name}[^\]]*/?\]", f'<div class="{css_class}">', text, flags=re.I)
    return text


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

    fusion_count = len(re.findall(r"\[fusion_code[^\]]*\].*?\[/fusion_code\]", text, flags=re.S | re.I))
    if fusion_count:
        notes.append(f"{fusion_count} fusion_code shortcode(s) niet blind gerenderd.")
        text = re.sub(r"\[fusion_code[^\]]*\].*?\[/fusion_code\]", '<div class="notice">Ingesloten code moet handmatig worden beoordeeld.</div>', text, flags=re.S | re.I)

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


def clean_wordpress_blocks(content):
    text = content or ""
    text = re.sub(r"<!--\s*/?wp:[^>]*-->", "", text, flags=re.I)
    text = text.replace("<!--more-->", "").replace("<!--noteaser-->", "")
    text = re.sub(
        r"(?<![\"'=])https?://youtu\.be/([A-Za-z0-9_-]+)(?:\?[^<\s]*)?",
        r'<iframe src="https://www.youtube.com/embed/\1" width="560" height="315" frameborder="0" allowfullscreen="allowfullscreen"></iframe>',
        text,
        flags=re.I
    )
    text = re.sub(r'<div class="embed-container embed-responsive embed-responsive-4by3">\s*</div>', "", text)
    return text


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


def main():
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

    meta_keys = {"_yoast_wpseo_title", "_yoast_wpseo_metadesc"}
    meta_by_post = {}
    for row in iter_insert_rows(SQL, "wp_postmeta", meta_cols):
        if row.get("meta_key") in meta_keys:
            meta_by_post.setdefault(str(row.get("post_id")), {})[row.get("meta_key")] = row.get("meta_value") or ""

    redirects = read_csv(GENERATED / "redirects.csv")
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
        converted = clean_wordpress_blocks(converted)
        title = clean_text(post.get("post_title") or "") or "Zonder titel"
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
        intro = f"<p>{html.escape(description)}</p>" if description else ""
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
            "plainText": clean_text(description + " " + " ".join(p["title"] for p in related_pages)),
            "conversionNotes": []
        }
        pages.append(page)
        existing_urls.add(url)

    pages.sort(key=lambda p: (p["url"] != "/", p["url"]))
    (SITE / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / "redirects.json").write_text(json.dumps(redirects, ensure_ascii=False, indent=2), encoding="utf-8")

    netlify_lines = [f'{r["source"]} {r["target"]} {r["status"]}' for r in redirects]
    (SITE / "_redirects").write_text("\n".join(netlify_lines) + "\n", encoding="utf-8")
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "_redirects").write_text("\n".join(netlify_lines) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(pages), "redirects": len(redirects)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
