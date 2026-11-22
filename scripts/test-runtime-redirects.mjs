import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRedirectMiddleware } from '../lib/redirect-middleware.js';

const redirects = JSON.parse(readFileSync(new URL('../data/site/redirects.json', import.meta.url)));
const gone = JSON.parse(readFileSync(new URL('../data/site/gone.json', import.meta.url)));
const onRequest = createRedirectMiddleware(redirects, gone.paths);
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

for (const path of gone.paths) {
  const sourceSet = new Set(redirects.map((redirect) => redirect.source));
  assert(!sourceSet.has(path), `Gone path ${path} must not also be a redirect`);
  for (const variant of [path, path.replace(/\/$/, ''), `${path}feed/`]) {
    for (const host of [origin, 'https://www.maatschappijkunde.nl']) {
      const response = await request(`${host}${variant}`);
      assert.equal(response.status, 410, `${host}${variant}`);
      assert.match(await response.text(), /verwijderd/, `${host}${variant}`);
    }
  }
}

for (const path of ['/', '/examenstof/', '/unknown-page/', '/_redirects', '/wp-content/uploads/example.pdf']) {
  const response = await request(`${origin}${path}`);
  assert.equal(await response.text(), 'static asset', path);
}
const www = await request('http://www.maatschappijkunde.nl/downloads/?source=test');
assert.equal(www.headers.get('location'), `${origin}/downloads/?source=test`);
console.log(`Runtime redirects ok: ${redirects.length} rules and ${gone.paths.length} gone paths with slash, host and query variants; feeds and passthrough checked`);
