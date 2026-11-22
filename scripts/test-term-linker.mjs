import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { extractTerms, linkTerms } from '../lib/term-linker.js';

const pages = JSON.parse(readFileSync(new URL('../data/site/pages.json', import.meta.url), 'utf8'));
const glossary = pages.find((page) => page.url === '/begrippen/');
const terms = extractTerms(glossary.html);
assert(terms.length > 150, `Expected many glossary terms, got ${terms.length}`);
assert(terms.every((entry) => entry.href.startsWith('https://schoolwoorden.nl/begrip/')));

const sample = [
  { term: 'Eerste Kamer', href: 'https://schoolwoorden.nl/begrip/eerste-kamer' },
  { term: 'Kamerlid', href: 'https://schoolwoorden.nl/begrip/kamerlid' },
  { term: 'Coalitie', href: 'https://schoolwoorden.nl/begrip/coalitie' }
];
const html = '<h2>Eerste Kamer</h2><p>De Eerste&nbsp;Kamer en de eerste kamer. Een <a href="/x/">coalitie</a> en een coalitie. Kamerlidmaatschap. <em>Kamerlid</em></p><script>coalitie</script>';
const out = linkTerms(html, sample);
assert(!out.includes('<h2><a'), 'headings must not be linked');
assert.equal((out.match(/class="term-link"/g) || []).length, 3, out);
assert(out.includes('>Eerste&nbsp;Kamer</a>'), 'first occurrence with nbsp is linked');
assert(out.includes('<a href="/x/">coalitie</a>'), 'existing links stay untouched');
assert(!out.includes('>Kamerlidmaatschap'), 'partial words are not linked');
assert(out.includes('<script>coalitie</script>'), 'script content is untouched');
assert.equal(linkTerms(out, sample), out, 'linking twice must not change the output');
assert(!linkTerms('<p>FNV Media en Cultuur en de Vreemdelingenzaken en Integratie.</p>', [{ term: 'Cultuur', href: 'https://schoolwoorden.nl/begrip/cultuur' }, { term: 'Integratie', href: 'https://schoolwoorden.nl/begrip/integratie' }]).includes('term-link'), 'protected names are not linked');

// Elke echte pagina: ten hoogste acht koppelingen, geen koppelingen in koppen of bestaande links.
let total = 0;
for (const page of pages.filter((item) => item.url.startsWith('/examenstof/') && item.type === 'ht_kb')) {
  const linked = linkTerms(page.html, terms);
  const count = (linked.match(/class="term-link"/g) || []).length;
  assert(count <= 8, `${page.url} has ${count} links`);
  // Tel open koppen en open koppelingen mee: een term-link mag nooit in een kop of in een andere link staan.
  let headingDepth = 0;
  let linkDepth = 0;
  for (const tag of linked.match(/<\/?[a-zA-Z][^>]*>/g) || []) {
    const name = /^<\/?([a-zA-Z][a-zA-Z0-9]*)/.exec(tag)[1].toLowerCase();
    const closing = tag.startsWith('</');
    if (/^h[1-6]$/.test(name)) headingDepth = Math.max(0, headingDepth + (closing ? -1 : 1));
    if (name === 'a') {
      if (!closing) {
        assert(!(tag.includes('class="term-link"') && (headingDepth > 0 || linkDepth > 0)), `${page.url}: term-link inside heading or link`);
        linkDepth += 1;
      } else linkDepth = Math.max(0, linkDepth - 1);
    }
  }
  total += count;
}
console.log(`Term linker ok: ${terms.length} terms, ${total} links over examenstof pages`);
