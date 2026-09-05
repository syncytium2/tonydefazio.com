# Deployed

| | |
|---|---|
| **Worker** | `tonydefazio-com` |
| **Version ID** | `11997c97-b38f-49fd-8d81-a0d70bc3e88a` |
| **Deployed** | 2026-09-04 |
| **Site version** | 1.6.1 |
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
stylesheet, via `currentColor` and each card's `--c`. That is what gives five accent
colours from one copy of each figure — and it is why the SVGs are useless to look at
outside the page. *(It also gave both themes until 2026-09-04, when dark mode was removed;
see §1.6.1.)*

Source, generator and a viewer live in `~/Dropbox/darkroom/tonydefazio/figures/`, not in
this repo. `make_figures.py` regenerates them; `FIGURES.html` displays them with captions.
**The figures here are hand-inlined** — editing them means regenerating there and pasting
back, and `figures/HOW-TO-VIEW.md` records why.

The AP panel was redrawn in 1.5.1. Two defects, one visual and one real: the spikes had a
fast upstroke and a long ski-slope repolarisation, nothing like the published record; and the
AHP, at `AHP_TD = 4.0 ms`, took **10.56 ms to recover inside an 8 ms panel**, so it never came
back and the trace simply ended below rest. The AHP onset is now raised to a power (`AHP_P`)
so it no longer bites the peak, and `PEAK_MV` / `AHP_AMP` were re-solved so the measured peak
(+35.8 mV) and trough (−72.7 mV) are held **exactly** — both numbers are unchanged from 1.4.0.
Recovery is 5.1 ms. Sampling density was picked by measurement: at 0.040 ms the drawn peak sits
0.028 px below the true one against a 1.5 px stroke, where the first attempt used 0.012 ms and
spent 4 KB of path on 0.027 px nobody can see.

The data in three of the five is **computed but simulated**. Nothing on this page comes from
a real recording, deliberately, since the page is public. The other two (murderboard, It
Looked Right) are process diagrams, not data.

Two decisions that must not be quietly reverted, both taken 2026-08-26:

- **Nothing marks the coordinated events** in the bugarach figure. Vertical bands (`.ev`)
  and recoloured ticks (`.tk.hi`) both existed and were both removed. The events are found
  by eye and by the rate trace, or the figure colours in the answer the detector is meant
  to earn. Neither rule remains in the stylesheet.
- **The kernel panel draws real action potentials** — peak +36 mV, half-width 0.42 ms, AHP
  trough −73 mV. **The 8 ms expanded time base was retired in 1.5.1, deliberately and at
  Tony's call**, in favour of the 40 ms base the 1996 paper's Fig. A2 uses. The old rule read
  "the waveform shows what a spike is, not its scale against the trace"; the new one gives up
  morphology on purpose — at 40 ms the half-width is 0.8 px, so the panel shows *that* it
  spiked, which is what the convolution is over. **What survives unchanged is the requirement
  that the `aria-label` state the base**, and it does: "on a 40 ms base". If the figure changes
  again, keep that.

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

## 1.6.0 — the sixth destination

**Deployed 2026-09-04**, version ID `11997c97-b38f-49fd-8d81-a0d70bc3e88a`. Two files
changed at the edge (`index.html`, `thanks.html`); `robots.txt` and `sitemap.xml` were
already current.

**What 1.6.0 is.** A sixth destination, `draughtsman` — readable architecture diagrams for
PyTorch models — placed first on the shelf and carrying the `NEW` star, which it takes from
It Looked Right on the honest grounds that it is newer (first commit 2026-09-01 against
2026-08-28). It linked to `github.com/syncytium2/draughtsman` at first, because
`draughtsman.tonydefazio.com` served over HTTP with no certificate. **Resolved 2026-09-04
and the card now points at the site.** GitHub had never *requested* the certificate — the
domain was set by committing a `CNAME` file rather than through the Pages API, so
`https_certificate` read `state: None`, not `in_progress` and not an error, for about ten
hours. Re-setting the custom domain through the API fired the request and it issued within
seconds:

```bash
gh api -X PUT repos/<owner>/<repo>/pages -f cname=''
gh api -X PUT repos/<owner>/<repo>/pages -f cname='<host>'
```

**That distinction is the useful part**: `state: None` means never asked, and waiting longer
would never have fixed it. `in_progress` is the one you wait on.

**Also in 1.6.0: a `Born` stamp on every card**, being that repository's first commit,
emitted as `<time datetime=…>`. Born only — no version, no revised date. Both of those move
on every upstream commit and this page has no build step, so a copy of either becomes a
second source that rots silently. Born cannot move. The estate runs two conventions and
this page follows the first: `Born` means repo birth (colonel_kernel, no_peak), `First
published` means page birth (bugarach, short-course). See README §3, including the trap
that three of six destinations are client-side apps whose stamps are invisible to `curl`.

