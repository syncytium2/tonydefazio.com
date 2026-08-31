# Deployed

| | |
|---|---|
| **Worker** | `tonydefazio-com` |
| **Version ID** | `bf7e605c-a678-45c1-806b-56451fcaee62` |
| **Deployed** | 2026-08-31 |
| **Site version** | 1.5.0 |
| **Commit** | see `git log` for the commit this file lands in |
| **Account** | tony.defazio@gmail.com (`9915fb1a39095fa035bccfd49c9434d7`) |

## Live

- https://tonydefazio.com — **apex, custom domain**
- https://www.tonydefazio.com — custom domain, same page. **Took roughly an hour** to go
  from `wrangler deploy` to serving 200; the apex was live within seconds. A first
  custom-domain claim provisions its cert asynchronously, so a 000 on www right after a
  deploy is expected, not a failure. Confirmed byte-identical to the apex, with the
  canonical tag on both pointing at the bare apex.
- https://tonydefazio-com.tonydefazio.workers.dev — workers.dev

## Verified at the edge on deploy day

- `/` 200, `<title>` and `rel="canonical"` correct, canonical points at the bare apex
- `/robots.txt` 200 and **byte-identical to `site/robots.txt`** — ours is served, not a
  host-injected copy. (This is the failure bugarach hit; worth re-checking after any
  Cloudflare zone-setting change.)
- `/sitemap.xml` 200
- **No Cloudflare beacon injected** — 0 matches for `beacon.min.js` in the served HTML, so
  the page's privacy claim is true as served, not just as authored. Since the contact form
  landed, that claim is "no fonts, no JavaScript, no cookies, no analytics; exactly one
  network request, and only if you send the form" — the beacon check is what keeps the
  *first* half honest.
- All five subdomains still 200 — `custom_domain` routes claim only the exact hostname,
  so lookedright / kernel / nopeak / bugarach / murderboard were untouched.

## Masthead provenance strip

Since **1.1.0** the masthead carries `Born / Version / Version date` directly above the
wordmark. `Born` is the first deploy (2026-08-25) and does not change; the other two track
`package.json` and the deploy date. **They are hand-written in `site/index.html`** — there is
no build step to interpolate them, so bumping the version means editing both the JSON and
the `.meta` block, and the `<time datetime>` attributes alongside the visible text.

**The one-row wordmark ended at 1.5.0, and the warning that used to live here is why.**
Until then it was sized to sit on one row at every viewport: `min(2.7rem, (content width)/21)`
with `white-space: nowrap`, the 21 being the string's measured width in ems (18.09 at weight
800 in SF Pro) plus ~16% slack for wider non-Apple sans fallbacks — with a note that editing
the text invalidates the constant, because `body` sets `overflow-x: hidden` and a long string
is therefore **clipped rather than scrolled, and looks deliberate.**

That is exactly what happened. 1.5.0's wordmark is 61 characters ~ 27em against the old 38 ~
18.1em, and measured in Chromium it overflowed at 360, 414, 768, 1024 and 1440 — every
viewport, by 100–260px. Holding one row would have meant a **10px** headline at 360px.

So it wraps now: `clamp(1.5rem, 5vw, 2.4rem)` with `text-wrap: balance` and no `nowrap`. Two
rows on a desktop, three at 360px, nothing clipped. **The rule survives in its new form** — if
the wordmark text changes again, re-measure in a browser rather than trusting either constant.

## Card copy

**1.2.0 cut each card to a single sentence** and removed the licence chips. What the cards
say is paraphrase, not quotation — checked against the five live sites, four on 2026-08-26 and
lookedright on 2026-08-31, none of the card sentences appears verbatim on the site it
describes; only the short chips do.
See README § *Keeping it honest* for which claims survive and which were retired.

The page now names **no licence anywhere**. The footer defers to the repositories, which is
deliberate: a licence can change upstream without this page becoming wrong.

## Graphical abstracts

**1.4.0 inlined a figure into each of the four cards**, and the fifth arrived with the
It Looked Right card on 2026-08-28. They are inline `<svg>` carrying
geometry only; every stroke and fill comes from the `graphical abstracts` block in the page
stylesheet, via `currentColor` and each card's `--c`. That is what gives both themes and
five accent colours from one copy of each figure — and it is why the SVGs are useless to
look at outside the page.

Source, generator and a viewer live in `~/Dropbox/darkroom/tonydefazio/figures/`, not in
this repo. `make_figures.py` regenerates them; `FIGURES.html` displays them with captions.
**The figures here are hand-inlined** — editing them means regenerating there and pasting
back, and `figures/HOW-TO-VIEW.md` records why.

The data in three of the five is **computed but simulated**. Nothing on this page comes from
a real recording, deliberately, since the page is public. The other two (murderboard, It
Looked Right) are process diagrams, not data.

Two decisions that must not be quietly reverted, both taken 2026-08-26:

- **Nothing marks the coordinated events** in the bugarach figure. Vertical bands (`.ev`)
  and recoloured ticks (`.tk.hi`) both existed and were both removed. The events are found
  by eye and by the rate trace, or the figure colours in the answer the detector is meant
  to earn. Neither rule remains in the stylesheet.
- **The kernel panel draws real action potentials** — peak +36 mV, half-width 0.41 ms, AHP
  trough −73 mV — on an **expanded time base** (8 ms across). On the ΔF/F₀ axis those two
  spikes are 500 ms apart and each would be a quarter of a pixel wide. The convolution is
  over spike *times*; the waveform shows what a spike is, not its scale against the trace.
  The `aria-label` says so; keep that if the figure changes.

Page weight went 20 KB → 42 KB (13.4 KB gzipped on the wire). Still no fonts, no scripts,
no cookies, and no network request unless the form is sent.

## Contact form

Verified end to end on **2026-08-25**: submitted from a real browser against the live page,
reached `/thanks`, and **the message arrived in the inbox**. The shared Web3Forms key
(`b8c22a4e-…`, also used by `no_peak`) delivers correctly. See README § *The contact form*
for how to re-test — and for why `curl` cannot.

## 1.5.0 — the counting fixes

**Deployed 2026-08-31.** No new card; this is the commit that made the page agree with the
shelf it already had. The fifth destination landed 2026-08-28 and fixed three counting sites;
this one fixed the rest, including the wordmark, which was the largest text on the page and
said "Three instruments and one murderboard" above five cards for three days.

Re-verified at the edge on deploy day: apex and www **200 and byte-identical to `site/`**,
`robots.txt` byte-identical, `/sitemap.xml` and `/thanks` 200, **0 matches for
`beacon.min.js`**, five `<a class="card">` served, JSON-LD parses with `subjectOf` of five,
canonical on the bare apex, masthead reading 1.5.0.

**One claim was false, not stale**, and is worth remembering as a category: "each repository
carries an instruction file written for an agent" held for four repositories and not the
fifth (`short-course` has `.claude/` and a HANDOFF.md, no CLAUDE.md or AGENTS.md). Adding a
destination can falsify a sentence that names no number at all — counting the cards is not
enough to find everything a new card breaks.

**`19 worked failures` is the one unverified number on the page.** See README §3. It was
deployed as-is rather than quietly dropped, because an unverified claim that is recorded as
unverified is a different thing from one that looks checked.

## Rolling back

```bash
npx wrangler delete --name tonydefazio-com
```

Removes the Worker **and** both DNS records, returning the apex and www to the empty state
they were in before 2026-08-25. Nothing else on the zone is affected.
