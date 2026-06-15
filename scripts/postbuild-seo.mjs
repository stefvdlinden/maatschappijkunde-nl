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
const writeText = (file, content) => { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, content, 'utf8'); };
if (!fs.existsSync(DIST)) throw new Error('dist directory is missing.');
if (!fs.existsSync(PAGES_JSON)) throw new Error('data/site/pages.json is missing.');
const pages = JSON.parse(readText(PAGES_JSON));
const urls = pages.filter((p) => p && typeof p.url === 'string').filter((p) => !p.url.includes('/feed/')).map((p) => ({ loc: absoluteUrl(p.url), lastmod: toDate(p.modified || p.date || '') })).sort((a,b)=>a.loc.localeCompare(b.loc));
const urlset=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',...urls.map((i)=>`  <url>\n    <loc>${xmlEscape(i.loc)}</loc>${i.lastmod?`\n    <lastmod>${xmlEscape(i.lastmod)}</lastmod>`:''}\n  </url>`),'</urlset>',''].join('\n');
writeText(path.join(DIST,'sitemap.xml'),urlset);
writeText(path.join(DIST,'sitemap-index.xml'),['<?xml version="1.0" encoding="UTF-8"?>','<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">','  <sitemap>',`    <loc>${SITE_ORIGIN}/sitemap.xml</loc>`,'  </sitemap>','</sitemapindex>',''].join('\n'));
