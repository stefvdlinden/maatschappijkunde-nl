import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));

const readCsv = (path) => {
  const text = readFileSync(path, 'utf8').trim();
  const rows = [];
  let row = [];
  let value = '';
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];
    if (quoted && char === '"' && next === '"') {
      value += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (!quoted && char === ',') {
      row.push(value);
      value = '';
    } else if (!quoted && (char === '\n' || char === '\r')) {
      if (char === '\r' && next === '\n') index += 1;
      row.push(value);
      rows.push(row);
      row = [];
      value = '';
    } else {
      value += char;
    }
  }
  row.push(value);
  rows.push(row);

  const [fields, ...records] = rows;
  return records
    .filter((record) => record.length > 1)
    .map((record) => Object.fromEntries(fields.map((field, index) => [field, record[index] || ''])));
};

const writeCsv = (path, rows, fields) => {
  const escape = (value) => `"${String(value ?? '').replaceAll('"', '""')}"`;
  const csv = [
    fields.join(','),
    ...rows.map((row) => fields.map((field) => escape(row[field])).join(','))
  ].join('\n');
  writeFileSync(path, `${csv}\n`);
};

const sitemapRows = readCsv(join(root, 'data/generated/sitemap-urls.csv'));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));
const redirects = JSON.parse(readFileSync(join(root, 'data/site/redirects.json'), 'utf8'));

const pagesByUrl = new Map(pages.map((page) => [page.url, page]));
const redirectsBySource = new Map(redirects.map((redirect) => [redirect.source, redirect]));

const rows = sitemapRows.map((row) => {
  const page = pagesByUrl.get(row.path);
  const redirect = redirectsBySource.get(row.path);
  const status = page ? 'page' : redirect ? 'redirect' : 'missing';
  return {
    sitemap: row.sitemap,
    url: row.url,
    path: row.path,
    images: row.images,
    lastmod: row.lastmod,
    status,
    title: page?.title || '',
    redirect_status: redirect?.status || '',
    redirect_target: redirect?.target || ''
  };
});

const bySitemap = new Map();
for (const row of rows) {
  const bucket = bySitemap.get(row.sitemap) || {
    sitemap: row.sitemap,
    total: 0,
    pages: 0,
    redirects: 0,
    missing: 0
  };
  bucket.total += 1;
  if (row.status === 'page') bucket.pages += 1;
  if (row.status === 'redirect') bucket.redirects += 1;
  if (row.status === 'missing') bucket.missing += 1;
  bySitemap.set(row.sitemap, bucket);
}

const fields = ['sitemap', 'url', 'path', 'images', 'lastmod', 'status', 'title', 'redirect_status', 'redirect_target'];
writeCsv(join(root, 'data/site/sitemap-url-coverage.csv'), rows, fields);

const summary = {
  total_sitemap_urls: rows.length,
  pages: rows.filter((row) => row.status === 'page').length,
  redirects: rows.filter((row) => row.status === 'redirect').length,
  missing: rows.filter((row) => row.status === 'missing').length,
  by_sitemap: [...bySitemap.values()].sort((a, b) => a.sitemap.localeCompare(b.sitemap)),
  missing_urls: rows
    .filter((row) => row.status === 'missing')
    .map((row) => ({ sitemap: row.sitemap, path: row.path, url: row.url })),
  redirected_urls: rows
    .filter((row) => row.status === 'redirect')
    .map((row) => ({
      sitemap: row.sitemap,
      path: row.path,
      target: row.redirect_target,
      status: row.redirect_status
    }))
};

writeFileSync(join(root, 'data/site/sitemap-url-coverage-summary.json'), `${JSON.stringify(summary, null, 2)}\n`);

if (summary.missing > 0) {
  throw new Error(`Sitemap URL coverage found ${summary.missing} missing URL(s). See data/site/sitemap-url-coverage.csv`);
}

console.log(`Sitemap URL coverage ok: ${summary.total_sitemap_urls} sitemap URLs, ${summary.pages} pages, ${summary.redirects} redirects, 0 missing`);
