import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { onRequest } from '../functions/_middleware.js';

const redirects = JSON.parse(readFileSync(new URL('../data/site/redirects.json', import.meta.url)));
const origin = 'https://maatschappijkunde.nl';
const request = (url) => onRequest({
  request: new Request(url),
  next: async () => new Response('static asset', { status: 200 })
});

for (const { source, target, status } of redirects) {
  for (const host of [origin, 'https://www.maatschappijkunde.nl']) {
    for (const path of [source, source.replace(/\/$/, '')]) {
      const response = await request(`${host}${path}?utm_source=test`);
      const expected = new URL(target, origin);
      expected.search = '?utm_source=test';
      assert.equal(response.status, Number(status), `${host}${path}`);
      assert.equal(response.headers.get('location'), expected.href, `${host}${path}`);
    }
  }
}

for (const [path, target] of [
  ['/home/', '/'],
  ['/sitemap_index.xml', '/sitemap.xml'],
  ['/feed/', '/'],
  ['/comments/feed/', '/'],
  ['/examenstof/politiekenbeleid-kerndoel1-2/feed/', '/examenstof/politiekenbeleid-kerndoel1-2/'],
  ['/examenstof/criminaliteitenrechtsstaat-kerndoel2/feed/', '/examenstof/criminaliteitenrechtsstaat-kerndoel2/'],
  ['/examenstof/multiculturelemsamenleving-kerndoel-1/feed/', '/examenstof/multiculturelemsamenleving-kerndoel-1/'],
  ['/multiculturelemsamenleving-kerndoel-1/feed/', '/multiculturelemsamenleving-kerndoel-1/'],
  ['/planning/feed/', '/examenstof/']
]) {
  const response = await request(`${origin}${path}`);
  assert.equal(response.status, 301, path);
  assert.equal(response.headers.get('location'), `${origin}${target}`, path);
}

for (const path of ['/', '/examenstof/', '/unknown-page/', '/_redirects', '/wp-content/uploads/example.pdf']) {
  const response = await request(`${origin}${path}`);
  assert.equal(await response.text(), 'static asset', path);
}
const www = await request('http://www.maatschappijkunde.nl/downloads/?source=test');
assert.equal(www.headers.get('location'), `${origin}/downloads/?source=test`);
console.log(`Runtime redirects ok: ${redirects.length} rules with slash, host and query variants; feeds and passthrough checked`);
