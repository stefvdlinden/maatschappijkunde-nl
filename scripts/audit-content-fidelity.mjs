import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));

const rows = [];

for (const page of pages) {
  const html = String(page.html || '').trim();
  const plainText = String(page.plainText || '').trim();
  const wordCount = plainText ? plainText.split(/\s+/).length : 0;

  if (!String(page.title || '').trim()) {
    rows.push({ page: page.url, title: page.title, issue: 'missing_title', severity: 'high', detail: '' });
  }
  if (!html) {
    rows.push({ page: page.url, title: page.title, issue: 'empty_html', severity: 'medium', detail: `${wordCount} words` });
  } else if (wordCount < 30 && !html.includes('legacy-module-list')) {
    rows.push({ page: page.url, title: page.title, issue: 'short_content', severity: 'low', detail: `${wordCount} words` });
  }
}

const csv = [
  'page,title,issue,severity,detail',
  ...rows.map((row) => [row.page, row.title, row.issue, row.severity, row.detail].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');
writeFileSync(join(root, 'data/site/content-fidelity-audit.csv'), `${csv}\n`);
writeFileSync(join(root, 'data/site/content-fidelity-audit-summary.json'), `${JSON.stringify({
  total_issues: rows.length,
  high_issues: rows.filter((row) => row.severity === 'high').length,
  medium_issues: rows.filter((row) => row.severity === 'medium').length,
  low_issues: rows.filter((row) => row.severity === 'low').length,
  issues: rows
}, null, 2)}\n`);

const high = rows.filter((row) => row.severity === 'high');
if (high.length > 0) {
  throw new Error(`Content fidelity audit found ${high.length} high issue(s). See data/site/content-fidelity-audit.csv`);
}

console.log(`Content fidelity audit report: ${rows.length} issue rows, ${high.length} high`);
