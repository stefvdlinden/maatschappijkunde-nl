import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));
const redirects = JSON.parse(readFileSync(join(root, 'data/site/redirects.json'), 'utf8'));

const pageUrls = new Set(pages.map((page) => page.url));
const seenSources = new Map();
const rows = [];

const isPath = (value) => value.startsWith('/') && !value.startsWith('//');
const hasTrailingSlash = (value) => value === '/' || value.endsWith('/');

for (const redirect of redirects) {
  const source = redirect.source || '';
  const target = redirect.target || '';
  const status = String(redirect.status || '');

  if (seenSources.has(source)) {
    rows.push({ source, target, status, issue: `duplicate_source:first_seen_line_${seenSources.get(source)}` });
  } else {
    seenSources.set(source, redirect.line || '');
  }

  if (!['301', '302', '307', '308'].includes(status)) {
    rows.push({ source, target, status, issue: 'invalid_status' });
  }

  if (!isPath(source)) {
    rows.push({ source, target, status, issue: 'invalid_source_path' });
  }

  if (isPath(source) && !hasTrailingSlash(source)) {
    rows.push({ source, target, status, issue: 'source_without_trailing_slash' });
  }

  if (pageUrls.has(source)) {
    rows.push({ source, target, status, issue: 'source_conflicts_with_static_page' });
  }

  if (!isPath(target)) {
    try {
      const url = new URL(target);
      if (url.protocol !== 'https:') {
        rows.push({ source, target, status, issue: 'insecure_external_target' });
      }
    } catch {
      rows.push({ source, target, status, issue: 'invalid_target' });
    }
  }
}

const csv = [
  'source,target,status,issue',
  ...rows.map((row) => [row.source, row.target, row.status, row.issue].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');
writeFileSync(join(root, 'data/site/redirect-audit.csv'), `${csv}\n`);
writeFileSync(join(root, 'data/site/redirect-audit-summary.json'), `${JSON.stringify({
  total_redirects: redirects.length,
  total_issues: rows.length,
  issues: rows
}, null, 2)}\n`);

if (rows.length > 0) {
  throw new Error(`Redirect audit found ${rows.length} issue(s). See data/site/redirect-audit.csv`);
}

console.log(`Redirect audit ok: ${redirects.length} redirects, 0 issues`);
