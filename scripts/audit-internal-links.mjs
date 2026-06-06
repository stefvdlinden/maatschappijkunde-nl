import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));
const redirects = JSON.parse(readFileSync(join(root, 'data/site/redirects.json'), 'utf8'));

const pageUrls = new Set(pages.map((page) => page.url));
const redirectSources = new Set(redirects.map((redirect) => redirect.source));

const normalizePath = (raw) => {
  try {
    const url = raw.startsWith('http') ? new URL(raw) : new URL(raw, 'https://maatschappijkunde.nl');
    if (!['maatschappijkunde.nl', 'www.maatschappijkunde.nl'].includes(url.hostname)) return null;
    if (url.pathname.startsWith('/wp-content/uploads/')) return null;
    let path = url.pathname || '/';
    if (!path.endsWith('/')) path += '/';
    return path;
  } catch {
    return null;
  }
};

const linkPattern = /href=["']([^"']+)["']/gi;
const rows = [];
for (const page of pages) {
  const html = page.html || '';
  for (const match of html.matchAll(linkPattern)) {
    const href = match[1];
    if (href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) continue;
    const path = normalizePath(href);
    if (!path) continue;
    let status = 'missing';
    if (pageUrls.has(path)) status = 'page';
    else if (redirectSources.has(path)) status = 'redirect';
    rows.push({ page: page.url, href, normalized: path, status });
  }
}

const missing = rows.filter((row) => row.status === 'missing');
const csv = [
  'page,href,normalized,status',
  ...rows.map((row) => [row.page, row.href, row.normalized, row.status].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');
writeFileSync(join(root, 'data/site/internal-link-audit.csv'), `${csv}\n`);
writeFileSync(join(root, 'data/site/internal-link-audit-summary.json'), `${JSON.stringify({
  total_internal_links: rows.length,
  missing_links: missing.length,
  redirect_links: rows.filter((row) => row.status === 'redirect').length,
  page_links: rows.filter((row) => row.status === 'page').length,
  missing: missing
}, null, 2)}\n`);

if (missing.length > 0) {
  throw new Error(`Internal link audit found ${missing.length} missing link(s). See data/site/internal-link-audit.csv`);
}

console.log(`Internal link audit ok: ${rows.length} links, ${missing.length} missing`);
