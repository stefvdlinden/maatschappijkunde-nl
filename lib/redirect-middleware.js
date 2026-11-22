import { seoRedirects } from './seo-redirects.js';

const goneBody = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Pagina verwijderd | Maatschappijkunde.nl</title>
<style>body{font-family:system-ui,sans-serif;max-width:40rem;margin:4rem auto;padding:0 1rem;line-height:1.5}a{color:#0b5cad}</style>
</head>
<body>
<h1>Deze pagina is verwijderd</h1>
<p>Deze pagina bestaat niet meer. Maatschappijkunde.nl richt zich op het vmbo en de examenstof voor havo is verwijderd.</p>
<p><a href="/examenstof/">Naar de examenstof</a> of <a href="/">naar de homepage</a>.</p>
</body>
</html>
`;

export function createRedirectMiddleware(redirects, gonePaths = []) {
  const gone = new Set(gonePaths);
  const rules = new Map([
    ...redirects.map(({ source, target, status }) => [source, { target, status: Number(status) }]),
    ...seoRedirects.filter(([source]) => !source.includes('*'))
      .map(([source, target, status]) => [source, { target, status }])
  ]);

  return async function onRequest(context) {
    const url = new URL(context.request.url);
    const pathname = url.pathname;
    const normalizedPath = pathname.endsWith('/') ? pathname : `${pathname}/`;
    let rule = rules.get(pathname) || rules.get(normalizedPath);

    // Verwijderde pagina's (en hun feed) geven 410 Gone in plaats van 404.
    const feedParent = normalizedPath.endsWith('/feed/') ? normalizedPath.slice(0, -5) : null;
    if (!rule && (gone.has(normalizedPath) || (feedParent && gone.has(feedParent)))) {
      return new Response(context.request.method === 'HEAD' ? null : goneBody, {
        status: 410,
        headers: {
          'content-type': 'text/html; charset=utf-8',
          'cache-control': 'public, max-age=3600',
          'x-robots-tag': 'noindex'
        }
      });
    }

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
}
