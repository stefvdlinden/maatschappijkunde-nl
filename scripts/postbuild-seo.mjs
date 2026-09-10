import fs from 'node:fs';
import path from 'node:path';
import { seoRedirects } from '../lib/seo-redirects.js';

const ROOT = process.cwd();
const DIST = path.join(ROOT, 'dist');
const PAGES_JSON = path.join(ROOT, 'data', 'site', 'pages.json');
const SITE_ORIGIN = 'https://maatschappijkunde.nl';

const xmlEscape = (value = '') => String(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&apos;');

const normalizePath = (url = '/') => {
  if (!url || url === '/') return '/';
  const pathname = url.startsWith('/') ? url : `/${url}`;
  return pathname.endsWith('/') ? pathname : `${pathname}/`;
};

const absoluteUrl = (url = '/') => `${SITE_ORIGIN}${normalizePath(url)}`;

const toDate = (value = '') => {
  const match = String(value).match(/^\d{4}-\d{2}-\d{2}/);
  return match ? match[0] : '';
};

const readText = (file) => fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';

const writeText = (file, content) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content, 'utf8');
};

if (!fs.existsSync(DIST)) {
  throw new Error('dist directory is missing. Run this script after astro build.');
}

if (!fs.existsSync(PAGES_JSON)) {
  throw new Error('data/site/pages.json is missing. Run npm run prepare:content first.');
}

const pages = JSON.parse(readText(PAGES_JSON));
const redirectSources = new Set(seoRedirects.map(([source]) => source));
const urls = pages
  .filter((page) => page && typeof page.url === 'string')
  .filter((page) => !redirectSources.has(page.url))
  .filter((page) => !page.url.includes('/feed/'))
  .map((page) => ({
    loc: absoluteUrl(page.url),
    lastmod: toDate(page.modified || page.date || '')
  }))
  .sort((a, b) => a.loc.localeCompare(b.loc));

const urlset = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...urls.map((item) => {
    const lastmod = item.lastmod ? `\n    <lastmod>${xmlEscape(item.lastmod)}</lastmod>` : '';
    return `  <url>\n    <loc>${xmlEscape(item.loc)}</loc>${lastmod}\n  </url>`;
  }),
  '</urlset>',
  ''
].join('\n');

writeText(path.join(DIST, 'sitemap.xml'), urlset);

for (const file of fs.readdirSync(DIST)) {
  if (/^sitemap-\d+\.xml$/i.test(file)) {
    fs.unlinkSync(path.join(DIST, file));
  }
}

const sitemapIndex = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  '  <sitemap>',
  `    <loc>${xmlEscape(`${SITE_ORIGIN}/sitemap.xml`)}</loc>`,
  '  </sitemap>',
  '</sitemapindex>',
  ''
].join('\n');

writeText(path.join(DIST, 'sitemap-index.xml'), sitemapIndex);

const robotsPath = path.join(DIST, 'robots.txt');
const existingRobots = readText(robotsPath).trim();
const robotsLines = existingRobots
  ? existingRobots.split(/\r?\n/).filter((line) => !/^\s*Sitemap:/i.test(line))
  : ['User-agent: *', 'Allow: /'];
robotsLines.push(`Sitemap: ${SITE_ORIGIN}/sitemap.xml`);
writeText(robotsPath, `${robotsLines.join('\n')}\n`);

const redirectsPath = path.join(DIST, '_redirects');
const existingRedirects = readText(redirectsPath)
  .split(/\r?\n/)
  .map((line) => line.trim())
  .filter(Boolean);

const seenSources = new Set();
const mergedRedirects = [];
for (const line of [...seoRedirects.map((rule) => rule.join(' ')), ...existingRedirects]) {
  if (line.startsWith('#')) {
    mergedRedirects.push(line);
    continue;
  }
  const source = line.split(/\s+/)[0];
  if (seenSources.has(source)) continue;
  seenSources.add(source);
  mergedRedirects.push(line);
}

writeText(redirectsPath, `${mergedRedirects.join('\n')}\n`);

const headersPath = path.join(DIST, '_headers');
writeText(headersPath, [
  '/*',
  '  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload',
  '  X-Content-Type-Options: nosniff',
  ''
].join('\n'));

const htaccessPath = path.join(DIST, '.htaccess');
if (fs.existsSync(htaccessPath)) {
  fs.unlinkSync(htaccessPath);
}

console.log(JSON.stringify({
  canonical: SITE_ORIGIN,
  sitemapUrls: urls.length,
  wrote: [
    'dist/sitemap.xml',
    'dist/sitemap-index.xml',
    'dist/robots.txt',
    'dist/_redirects',
    'dist/_headers'
  ]
}, null, 2));
