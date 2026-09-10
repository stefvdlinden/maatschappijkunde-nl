import redirects from '../data/site/redirects.json' with { type: 'json' };
import { seoRedirects } from '../lib/seo-redirects.js';

const rules = new Map([
  ...redirects.map(({ source, target, status }) => [source, { target, status: Number(status) }]),
  ...seoRedirects.filter(([source]) => !source.includes('*'))
    .map(([source, target, status]) => [source, { target, status }])
]);

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const pathname = url.pathname;
  const normalizedPath = pathname.endsWith('/') ? pathname : `${pathname}/`;
  let rule = rules.get(pathname) || rules.get(normalizedPath);

  // Pages does not apply _redirects to requests handled by Functions.
  if (!rule && normalizedPath.endsWith('/feed/')) {
    const parent = normalizedPath.slice(0, -5);
    rule = rules.get(parent) || { target: parent, status: 301 };
  }

  if (rule) {
    const origin = url.hostname === 'www.maatschappijkunde.nl'
      ? 'https://maatschappijkunde.nl' : url.origin;
    const target = new URL(rule.target, origin);
    if (!target.search) target.search = url.search;
    return Response.redirect(target.toString(), rule.status);
  }

  if (url.hostname === 'www.maatschappijkunde.nl') {
    url.protocol = 'https:';
    url.hostname = 'maatschappijkunde.nl';
    return Response.redirect(url.toString(), 301);
  }

  return context.next();
}
