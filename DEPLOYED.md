# Deployed

| | |
|---|---|
| **Worker** | `tonydefazio-com` |
| **Version ID** | `9b40a5eb-b7b3-4741-83c6-aab73e2ac738` |
| **Deployed** | 2026-10-21 |
| **Site version** | 1.11.1 |
| **Commit** | see `git log` for the commit this file lands in |
| **Account** | tony.defazio@gmail.com (`9915fb1a39095fa035bccfd49c9434d7`) |

## 1.7.0 — 2026-09-09 — the CV, with fifteen students taken out of it

Version ID `c0187e47-8151-43dc-bd66-9afdade72516`. Two assets uploaded: `/index.html` and
`/cv.pdf`. **`site/` now holds a binary**, which it never has before.

The masthead gained **CV (PDF)** → `/cv.pdf`, beside GitHub / ORCID / Publications.

**What is served is not the CV Tony sends people.** The file td-resume produced named 7
graduate mentees, 6 undergraduates and 2 dissertation-committee students, most from
2009-2011. `robots.txt` invites every crawler, so publishing it as-is would have made former
students searchable against a document they never agreed to appear in — and one carried a
health-adjacent internship detail. Each block is now a count and its institutions, and the
page-1 header says so and gives `tony@tonydefazio.com` for the real one. Built by
`tools/make_public_cv.py`; see README §3 for what the link asserts.

**⚠ THIS FILE WILL GO STALE AND NOTHING HERE WILL NOTICE.** The four corrections in the
private CV (degree fields, PhD advisor, a duplicated chapter, the Physiol 578 lecture count)
live in Symplectic Elements records, not in the document. The next CV generated from Elements
has all four defects back and disagrees with the published copy on a date nobody picks. The
durable fix is in Elements. Whoever replaces `site/cv.pdf` must re-run `make_public_cv.py`,
which fails loudly rather than quietly publishing a name.

### Verified at the edge, 2026-09-09

- `/cv.pdf` 200, `content-type: application/pdf`, **byte-identical to `site/cv.pdf`**
- **Zero of the fifteen student names** in the PDF text pulled back off the live URL — checked
  against the served file, not the local one
- The `Full CV on request — tony@tonydefazio.com` header line is present in the live file
- `/`, `/robots.txt`, `/sitemap.xml`, `/thanks`, `/cv.pdf` all byte-identical to source
- masthead reads 1.7.0; 0 matches for `beacon.min.js`; 0 external subresources

> **`/index.html` 307s to `/`, exactly as `/thanks.html` 307s to `/thanks`.** Byte-comparing
> the served page needs `curl -sL` or the check reports DIFFERS against a redirect body. This
> bit during the 1.7.0 edge checks and looked briefly like a host-injection failure. It is the
> assets Worker's default `auto-trailing-slash`, not a fault.

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

bugarach's card took the same treatment from `examples/tube` — the model bugarach actually
runs, vendored from draughtsman — on 2026-09-04, as an **editorial** change rather than a
repair. **It was reverted on 2026-10-15 at Tony's call**: the card shows the raster again,
which illustrates the card's sentence where the model mark did not. The tube mark is still in
the darkroom as `ds-b.svg`, so either direction is a one-block swap.

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

## A comment quoting the old byline, and a report that was not caused by it

**Deployed 2026-09-10**, version ID `957f99da-8676-4013-b7e2-e70a55b64423`. One file
uploaded: `/index.html`. No rendered output changed — the edit is to a CSS comment above
`.whois` that quoted the superseded byline, `Neuroendocrinology & calcium imaging`,
verbatim. Comments in `site/index.html` ship, because there is no build step and
`wrangler deploy` uploads the file as committed. Removing the quotation is mild
housekeeping and stands on its own.

