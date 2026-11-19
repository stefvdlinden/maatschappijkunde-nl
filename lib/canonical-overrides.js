// Pages whose content is identical to another page. They stay reachable on their own URL,
// but declare the primary page as canonical and are left out of the sitemap.
// Used by the layout (rel=canonical, og:url) and by scripts/postbuild-seo.mjs (sitemap).
export const canonicalOverrides = {
  '/multiculturelemsamenleving-kerndoel-1/': '/examenstof/multiculturelemsamenleving-kerndoel-1/',
  '/ml2-k-6-2-het-overheidsbeleid/': '/examenstof/multiculturelesamenleving-kerndoel2/',
  '/ml2-k-6-3-sociaaleconomische-positie-allochtonen/': '/examenstof/multiculturelesamenleving-kerndoel3/',
  '/ml2-k-6-4-culturele-differentiatie/': '/examenstof/multiculturelesamenleving-kerndoel4/',
  '/ml2-k-6-5-vooroordelen-stereotypen-en-discriminatie/': '/examenstof/multiculturelesamenleving-kerndoel5/'
};
