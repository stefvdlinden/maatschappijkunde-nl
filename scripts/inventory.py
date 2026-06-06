#!/usr/bin/env python3
import csv, json, os, re, sys, zipfile, html
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data' / 'source'
OUT = ROOT / 'data' / 'generated'
OUT.mkdir(parents=True, exist_ok=True)
SQL = SRC / 'maatsk_nkhniy67.sql'

SELECTED = {'wp_posts','wp_postmeta','wp_terms','wp_term_taxonomy','wp_term_relationships','wp_options'}


def mysql_unescape(s):
    if s is None: return None
    # MySQL dump escape handling sufficient for WordPress text fields.
    repl = {
        r"\\0":"\0", r"\\'":"'", r'\\"':'"', r"\\b":"\b", r"\\n":"\n",
        r"\\r":"\r", r"\\t":"\t", r"\\Z":"\x1a", r"\\\\":"\\"
    }
    # Ordered replacement: double backslash last would be tricky, so parse charwise.
    out=[]; i=0
    while i < len(s):
        if s[i] == '\\' and i+1 < len(s):
            c=s[i+1]
            out.append({'0':'\0',"'":"'",'"':'"','b':'\b','n':'\n','r':'\r','t':'\t','Z':'\x1a','\\':'\\'}.get(c,c))
            i += 2
        else:
            out.append(s[i]); i += 1
    return ''.join(out)


def parse_tuple_values(text):
    rows=[]; row=[]; val=[]; in_str=False; esc=False; in_tuple=False; token_was_quoted=False
    cur_quoted=False
    def finish_value():
        nonlocal val, cur_quoted
        raw=''.join(val)
        if cur_quoted:
            v=mysql_unescape(raw).strip()
        else:
            x=raw.strip()
            if x.upper() == 'NULL': v=None
            else: v=x
        row.append(v); val=[]; cur_quoted=False
    for ch in text:
        if not in_tuple:
            if ch == '(':
                in_tuple=True; row=[]; val=[]; in_str=False; esc=False; cur_quoted=False
            continue
        if in_str:
            if esc:
                val.append('\\'); val.append(ch); esc=False
            elif ch == '\\':
                esc=True
            elif ch == "'":
                in_str=False
            else:
                val.append(ch)
        else:
            if ch == "'":
                in_str=True; cur_quoted=True
            elif ch == ',':
                finish_value()
            elif ch == ')':
                finish_value(); rows.append(row); in_tuple=False
            else:
                val.append(ch)
    return rows


def get_columns(sql_text, table):
    m = re.search(r"CREATE TABLE `"+re.escape(table)+r"` \((.*?)\n\) ENGINE", sql_text, re.S)
    if not m: return []
    cols=[]
    for line in m.group(1).splitlines():
        line=line.strip()
        if line.startswith('`'):
            cols.append(line.split('`',2)[1])
    return cols


def iter_insert_rows(path, table, default_cols):
    # Supports both: INSERT INTO `table` VALUES (...) and
    # INSERT INTO `table` (`a`, `b`) VALUES (...). Dumps often wrap after VALUES.
    start_re = re.compile(r"INSERT INTO `" + re.escape(table) + r"`(?: \((.*?)\))? VALUES\s*")
    buf = ''
    active = False
    active_cols = default_cols
    with path.open('r', encoding='utf-8', errors='replace') as f:
        for line in f:
            if not active:
                m = start_re.match(line)
                if m:
                    active_cols = [c.strip().strip('`') for c in m.group(1).split(',')] if m.group(1) else default_cols
                    buf = line[m.end():]
                    active = not line.rstrip().endswith(';')
                    if not active:
                        data = buf.rstrip().rstrip(';')
                        for vals in parse_tuple_values(data):
                            yield dict(zip(active_cols, vals))
            else:
                buf += line
                if line.rstrip().endswith(';'):
                    data = buf.rstrip().rstrip(';')
                    for vals in parse_tuple_values(data):
                        yield dict(zip(active_cols, vals))
                    buf = ''
                    active = False


def clean_text(s):
    if not s: return ''
    s = html.unescape(s)
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S|re.I)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S|re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\[[^\]]+\]', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def rel_url(post, posts_by_id=None):
    pt=post.get('post_type'); slug=post.get('post_name') or str(post.get('ID'))
    if pt == 'page':
        # reconstruct hierarchical page URLs when possible
        parts=[slug]
        parent=str(post.get('post_parent') or '0')
        seen=set()
        while posts_by_id and parent not in ('0','',None) and parent not in seen and parent in posts_by_id:
            seen.add(parent); p=posts_by_id[parent]; parts.append(p.get('post_name') or str(p.get('ID'))); parent=str(p.get('post_parent') or '0')
        return '/' + '/'.join(reversed([p for p in parts if p])) + '/'
    if pt == 'ht_kb': return f'/examenstof/{slug}/'
    if pt == 'glossary': return f'/begrippen/{slug}/'
    if pt == 'post': return f'/{slug}/'
    if pt == 'attachment': return post.get('guid') or ''
    return f'/{slug}/'