**The reason recorded here at first was wrong, and the correction is the point.** A
reviewer had reported three defects on the live site — the old byline, the draughtsman
card linking to GitHub, and draughtsman missing from the footer's "The sites". All three
were false against the live page. This entry originally claimed the reviewer had found the
string by reading the delivered source, and that the comment was therefore a live false
claim. That was a guess presented as a cause. The reviewer never saw the source; they were
working from extracted rendered text, where a CSS comment is invisible. And the comment
could not have produced the other two findings at all.

**The actual cause was a stale cached fetch.** The reviewer was served a copy of the page
predating `f2ed3b1`, stamped `Version 1.6.0 · 2026-09-04`. That build is internally
consistent with everything they reported: the old byline rendered in the markup, the
draughtsman card's href resolving to `github.com/syncytium2/draughtsman`, a five-item
footer with draughtsman absent, and prose reading "all five sites". `19c28a3` changed the
href, the footer and the count together; `f2ed3b1` had changed the byline just before it.
One stale build explains all three findings. The comment explains none of them.

**The version stamp is a weaker check than it looks.** `Version` and `Version date` do not
move per commit — `1.6.0 · 2026-09-04` covers the broken build *and* the repaired one, so
the stamp cannot distinguish them. It would have caught this particular case only because
the stale copy was five days and one minor version behind. For site-state claims, fetch
with `curl` and diff against `site/index.html`; treat the stamp as a coarse smoke test, not
proof.

Verified after: `curl https://tonydefazio.com/` contains zero occurrences of the old
string, the `.whois` byline renders unchanged, and `draughtsman.tonydefazio.com` still
appears three times — the card link, the footer's "The sites" entry, and the `WebSite`
schema block.

## 1.7.1 — 2026-09-11 — neurophysiologist

Version ID `d16ecbe6-a0c7-4419-8575-8208cc0b5dfc`. One asset uploaded: `/index.html`.

The byline read "Neuroendocrinologist by training". Tony is a neurophysiologist and said so, so it
now reads **"Neurophysiologist by training"**. `knowsAbout` in the JSON-LD gains `Neurophysiology`;
`Neuroendocrinology` stays in that list as a topic, not a title — the hormone-pulse tools are real
work in it. Masthead and `package.json` move to 1.7.1, dated 2026-09-11.

**The table above had been stale since 2026-09-10.** That day's comment-only deploy (`957f99da`,
below) was recorded in its own section but never reached this file's header, which went on
naming 1.7.0's `c0187e47`. Corrected here.

Verified after: apex and `www` both byte-identical to `site/index.html`; the byline, version and
date render as committed; no identity-sense "Neuroendocrinologist" remains on the page.

## 1.8.0 — 2026-09-23 — gaba_excites, the seventh card

Version ID `cee1d4c0-6759-48f4-b4e7-cd6c33334054`. One asset uploaded: `/index.html`.

A card for `gaba.tonydefazio.com`, first on the shelf, in `--c-gaba` `#B5461A`. The NEW
sticker moves to it from draughtsman. Its figure is gaba_excites' own simulation (README §3):
one 600 pA step, the same GABA in each panel, E_GABA at −80 / −60 / −35 mV, firing 0 / 0 / 4.
The footer, JSON-LD `subjectOf`, meta descriptions and deck gain it; "six" becomes "seven"
wherever the page counts. Masthead and `package.json` move to 1.8.0, dated 2026-09-23.

Verified after, by `curl` with a cache-busting query: `/`, `/robots.txt`, `/sitemap.xml`,
`/thanks`, `/cv.pdf` byte-identical to `site/`; `www` byte-identical to `site/index.html`;
seven `class="card"` served; masthead 1.8.0; 0 matches for `beacon.min.js`.

## 1.9.0 — 2026-09-25 — ml2dl, the eighth card

