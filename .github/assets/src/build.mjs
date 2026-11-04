// SPDX-License-Identifier: Apache-2.0
// Draws the README images in .github/assets/: the banner (light and dark) and the
// four steps (light, dark and phone). Text is turned into outlines with the brand
// fonts, so the SVGs need no web fonts. Run it from this folder:
//
//   npm ci && node build.mjs            writes into .github/assets/
//   node build.mjs <folder>             writes into another folder instead
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const MODULES = path.join(HERE, 'node_modules');
if (!fs.existsSync(path.join(MODULES, 'opentype.js'))) {
  console.error('The dependencies are missing. Run "npm ci" in this folder first.');
  process.exit(1);
}
const { default: opentype } = await import('opentype.js');
const OUT = process.argv[2] ? path.resolve(process.argv[2]) : path.join(HERE, '..');
fs.mkdirSync(OUT, { recursive: true });

// The static TTFs from Google Fonts, as the @expo-google-fonts packages ship them.
const font = (file) => opentype.loadSync(path.join(MODULES, '@expo-google-fonts', file));
const F = {
  display: font('funnel-display/400Regular/FunnelDisplay_400Regular.ttf'),
  body: font('geist/400Regular/Geist_400Regular.ttf'),
  mono: font('geist-mono/500Medium/GeistMono_500Medium.ttf'),
};

const C = {
  burnt: '#B84D16',
  o700: '#8F3A0F',
  ember: '#5A1A10',
  flame: '#E2672C',
  night: '#140D0A',
  paper: '#F6F4F2',
  apricot100: '#FBE8DA',
  apricot200: '#F6CFB1',
  apricot300: '#F0A46A',
  white: '#FFFFFF',
  ink: '#251913',
  stoneText: '#5F524C',
  hairline: '#E2DDD7',
};

const r1 = (v) => Math.round(v * 10) / 10;

// Each glyph outline is defined once and placed with <use>, which keeps the files small.
const DEFS = new Map();
function glyphRef(f, g, size) {
  const key = `${f.names.fullName.en}|${size}|${g.index}`;
  if (!DEFS.has(key)) {
    const d = g.getPath(0, 0, size).toPathData(1);
    DEFS.set(key, { id: 'g' + DEFS.size.toString(36), d });
  }
  return DEFS.get(key);
}
// A run of glyphs with kerning and tracking (a fraction of the em), as <use> elements.
function run(f, str, size, x, y, tracking = 0) {
  const glyphs = f.stringToGlyphs(str);
  const scale = size / f.unitsPerEm;
  let d = '';
  let cx = x;
  glyphs.forEach((g, i) => {
    const ref = glyphRef(f, g, size);
    if (ref.d) d += `<use href="#${ref.id}" x="${r1(cx)}" y="${r1(y)}"/>`;
    let adv = g.advanceWidth * scale + tracking * size;
    if (i < glyphs.length - 1) adv += f.getKerningValue(g, glyphs[i + 1]) * scale;
    cx += adv;
  });
  return { d, width: cx - x - tracking * size };
}
function measure(f, str, size, tracking = 0) {
  const glyphs = f.stringToGlyphs(str);
  const scale = size / f.unitsPerEm;
  let w = 0;
  glyphs.forEach((g, i) => {
    w += g.advanceWidth * scale + tracking * size;
    if (i < glyphs.length - 1) w += f.getKerningValue(g, glyphs[i + 1]) * scale;
  });
  return w - tracking * size;
}

function wrap(f, str, size, max) {
  const words = str.split(' ');
  const lines = [];
  let line = '';
  for (const w of words) {
    const t = line ? line + ' ' + w : w;
    if (measure(f, t, size) <= max || !line) line = t;
    else {
      lines.push(line);
      line = w;
    }
  }
  if (line) lines.push(line);
  return lines;
}

// ------------------------------------------------------------------ banner --
// The Nova Forma logo is not covered by the Apache License 2.0: see NOTICE.
function logoPaths() {
  const svg = fs.readFileSync(path.join(HERE, 'nova-forma-logo-horizontal.svg'), 'utf8');
  const mark = svg.match(/id="nf-modules"[^>]* d="([^"]+)"/)[1];
  const word = svg.match(/id="wordmark"[^>]* d="([^"]+)"/)[1];
  return { mark, word };
}

function radial(id, cx, cy, rx, ry, color, stopAt = 0.7, peak = 1) {
  return (
    `<radialGradient id="${id}" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" ` +
    `gradientTransform="translate(${r1(cx)} ${r1(cy)}) scale(${r1(rx)} ${r1(ry)})">` +
    `<stop offset="0" stop-color="${color}" stop-opacity="${peak}"/>` +
    `<stop offset="${stopAt}" stop-color="${color}" stop-opacity="0"/></radialGradient>`
  );
}

