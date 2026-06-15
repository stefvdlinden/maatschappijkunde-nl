import fs from 'node:fs';
import path from 'node:path';

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
const urls = pages
  .filter((page) => page && typeof page.url === 'string')
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

const seoRedirects = [
  '# SEO cleanup for Cloudflare Pages',
  '/home / 301',
  '/home/ / 301',
  '/index.html / 301',
  '/sitemap /sitemap.xml 301',
  '/sitemap/ /sitemap.xml 301',
  '/sitemap_index.xml /sitemap.xml 301',
  '/wp-sitemap.xml /sitemap.xml 301',
  '/feed/ / 301',
  '/comments/feed/ / 301',
  '/*/feed/ /:splat/ 301'
];

const seenSources = new Set();
const mergedRedirects = [];
for (const line of [...seoRedirects, ...existingRedirects]) {
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

console.log(JSON.stringify({
  canonical: SITE_ORIGIN,
  sitemapUrls: urls.length,
  wrote: [
    'dist/sitemap.xml',
    'dist/sitemap-index.xml',
    'dist/robots.txt',
    'dist/_redirects'
  ]
}, null, 2));