Version ID `00d2ee03-37e6-49bc-b164-3587fa0d1489`, deployed by Tony from the `ml2dl-card`
worktree (the session's own `npm run deploy` was refused by its permission check).

A card for `ml2dl.tonydefazio.com`, first on the shelf, in `--c-ml2dl` `#A3246A`, carrying a
`development preview` chip because the site says it is one. The NEW sticker moves to it from
gaba_excites. Its figure is ml2dl's own XOR lesson (README §3): best single line 75%, two ReLU
hidden units 100%. **ml2dl's repository is private**, so it has no source link and the common
thread now reads "Seven of the eight repositories are public". "Seven" becomes "eight" wherever
the page counts. Masthead and `package.json` move to 1.9.0, dated 2026-09-25.

Verified after, by `curl` with a cache-busting query: `/`, `/robots.txt`, `/sitemap.xml`,
`/thanks`, `/cv.pdf` byte-identical to `site/`; `www` byte-identical to `site/index.html`;
eight `class="card"` served; masthead 1.9.0; 0 matches for `beacon.min.js`.

## 1.9.1 — 2026-10-13 — the CV rebuilt from the October source

Version ID `ff7d31ce-87e4-40db-a6e3-b650d3bf62c6`, deployed from the `cv-republish` worktree.
Two assets uploaded: `/index.html` and `/cv.pdf`.

`site/cv.pdf` is rebuilt by `tools/make_public_cv.py` from `td-resume/cv/defazio_cv_2026b.docx`
as it stood on 2026-10-12, on td-resume's handoff of 2026-09-18. The script itself did not
change: the Under Review strip that handoff first asked for was overtaken when the paper was
accepted, so the entry is published under *In Press*. README §3 lists what the new copy carries
that the 1.7.0 copy did not. 13 pages (`/Count` read from the file), 551,855 bytes, MD5
`8195c30d5e1b3dbd9589e0601171cde2`. Nothing on the page changed but the version strip.

Build output: positive control 15/15 names found in the unredacted source, 0/15 in the
published copy, co-author citations intact, header line present. The name grep over the
outgoing commit returned nothing, and the same pipe counted a word known to be in the diff.

Verified after, by `curl` with a cache-busting query: `/`, `/robots.txt`, `/sitemap.xml`,
`/thanks`, `/cv.pdf` byte-identical to `site/`; `www` byte-identical to `site/index.html`;
`/cv.pdf` 200, `application/pdf`. In the text pulled back off the live URL: 0 of 15 names, with
`DeFazio` found by the same matcher; the public-copy header line once; the In Press entry
present and no Under Review heading; all guarded co-author citations present. Eight
`class="card"` served; masthead 1.9.1; 0 matches for `beacon.min.js`.

## 1.10.0 — 2026-10-13 — a resume beside the CV

Version ID `30dc724c-1a26-441e-9ce6-2f14342155ba`, deployed from the `cv-republish` worktree.
Two assets uploaded: `/index.html` and `/resume.pdf`. `site/` now holds two binaries.

The masthead gained **Resume (PDF)** → `/resume.pdf`, ahead of CV (PDF). The file is td-resume's
technical variant, copied in as built and not generated here; README §3 has what the link
asserts. Tony approved the electrophysiology-led cut for the site the same day, after td-resume
and this session both raised the unpublished lab figures it carries. 2 pages, 99,735 bytes, MD5
`381384d6b11627cadaf95f84c24ce5a2`.

Verified after, by `curl` with a cache-busting query: `/`, `/robots.txt`, `/sitemap.xml`,
`/thanks`, `/cv.pdf`, `/resume.pdf` byte-identical to `site/`; `www` byte-identical to
`site/index.html`; `/resume.pdf` 200, `application/pdf`; eight `class="card"` served; masthead
1.10.0; 0 matches for `beacon.min.js`.

## 1.10.1 — 2026-10-13 — one prose width in the masthead

Version ID `b7dab007-f1e5-487d-a4a3-a04e88bb6765`, deployed from the `cv-republish` worktree.
One asset uploaded: `/index.html`.

Tony counted about five different column widths above the cards. The byline and the intro
paragraph each set a width in `ch` at a different font size, so they ended at different right
edges, and the fifth link added in 1.10.0 wrapped alone onto its own line. Both paragraphs now
use `--measure`, set in `rem` (34rem) and shared with the common-thread prose, and the identity
links sit in a row of their own beneath the byline. The headline keeps its balanced wrap, so
there are three right edges above the cards: the full rule, the headline and the prose. Looked
at in headless Chrome at 1100 px and 500 px before upload.

**The edge lagged after the 1.10.0 upload.** The first `curl` of `/` straight after that deploy
returned the 1.9.1 page while `/resume.pdf` was already served; repeat checks returned 1.10.0.
A DIFFERS in the first seconds after a deploy is worth one retry before it is believed.

Verified after, by `curl` with a cache-busting query: `/`, `/robots.txt`, `/sitemap.xml`,
`/thanks`, `/cv.pdf`, `/resume.pdf` byte-identical to `site/`; `www` byte-identical to
`site/index.html`; eight `class="card"` served; masthead 1.10.1; 0 matches for `beacon.min.js`.

## 1.10.2 — 2026-10-13 — the masthead on the cards' grid

Version ID `8348a1d8-4a13-44d6-83f9-8e61920fe7d6`, deployed from the `cv-republish` worktree.
One asset uploaded: `/index.html`.

1.10.1 was not enough: Tony looked at it in Chrome and it still read as sloppy, with three
right edges above the cards and the right half of the page empty beside the prose. The masthead
now sits on the same two-column grid as the cards (`--col-min`, `--col-gap`). The byline takes
the first column and the identity links the second, on a shared baseline. The intro is two
paragraphs, one per column, split where it turns from the instruments to the rest; its words
are unchanged. Below 1030 px, where the grid is one column, the byline and intro are capped at
`--measure` so the lines do not run the full width. The headline is untouched.

Looked at in headless Chrome at 1440, 1206, 1040, 1020 and 700 px before upload.

Verified after, by `curl` with a cache-busting query: `/`, `/robots.txt`, `/sitemap.xml`,
`/thanks`, `/cv.pdf`, `/resume.pdf` byte-identical to `site/`; `www` byte-identical to
`site/index.html`; eight `class="card"` served; masthead 1.10.2; 0 matches for `beacon.min.js`.

## 1.10.3 — 2026-10-14 — the lecture line corrected on the CV and the resume

Version ID `3133564b-caa9-4a02-99d3-7035e887be04`, deployed from the `teaching-line` worktree.
Three assets uploaded: `/index.html`, `/cv.pdf`, `/resume.pdf`.

On td-resume's request, which said Tony asked for it that day; Tony confirmed it on 2026-10-16.
Both documents had given 18 lectures for Physiol 578, which was Tony's total across three
courses. The CV now says 578 is a 42-lecture course taught by 10 faculty, 12 of the lectures his
in 2026-27, and gives 592 as 2 lectures and a student presentation; its footer is dated
`10/14/2026`. The resume carries the same figures and adds the team-taught Human Physiology and
Integrative Neuroscience. Source: td-resume `main`, commit `62b2871`.

`cv.pdf` rebuilt by `tools/make_public_cv.py`: positive control 15/15, published copy 0/15,
co-author citations intact, header line present. 13 pages, 551,765 bytes, MD5
`aef30e89772b887c8c8c095d73d516d9`. `resume.pdf` copied from td-resume's `out/technical.pdf`:
2 pages, 99,865 bytes, MD5 `2f57f1623d32c0883d06d1f99c9bb465`. Name grep over the outgoing
commit: nothing.

Verified after, on 2026-10-14, by `curl` with a cache-busting query: all six files
byte-identical to `site/`; `www` byte-identical to `site/index.html`; both PDFs 200,
`application/pdf`. In the text pulled back off the live URLs: 0 of 15 names in either, with the
control found; the 42-lecture line in both and no 18-lecture line in either; the CV's header
line once and its guarded citations all present. Eight `class="card"`; masthead 1.10.3.

The record itself was not committed that day; the permission check refused the command.

### Overwritten at the edge on 2026-10-15, and put right by 1.10.4

`wrangler deployments list` shows version `034ad65c-5fd7-47fe-8553-5a97eb1c6046`, created
2026-10-15T16:59Z, after this one. Checked on 2026-10-16, it serves:

- `/index.html` with the bugarach raster card from the `bugarach-raster` worktree, but stamped
  **`1.10.3` / `2026-10-13`**: a version number that described a different page, and a date
  older than this deploy;
- **the 1.9.1 `cv.pdf`** (MD5 `8195c30d…`, 551,855 bytes, footer `10/12/2026`) and **the 1.10.0
  `resume.pdf`** (MD5 `381384d6…`, 99,735 bytes) — both with the old 18-lecture line.

So the lecture correction above is **not live**, though nothing on the page says so. The
`bugarach-raster` branch (`0536561`, `8e6875a`) already sits on top of this commit and holds the
corrected PDFs; deploying it, or this branch, puts them back. Whoever does that: re-verify the
two PDFs by MD5 at the edge rather than trusting the masthead, which is exactly what failed here.

**Resolved 2026-10-16 by 1.10.4.** The overwriting deploy came from `bugarach-raster` before it
was rebased onto this commit (its tree then was `3f0742a`, cut from a `main` that did not have
`f033004`), so it was on a branch, just not one anyone kept: the rebase replaced it.

## 1.10.4 — 2026-10-16 — the bugarach raster, the corrected PDFs back, American spelling

Version ID `d15a1944-9497-4965-b356-faefeaab2ce3`, created 2026-10-16T17:30Z, deployed by Tony
with `npm run deploy` from the `bugarach-raster` worktree at `2365334`.

- **The bugarach card shows the raster/rate abstract again**, in place of draughtsman's `tube`
  mark, at Tony's call. `ga-bugarach.svg` from the darkroom, inlined unchanged; the other five
  data figures were confirmed byte-identical to their darkroom files first. README §3 has the
  editorial reasoning; the mark is kept in the darkroom as `ds-b.svg`.
- **The 1.10.3 `cv.pdf` and `resume.pdf` are live again**, undoing the 2026-10-15 overwrite.
- **American spelling:** analyze and license in visible text; recognizable (homepage and
  thanks page), recolored and depolarized in the stylesheet comments, which ship.
- **`tools/predeploy.py` now runs before every `npm run deploy`.** It writes the
  `package.json` version and today's date into the masthead, and refuses the upload unless that
  version is greater than the one live. Either half would have stopped the 2026-10-15 deploy.

Verified after, by `curl` with a cache-busting query: `/`, `/robots.txt`, `/sitemap.xml`,
`/thanks`, `/cv.pdf`, `/resume.pdf` byte-identical to `site/`; `www` byte-identical to
`site/index.html`; `cv.pdf` MD5 `aef30e89772b887c8c8c095d73d516d9` and `resume.pdf` MD5
`2f57f1623d32c0883d06d1f99c9bb465`, both `200 application/pdf`; eight `class="card"`; the
raster (`ga-b`) served; masthead 1.10.4 / 2026-10-16; 0 matches for `beacon.min.js`.
Checked independently by two sessions.

## 1.10.5 — 2026-10-19 — the public CV's links go to PubMed

Version ID `f0c9ef5f-35aa-465e-bbff-290bda7d4cd2`, deployed from the `cv-pubmed-links` worktree
through `tools/predeploy.py`, which stamped the masthead 1.10.5 / 2026-10-19 against a live
1.10.4. Two assets uploaded: `/index.html` and `/cv.pdf`.

On td-resume's request, which Tony confirmed in this session before the deploy. td-resume moved
every citation link in the private CV from Symplectic (behind a U-M login) to the paper on
PubMed, and dropped the link from talks and posters with no PubMed record (td-resume `fcae9af`).
`cv.pdf` rebuilt by `tools/make_public_cv.py`: positive control 15/15, published copy 0/15,
co-author citations intact, header line present. 13 pages, 442,828 bytes, MD5
`97593acfb3d6c5f66ca264abc38d4a13`, footer `10/19/2026`. Name grep over the outgoing commit:
nothing.

Verified after, by `curl` with a cache-busting query: all six files byte-identical to `site/`;
`www` byte-identical to `site/index.html`; `/cv.pdf` 200, `application/pdf`. In the live CV: 461
`/URI` annotations, every one to `pubmed.ncbi.nlm.nih.gov`, none to Symplectic; 0 of 15 names
with the `DeFazio` control found; the header line once; 3 of 3 guarded citations; the
42-lecture line still present. Eight `class="card"`; masthead 1.10.5; 0 matches for
`beacon.min.js`.

## 1.11.0 — 2026-10-20 — ionhomie, the ninth card

Version ID `2f5d491b-c046-46c0-b497-41e439c85e39`, deployed from the `ionhomie-card` worktree
through `tools/predeploy.py`, which stamped 1.11.0 / 2026-10-20 against a live 1.10.5. One asset
uploaded: `/index.html`.

Tony: "add ionhomie as a new tile", and "make sure it has a return tag". The card went out only
after ionhomie v0.1.4 (release commit `3a6f88b`) put "← tonydefazio.com" in the top bar of every
route; checked in its live bundle and in a screenshot of the live page first. The card is first
on the shelf and takes the NEW sticker from ml2dl; accent `#4A4FC0`; figure `ga-i`, ionhomie's
rundown computed by ionhomie (README §3). The sentences that counted the sites now name no
number. Figure drift check before upload: the three known rows and nothing new.

Verified after, by `curl` with a cache-busting query: all six files byte-identical to `site/`;
`www` byte-identical to `site/index.html`; nine `class="card"`, the first and the one with the
NEW sticker both ionhomie; `ga-i` present; masthead 1.11.0; 0 matches for `beacon.min.js`.

## 1.11.1 — 2026-10-21 — the ionhomie tile shows the living cell

Version ID `9b40a5eb-b7b3-4741-83c6-aab73e2ac738`, deployed from the `ionhomie-cell` worktree
through `tools/predeploy.py` (1.11.1 / 2026-10-21 against a live 1.11.0). One asset uploaded:
`/index.html`.

Tony rejected the 1.11.0 rundown graph ("we've got these beautiful animations and you pulled a
graph that half or more of our audience will ignore"), then a light restyle of the cell ("are
those the original colors?"). What shipped is ionhomie's home-page cell drawn through its own
stage code at ionhomie `5c225e6`: dark ground, its own ion colors and labels, a 12 s CSS loop
of the model's fluxes, a still frame under reduced motion. The page's first moving figure; still
no script. Its styles are scoped to `.ga-i`. Tony approved it from screenshots before upload.

Checked before upload in headless Chrome at 1206 and 500 px: the figure moves between frames,
does not under `--force-prefers-reduced-motion`, and no other card changes over time. Figure
drift check: the three known rows only.

Verified after, by `curl` with a cache-busting query: all six files byte-identical to `site/`;
`www` byte-identical to `site/index.html`; nine `class="card"`; `ga-i` at viewBox 420×210;
one `<script`, the JSON-LD block (`application/ld+json`, not executable, unchanged), so
no executable script; masthead 1.11.1; 0 matches for `beacon.min.js`.

## Rolling back

```bash
npx wrangler delete --name tonydefazio-com
```

Removes the Worker **and** both DNS records, returning the apex and www to the empty state
they were in before 2026-08-25. Nothing else on the zone is affected.
