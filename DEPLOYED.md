# Deployed

| | |
|---|---|
| **Worker** | `tonydefazio-com` |
| **Version ID** | `79368695-47ac-4683-b121-e83f827ca536` |
| **Deployed** | 2026-08-26 |
| **Site version** | 1.4.0 |
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
- All four subdomains still 200 — `custom_domain` routes claim only the exact hostname,
  so kernel / nopeak / bugarach / murderboard were untouched.

## Masthead provenance strip

Since **1.1.0** the masthead carries `Born / Version / Version date` directly above the
wordmark. `Born` is the first deploy (2026-08-25) and does not change; the other two track
`package.json` and the deploy date. **They are hand-written in `site/index.html`** — there is
no build step to interpolate them, so bumping the version means editing both the JSON and
the `.meta` block, and the `<time datetime>` attributes alongside the visible text.

The wordmark is sized to sit on one row at every viewport: `min(2.7rem, (content width)/21)`
with `white-space: nowrap`. The 21 is the string's measured width in ems (18.09 at weight 800
in SF Pro) plus ~16% slack for wider non-Apple sans fallbacks. **Editing the wordmark text
invalidates that constant** — a longer string will overflow, silently, because `body` sets
`overflow-x: hidden`.

## Card copy

**1.2.0 cut each card to a single sentence** and removed the licence chips. What the cards
say is paraphrase, not quotation — checked against the four live sites on 2026-08-26, none
of the card sentences appears verbatim on the site it describes; only the short chips do.
See README § *Keeping it honest* for which claims survive and which were retired.

The page now names **no licence anywhere**. The footer defers to the repositories, which is
deliberate: a licence can change upstream without this page becoming wrong.

## Graphical abstracts

**1.4.0 inlined a figure into each of the four cards.** They are inline `<svg>` carrying
geometry only; every stroke and fill comes from the `graphical abstracts` block in the page
stylesheet, via `currentColor` and each card's `--c`. That is what gives both themes and
four accent colours from one copy of each figure — and it is why the SVGs are useless to
look at outside the page.

Source, generator and a viewer live in `~/Dropbox/darkroom/tonydefazio/figures/`, not in
this repo. `make_figures.py` regenerates them; `FIGURES.html` displays them with captions.
**The figures here are hand-inlined** — editing them means regenerating there and pasting
back, and `figures/HOW-TO-VIEW.md` records why.

The data in three of the four is **computed but simulated**. Nothing on this page comes from
a real recording, deliberately, since the page is public. The fourth (murderboard) is a
process diagram, not data.

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

## Rolling back

```bash
npx wrangler delete --name tonydefazio-com
```

Removes the Worker **and** both DNS records, returning the apex and www to the empty state
they were in before 2026-08-25. Nothing else on the zone is affected.
