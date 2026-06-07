import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const origin = process.env.MK_DEV_ORIGIN || 'https://dev.maatschappijkunde.nl';
const auth = process.env.MK_DEV_AUTH || '';

const checks = [
  {
    path: '/begrippen/tweede-kamer/',
    expectedStatus: 301,
    expectedLocation: 'https://schoolwoorden.nl/begrip/tweede-kamer/'
  },
  {
    path: '/begrippen/parlement/',
    expectedStatus: 301,
    expectedLocation: 'https://schoolwoorden.nl/begrip/parlement/'
  },
  {
    path: '/begrippen/reageerakkoord/',
    expectedStatus: 301,
    expectedLocation: 'https://schoolwoorden.nl/begrip/regeerakkoord/'
  },
  {
    path: '/politiekenbeleid-kerndoel1-1/',
    expectedStatus: 301,
    expectedLocation: '/examenstof/politiekenbeleid-kerndoel1-1/'
  },
  {
    path: '/amv-kerndoel1/',
    expectedStatus: 301,
    expectedLocation: '/examenstof/amv-kerndoel1/'
  },
  {
    path: '/ciminaliteitenrechtsstaat-kerndoel1/',
    expectedStatus: 301,
    expectedLocation: '/examenstof/criminaliteitenrechtsstaat-kerndoel1/'
  }
];

const headers = auth
  ? { authorization: `Basic ${Buffer.from(auth).toString('base64')}` }
  : {};

const absolutize = (value) => {
  if (!value) return '';
  return value.startsWith('/') ? `${origin}${value}` : value;
};

const rows = [];

for (const check of checks) {
  const url = `${origin}${check.path}`;
  try {
    const response = await fetch(url, { headers, redirect: 'manual' });
    const location = response.headers.get('location') || '';
    const expectedLocation = absolutize(check.expectedLocation);
    const normalizedLocation = absolutize(location);
    const issues = [];

    if (response.status !== check.expectedStatus) {
      issues.push(`status:${response.status}`);
    }
    if (normalizedLocation !== expectedLocation) {
      issues.push(`location:${location || 'missing'}`);
    }

    rows.push({
      path: check.path,
      expectedStatus: check.expectedStatus,
      actualStatus: response.status,
      expectedLocation,
      actualLocation: normalizedLocation,
      issue: issues.join(';')
    });
  } catch (error) {
    rows.push({
      path: check.path,
      expectedStatus: check.expectedStatus,
      actualStatus: '',
      expectedLocation: absolutize(check.expectedLocation),
      actualLocation: '',
      issue: `request_failed:${error.message}`
    });
  }
}

const csv = [
  'path,expected_status,actual_status,expected_location,actual_location,issue',
  ...rows.map((row) => [
    row.path,
    row.expectedStatus,
    row.actualStatus,
    row.expectedLocation,
    row.actualLocation,
    row.issue
  ].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(','))
].join('\n');

writeFileSync(join(root, 'data/site/live-redirect-audit.csv'), `${csv}\n`);
writeFileSync(join(root, 'data/site/live-redirect-audit-summary.json'), `${JSON.stringify({
  origin,
  total_checks: rows.length,
  total_issues: rows.filter((row) => row.issue).length,
  checks: rows
}, null, 2)}\n`);

const failures = rows.filter((row) => row.issue);
if (failures.length > 0) {
  throw new Error(`Live redirect audit found ${failures.length} issue(s). See data/site/live-redirect-audit.csv`);
}

console.log(`Live redirect audit ok: ${rows.length} checks, 0 issues`);