function banner(mode) {
  const W = 1280;
  const H = 320;
  const { mark, word } = logoPaths();
  // The logo's ink box (its data-ink attribute): x -177.135 to 821.358, y -12.5 to 113.98.
  const ink = { x: -177.135, y: -12.5, w: 998.493, h: 126.48 };
  const lw = 520;
  const s = lw / ink.w;
  const tx = (W - lw) / 2 - ink.x * s;
  const ty = (H - ink.h * s) / 2 - ink.y * s;
  const dark = mode === 'dark';
  // The gradient fields of the novaforma.ai site (day and night), laid out for a
  // wide banner: the glow sits right of the wordmark, a softer one bottom left.
  const fields = dark
    ? [
        ['a', 0.84 * W, 0.18 * H, 0.42 * W, 1.25 * H, C.burnt, 0.72, 0.95],
        ['b', 1.0 * W, 1.05 * H, 0.24 * W, 0.8 * H, C.apricot300, 0.7, 0.35],
        ['c', 0.14 * W, 1.05 * H, 0.4 * W, 1.0 * H, C.ember, 0.72, 1],
      ]
    : [
        ['a', 0.86 * W, 0.12 * H, 0.42 * W, 1.3 * H, C.flame, 0.72, 0.9],
        ['b', 0.1 * W, 1.05 * H, 0.36 * W, 1.05 * H, C.apricot300, 0.72, 0.75],
      ];
  const grain = dark
    ? '0 0 0 0 1 0 0 0 0 .95 0 0 0 0 .92 0 0 0 .07 0'
    : '0 0 0 0 .45 0 0 0 0 .4 0 0 0 0 .36 0 0 0 .1 0';
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">` +
    `<!-- Nova Forma README banner (${mode}). The Nova Forma logo is not covered by the Apache License 2.0: see NOTICE. -->` +
    `<defs>${fields.map((f) => radial(...f)).join('')}` +
    `<clipPath id="k"><rect width="${W}" height="${H}" rx="20"/></clipPath>` +
    `<filter id="g" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="${grain}"/></filter>` +
    `</defs>` +
    `<g clip-path="url(#k)">` +
    `<rect width="${W}" height="${H}" fill="${dark ? C.night : C.paper}"/>` +
    fields.map((f) => `<rect width="${W}" height="${H}" fill="url(#${f[0]})"/>`).join('') +
    `<rect width="${W}" height="${H}" filter="url(#g)"/>` +
    `</g>` +
    `<g transform="translate(${r1(tx * 100) / 100} ${r1(ty * 100) / 100}) scale(${s.toFixed(5)})">` +
    `<path fill="${C.burnt}" d="${mark}"/>` +
    `<path fill="${dark ? '#F5F2F1' : C.ink}" d="${word}"/>` +
    `</g></svg>\n`
  );
}

// ------------------------------------------------------------- four steps --
// The step names and results. Keep them the same as the table in the README and
// the alt text of the four-steps image, then rebuild.
const STEPS = [
  { label: 'STEP 1', title: 'Pick the workflow', out: 'A ranked shortlist and a scope card', icon: 'search' },
  { label: 'STEP 2', title: 'Define success', out: 'An outcome, its measures and red lines', icon: 'target' },
  { label: 'STEP 3', title: 'Map today’s work', out: 'Every requirement, owner and exception', icon: 'list' },
  { label: 'STEP 4', title: 'Size the value', out: 'A yearly value range, low to high', icon: 'chart' },
  { label: 'THE RESULT', title: 'One-page brief', out: 'For the redesign week', icon: 'doc', result: true },
];

function icon(kind, x, y, k = 1) {
  // Simple line glyphs on a 24-unit grid, centred on (x, y).
  const shapes = {
    search: `<circle cx="${x - 2 * k}" cy="${y - 2 * k}" r="${7.5 * k}"/><path d="M${x + 3.5 * k} ${y + 3.5 * k}L${x + 9.5 * k} ${y + 9.5 * k}"/>`,
    target: `<circle cx="${x}" cy="${y}" r="${10 * k}"/><circle cx="${x}" cy="${y}" r="${5 * k}"/><circle cx="${x}" cy="${y}" r="${0.6 * k}"/>`,
    list: `<path d="M${x - 4 * k} ${y - 7 * k}H${x + 10 * k}M${x - 4 * k} ${y}H${x + 10 * k}M${x - 4 * k} ${y + 7 * k}H${x + 10 * k}M${x - 10 * k} ${y - 7 * k}h.1M${x - 10 * k} ${y}h.1M${x - 10 * k} ${y + 7 * k}h.1"/>`,
    chart: `<path d="M${x - 10 * k} ${y - 10 * k}V${y + 10 * k}H${x + 10 * k}M${x - 6 * k} ${y + 4 * k}L${x - 1 * k} ${y - 2 * k}L${x + 3 * k} ${y + 1 * k}L${x + 9 * k} ${y - 7 * k}"/>`,
    doc: `<path d="M${x - 9 * k} ${y - 12 * k}H${x + 4 * k}L${x + 10 * k} ${y - 6 * k}V${y + 12 * k}H${x - 9 * k}Z M${x + 4 * k} ${y - 12 * k}V${y - 6 * k}H${x + 10 * k}M${x - 4.5 * k} ${y}H${x + 5 * k}M${x - 4.5 * k} ${y + 5.5 * k}H${x + 5 * k}"/>`,
  };
  return shapes[kind];
}

