// Bare JSON imports are supported by the Pages Wrangler 3 bundler.
import redirects from '../data/site/redirects.json';
import { createRedirectMiddleware } from '../lib/redirect-middleware.js';

export const onRequest = createRedirectMiddleware(redirects);