def extract_redirects():
    ht = SRC / 'htaccess.txt'
    rows=[]
    for i,line in enumerate(ht.read_text(encoding='utf-8', errors='replace').splitlines(),1):
        m=re.match(r'\s*Redirect\s+(\d+)\s+(\S+)\s+(\S+)', line)
        if m:
            rows.append({'line':i,'status':m.group(1),'source':m.group(2),'target':m.group(3)})
    write_csv(OUT/'redirects.csv', rows, ['line','status','source','target'])
    return rows


def extract_sitemap():
    rows=[]
    text=(SRC/'sitemap-data.txt').read_text(encoding='utf-8', errors='replace')
    current=''
    for line in text.splitlines():
        line=line.strip().replace('\u2028','')
        if not line: continue
        if line.startswith('https://maatschappijkunde.nl/'):
            parts=line.split()
            url=parts[0]
            if url.endswith('.xml'):
                current=url.rsplit('/',1)[-1]
                continue
            parsed=urlparse(url)
            rows.append({'sitemap':current,'url':url,'path':parsed.path,'images':parts[1] if len(parts)>1 and parts[1].isdigit() else '', 'lastmod':' '.join(parts[2:]) if len(parts)>2 else ''})
    write_csv(OUT/'sitemap-urls.csv', rows, ['sitemap','url','path','images','lastmod'])
    return rows


def extract_analytics():
    # Use pdftotext output if available
    pdf=SRC/'analytics-pages.pdf'
    rows=[]
    txt_path=OUT/'analytics-pages.txt'
    os.system(f"pdftotext -layout '{pdf}' '{txt_path}' >/dev/null 2>&1")
    text=txt_path.read_text(encoding='utf-8', errors='replace') if txt_path.exists() else ''
    lines=text.splitlines()
    # Join line-broken paths: a row number may appear with path, or path may be preceding/following line.
    pending_path=None
    for i,line in enumerate(lines):
        # match normal rows: rank path views (... active users (...
        m=re.match(r'\s*(\d+)\s+(/\S*)\s+([0-9\.]+)\s+\(', line)
        if m:
            rows.append({'rank':int(m.group(1)),'path':m.group(2),'views':int(m.group(3).replace('.',''))})
            continue
        # lines with path split: rank and numbers on next line after path chunks are too messy; collect top 100 names from PDF text list if no views.
    # Fallback: parse bottom list from file_search-like text is not here; keep top normal rows.
    write_csv(OUT/'analytics-top-pages.csv', rows, ['rank','path','views'])
    return rows


def zip_media_inventory():
    zpath=SRC/'uploads.zip'
    rows=[]
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            if info.is_dir(): continue
            ext=Path(info.filename).suffix.lower()
            rows.append({'path':info.filename,'size':info.file_size,'ext':ext})
    write_csv(OUT/'media-files.csv', rows, ['path','size','ext'])
    return rows