function steps(mode) {
  DEFS.clear();
  const dark = mode === 'dark';
  const col = dark
    ? { bg: C.night, border: '#3A2C25', line: C.flame, nodeFill: C.night, label: C.apricot300, title: C.paper, accent: C.flame, out: '#BFB3AB', resultFill: C.flame, resultIcon: C.night }
    : { bg: C.paper, border: C.hairline, line: C.burnt, nodeFill: C.white, label: C.o700, title: C.ink, accent: C.burnt, out: C.stoneText, resultFill: C.burnt, resultIcon: C.white };
  const W = 1280;
  const pad = 56;
  const colW = (W - 2 * pad) / STEPS.length;
  const textMax = colW - 20;
  const node = 52;
  const big = 64;
  const nodeY = 56 + big / 2;
  const labelY = nodeY + big / 2 + 44;
  const titleSize = 36;
  const titleLead = 42;
  const outSize = 20;
  const outLead = 28;
  const labelSize = 15;

  const paths = { label: '', title: '', accent: '', out: '' };
  let maxOutLines = 0;
  const layout = STEPS.map((s, i) => {
    const x0 = pad + i * colW;
    const tl = wrap(F.display, s.title, titleSize, textMax);
    const ol = wrap(F.body, s.out, outSize, textMax);
    maxOutLines = Math.max(maxOutLines, ol.length);
    return { s, x0, tl, ol };
  });
  const titleY = labelY + 48;
  const outY = titleY + titleLead + 42;
  const H = Math.round(outY + (maxOutLines - 1) * outLead + 50);

  layout.forEach(({ s, x0, tl, ol }) => {
    paths.label += run(F.mono, s.label, labelSize, x0, labelY, 0.12).d;
    tl.forEach((t, j) => {
      paths[s.result ? 'accent' : 'title'] += run(F.display, t, titleSize, x0, titleY + j * titleLead, -0.01).d;
    });
    ol.forEach((t, j) => {
      paths.out += run(F.body, t, outSize, x0, outY + j * outLead).d;
    });
  });

  const first = layout[0].x0 + node / 2;
  const lastL = layout[layout.length - 1];
  const nodes = layout
    .map(({ s, x0 }) => {
      if (s.result) {
        return `<rect x="${r1(x0)}" y="${nodeY - big / 2}" width="${big}" height="${big}" rx="5" fill="${col.resultFill}"/>` +
          `<g fill="none" stroke="${col.resultIcon}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">${icon('doc', r1(x0 + big / 2), nodeY, 1.15)}</g>`;
      }
      return `<rect x="${r1(x0 + 1.5)}" y="${nodeY - node / 2 + 1.5}" width="${node - 3}" height="${node - 3}" rx="4" fill="${col.nodeFill}" stroke="${col.line}" stroke-width="3"/>` +
        `<g fill="none" stroke="${col.line}" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round">${icon(s.icon, r1(x0 + node / 2), nodeY, 1.02)}</g>`;
    })
    .join('');

  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">` +
    `<!-- The four Nova Forma steps (${mode}). Text is outlined from Funnel Display, Geist and Geist Mono (SIL Open Font License 1.1). -->` +
    `<defs>${[...DEFS.values()].filter((g) => g.d).map((g) => `<path id="${g.id}" d="${g.d}"/>`).join('')}</defs>` +
    `<rect x="1" y="1" width="${W - 2}" height="${H - 2}" rx="20" fill="${col.bg}" stroke="${col.border}" stroke-width="2"/>` +
    `<path d="M${r1(first)} ${nodeY}H${r1(lastL.x0 + 2)}" stroke="${col.line}" stroke-width="3"/>` +
    nodes +
    `<g fill="${col.label}">${paths.label}</g>` +
    `<g fill="${col.title}">${paths.title}</g>` +
    `<g fill="${col.accent}">${paths.accent}</g>` +
    `<g fill="${col.out}">${paths.out}</g>` +
    `</svg>\n`
  );
}

