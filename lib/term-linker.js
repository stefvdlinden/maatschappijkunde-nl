// Koppelt begrippen uit de lopende tekst aan de uitleg op schoolwoorden.nl.
// Werkt op HTML-tekst tijdens het bouwen; de bronteksten in pages.json blijven ongewijzigd.

const GLOSSARY_ITEM = /<h3><a href="(https:\/\/schoolwoorden\.nl\/begrip\/[^"]+)">([^<]+)<\/a><\/h3>/g;
const SKIP_TAGS = new Set(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'script', 'style', 'iframe', 'button', 'th', 'figcaption', 'select', 'option', 'textarea']);
const VOID_TAGS = new Set(['br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'wbr']);
const MIN_LENGTH = 6;
const MAX_LINKS = 8;

const decode = (value) => value.replaceAll('&amp;', '&').replaceAll('&nbsp;', ' ').trim();
const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export function extractTerms(glossaryHtml) {
  const terms = new Map();
  for (const match of glossaryHtml.matchAll(GLOSSARY_ITEM)) {
    const term = decode(match[2]);
    if (term.length < MIN_LENGTH || /[()/\d]/.test(term)) continue;
    const key = term.toLowerCase();
    if (!terms.has(key)) terms.set(key, { term, href: match[1] });
  }
  // Langste termen eerst, zodat "Eerste Kamer" voor "Kamer" gaat.
  return [...terms.values()].sort((a, b) => b.term.length - a.term.length);
}

const termPattern = (term) => new RegExp(
  `(?<![\\p{L}\\p{N}-])${term.split(/\s+/).map(escapeRegExp).join('(?:\\s|&nbsp;|\\u00a0)+')}(?![\\p{L}\\p{N}-])`,
  'iu'
);

export function linkTerms(html, terms, { maxLinks = MAX_LINKS } = {}) {
  if (!html || terms.length === 0) return html;
  const parts = html.split(/(<!--[\s\S]*?-->|<[^>]+>)/);
  let skipDepth = 0;
  const textIndexes = [];
  parts.forEach((part, index) => {
    if (index % 2 === 1) {
      const tag = /^<(\/?)([a-zA-Z][a-zA-Z0-9]*)/.exec(part);
      if (tag && SKIP_TAGS.has(tag[2].toLowerCase()) && !part.endsWith('/>')) {
        skipDepth += tag[1] ? -1 : 1;
        if (skipDepth < 0) skipDepth = 0;
      }
    } else if (skipDepth === 0 && part.trim()) {
      textIndexes.push(index);
    }
  });

  // Zoek per term de eerste vindplaats; neem alleen vindplaatsen die geen eerder gekozen stuk overlappen.
  const taken = new Map(); // partIndex -> [{start,end,entry}]
  const found = [];
  for (const entry of terms) {
    const pattern = termPattern(entry.term);
    for (const index of textIndexes) {
      const match = pattern.exec(parts[index]);
      if (!match) continue;
      const start = match.index;
      const end = start + match[0].length;
      const overlaps = (taken.get(index) || []).some((range) => start < range.end && end > range.start);
      if (overlaps) continue;
      const range = { start, end, entry, index };
      taken.set(index, [...(taken.get(index) || []), range]);
      found.push(range);
      break;
    }
  }

  const chosen = found
    .sort((a, b) => a.index - b.index || a.start - b.start)
    .slice(0, maxLinks);
  const byPart = new Map();
  for (const range of chosen) byPart.set(range.index, [...(byPart.get(range.index) || []), range]);
  for (const [index, ranges] of byPart) {
    let text = parts[index];
    for (const range of ranges.sort((a, b) => b.start - a.start)) {
      const original = text.slice(range.start, range.end);
      const link = `<a class="term-link" href="${range.entry.href}" target="_blank" rel="noopener" title="Uitleg op Schoolwoorden.nl">${original}</a>`;
      text = text.slice(0, range.start) + link + text.slice(range.end);
    }
    parts[index] = text;
  }
  return parts.join('');
}
