// Shared by the Pages middleware and the static postbuild output.
export const seoRedirects = [
  ['/home', '/', 301],
  ['/home/', '/', 301],
  ['/index.html', '/', 301],
  ['/sitemap', '/sitemap.xml', 301],
  ['/sitemap/', '/sitemap.xml', 301],
  ['/sitemap_index.xml', '/sitemap.xml', 301],
  ['/wp-sitemap.xml', '/sitemap.xml', 301],
  ['/feed/', '/', 301],
  ['/comments/feed/', '/', 301],
  ['/*/feed/', '/:splat/', 301]
];
