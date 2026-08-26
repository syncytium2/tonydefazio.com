#!/usr/bin/env node
// Hold the version stamp to one number and two dates.
//
// The stamp is written out in eight places across four files — there is no
// build step, so nothing generates one from another and every one of them is
// hand-edited. This is what stops them drifting apart. `npm run deploy` and
// `npm run dry` both run it first, so a half-bumped version cannot ship.
//
// Checked:
//   package.json    version
//   index.html      JSON-LD version / datePublished / dateModified
//                   footer  Version <b>…</b> · Updated <time> · Online since <time>
//   thanks.html     the same footer triple
//   sitemap.xml     <lastmod>, which must equal the modified date
//
// Both the machine-readable datetime attribute and the prose beside it are
// compared, because "26 August 2026" going stale while datetime="2026-08-26"
// stays right is exactly the drift a reader would notice and a crawler
// would not.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => readFileSync(join(root, p), 'utf8');

const problems = [];
const fail = (msg) => problems.push(msg);

/** "2026-08-26" -> "26 August 2026", the form the pages print. */
function longForm(iso) {
  const [y, m, d] = iso.split('-').map(Number);
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December'];
  return `${d} ${months[m - 1]} ${y}`;
}

/** The footer stamp, parsed out of a page. */
function stamp(file, html) {
  const m = html.match(
    /<p class="version">\s*<span>Version <b>([^<]+)<\/b><\/span>\s*<span>Updated <time datetime="([^"]+)">([^<]+)<\/time><\/span>\s*<span>Online since <time datetime="([^"]+)">([^<]+)<\/time><\/span>\s*<\/p>/
  );
  if (!m) {
    fail(`${file}: no <p class="version"> stamp found, or it does not match the expected shape`);
    return null;
  }
  const [, version, modified, modifiedText, born, bornText] = m;
  if (longForm(modified) !== modifiedText) {
    fail(`${file}: "Updated ${modifiedText}" does not read as datetime="${modified}" (expected "${longForm(modified)}")`);
  }
  if (longForm(born) !== bornText) {
    fail(`${file}: "Online since ${bornText}" does not read as datetime="${born}" (expected "${longForm(born)}")`);
  }
  return { version, modified, born };
}

const pkg = JSON.parse(read('package.json'));
const index = read('site/index.html');
const thanks = read('site/thanks.html');
const sitemap = read('site/sitemap.xml');

// --- the JSON-LD WebSite node ---------------------------------------------
const ld = index.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
let site = null;
if (!ld) {
  fail('site/index.html: no JSON-LD block');
} else {
  let graph;
  try {
    graph = JSON.parse(ld[1]);
  } catch (e) {
    fail(`site/index.html: JSON-LD does not parse — ${e.message}`);
  }
  site = graph?.['@graph']?.find((n) => n['@type'] === 'WebSite');
  if (!site) fail('site/index.html: JSON-LD has no WebSite node to carry the version');
}

// --- the two footer stamps -------------------------------------------------
const a = stamp('site/index.html', index);
const b = stamp('site/thanks.html', thanks);

// --- everything must agree -------------------------------------------------
const truth = a ?? b ?? (site ? { version: site.version, modified: site.dateModified, born: site.datePublished } : null);

if (truth) {
  const { version, modified, born } = truth;

  if (pkg.version !== version) fail(`package.json version ${pkg.version} != page version ${version}`);
  if (site) {
    if (site.version !== version) fail(`JSON-LD version ${site.version} != page version ${version}`);
    if (site.dateModified !== modified) fail(`JSON-LD dateModified ${site.dateModified} != page ${modified}`);
    if (site.datePublished !== born) fail(`JSON-LD datePublished ${site.datePublished} != page ${born}`);
  }
  if (b && a) {
    if (b.version !== a.version) fail(`thanks.html version ${b.version} != index.html ${a.version}`);
    if (b.modified !== a.modified) fail(`thanks.html updated ${b.modified} != index.html ${a.modified}`);
    if (b.born !== a.born) fail(`thanks.html born ${b.born} != index.html ${a.born}`);
  }

  const lastmod = sitemap.match(/<lastmod>([^<]+)<\/lastmod>/)?.[1];
  if (!lastmod) fail('site/sitemap.xml: no <lastmod>');
  else if (lastmod !== modified) fail(`sitemap lastmod ${lastmod} != version date ${modified}`);

  if (born > modified) fail(`born-on date ${born} is after the version date ${modified}`);

  if (problems.length === 0) {
    console.log(`v${version} · updated ${modified} · online since ${born} — consistent in all four files`);
  }
}

if (problems.length) {
  console.error('Version stamp is inconsistent:');
  for (const p of problems) console.error(`  - ${p}`);
  console.error('\nSee README § The version stamp for the list of places to bump.');
  process.exit(1);
}
