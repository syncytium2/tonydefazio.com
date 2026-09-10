# Next session

Handoff written **2026-09-09**, replacing one written 2026-09-02 that had gone stale at 1.5.1
while the site moved to 1.7.0. Everything below was verified against the live site and the repo
on that date, not recalled. Re-verify before trusting any of it — this file is exactly the kind
of document §3 of the README warns about, and it has already been wrong once.

## 1. Status

| | |
|---|---|
| Live | https://tonydefazio.com — **1.7.0**, deployed 2026-09-09 |
| Cloudflare version ID | `c0187e47-8151-43dc-bd66-9afdade72516` — matches `DEPLOYED.md` |
| Served vs `site/` | all five files **byte-identical** (`index.html`, `robots.txt`, `sitemap.xml`, `thanks.html`, `cv.pdf`) |
| Version agreement | `package.json`, masthead strip, `DEPLOYED.md` all say 1.7.0 |

**Outstanding: `main` is ahead of `origin/main`.** The repo is **public** — ask before pushing.

## 2. What this is

One static page in `site/`, **no build step**, deployed to Cloudflare Workers. It routes to six
destinations (draughtsman, It Looked Right, Colonel Kernel, no_peak, bugarach, The Murderboard)
and, since 1.7.0, serves Tony's CV.

```bash
npm run serve    # localhost:5099  -- SEE THE WARNING IN §7, THIS PORT LIES
npm run dry      # wrangler dry-run
npm run deploy   # wrangler deploy
```

After any deploy, run the §2 edge checks in the README.

## 3. The CV is a redacted copy, and that is the whole point

`site/cv.pdf` is **not** the CV Tony sends people. `tools/make_public_cv.py` builds it from the
private one in `td-resume/cv/`, removing 15 named students — 7 graduate mentees, 6
undergraduates, 2 dissertation-committee members — and replacing each block with a count and its
institutions.

**If you regenerate or replace that file, run the script. Do not copy the private CV in.**
The script fails loudly rather than quietly publishing a name: it fails if any of the 15 names
survives into the rendered PDF, if a name matches zero or more than one row, or if the rows stop
being contiguous. A regenerated CV that reorders entries stops the build.

**Some of those people stay in the document on purpose.** Where a student is also a co-author
in the publication list, the citation stays: a co-authorship is a published fact they hold
credit for, and stripping it would falsify the citation. The script fails if a guarded citation
goes missing. **Do not write down here which co-authors were students** — that is the
relationship being redacted, and this repository is public. The names live in
`td-resume/cv/public_cv_redactions.json`, which is private; the script will not run without it.

**Do not reword the `Public copy: student names are withheld` header line.** `td-resume`'s
`claims.yml` greps the served PDF for it, so serving the un-redacted CV in its place fails their
checker instead of surprising a reader. Both ends enforce it.

**⚠ It will go stale silently.** The four corrections in the private CV live in Symplectic
Elements records, not in the document. The next Elements-generated CV has all four defects back.
README §3 has the record ids.

**Two numbers queried on 2026-09-10, both settled against the served PDF.** Check claims like
these against `site/cv.pdf` itself rather than against a handoff that paraphrases it.

- **Book chapters: 3, not 4.** "Books and Chapters" in the served PDF lists three entries —
  Dudek *et al.* 2002, Perez-Pinzon *et al.* 2009, Hughes *et al.* 2014. Four was a handoff
  error, and it is the duplicate described in README §3: Elements records `id=2560231`
  (deleted) and `id=396247` (kept) were the same chapter.
- **Physiol 578 lectures: not a contradiction.** The CV states both figures in one sentence —
  "Lectures range from 9-14 x 50 minute lectures per semester; academic year 2026-27 is 18 x
  50 minute lectures (15 fall, 3 spring)". 9–14 is the ordinary per-*semester* range; 18 is
  the 2026-27 *academic-year* total. Anything quoting "18 lectures per academic year" against
  "9–14 per semester" is comparing two different units.

