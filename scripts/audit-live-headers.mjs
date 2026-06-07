import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const origin = process.env.MK_LIVE_ORIGIN || process.env.MK_DEV_ORIGIN || 'https://dev.maatschappijkunde.nl';
const auth = process.env.MK_DEV_AUTH || '';

const checks = [
  { path: '/', type: 'html', expectedStatus: 200 },
  { path: '/examenstof/', type: 'html', expectedStatus: 200 },
  { path: '/sitemap-index.xml', type: 'xml', expectedStatus: 200 },
  { path: '/_redirects', type: 'redirect-file', expectedStatus: 200 },
  { path: '/.htaccess', type: 'protected-config', expectedStatus: 403 },
  { path: '/wp-content/uploads/2016/12/Analyse-Maatschappelijk-Vraagstuk-212x300.png', type: 'asset', expectedStatus: 200 }
];

const headers = auth
  ? { authorization: `Basic ${Buffer.from(auth).toString('base64')}` }
  : {};

const pickHeaders = (response) => ({
  cacheControl: response.headers.get('cache-control') || '',
  contentType: response.headers.get('content-type') || '',
  contentEncoding: response.headers.get('content-encoding') || '',
  strictTransportSecurity: response.headers.get('strict-transport-security') || '',
  xContentTypeOptions: response.headers.get('x-content-type-options') || '',
  xFrameOptions: response.headers.get('x-frame-options') || '',
  referrerPolicy: response.headers.get('referrer-policy') || ''
});

const classifyIssues = (check, response, headerValues) => {
  const issues = [];

  if (response.status !== check.expectedStatus) {
    issues.push(`status:${response.status}`);
  }

  if ((check.type === 'html' || check.type === 'xml') && !headerValues.contentType) {
    issues.push('missing_content_type');
  }

  if (check.type === 'asset' && !headerValues.cacheControl) {
    issues.push('asset_missing_cache_control');
  }

  if (check.type === 'html' && !headerValues.strictTransportSecurity) {
    issues.push('html_missing_hsts');
  }

  if (check.type === 'html' && !headerValues.xContentTypeOptions) {
    issues.push('html_missing_x_content_type_options');
  }

  if (check.type === 'protected-config' && response.status !== 403) {
    issues.push('config_not_protected');
  }

  return issues;
};

const rows = [];

for (const check of checks) {
  const url = `${origin}${check.path}`;
  try {
    const response = await fetch(url, { headers, redirect: 'manual' });
    const headerValues = pickHeaders(response);
    const issues = classifyIssues(check, response, headerValues);

    rows.push({
      path: check.path,
      type: check.type,
      expectedStatus: check.expectedStatus,
      actualStatus: response.status,
      ...headerValues,
      issue: issues.join(';')
    });
  } catch (error) {
    rows.push({
      path: check.path,
      type: check.type,
      expectedStatus: check.expectedStatus,
      actualStatus: '',
      cacheControl: '',
      contentType: '',
      contentEncoding: '',
      strictTransportSecurity: '',
      xContentTypeOptions: '',
      xFrameOptions: '',
      referrerPolicy: '',
      issue: `request_failed:${error.message}`
    });
  }
}

const csv = [
  'path,type,expected_status,actual_status,cache_control,content_type,content_encoding,strict_transport_security,x_content_type_options,x_frame_options,referrer_policy,issue',
  ...rows.map((row) => [
    row.path,
    row.type,
    row.expectedStatus,
    row.actualStatus,
    row.cacheControl,
    row.contentType,
    row.contentEncoding,
    row.strictTransportSecurity,
    row.xContentTypeOptions,
    row.xFrameOptions,
    row.referrerPolicy,
    row.issue
  ].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');

writeFileSync(join(root, 'data/site/live-header-audit.csv'), `${csv}\n`);
writeFileSync(join(root, 'data/site/live-header-audit-summary.json'), `${JSON.stringify({
  origin,
  total_checks: rows.length,
  total_warnings: rows.filter((row) => row.issue).length,
  checks: rows
}, null, 2)}\n`);

console.log(`Live header audit report: ${rows.length} checks, ${rows.filter((row) => row.issue).length} warning row(s)`);
