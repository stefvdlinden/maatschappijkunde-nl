import { readFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalOverrides } from '../lib/canonical-overrides.js';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));
const byUrl = new Map(pages.map((page) => [page.url, page]));
const issues = [];

for (const [source, target] of Object.entries(canonicalOverrides)) {
  if (!byUrl.has(source)) issues.push(`${source}: source page does not exist`);
  if (!byUrl.has(target)) issues.push(`${source}: canonical target ${target} does not exist`);
  if (target in canonicalOverrides) issues.push(`${source}: canonical target ${target} is itself overridden`);
  if (source === target) issues.push(`${source}: canonical points to itself`);
}

const sitemapPath = join(root, 'dist', 'sitemap.xml');
if (existsSync(sitemapPath)) {
  const sitemap = readFileSync(sitemapPath, 'utf8');
  for (const source of Object.keys(canonicalOverrides)) {
    if (sitemap.includes(`<loc>https://maatschappijkunde.nl${source}</loc>`)) issues.push(`${source}: still in sitemap`);
  }
}

if (issues.length) {
  console.error(issues.join('\n'));
  throw new Error(`Canonical override test found ${issues.length} issue(s).`);
}
console.log(`Canonical overrides ok: ${Object.keys(canonicalOverrides).length} duplicate pages point to their primary page`);
