// Measurement probe (DADA evidence seat). Run in a page; returns JSON.
// Contrast takes the worst background stop; the first-screen check uses the poster's BOTTOM edge.
(() => {
  const parse = c => { const m = c.match(/[\d.]+/g); return m ? m.slice(0, 4).map(Number) : null; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const bgsOf = el => { for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e); if (s.backgroundImage && s.backgroundImage.includes('gradient')) { const m = s.backgroundImage.match(/rgba?\([^)]+\)/g); if (m) return m.map(parse).filter(c => c.length < 4 || c[3] > 0.5); } const c = parse(s.backgroundColor); if (c && (c.length < 4 || c[3] > 0.5)) return [c]; } return [[255, 255, 255]]; };
  const vw = document.documentElement.clientWidth, vh = innerHeight;
  const fails = []; let min = 99, checked = 0, smallest = 99, smallestText = '';
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); const seen = new Set();
  while (walker.nextNode()) {
    const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const el = t.parentElement; if (seen.has(el)) continue; seen.add(el);
    if (el.closest('[aria-hidden="true"]') || el.closest('.skip')) continue;
    const s = getComputedStyle(el); if (s.visibility === 'hidden' || s.display === 'none') continue;
    const r = el.getBoundingClientRect(); if (!r.width) continue;
    const fs = parseFloat(s.fontSize); if (fs < smallest) { smallest = fs; smallestText = t.textContent.trim().slice(0, 30); }
    const cr = Math.min(...bgsOf(el).map(b => ratio(parse(s.color), b))); checked++;
    const large = fs >= 24 || (fs >= 18.66 && +s.fontWeight >= 700);
    if (cr < min) min = cr;
    if (cr < (large ? 3 : 4.5)) fails.push({ text: t.textContent.trim().slice(0, 30), ratio: +cr.toFixed(2) });
  }
  const small = [];
  for (const a of document.querySelectorAll('a, button, [tabindex]')) {
    const r = a.getBoundingClientRect();
    if (r.width && r.height < 24 && !a.closest('.skip') && getComputedStyle(a).display !== 'inline') small.push({ text: a.textContent.trim().slice(0, 24), h: +r.height.toFixed(1) });
  }
  const res = { page: location.pathname, scheme: matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light', vw, vh,
    docOverflowX: document.documentElement.scrollWidth - vw, textNodes: checked, minContrast: +min.toFixed(2), contrastFails: fails,
    smallTargets: small, smallestFontPx: smallest, smallestText, h1: document.querySelectorAll('h1').length };
  const poster = document.querySelector('.poster');
  if (poster) {
    const p = poster.getBoundingClientRect();
    const tiles = [...poster.querySelectorAll('.tile a')];
    res.firstScreen = { posterTop: Math.round(p.top + scrollY), posterBottom: Math.round(p.bottom + scrollY), fold: vh,
      completeAboveFold: p.bottom + scrollY <= vh, posterScrollsSideways: poster.scrollWidth > poster.clientWidth + 1,
      tiles: tiles.length,
      tilesWithClippedText: tiles.filter(a => [...a.querySelectorAll('.t-name,.t-fig,.t-out')].some(e => { const r = e.getBoundingClientRect(), q = a.getBoundingClientRect(); return r.bottom > q.bottom + 1 || r.right > q.right + 1; })).map(a => a.textContent.trim().slice(0, 12)),
      glyphHeights: Object.fromEntries(tiles.map(a => [a.querySelector('.t-name').textContent, Math.round(a.querySelector('.t-glyph').getBoundingClientRect().height)])) };
  }
  return res;
})()
