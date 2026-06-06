import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));

const checks = [
  { name: 'replacement_character', pattern: /�/g },
  { name: 'question_mark_run', pattern: /\?{3,}/g },
  { name: 'mojibake_sequence', pattern: /(?:Ã.|Â.|â[^\s<]*)/g }
];

const fields = ['title', 'seoTitle', 'description', 'html', 'plainText'];
const rows = [];

for (const page of pages) {
  for (const field of fields) {
    const value = String(page[field] || '');
    for (const check of checks) {
      const matches = value.match(check.pattern) || [];
      if (matches.length > 0) {
        rows.push({
          page: page.url,
          title: page.title,
          field,
          issue: check.name,
          count: matches.length,
          sample: matches.slice(0, 3).join(' ')
        });
      }
    }
  }
}

const csv = [
  'page,title,field,issue,count,sample',
  ...rows.map((row) => [row.page, row.title, row.field, row.issue, row.count, row.sample].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');
writeFileSync(join(root, 'data/site/visible-artifacts-audit.csv'), `${csv}\n`);
writeFileSync(join(root, 'data/site/visible-artifacts-audit-summary.json'), `${JSON.stringify({ total_issues: rows.length, issues: rows }, null, 2)}\n`);

if (rows.length > 0) {
  throw new Error(`Visible artifact audit found ${rows.length} issue(s). See data/site/visible-artifacts-audit.csv`);
}

console.log('Visible artifact audit ok: 0 issue rows');
