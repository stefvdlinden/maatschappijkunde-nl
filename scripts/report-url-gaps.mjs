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
  return records.filter((record) => record.length > 1).map((record) => Object.fromEntries(fields.map((field, index) => [field, record[index] || ''])));
};

const writeCsv = (path, rows, fields) => {
  const escape = (value) => `"${String(value ?? '').replaceAll('"', '""')}"`;
  const csv = [
    fields.join(','),
    ...rows.map((row) => fields.map((field) => escape(row[field])).join(','))
  ].join('\n');
  writeFileSync(path, `${csv}\n`);
};

const rows = readCsv(join(root, 'data/generated/url-inventory.csv'));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));
const redirects = JSON.parse(readFileSync(join(root, 'data/site/redirects.json'), 'utf8'));
const pageUrls = new Set(pages.map((page) => page.url));
const redirectSources = new Set(redirects.map((redirect) => redirect.source));
const gaps = rows
  .filter((row) => row.advice.startsWith('investigate'))
  .filter((row) => !pageUrls.has(row.url) && !redirectSources.has(row.url))
  .sort((a, b) => Number(b.analytics_views || 0) - Number(a.analytics_views || 0));

const fields = ['url', 'in_sitemap', 'sitemap', 'lastmod', 'analytics_rank', 'analytics_views', 'advice'];
writeCsv(join(root, 'data/site/url-gaps.csv'), gaps, fields);

const summary = {
  total_gaps: gaps.length,
  sitemap_gaps: gaps.filter((row) => row.in_sitemap === 'yes').length,
  analytics_gaps: gaps.filter((row) => Number(row.analytics_views || 0) > 0).length,
  top_analytics_gaps: gaps
    .filter((row) => Number(row.analytics_views || 0) > 0)
    .slice(0, 15)
    .map((row) => ({
      url: row.url,
      rank: Number(row.analytics_rank || 0),
      views: Number(row.analytics_views || 0),
      advice: row.advice
    }))
};

writeFileSync(join(root, 'data/site/url-gaps-summary.json'), `${JSON.stringify(summary, null, 2)}\n`);
console.log(`URL gap report: ${summary.total_gaps} investigate URLs (${summary.analytics_gaps} with analytics, ${summary.sitemap_gaps} in sitemap)`);