## 3a. OPEN, AND AWAITING TONY: the U-M address is still on page one

**The published CV carries both addresses.** Verified in the bytes served from the edge on
2026-09-09, not in the local file:

```
                    Tony DeFazio
              Associate Research Scientist
                  defazio@umich.edu                      <- the original Elements header
Public copy: student names are withheld ... tony@tonydefazio.com   <- the line added beside it
```

The name redaction is sound and independently confirmed — all fifteen absent, with a positive
control that fires. **The address was not part of it.** The handoff from `tonydefazio-com-a0`
described the change as "a header line giving `tony@tonydefazio.com` for the real one", which
reads as a replacement; it is an addition.

**This may be exactly right.** `defazio@umich.edu` is already public through the U-M directory
and sixty-odd papers, so an argument that publishing it costs nothing is reasonable. But the
concern put to Tony before publication was specifically *"a deliberate publication of an address
to scrapers"*, and the file that shipped does that. **He has not been told the address stayed.**
Ask him; do not quietly remove it either, since it may be deliberate.

If it comes out, it is a `tools/make_public_cv.py` change plus a re-render, a version bump and a
deploy — not a hand-edit of the PDF.

## 4. Rules this page is built on. Do not quietly break them.

- **No network requests on load.** No fonts, no scripts, no cookies, no analytics. The page makes
  exactly one request, and only if the contact form is sent. A PDF fetched on click is a
  navigation, not a subresource, so the CV link does not touch this claim.
- **Nothing marks the coordinated events** in the bugarach figure. Vertical bands and recoloured
  ticks both existed and were both deliberately removed.
- **The kernel panel's spike trace is on an expanded time base.** The `aria-label` says so.
- **Figure data is simulated, on purpose.** Nothing on the public page comes from a real recording.
- **README §3 is a claim ledger.** Add a claim, add a row.
- **The page is light only.** The figures are plates on paper; a second ground meant every figure
  had to work twice and half of them did not.

## 5. The trap that has now bitten five times

**A claim goes stale and nothing says so. Grepping for the old number does not find the
sentences that name no number, and re-reading the page does not find a copy that is not the
page.**

1. The fifth destination left "Three instruments and one murderboard" over five cards for 3 days.
2. The sixth left several more wrong.
3. A claim narrowed to "destination **sites**" silently stopped excluding draughtsman the moment
   draughtsman became a site. **A category is a worse fence than a name.**
4. **1.7.0 found two that had been wrong for a while**: `wrangler.jsonc` said "three static files"
   when there were four, and README §2 claimed "fourteen distinct outbound URLs" when there were
   sixteen — draughtsman's card moved to its own site and the number moved underneath the prose.
   Both are now fixed by *removing* the count rather than correcting it: README §2 gives the
   command instead of a number, and `wrangler.jsonc` and README §1 name the files instead of
   counting them. Prefer that shape. A number nobody recomputes is what this page keeps getting
   caught by.
5. **The stale copy can be the reader's, not the repo's.** On 2026-09-10 a reviewer reported
   three live-site defects — the old byline, the draughtsman card pointing at GitHub, and
   draughtsman absent from the footer. All three were false against the live page, and all
   three were true of the build before `19c28a3`. Chat's fetch had returned a copy roughly five
   days old and gave no indication it was cached.

**So: verify site state with `curl` from Claude Code and diff against `site/index.html`.** Do
not assert what the live site says on the strength of a chat fetch. The page's own `Version` /
`Version date` stamp is a useful smoke test but not proof — it does not move per commit, so
`1.6.0 · 2026-09-04` covers both the broken build and its repair.

