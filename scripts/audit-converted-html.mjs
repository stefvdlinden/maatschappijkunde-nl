import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = JSON.parse(readFileSync(join(root, 'data/site/pages.json'), 'utf8'));

const checks = [
  { name: 'wordpress_block_comment', pattern: /<!--\s*\/?wp:/i, severity: 'high' },
  { name: 'legacy_shortcode', pattern: /\[\/?[a-zA-Z0-9_:-]+(?:\s|\]|\/)/, severity: 'high' },
  { name: 'youtube_reference', pattern: /(?:youtube\.com|youtube-nocookie\.com|youtu\.be)/i, severity: 'high' },
  { name: 'empty_embed_container', pattern: /<div class="embed-container embed-responsive embed-responsive-4by3">\s*<\/div>/i, severity: 'medium' },
  { name: 'empty_legacy_wrapper', pattern: /<(?:div|section) class="(?:wp-row|wp-column|wp-column-text|shortcode-panel|tab-section|toggle)">\s*<\/(?:div|section)>/i, severity: 'high' },
  { name: 'manual_code_review_notice', pattern: /Ingesloten code moet handmatig worden beoordeeld/i, severity: 'medium' },
  { name: 'php_reference', pattern: /(?:href|src)=["'][^"']+\.php(?:\?|["'])/i, severity: 'high' }
];

const rows = [];
for (const page of pages) {
  const html = page.html || '';
  for (const check of checks) {
    const matches = html.match(new RegExp(check.pattern.source, check.pattern.flags.includes('g') ? check.pattern.flags : `${check.pattern.flags}g`)) || [];
    if (matches.length > 0) {
      rows.push({
        page: page.url,
        title: page.title,
        issue: check.name,
        severity: check.severity,
        count: matches.length
      });
    }
  }
}

const csv = [
  'page,title,issue,severity,count',
  ...rows.map((row) => [row.page, row.title, row.issue, row.severity, row.count].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');
writeFileSync(join(root, 'data/site/html-conversion-audit.csv'), `${csv}\n`);

const high = rows.filter((row) => row.severity === 'high');
const summary = {
  total_issues: rows.length,
  high_issues: high.length,
  medium_issues: rows.filter((row) => row.severity === 'medium').length,
  issues: rows
};
writeFileSync(join(root, 'data/site/html-conversion-audit-summary.json'), `${JSON.stringify(summary, null, 2)}\n`);

if (high.length > 0) {
  throw new Error(`HTML conversion audit found ${high.length} high issue(s). See data/site/html-conversion-audit.csv`);
}

console.log(`HTML conversion audit ok: ${rows.length} issue rows, ${high.length} high`);
