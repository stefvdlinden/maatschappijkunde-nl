import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const readJson = (path) => JSON.parse(readFileSync(new URL(path, import.meta.url), 'utf8'));
const readCsv = (path) => {
  const text = readFileSync(new URL(path, import.meta.url), 'utf8').trim();
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
  return records.filter((record) => record.length > 1).map((record) => Object.fromEntries(fields.map((field, index) => [field, record[index] || ''])));
};

const pages = readJson('../data/site/pages.json');
const redirects = readJson('../data/site/redirects.json');
const urlInventory = readCsv('../data/generated/url-inventory.csv');
const pageUrls = new Set(pages.map((page) => page.url));
const redirectSources = new Set(redirects.map((redirect) => redirect.source));

for (const row of urlInventory) {
  const url = row.url;
  if (!url) continue;
  if (row.advice === 'preserve as static page') {
    assert(pageUrls.has(url), `Expected static page for ${url}`);
  }
  if (row.advice === 'keep redirect') {
    assert(redirectSources.has(url), `Expected redirect for ${url}`);
  }
  const hasTraffic = Number(row.analytics_views || 0) > 0;
  if (row.in_sitemap === 'yes' || hasTraffic) {
    assert(pageUrls.has(url) || redirectSources.has(url) || row.advice.startsWith('investigate'), `Uncovered known URL ${url}`);
  }
}

assert(pageUrls.has('/'), 'Root URL should be generated');
console.log(`URL coverage ok: ${pageUrls.size} pages, ${redirectSources.size} redirects`);