**The reader can also be wrong about *why*.** The first diagnosis of that report blamed a CSS
comment which quoted the retired byline and which does ship, there being no build step. It was
a plausible mechanism that happened to be false: the reviewer had rendered text, not source,
and no comment could produce the other two findings. **A mechanism that explains one symptom is
not thereby the cause of three.** The comment was removed anyway, on its own small merits; see
DEPLOYED.md.

## 6. Where the figures live

Source, generator and viewer are in the darkroom, **not in this repo**. Resolve the path with
`python3 ~/Developer/armory/tools/show.py --where` rather than typing it — it contains a personal
name and must never be spelled in a committed file.

The `ga-*.svg` files carry no stroke or fill; every colour comes from `ga.css` via `currentColor`.
Opening one directly shows a few words and nothing else. That is not a broken file.

**The gap:** the figures in `site/index.html` are hand-inlined. Run the drift check before every
deploy:

```bash
ROOT=$(python3 ~/Developer/armory/tools/show.py --where | sed 's#/[^/]*$##')
python3 ~/Developer/armory/tools/inline_asset_drift.py \
  --generated "$ROOT/tonydefazio/figures" --into site/index.html \
  --pattern '<svg[^>]*class="(?:ga|ds) (?P<id>(?:ga|ds)-[a-z0-9-]+)"[\s\S]*?</svg>'
```

Expect exactly three known rows: `ga-l` ORPHAN, `ga-b`/`ga-d` UNUSED. **A new row is a
regression; those three are not.** `tools/make_public_cv.py` exists partly because of this gap —
the CV's generator is in the repo so the same weakness is not repeated for it.

## 7. Small things worth knowing

- **⚠ A stale `python3 -m http.server` has been squatting on port 5099 since 2026-08-28** with no
  `--directory` flag, so it serves whatever directory it was started in. `npm run serve` cannot
  bind, dies silently, and `curl localhost:5099` hits the squatter. **This makes the README's
  "look at it before you upload" check return results from the wrong tree.** It caused a false
  404 on `/cv.pdf` during 1.7.0. `kill 75871` — or use any other port. Left running because it is
  not this session's process to kill.
- **`/index.html` 307s to `/`**, exactly as `/thanks.html` 307s to `/thanks`. Byte-comparing the
  served page needs `curl -sL`, or the check reports DIFFERS against a redirect body and looks
  briefly like the host-injection failure bugarach actually hit.
- `DEPLOYED.md` dates are **local time**. Do not "fix" the offset against Cloudflare's UTC log.
- `Preview.app` cannot open SVG. Use Quick Look or Safari. `qlmanage -t` crops anything far from
  square — never judge figure framing from its thumbnail.
- The Dropbox MCP server **cannot overwrite a file**; delete then create. Text only, no binary.
- Rolling back is `npx wrangler delete --name tonydefazio-com`, which removes the Worker **and
  both DNS records**. See `DEPLOYED.md`.

## 8. Candidate work

1. **Push to GitHub** (§1). The repo is public; ask first.
2. **Inbound links** — README §4 calls this the single biggest reason `kernel` was never indexed.
   The apex needs a link from somewhere real and `sitemap.xml` submitted to Google and Bing. Now
   that a CV is served, a link from a U-M page is worth more than it was. **Highest-value item on
   this list, and not a code change.**
3. **`sitemap.xml` does not list `/cv.pdf`.** Deliberate — the ask was a link people can find, and
   the crawler question was answered separately. Adding it is one line if Tony wants it indexed
   harder.
4. **Destinations do not link back.** A parent link in each site's footer closes the loop.
5. **Verify or drop `19 worked failures`** — the one unverified number on the page.
6. **A staleness check.** Nothing detects a claim going stale, and §5 shows that is this page's
   actual failure mode. The CV's Elements divergence (§3) has no detector either.
7. **Page weight.** `site/cv.pdf` is 524 KB, ~17x the rest of the site combined. It is a
   navigation, not a page load, so it costs nothing until clicked.
8. **`is-new` is a dead class** on the It Looked Right card. Either style it or drop it.
