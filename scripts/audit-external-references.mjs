import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));

const allowedExternalSrcHosts = new Set([
  'docs.google.com'
]);

const attrPattern = /<(?<tag>[a-z0-9-]+)\b(?<attrs>[^>]*?)>/gi;
const urlAttrPattern = /\b(?<attr>href|src)=["'](?<url>https?:\/\/[^"']+)["']/gi;

const rows = [];

const getAttribute = (attrs, name) => {
  const match = attrs.match(new RegExp(`\\b${name}=["']([^"']*)["']`, 'i'));
  return match ? match[1] : '';
};

for (const page of pages) {
  const html = page.html || '';
  for (const tagMatch of html.matchAll(attrPattern)) {
    const tag = tagMatch.groups.tag.toLowerCase();
    const attrs = tagMatch.groups.attrs || '';

    for (const urlMatch of attrs.matchAll(urlAttrPattern)) {
      const attr = urlMatch.groups.attr.toLowerCase();
      const rawUrl = urlMatch.groups.url;
      const url = new URL(rawUrl);

      if (url.protocol !== 'https:') {
        rows.push({ page: page.url, tag, attr, url: rawUrl, issue: 'insecure_external_url' });
      }

      if (attr === 'src' && !allowedExternalSrcHosts.has(url.hostname)) {
        rows.push({ page: page.url, tag, attr, url: rawUrl, issue: 'disallowed_external_src' });
      }

      if (tag === 'a' && attr === 'href' && getAttribute(attrs, 'target') === '_blank') {
        const rel = getAttribute(attrs, 'rel').toLowerCase().split(/\s+/);
        if (!rel.includes('noopener')) {
          rows.push({ page: page.url, tag, attr, url: rawUrl, issue: 'target_blank_without_noopener' });
        }
      }
    }
  }
}

const csv = [
  'page,tag,attr,url,issue',
  ...rows.map((row) => [row.page, row.tag, row.attr, row.url, row.issue].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');
writeFileSync(join(root, 'data/site/external-reference-audit.csv'), `${csv}\n`);
writeFileSync(join(root, 'data/site/external-reference-audit-summary.json'), `${JSON.stringify({
  total_issues: rows.length,
  issues: rows
}, null, 2)}\n`);

if (rows.length > 0) {
  throw new Error(`External reference audit found ${rows.length} issue(s). See data/site/external-reference-audit.csv`);
}

console.log('External reference audit ok: 0 issues');
