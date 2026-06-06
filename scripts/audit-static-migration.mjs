import assert from 'node:assert/strict';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));
const redirects = JSON.parse(readFileSync(join(root, 'data/site/redirects.json'), 'utf8'));

const uploadRefPattern = /(?:href|src)=["']([^"']*\/wp-content\/uploads\/[^"']+)["']/gi;
const shortcodePattern = /\[\/?([a-zA-Z0-9_:-]+)(?:\s|\]|\/)/g;
const rows = [];
const missing = [];
const shortcodeCounts = new Map();

for (const page of pages) {
  const html = page.html || '';
  for (const match of html.matchAll(uploadRefPattern)) {
    const assetUrl = match[1];
    const path = assetUrl.replace(/^https?:\/\/(?:www\.)?maatschappijkunde\.nl/i, '');
    const publicPath = join(root, 'public', path);
    const exists = existsSync(publicPath);
    const row = { page: page.url, asset: path, status: exists ? 'ok' : 'missing' };
    rows.push(row);
    if (!exists) missing.push(row);
  }
  for (const match of html.matchAll(shortcodePattern)) {
    shortcodeCounts.set(match[1], (shortcodeCounts.get(match[1]) || 0) + 1);
  }
}

const csv = [
  'page,asset,status',
  ...rows.map((row) => [row.page, row.asset, row.status].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');
writeFileSync(join(root, 'data/site/asset-audit.csv'), `${csv}\n`);

const shortcodeRows = [...shortcodeCounts.entries()].sort((a, b) => b[1] - a[1]).map(([shortcode, count]) => ({ shortcode, count }));
writeFileSync(join(root, 'data/site/unresolved-shortcodes.json'), `${JSON.stringify(shortcodeRows, null, 2)}\n`);

const redirectSources = new Set(redirects.map((redirect) => redirect.source));
assert(!redirectSources.has('/begrippen/'), '/begrippen/ should remain a static overview, not a redirect');
assert.equal(missing.length, 0, `Missing local upload assets: ${missing.slice(0, 10).map((row) => `${row.page} -> ${row.asset}`).join('; ')}`);

console.log(`Asset audit ok: ${rows.length} upload references, ${missing.length} missing, ${shortcodeRows.length} unresolved shortcode types`);