def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def main():
    sql_text=SQL.read_text(encoding='utf-8', errors='replace')
    table_rows=[]
    for m in re.finditer(r'CREATE TABLE `([^`]+)`', sql_text):
        table_rows.append({'table':m.group(1)})
    write_csv(OUT/'tables.csv', table_rows, ['table'])

    cols={t:get_columns(sql_text,t) for t in SELECTED}
    posts=[]
    for row in iter_insert_rows(SQL,'wp_posts',cols['wp_posts']):
        posts.append(row)
    posts_by_id={str(p['ID']):p for p in posts}

    # postmeta only selected keys
    meta_keys={'_wp_attached_file','_yoast_wpseo_title','_yoast_wpseo_metadesc','_yoast_wpseo_focuskw','_thumbnail_id'}
    meta_by_post={}
    for row in iter_insert_rows(SQL,'wp_postmeta',cols['wp_postmeta']):
        if row.get('meta_key') in meta_keys:
            meta_by_post.setdefault(str(row.get('post_id')), {})[row.get('meta_key')]=row.get('meta_value')

    content_rows=[]; shortcode_rows=[]
    shortcode_counts={}
    public_types={'page','post','ht_kb','glossary'}
    for p in posts:
        pid=str(p.get('ID'))
        pt=p.get('post_type')
        status=p.get('post_status')
        content=p.get('post_content') or ''
        title=clean_text(p.get('post_title') or '')
        plain=clean_text(content)
        words=len(re.findall(r'\w+', plain, flags=re.U))
        url=rel_url(p, posts_by_id)
        m=meta_by_post.get(pid,{})
        if status=='publish' and pt in public_types:
            content_rows.append({
                'id':pid,'type':pt,'title':title,'slug':p.get('post_name') or '', 'url':url,
                'date':p.get('post_date') or '', 'modified':p.get('post_modified') or '',
                'word_count':words,'yoast_title':m.get('_yoast_wpseo_title',''),'yoast_metadesc':m.get('_yoast_wpseo_metadesc',''),
                'focus_keyword':m.get('_yoast_wpseo_focuskw','')
            })
        found=re.findall(r'\[/?([a-zA-Z0-9_:-]+)(?:\s|\]|/)', content)
        if found and status=='publish' and pt in public_types:
            uniq=sorted(set(found))
            shortcode_rows.append({'id':pid,'type':pt,'title':title,'url':url,'shortcodes':';'.join(uniq)})
            for sc in found: shortcode_counts[sc]=shortcode_counts.get(sc,0)+1
    write_csv(OUT/'content-inventory.csv', content_rows, ['id','type','title','slug','url','date','modified','word_count','yoast_title','yoast_metadesc','focus_keyword'])
    (OUT/'content-inventory.json').write_text(json.dumps(content_rows, ensure_ascii=False, indent=2), encoding='utf-8')
    write_csv(OUT/'shortcode-report.csv', shortcode_rows, ['id','type','title','url','shortcodes'])
    write_csv(OUT/'shortcode-counts.csv', [{'shortcode':k,'count':v} for k,v in sorted(shortcode_counts.items(), key=lambda kv:-kv[1])], ['shortcode','count'])

    # attachments from DB
    attach_rows=[]
    for p in posts:
        if p.get('post_type')=='attachment':
            pid=str(p.get('ID')); m=meta_by_post.get(pid,{})
            attach_rows.append({'id':pid,'title':clean_text(p.get('post_title') or ''),'guid':p.get('guid') or '', 'attached_file':m.get('_wp_attached_file',''), 'mime_type':p.get('post_mime_type') or ''})
    write_csv(OUT/'db-attachments.csv', attach_rows, ['id','title','guid','attached_file','mime_type'])

    redirects=extract_redirects()
    sitemap=extract_sitemap()
    media=zip_media_inventory()
    analytics=extract_analytics()

    # URL action list: combine content/sitemap/redirect/analytics
    url_map={}
    for r in content_rows:
        url_map.setdefault(r['url'],{}).update({'url':r['url'],'content_type':r['type'],'title':r['title'],'source_content':'yes'})
    for r in sitemap:
        url_map.setdefault(r['path'],{}).update({'url':r['path'],'in_sitemap':'yes','sitemap':r['sitemap'],'lastmod':r['lastmod']})
    for r in redirects:
        url_map.setdefault(r['source'],{}).update({'url':r['source'],'redirect_target':r['target'],'redirect_status':r['status']})
    for r in analytics:
        url_map.setdefault(r['path'],{}).update({'url':r['path'],'analytics_rank':r['rank'],'analytics_views':r['views']})
    rows=[]
    for url, v in sorted(url_map.items()):
        has_content=v.get('source_content')=='yes'; has_redirect='redirect_target' in v; in_sitemap=v.get('in_sitemap')=='yes'; views=int(v.get('analytics_views') or 0)
        if has_redirect: advice='keep redirect'
        elif has_content: advice='preserve as static page'
        elif in_sitemap: advice='investigate - sitemap URL not matched to extracted content'
        elif views: advice='investigate - analytics URL not matched to extracted content'
        else: advice='investigate'
        v.setdefault('content_type',''); v.setdefault('title',''); v.setdefault('source_content',''); v.setdefault('in_sitemap',''); v.setdefault('sitemap',''); v.setdefault('lastmod',''); v.setdefault('redirect_status',''); v.setdefault('redirect_target',''); v.setdefault('analytics_rank',''); v.setdefault('analytics_views',''); v['advice']=advice
        rows.append(v)
    fields=['url','content_type','title','source_content','in_sitemap','sitemap','lastmod','redirect_status','redirect_target','analytics_rank','analytics_views','advice']
    write_csv(OUT/'url-inventory.csv', rows, fields)

    summary={
        'tables': len(table_rows),
        'public_content_items': len(content_rows),
        'public_by_type': {t:sum(1 for r in content_rows if r['type']==t) for t in sorted(public_types)},
        'attachments_in_db': len(attach_rows),
        'media_files_in_uploads_zip': len(media),
        'redirects_in_htaccess': len(redirects),
        'sitemap_urls': len(sitemap),
        'analytics_rows_parsed': len(analytics),
        'shortcode_rows': len(shortcode_rows),
        'top_shortcodes': sorted(shortcode_counts.items(), key=lambda kv:-kv[1])[:20]
    }
    (OUT/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
