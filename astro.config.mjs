import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.maatschappijkunde.nl',
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()]
});