**The recount §4 warns about was run and found four more.** Two README sentences, two
`thanks.html` comments. One went *false* rather than stale: the no-external-requests
posture, which draughtsman's page does not hold — it requests a webfont from
`fonts.googleapis.com`. Narrowed rather than widened; nothing shipped was ever wrong.

**The card's figure is draughtsman's own output, as of 2026-09-04.** It was a schematic, on
the measurement that all ten figures rendered detail type between 1.6px and 3.6px at 420×104
against a screen floor near 8px. Tony's condition for revisiting was stated in advance —
*once draughtsman has an icon mode that drops text rather than shipping it as grey noise* —
and it was met the same day. `render --icon 420x104` on `examples/gallery/lenet` fits at
0.86x and carries no text at all. **The condition was written down before it was met, which
is why the swap took one measurement rather than an argument.**

bugarach's card takes the same treatment from `examples/tube` — which is the model bugarach
actually runs, vendored from draughtsman. That one is an **editorial** change rather than a
repair: it replaced a raster figure that illustrated the card's sentence with a model mark
that does not. Both retired abstracts are still generated and show as UNUSED in the drift
check, so either card reverts in one line.

**The marks' stage fills are restatable.** draughtsman emits `var(--ds-fill-<kind>, <hex>)`.
This page restated the nine kinds for dark mode; since 1.6.1 there is no dark mode and the
hex fallback is what renders. The mechanism is worth keeping in mind rather than deleting:
it is how a host supplies its own ground. Its rule
is *hue is the family, value is the kind* — the three convolutional kinds must stay apart by
value so a figure survives a greyscale print. Verified here rather than assumed: within-family
separation is preserved and mostly improved (kernel|conv 1.083:1 → 1.139:1, conv|stack 1.114 →
1.194), and all three greens stay green-dominant. **Do not flatten these to `currentColor`** to
make them match the card accent; that discards a tested property.

## Verified at the edge on 2026-09-04

- `index.html`, `robots.txt`, `sitemap.xml` **byte-identical** to `site/`.
- **`thanks.html` needs a followed redirect, and this is not a fault.** `/thanks.html`
  returns **307 → `/thanks`**; the Workers assets runtime drops the `.html` extension.
  A plain `diff <(curl -s …/thanks.html) site/thanks.html` therefore compares against an
  empty body and reports DIFFERS. With `curl -sL` it is byte-identical. **Use `-L` for that
  one file** — this cost a few minutes on deploy day and would read as a broken page to
  anyone who did not.
- **No analytics as served**: zero `beacon.min.js`, and — checked properly this time — no
  external `<script>`, `<img>` or stylesheet, and no webfont reference. The page's one
  `<script>` is `type="application/ld+json"`, which is data, not executable JavaScript, so
  the colophon's "runs no JavaScript" holds as served. Counting *anchor hrefs* to other
  sites is the wrong check and reports 21; those are links, not loads.
- Six `<a class="card">` served, six `Born` stamps, two draughtsman model marks, version
  strip reads 1.6.0, `HTTP/2 200`.
- The deploy gate held: `github.com/syncytium2/draughtsman` returned 200 to an anonymous
  request immediately before upload.

## 1.6.1 — light only

**Deployed 2026-09-04.** Removed the `prefers-color-scheme: dark` palette and the
`[data-theme="dark"]` override from both pages, and declared `color-scheme: light` on
`:root`.

**Why: most of the figures were wrong on a dark ground, and that is not a palette problem.**
They are drawn as plates on paper. `no_peak`'s pulse bands are pale blue highlights behind a
trace; inverted they read as heavy navy slabs that look like the data. Both draughtsman model
marks went muddy — their stage fills were restated dark and still sat too close to the card.
Supporting a second ground meant every figure had to work twice, and half did not.

**A defect the removal exposed.** With the dark block gone, `form.contact button` was still
governed by `:root:not([data-theme="light"]) form.contact button { color: #1B1719 }`, which
matches when no `data-theme` is set — i.e. always — and outranks a plain `form.contact
button` on specificity. The Send button would have rendered dark text on the dark red button.
Both `[data-theme]` rules are gone and the colour is stated once. **A conditional rule whose
condition can never be false is not a conditional rule**, and deleting the branch that made
it look conditional is what surfaced it.

Verified after: page renders identically under `prefers-color-scheme: dark`, all six accents
resolve, Send is `#fff` on `#8A1C2B` in both OS settings.

## Rolling back

```bash
npx wrangler delete --name tonydefazio-com
```

Removes the Worker **and** both DNS records, returning the apex and www to the empty state
they were in before 2026-08-25. Nothing else on the zone is affected.
