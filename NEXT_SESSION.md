# Next session

Handoff written **2026-09-02**. Everything below was verified against the live site and the
repo on that date, not recalled. Re-verify before trusting any of it — this file is exactly
the kind of document §3 of the README warns about.

## 1. Status: the site is up to date. The GitHub repo is not.

| | |
|---|---|
| Live | https://tonydefazio.com — **1.5.1**, deployed 2026-08-31 |
| Cloudflare version ID | `82289c9e-f852-4f7c-a4f7-809789a02461` — matches `DEPLOYED.md` |
| Served vs `site/` | all four files **byte-identical** (`index.html`, `robots.txt`, `sitemap.xml`, `thanks.html`) |
| Working tree | clean at `2473bc6` |
| Version agreement | `package.json`, masthead strip, `DEPLOYED.md` all say 1.5.1 |

**The one thing outstanding: `main` is 4 commits ahead of `origin/main`.** The public repo's
last push was 2026-08-28, so all of the 2026-08-31 work is local only:

```
2473bc6  Record the 1.5.1 version ID
7218d77  Proud action potentials, drawn the way the 1996 paper draws them
0037162  Record the 1.5.0 deploy, and retire the one-row wordmark rule
de089fc  Everything else that was still counting to four
```

`git push origin main` fixes it. Ask first — the repo is **public**.

Also stale: `origin/claude/website-dev-status-flags-g3ihxd`, two commits branched from
`5be73c8` on 2026-08-25 ("Flag all four projects as under development", "Version stamp").
`main` is 9 commits ahead of it and the version-stamp idea landed on main independently.
It is superseded; delete it or rebase it, but do not merge it as-is — it still says *four*
projects.

## 2. What this is

One static page, four files in `site/`, **no build step**, deployed to Cloudflare Workers.
It routes to five destinations:

| Card | Subdomain | What it is |
|---|---|---|
| It Looked Right | `lookedright` | AI-coding short course — **newest**, carries the `NEW` star badge |
| Colonel Kernel | `kernel` | calcium-imaging kernel recovery |
| no_peak | `nopeak` | CLUSTER pulse detection |
| bugarach | `bugarach` | coordinated-event detection |
| The Murderboard | `murderboard` | adversarial document review |

Page is 46,400 bytes, **14.4 KB gzipped on the wire**. Five inline `<svg>` graphical
abstracts account for most of the weight.

```bash
npm run serve    # localhost:5099
npm run dry      # wrangler dry-run
npm run deploy   # wrangler deploy
```

After any deploy, run the §2 edge checks in the README. They are not ceremony — `robots.txt`
being byte-identical to source is the check that caught a real host-injection failure on
`bugarach`, and the `beacon.min.js` check is what keeps the no-analytics claim true *as
served* rather than merely as authored.

## 3. Rules this page is built on. Do not quietly break them.

These look like style. They are the product.

- **No network requests.** No fonts, no scripts, no cookies, no analytics. The page makes
  exactly one request, and only if the contact form is sent. Every asset is inline. Adding a
  CDN font or an analytics snippet falsifies a claim in the colophon.
- **Nothing marks the coordinated events** in the bugarach figure. Vertical bands (`.ev`) and
  recoloured ticks (`.tk.hi`) both existed and were both deliberately removed. Every tick is
  drawn identically; the events are found by the eye and by the rate trace. Re-adding a
  highlight makes the figure colour in the answer the detector is supposed to earn. Neither
  rule remains in the stylesheet.
- **The kernel panel's spike trace is on an expanded time base** (currently 40 ms across).
  On the ΔF/F₀ axis the two spikes are 500 ms apart and each would be a fraction of a pixel.
  The `aria-label` says so. Keep that sentence if the figure changes.
- **Figure data is simulated, on purpose.** Nothing on this public page comes from a real
  recording. Real LH and raster data sit in `~/Dropbox/darkroom/{no_peak,bugarach}/`. If that
  is ever revisited, the page owes the reader a provenance statement.
