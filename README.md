# tonydefazio.com

The apex landing page. It is a **router**: one screen that tells a visitor which of the
six destination sites is closest to their problem, and gets them there. `draughtsman`
became the sixth site on 2026-09-04, when its GitHub Pages certificate finally issued;
before that its card pointed at the repository.

**Live:** https://tonydefazio.com — *not yet deployed, see §2.*

| Destination | What it is |
|---|---|
| [lookedright.tonydefazio.com](https://lookedright.tonydefazio.com) | It Looked Right — four challenges in working with coding agents, for researchers. Ships out of [`short-course`](https://github.com/syncytium2/short-course). **Added 2026-08-28, carries the NEW sticker** |
| [kernel.tonydefazio.com](https://kernel.tonydefazio.com) | Colonel Kernel — calcium-imaging convolution / deconvolution |
| [nopeak.tonydefazio.com](https://nopeak.tonydefazio.com) | no_peak — CLUSTER hormone pulse detection |
| [bugarach.tonydefazio.com](https://bugarach.tonydefazio.com) | bugarach — coordinated-event detection + raster viewer |
| [murderboard.tonydefazio.com](https://murderboard.tonydefazio.com) | The Murderboard — adversarial document review harness |

## 1. What is here

Four static files in [`site/`](site/), committed as-is. **There is no build step**, so
`wrangler deploy` uploads exactly what is in the repository and no generated artifact can
drift from source.

```
site/index.html     the page — self-contained, ~24 KB
site/thanks.html    where the contact form lands after a send (noindex)
site/robots.txt     allow-all + sitemap pointer
site/sitemap.xml    one URL
```

`index.html` inlines its own CSS and its favicon (a data-URI SVG). It loads **no fonts, runs
no JavaScript, sets no cookies, and carries no analytics** — **five of the six destination
sites hold the same posture**, and `draughtsman`'s is the exception: it requests a webfont
stylesheet from `fonts.googleapis.com` (§3). That is also why this page renders identically
from `file://`,
air-gapped, or behind a captive portal.

**One exception, and the page says so rather than burying it:** the contact form posts to
Web3Forms. That request happens *only* when a visitor presses Send — nothing is contacted on
load — which is why the colophon reads "exactly one network request, and only if you send
the form" rather than the flat "no network requests" it used to claim.

### The contact form

A **plain HTML `POST`**, no JavaScript. `no_peak` solves the same problem with a `fetch` and
React state; this page has no bundle to put that in, and a native form submit keeps the
scriptless posture intact while degrading perfectly.

- **Relay:** Web3Forms. The access key is `b8c22a4e-…`, **shared with `no_peak`** — it is
  public by design (client-side keys only name a destination inbox and can read nothing
  back). Submissions are tagged `subject: "tonydefazio.com contact form"` so the two sites
  are distinguishable in the inbox.
- **Destination:** the address registered with that key. **The address appears nowhere on
  the page or in the source**, which is the point — a scraper has nothing to take. Delivery
  lands at `tony@tonydefazio.com`, a Cloudflare Email Routing address on this zone (the
  zone's MX records point at `route{1,2,3}.mx.cloudflare.net` with SPF configured).
- **After a send:** Web3Forms redirects to `https://tonydefazio.com/thanks`.
- **Spam:** a `botcheck` honeypot field, hidden off-canvas — the same trick `no_peak` uses.

#### Testing it — what does and does not work

**Verified end to end on 2026-08-25**: a real submission from a real browser against the
live page reached `/thanks`, which Web3Forms redirects to only on success.

Getting there ruled out two dead ends worth writing down, because both look like a broken
form and neither is:

| How you test | What happens | Why |
|---|---|---|
| `curl` to the API | **403** — *"Use our API in client side"* | Web3Forms blocks server-side POSTs on the free plan. Adding an `Origin` header does not help. |
| `curl` with browser headers | Cloudflare **"Just a moment…"** interstitial | The API sits behind Cloudflare bot protection. curl cannot pass it, ever. |
| Headless browser, default | Stuck on Turnstile *"Verifying…"* | Cloudflare detects `navigator.webdriver`. |
| Headless browser, flag masked | **Reaches `/thanks`** | Turnstile clears immediately. This is the test that works. |

The working recipe, using `bugarach`'s Python Playwright:

```python
b = pw.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
ctx = b.new_context(user_agent="Mozilla/5.0 (Macintosh; …) Chrome/140.0.0.0 Safari/537.36")
ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
```

**Delivery confirmed 2026-08-25.** Reaching `/thanks` proves only that Web3Forms accepted
and relayed the submission; the key→inbox mapping lives on their side and nothing here can
read it. So the last step was done by eye: the test message arrived, which confirms the
shared key really does deliver to Tony. The chain is verified end to end — page → Web3Forms
→ inbox.

Only one message arrived, not two. The first (unmasked headless) attempt died at the
Turnstile challenge without submitting, so it never reached the relay.

**Ordinary visitors are unaffected.** A normal browser passes Turnstile without seeing it;
the interstitial above is an artifact of automation, not something a person hits.

> **Rotating the key breaks two sites.** If the Web3Forms key is ever regenerated, both this
> page and `no_peak/src/Contact.tsx` need the new one. Nothing enforces that.

> **`/thanks` only resolves on Cloudflare.** `wrangler.jsonc` sets no `html_handling`, so the
> assets Worker uses the default `auto-trailing-slash` and serves `thanks.html` at `/thanks`.
> A local `python -m http.server` **404s** on `/thanks` and serves only `/thanks.html`. That
> is a local-preview artifact, not a bug — but it means the redirect cannot be fully tested
> from `npm run serve`.

### Design

The palette, the Charter body face, and the mono kickers are inherited from
`murderboard.tonydefazio.com`, which is the most fully designed of the destinations.
This page is deliberately the **parent** of that language rather than another dialect. What
it adds is **one accent hue per destination**, taken from that site's own accent where it
had one, so a card is recognisable before its title is read:

| Card | Hue | Source |
|---|---|---|
| draughtsman | `#1F6B45` | assigned here — the one hue the other five leave free |
| It Looked Right | `#8A5D0F` | the site's own caution ochre |
| Colonel Kernel | `#7A1FC4` | its `--accent-solid` |
| no_peak | `#1F63B8` | its `--accent`, darkened to clear AA on white |
| bugarach | `#0E6674` | assigned here — bugarach's own site is neutral |
| The Murderboard | `#8A1C2B` | its `--blood` |

**The page is light only, and that is a decision rather than an omission.** It carried a
`prefers-color-scheme: dark` palette and a `[data-theme]` override until 2026-09-04; both are
gone and `:root` declares `color-scheme: light`, which is what stops a browser rendering form
fields and scrollbars dark around a light page.

*Why:* the figures are drawn as **plates on paper** — pale fills, hairline rules, traces that
assume ink on white. On a dark ground `no_peak`'s pulse bands became heavy navy slabs instead
of faint highlights, and both draughtsman model marks went muddy against the card. A second
ground meant every figure had to work twice, and half of them did not. One ground, and every
figure drawn for it.

The dark values are recoverable from git (`git log -S'--c-kernel: #C79BF5'`) if this is ever
revisited — but reviving them means re-drawing the figures, not restoring a palette.

## 2. Deploying

An **assets-only Cloudflare Worker**, the same shape `colonel_kernel` and `bugarach` use.

```bash
npm install         # once per clone — installs the pinned wrangler
npx wrangler login  # once per machine — OAuth browser flow, cannot be scripted
npm run dry         # everything except the upload
npm run deploy      # upload
```

`wrangler.jsonc` declares the apex as a `custom_domain` route, so **`wrangler deploy` creates
the DNS record and the Worker binding itself.** There is nothing to click in the Cloudflare
dashboard and nothing to do at Porkbun, which is only the registrar — `tonydefazio.com`'s
nameservers already delegate to Cloudflare.

> **Read before the first deploy.** As of 2026-08-25 the apex resolves to **nothing** —
> `dig +short tonydefazio.com` is empty, while all four subdomains answer. So the first
> deploy *creates* the apex record rather than replacing one, and there is nothing to lose.
> If that ever stops being true, look before you deploy: a `custom_domain` route takes the
> hostname over.

### Look at it before you upload

```bash
npm run serve       # http://127.0.0.1:5099
```

Then click **every card and every footer link** — the page is made almost entirely of links,
so a dead one is the whole failure mode. Thirteen were verified 200 on 2026-08-31 (five
destinations, five repositories, the GitHub profile, ORCID, the bibliography). **The draughtsman
card took that to fourteen distinct outbound URLs**, and the fourteenth is the one that is not
200 yet — see the DEPLOY GATE in §4. Count them rather than trusting this sentence:

```bash
python3 -c "import re,io;h=re.findall(r'href=\"(https?://[^\"]+)\"',io.open('site/index.html').read());print(len(set(h)))"
```

**Before deploying, check the inlined figures against their generator.** They are hand-pasted
from the darkroom and nothing else links the two — the page's one structural weakness, and it
has already been paid for once: `ga-lookedright` was drawn straight into the page on 2026-08-28,
never added to `make_figures.py`, and went unnoticed for five days.

```bash
# resolve the darkroom rather than spelling it -- the path carries a personal name
ROOT=$(python3 ~/Developer/armory/tools/show.py --where | sed 's#/[^/]*$##')
python3 ~/Developer/armory/tools/inline_asset_drift.py \
  --generated "$ROOT/tonydefazio/figures" \
  --into site/index.html \
  --pattern '<svg[^>]*class="(?:ga|ds) (?P<id>(?:ga|ds)-[a-z0-9-]+)"[\s\S]*?</svg>'
```

Two families now: `ga-` are this page's own abstracts from `make_figures.py`; `ds-` are model
marks drawn by **draughtsman's** `render --icon`, regenerated by the recipe in
`HOW-THE-MODEL-MARKS-ARE-MADE.md` beside them. Today the check reports `ga-l` ORPHAN (the
five-day-old gap above) and `ga-b` / `ga-d` UNUSED — the two abstracts the model marks replaced,
still generated on purpose so either card can be reverted in one line. **Neither is a
regression; a NEW row is.**

Exit 0 clean, 1 on DRIFTED or ORPHAN, **2 on a precondition failure** — a distinction worth
respecting: 2 means it could not look, and must never be spent as though it had looked. Today it
exits 1 on `ga-l`, which is the known orphan above and not a regression. Scope the pattern to
`ga-`; a wider selector also matches `new-star`, which is page furniture and never generated.

⚠ **If that exits 2 with `No such file`, the armory checkout is behind, not the tool missing.**
The tool is on `origin/main` (`570e2af`, warning fixed at `7d71642`); `~/Developer/armory` is a
**shared working tree** — several sessions use it at once and it routinely sits behind the
remote, so a path into it is not evidence about what exists. That happened while this very
paragraph was being written: the command above exited 2 on this machine with the tool sitting on
`origin/main` the whole time.

```bash
git -C ~/Developer/armory fetch --quiet
git -C ~/Developer/armory cat-file -e origin/main:tools/inline_asset_drift.py && echo present
git -C ~/Developer/armory rev-list --count HEAD..origin/main   # how far behind the tree is
```

`git -C ~/Developer/armory pull --ff-only` fast-forwards it — but **check with the other sessions
first**; that tree is shared and has carried uncommitted work in flight. `git branch --contains`
is the wrong instrument here: it lists local branches only and will tell you a commit is nowhere
when it is on `origin/main`. Use `git branch -r --contains` after a fetch.

What a local server cannot tell you, the same caveat `bugarach/docs/deploy.md` records: the
edge serves HTTPS and adds Cloudflare's own headers, and `robots.txt` may be host-injected
unless ours wins. After the first deploy, confirm ours is the one being served:

```bash
diff <(curl -s https://tonydefazio.com/robots.txt) site/robots.txt
curl -sI https://tonydefazio.com/ | head -1
```

## 3. Keeping it honest

The page makes claims about the six projects. Each was checked against the source
repository on 2026-08-25 — the fifth on 2026-08-31, the sixth on 2026-09-02/03 — not written
from memory.

⚠ **NARROWED TWICE ON 2026-09-04, and the second time undid the first.** §1 said the
no-fonts/no-external-requests posture was "the same posture the five destinations hold". It was
first narrowed to *destination **sites***, which excluded draughtsman because it was then a
repository card. **Hours later draughtsman became a site**, its certificate issued, and the
narrowing silently stopped excluding anything. §1 now states the exception by name rather than
by category: five of six hold the posture, and `draughtsman.tonydefazio.com` requests a webfont
stylesheet from `fonts.googleapis.com` — measured 2026-09-04, after the switch.
  - **A category is a worse fence than a name.** "Destination sites" was true when written and
    false a few hours later without a word of it changing, because the *world* moved across the
    category rather than the sentence moving. `NEXT_SESSION.md` §4 warns about sentences that
    name no number; this is the same failure one level up — a sentence that names no *instance*.
  - draughtsman is the only destination that phones out on load. Whether its page should drop
    the webfont is that repo's call; a `@font-face` with the file committed would get the same
    typography with no request. Nothing on this page claims otherwise, so nothing shipped is
    wrong.

**In 1.2.0 each card was cut to a single sentence**, which retired most of those claims from
the page. What the cards still assert:

- **The `11 roles` and `3 gate scripts` chips** — `murderboard/README.md`; the three gates are
  `murderboard_freshness.sh`, `murderboard_roster.sh`, `require_commit_before_message.sh`
  (`fetch_paper.py` is the lit tool, not a gate).
- **"Draft, attack, repair, re-attack, deliver"** — the site's own section heading for the
  process, quoted verbatim. Six steps, one of which loops.
- **"a reviewer shown neither the findings nor the fixes"** — the site describes Verify as
  "blind, then follow-up": "a reviewer who has not seen the findings reads it again, because
  fixes break things."
- **"stops after three rounds whether it converged or not" / the `≤3 rounds` chip** — the site
  states "≤3 re-review rounds, then it stops, converged or not"; the return edge from Verify
  to Review is labelled as capped at three.
- **"one fixed report"** — "Eleven reviewer roles, three scripts, one fixed report format."
- **"tied to no field"** — "Free, tied to no field, the same whether the reviewers are humans
  or AI." Note this is a claim about *scope*, not a denial of the vendoring: murderboard **is**
  vendored into the three research-tool repositories. The page no longer says so, and should
  not be read as saying the opposite.
- **"by being run against itself and by what people send back"** — the site records the full
  panel running against its own page on 2026-08-25, catching among other things a false
  self-contained claim and a fabricated quotation, with "most of the current wording"
  post-dating that pass; and its Feedback section solicits unsupported-claim reports.
- **The It Looked Right card and its `4 challenges` / `3 reading depths` chips** — checked
  against the live site on 2026-08-31: "Coding is no longer the barrier. Four challenges
  remain", enumerated as Communication / Idiosyncrasies / Validation / The forever asymptotes;
  the depth control offers *Headlines*, *+ incidents*, *+ sources*. **The `19 worked failures`
  chip is the one unverified number on this page.** The live page carries 26 `<details>`
  blocks, not all of which are incidents, and the count is not stated anywhere in the source —
  so 19 is neither confirmed nor refuted here. It also tracks a page that moves: lookedright
  was at version 0.1.57 on 2026-08-31, three days after first publication. Recount it or drop
  the chip.
- **The draughtsman card, and its `10 worked models` / `zero runtime deps` / `coverage-checked`
  chips** — checked against the repository on 2026-09-02, not from memory. The card sentence is
  `draughtsman/README.md`'s own opening, quoted verbatim: "Readable architecture diagrams for
  PyTorch models. The tracer supplies the facts, an agent supplies the abstraction, and a
  coverage check proves nothing was silently dropped." That makes it the **second** deliberate
  quotation on this page, alongside the Murderboard's "Draft, attack, repair, re-attack,
  deliver" — the rule below says the card sentences are paraphrase; these two are the
  exceptions and are marked as such.
  - `10 worked models` — ten committed figures, each with the `graph.json` it was measured from:
    nine in `examples/gallery/` (mlp, lstm, lenet, dual, vae, transformer, whisper, unet, resnet)
    plus `examples/tube/` alongside it. Verified against `origin/main` on 2026-09-03, not against
    a local checkout.
  - **The card links to `draughtsman.tonydefazio.com`, not the repository**, since 2026-09-04.
    The subdomain served over HTTP for about ten hours with no certificate: GitHub had never
    *requested* one, because the domain was set by committing a `CNAME` file rather than through
    the Pages API, and `https_certificate` read `state: None` rather than `in_progress` or an
    error. Re-setting the custom domain through the API fired the request and it issued within
    seconds. The repository is still linked from the footer's source list.
    **This chip was `11` for about four hours and is the page's first worked example of the
    hazard it exists to document.** `cascade` was removed on 2026-09-03 (`3652d81`): CascadeTorch
    is GPL-3.0 against draughtsman's BSD-3 — latent while the repo is private, real on the day it
    is not — so it moved to `haruspex`, which is private and is itself a CASCADE reimplementation.
    Recount here whenever that directory changes; do not infer the number from any sentence.
    **Upstream now derives it rather than asserting it.** When this chip was written the repo's
    README said ten while the directory held eleven; that turned out to be six stale prose counts,
    all invalidated by one addition and unnoticed for a day. `draughtsman/tests/test_counts.py`
    now derives every one from the directory and the committed graphs. A seventh count —
    `len(REPRODUCIBLE) >= 10` in `test_reproduces.py` — was the only one that was *executed*, and
    it was the only one that failed loudly when `cascade` came out. Executed counts fail loudly;
    prose counts go stale in silence. That is the page's own §4 lesson arriving from a repository
    it links to, and it is the best single answer to why that repo is worth a reader's time.
  - `zero runtime deps` — `pip install -e .` installs nothing but draughtsman; the layout engine
    and SVG emitter are in-repo. Asserted upstream by an install into an empty virtualenv that
    renders byte-identically to the committed `figure.svg`.
  - `coverage-checked` — every traced node must be accounted for in exactly one stage; a node
    may be `elided` only explicitly, with a reason.
  - **The figure on this card IS draughtsman's own output**, as of 2026-09-04 — `render
    --icon 420x104` on `examples/gallery/lenet`, fitted at 0.86x. It replaced a hand-drawn
    schematic, and the condition for the swap was set in advance and then met: icon mode drops
    text rather than shipping type nobody can read, so the mark is a mark instead of an
    unreadable diagram. Before it existed, every figure scaled to this slot rendered detail type
    between 1.3pt and 3.5pt against a screen floor near 8pt, and shipping one would have been the
    exact failure `draughtsman/README.md` convicts pytorch-graph of.
    **LeNet rather than ResNet**, on draughtsman's own measurement: ResNet is sparse at any size
    (0.17x at their 192x96 slot) and reads as a thin line of blocks. The retired schematic is
    still generated as `ga-d` and shows as UNUSED in the drift check; that is deliberate, not a
    leak.
  - **The card does NOT quote an install command.** `pip install draughtsman-nn` would name a
    package that does not exist: the distribution was renamed off PyPI's `draughtsman` (Kyle
    Fuller's API Blueprint parser, last released 2020) but nothing has been uploaded. The import
    name, the CLI and the repository all keep the unabbreviated spelling.
- **The six `Born` stamps.** Each is the destination repository's **first commit**, read from
  `git log --reverse` on 2026-09-03: draughtsman `ddc332f` 2026-09-01 · short-course `5a6ffc4`
  2026-08-26 · colonel_kernel `511893f` 2026-06-21 · no_peak `1827d70` 2026-08-07 · bugarach
  `3622dee` 2026-08-10 · murderboard `4a92748` 2026-07-20. Emitted as `<time datetime=…>` so a
  consumer can read them without scraping prose — the contract bugarach already offers and
  short-course does not.
  **Born only: no version, no revised date.** Those move on every upstream commit and this page
  has no build step, so a copy of either would be a second source that rots silently. Born is
  immutable by construction, and both repos that publish it say so — `no_peak/src/version.ts:2`
  ("BORN is the date of the first commit and never changes") and `murderboard/CLAUDE.md:48-51`
  ("Born never changes … a born-on date that can be quietly edited is just another mutable
  field").
  **The estate runs two conventions and this page follows the first:** `Born` means repo birth
  (colonel_kernel, no_peak); `First published` means page birth (bugarach 2026-08-13,
  short-course per-page). Both are used correctly upstream. Do not read a `Born` here as a
  publication date, and do not reconcile it against a destination's `First published` — they are
  different facts under different labels.
  ⚠ **How this was got wrong once, so it is not got wrong again.** The convention was first
  recorded here as page-birth, on the evidence that colonel_kernel and no_peak published no stamp
  at all. **They both do; they are JavaScript applications, and a `curl` that does not execute JS
  sees only their `<noscript>` summary.** Rendering them shows `Born June 21, 2026` and
  `born August 7, 2026`. Any future check of what a destination publishes must render the page,
  not fetch it — three of the six are client-side apps.
- **The bugarach card's figure is also draughtsman's output** — `render --icon 420x104` on
  `examples/tube`, fitted at 0.33x. **bugarach's model *is* draughtsman's `tube`**: its
  `docs/learned/architecture.spec.json` is the vendored copy and says so in its own first line,
  so this is the model bugarach actually runs, not an illustration of one.
  ⚠ **This replaced the raster/rate abstract, and that is an editorial change, not a repair.**
  The retired figure showed 22 cells over a ramping background with four coordinated events left
  deliberately unmarked — it illustrated the card's sentence, which is about finding those
  moments. The model mark does not; it shows the detector instead of the problem. It is still
  generated as `ga-b` and shows as UNUSED in the drift check, so putting it back is a one-line
  revert. Consistent with bugarach's own front page, which now leads with the model.
- **The `six detectors` chip** — `bugarach/README.md`.
- **The `Fortran + Igor implementations` chip** — 75/75 checks vs Igor; exact reproduction of
  CLUST5 v6.01 at documented defaults. The chip now carries this on its own, since the
  sentence that spelled it out is gone.
- **"each research-tool repository carries an instruction file written for an agent"** — in
  §*What these have in common*, which was not trimmed. The filename differs: `no_peak` uses
  `AGENTS.md`, `colonel_kernel` / `bugarach` / `murderboard` use `CLAUDE.md`. The page states
  the category rather than the filename for exactly this reason.
  **Narrowed on 2026-08-31.** It used to read "each repository", which the fifth destination
  falsified: `short-course` carries `.claude/` (hooks + `settings.json`) and a `HANDOFF.md`,
  but **no `CLAUDE.md` or `AGENTS.md`**. A handoff note is not an instruction file, so the
  claim was narrowed rather than stretched to cover it. If `short-course` ever gains one,
  the word "research-tool" can come back out.

Retired from the page in 1.2.0, and no longer this repo's problem to keep fresh: the 40%
CLUSTER miss rate, "validated point-by-point against both Igor Pro and the original Fortran"
as prose, "Six coordination detectors lifted out of MATLAB" as prose, "scored against planted
events with known times", "Vendored into the three projects above", and **the per-project
licence chips** (MIT / MIT / BSD-3 / Apache-2.0). The page no longer names a licence for any
of the five; the footer defers to the repositories, which is the only place a licence can go
stale without this page being wrong. For the record they were, on 2026-08-31: colonel_kernel
MIT · no_peak MIT · bugarach BSD-3-Clause · murderboard Apache-2.0 · short-course Apache-2.0.

**If any of the surviving claims change, the page is stale.** Nothing checks this automatically.

The card sentences are **paraphrase, not quotation**, with one deliberate exception — checked
against the live sites on 2026-08-26, none appears verbatim on the site it describes except
the Murderboard's "Draft, attack, repair, re-attack, deliver", which is that site's own
section heading and is quoted on purpose. The short chips also match (`teaching demonstrator`,
`browser raster viewer`, `11 roles`). Otherwise treat the sentences as this page's words about
those projects, not as those projects' own words.

## 4. Known gaps

- **No inbound links.** The single biggest reason `kernel.tonydefazio.com` was never indexed
  (`colonel_kernel/docs/archive/NEXT_SESSION-history-2026-08-24.md`). This page fixes the
  *internal* half — the five sites now have a common parent — but the apex itself still needs
  an inbound link from somewhere real (a UMich page, a GitHub profile README) before search
  engines will care. Submitting `sitemap.xml` to Google and Bing is the other half.
- **The destinations do not link back here.** Adding a parent link to each site's footer
  would close the loop; that is five separate repositories and five separate deploys —
  `short-course`, `colonel_kernel`, `no_peak`, `bugarach`, `murderboard`. (It was already
  "five" when there were four destinations, which was wrong then and is right now by
  accident. Recount it if a sixth lands.)
- **DEPLOY GATE: `draughtsman` is a private repository.** The card links to
  `github.com/syncytium2/draughtsman` and the colophon says "All six repositories are public".
  Both were false until the repo was flipped. **CLEARED 2026-09-03** — measured, not assumed.
  This is the "went false rather than stale" class from `DEPLOYED.md` §1.5.0, caught before
  shipping rather than after.

  **Check it the way a visitor would, not the way an owner can.** `gh repo view … --json
  visibility` answers while authenticated as the owner, and an owner can see a private repo;
  the question that matters is whether an anonymous request reaches it. Those are different
  questions and only one of them is the reader's:

  ```bash
  curl -s -o /dev/null -w '%{http_code}\n' https://github.com/syncytium2/draughtsman   # want 200
  ```

  Credit to `murderboard-7a` for the general form: a probe that answers confidently about
  something it cannot actually see is the same defect whether it is an authenticated
  visibility check or a `curl` that does not run JavaScript (see §3, the `Born` stamps). Both
  return a clean answer to a question you did not ask.
- **Nothing detects a stale claim.** See §3. `bugarach` has a `site-staleness.yml` workflow
  that is the model if this ever earns one.

## Licence

Page content © 2026 Richard Anthony DeFazio. Each linked project is under its own licence.
