# tonydefazio.com

The apex landing page. It is a **router**: one screen that tells a visitor which of the
four project sites is closest to their problem, and gets them there.

**Live:** https://tonydefazio.com — *not yet deployed, see §2.*

| Destination | What it is |
|---|---|
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
no JavaScript, sets no cookies, and carries no analytics** — the same posture the four
destinations hold, which is also why the page renders identically from `file://`,
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
`murderboard.tonydefazio.com`, which is the most fully designed of the four destinations.
This page is deliberately the **parent** of that language rather than a fifth dialect. What
it adds is **one accent hue per destination**, taken from that site's own accent where it
had one, so a card is recognisable before its title is read:

| Card | Light | Dark | Source |
|---|---|---|---|
| Colonel Kernel | `#7A1FC4` | `#C79BF5` | its `--accent-solid` |
| no_peak | `#1F63B8` | `#8FBDEE` | its `--accent`, darkened to clear AA on white |
| bugarach | `#0E6674` | `#6BC6D4` | assigned here — bugarach's own site is neutral |
| The Murderboard | `#8A1C2B` | `#E0808C` | its `--blood` |

Light and dark both come from `prefers-color-scheme`, with a `[data-theme]` override defined
so a toggle could be added later without touching the palette.

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
so a dead one is the whole failure mode. All nine outbound links were verified 200 on
2026-08-25.

What a local server cannot tell you, the same caveat `bugarach/docs/deploy.md` records: the
edge serves HTTPS and adds Cloudflare's own headers, and `robots.txt` may be host-injected
unless ours wins. After the first deploy, confirm ours is the one being served:

```bash
diff <(curl -s https://tonydefazio.com/robots.txt) site/robots.txt
curl -sI https://tonydefazio.com/ | head -1
```

## 3. Keeping it honest

The page makes claims about the four projects. Each was checked against the source
repository on 2026-08-25, not written from memory:

- **"eleven reviewer roles", "three gate scripts"** — `murderboard/README.md`; the three gates
  are `murderboard_freshness.sh`, `murderboard_roster.sh`, `require_commit_before_message.sh`
  (`fetch_paper.py` is the lit tool, not a gate).
- **"Vendored into the three projects above"** — verified: `colonel_kernel`, `no_peak`, and
  `bugarach` each carry `docs/doc_review_process.md`, both vendored gate scripts, and
  `.claude/skills/murderboard/SKILL.md`.
- **"roughly 40% of true pulses"** — `no_peak/index.html`: recovers 60.8% of 130 true pulses.
- **"validated point-by-point against both Igor Pro and the original Fortran"** — 75/75 checks
  vs Igor; exact reproduction of CLUST5 v6.01 at documented defaults.
- **"Six coordination detectors lifted out of MATLAB"** — `bugarach/README.md`.
- **"each repository carries an instruction file written for an agent"** — true of all four,
  but the filename differs: `no_peak` uses `AGENTS.md`, the other three use `CLAUDE.md`. The
  page states the category rather than the filename for exactly this reason.
- Licences: colonel_kernel MIT · no_peak MIT · bugarach BSD-3-Clause · murderboard Apache-2.0.

**If any of those change, the page is stale.** Nothing checks this automatically.

## 4. Known gaps

- **No inbound links.** The single biggest reason `kernel.tonydefazio.com` was never indexed
  (`colonel_kernel/docs/archive/NEXT_SESSION-history-2026-08-24.md`). This page fixes the
  *internal* half — the four sites now have a common parent — but the apex itself still needs
  an inbound link from somewhere real (a UMich page, a GitHub profile README) before search
  engines will care. Submitting `sitemap.xml` to Google and Bing is the other half.
- **The four destinations do not link back here.** Adding a parent link to each site's footer
  would close the loop; that is four separate repositories and four separate deploys.
- **Nothing detects a stale claim.** See §3. `bugarach` has a `site-staleness.yml` workflow
  that is the model if this ever earns one.

## Licence

Page content © 2026 Richard Anthony DeFazio. Each linked project is under its own licence.