- **README §3 is a claim ledger.** Every factual assertion on the page is listed there with
  its source. Add a claim, add a row. Change a destination, re-read the whole section.

## 4. The trap that has already bitten twice

**Adding a destination falsifies sentences that name no number.** The fifth card landed
2026-08-28 and fixed three counting sites; three more were still wrong three days later,
including the wordmark — the largest text on the page said "Three instruments and one
murderboard" above five cards. Grepping for "four" is not enough. `DEPLOYED.md` §1.5.0 has
the full account, including a claim that went *false* rather than stale: "each repository
carries an instruction file written for an agent" held for four repos and not the fifth.

If a sixth destination lands, budget real time for the recount and re-read §3 line by line.

## 5. Where the figures live

Source, generator and viewer are in **`~/Dropbox/darkroom/tonydefazio/figures/`**, not in
this repo:

```
FIGURES.html      the viewer — open this, works on phone and laptop
HOW-TO-VIEW.md    read first if anything looks blank
make_figures.py   regenerates the SVGs from computed data
ga.css            the stylesheet the SVGs require
ga-*.svg          geometry only — blank on their own, by design
```

The `ga-*.svg` files carry **no stroke or fill**. Every colour comes from the `ga.css` rules
via `currentColor` and each card's `--c`, which is what gives both themes and five accent
colours from one copy of each figure. Opening one directly shows a few words of text and
nothing else. That is not a broken file.

**The gap:** the figures in `site/index.html` are **hand-inlined**. Nothing links the page to
the Dropbox source, and nothing detects divergence. They matched on 2026-09-02. Editing a
figure means regenerating there and pasting back — and updating `ga.css` in *both* places.

## 6. Candidate work

Ordered by value, with what is already known.

1. **Push to GitHub** (§1). One command, four commits, zero risk beyond publicity.
2. **Inbound links** — README §4 calls this the single biggest reason `kernel` was never
   indexed. The page fixed the internal half; the apex still needs a link from somewhere real
   (a UMich page, a GitHub profile README) and `sitemap.xml` submitted to Google and Bing.
   This is the highest-value item on the list and it is not a code change.
3. **Destinations do not link back.** A parent link in each site's footer closes the loop —
   five repos, five deploys: `short-course`, `colonel_kernel`, `no_peak`, `bugarach`,
   `murderboard`.
4. **Verify or drop `19 worked failures`.** The one unverified number on the page, on the
   It Looked Right card. Recorded as unverified in README §3 rather than quietly dropped,
   which is the right posture — but it should get checked.
5. **A staleness check.** `bugarach` has `site-staleness.yml`; it is the model. Nothing here
   detects a claim going stale, and §4 above shows that is the failure mode this page
   actually has. Could also diff the inlined figures against the Dropbox source.
6. **Page weight.** 46 KB / 14.4 KB gzipped, roughly doubled by the figures. Coarser trace
   sampling in `make_figures.py` recovers ~6 KB with no visible difference at card size.
7. **Wide single-column figures.** Between roughly 700–1030 px the cards are one column and
   wide, so a figure renders far larger than the desktop thumbnail. Capping the figure width
   and left-aligning would hold it at abstract scale.
8. **`is-new` is a dead class.** Applied to the It Looked Right card, referenced nowhere in
   the CSS — the `NEW` badge works entirely through `.new-star` plus `.card{position}`.
   Harmless; either style it or drop it.

## 7. Small things worth knowing

- `DEPLOYED.md` dates are **local time**. The 1.4.0 deploy reads 2026-08-26 while
  Cloudflare's UTC log says `2026-08-27T00:00:08Z`. Both are right. Do not "fix" it.
- `Preview.app` cannot open SVG at all. Use Quick Look or Safari. `qlmanage -t` crops
  anything far from square — never judge figure framing from its thumbnail.
- The Dropbox MCP server **cannot overwrite a file**; delete then create. It also takes text
  only — no binary, so no PNG exports land there.
- Rolling back is `npx wrangler delete --name tonydefazio-com`, which removes the Worker
  **and both DNS records**. See `DEPLOYED.md`.