// ------------------------------------------------- four steps, phone layout --
// One column, read top to bottom, for screens up to 600px wide. It is drawn at
// 560 units so that at a 320px column the labels land near 12px and the lines
// under each title near 13px. Light and dark live in one file: its own CSS
// follows prefers-color-scheme, because GitHub's theme switch rewrites only the
// sources that name a colour scheme.
function stepsNarrow() {
  DEFS.clear();
  const W = 560;
  const pad = 28;
  const node = 52;
  const big = 64;
  const cx = pad + big / 2;
  const textX = pad + big + 26;
  const textMax = W - textX - pad;
  const labelSize = 21;
  const titleSize = 34;
  const titleLead = 40;
  const outSize = 22;
  const outLead = 30;
  const top = 38;
  const rowGap = 26;

  const paths = { label: '', title: '', accent: '', out: '' };
  let y = top;
  const rows = STEPS.map((s) => {
    const tl = wrap(F.display, s.title, titleSize, textMax);
    const ol = wrap(F.body, s.out, outSize, textMax);
    const labelY = y + 20;
    const titleY = labelY + 40;
    const outY = titleY + (tl.length - 1) * titleLead + 32;
    const bottom = outY + (ol.length - 1) * outLead + 7;
    const row = { s, tl, ol, labelY, titleY, outY, nodeY: y + 33 };
    paths.label += run(F.mono, s.label, labelSize, textX, labelY, 0.12).d;
    tl.forEach((t, j) => {
      paths[s.result ? 'accent' : 'title'] += run(F.display, t, titleSize, textX, titleY + j * titleLead, -0.01).d;
    });
    ol.forEach((t, j) => {
      paths.out += run(F.body, t, outSize, textX, outY + j * outLead).d;
    });
    y = bottom + rowGap;
    return row;
  });
  const H = Math.round(y - rowGap + 31);

  const nodes = rows
    .map(({ s, nodeY }) => {
      if (s.result) {
        return `<rect class="rs" x="${cx - big / 2}" y="${nodeY - big / 2}" width="${big}" height="${big}" rx="5"/>` +
          `<g class="ri" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">${icon('doc', cx, nodeY, 1.15)}</g>`;
      }
      return `<rect class="nd" x="${cx - node / 2 + 1.5}" y="${nodeY - node / 2 + 1.5}" width="${node - 3}" height="${node - 3}" rx="4" stroke-width="3"/>` +
        `<g class="ln" fill="none" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round">${icon(s.icon, cx, nodeY, 1.02)}</g>`;
    })
    .join('');

  const css =
    `.bg{fill:${C.paper};stroke:${C.hairline}}.ln,.nd{stroke:${C.burnt}}.nd{fill:${C.white}}` +
    `.rs{fill:${C.burnt}}.ri{stroke:${C.white}}.lb{fill:${C.o700}}.tt{fill:${C.ink}}.ac{fill:${C.burnt}}.ou{fill:${C.stoneText}}` +
    `@media (prefers-color-scheme:dark){.bg{fill:${C.night};stroke:#3A2C25}.ln,.nd{stroke:${C.flame}}.nd{fill:${C.night}}` +
    `.rs{fill:${C.flame}}.ri{stroke:${C.night}}.lb{fill:${C.apricot300}}.tt{fill:${C.paper}}.ac{fill:${C.flame}}.ou{fill:#BFB3AB}}`;

  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">` +
    `<!-- The four Nova Forma steps, phone layout (light and dark). Text is outlined from Funnel Display, Geist and Geist Mono (SIL Open Font License 1.1). -->` +
    `<style>${css}</style>` +
    `<defs>${[...DEFS.values()].filter((g) => g.d).map((g) => `<path id="${g.id}" d="${g.d}"/>`).join('')}</defs>` +
    `<rect class="bg" x="1" y="1" width="${W - 2}" height="${H - 2}" rx="20" stroke-width="2"/>` +
    `<path class="ln" fill="none" d="M${cx} ${rows[0].nodeY}V${rows[rows.length - 1].nodeY}" stroke-width="3"/>` +
    nodes +
    `<g class="lb">${paths.label}</g>` +
    `<g class="tt">${paths.title}</g>` +
    `<g class="ac">${paths.accent}</g>` +
    `<g class="ou">${paths.out}</g>` +
    `</svg>\n`
  );
}

const files = {
  'nova-forma-banner-light.svg': banner('light'),
  'nova-forma-banner-dark.svg': banner('dark'),
  'four-steps-light.svg': steps('light'),
  'four-steps-dark.svg': steps('dark'),
  'four-steps-narrow.svg': stepsNarrow(),
};
console.log(`Writing into ${OUT}`);
for (const [name, body] of Object.entries(files)) {
  fs.writeFileSync(path.join(OUT, name), body);
  console.log(`  ${name}  ${Buffer.byteLength(body)} bytes`);
}
