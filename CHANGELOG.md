# Changelog

What each version of the page says, so the number in the footer means something.
Dates are the day the change was written; see `DEPLOYED.md` for when a version
reached the edge.

The format is [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
version is [semantic](https://semver.org/) as applied to a page rather than an
API: **major** for a change that replaces what the page is, **minor** for new
sections or claims, **patch** for wording, styling and corrections.

## 1.1.0 — 2026-08-26

### Added

- **Every project is flagged as under development.** The four cards described
  the tools without saying anywhere that none of them is finished. The flag now
  appears in the meta and og descriptions, in the JSON-LD as
  `creativeWorkStatus`, in a notice under the masthead, as a chip on each of the
  four cards, as a row in *What these have in common*, and in the colophon.
- **A version stamp in the footer of both pages** — version, version date, and
  the date the site first went online. Carried in the JSON-LD as `version`,
  `datePublished` and `dateModified`, and in `sitemap.xml` as `lastmod`.
- **`npm run check`** (`tools/check-version.mjs`), which holds the stamp to one
  number and two dates across all four files, and now runs before both
  `npm run dry` and `npm run deploy`.
- This changelog.

## 1.0.0 — 2026-08-25

The born-on date: first commit and first deploy on the same day.

### Added

- The landing page — one screen routing a visitor to whichever of the four
  project sites is closest to their problem, with an accent hue per
  destination, a *What these have in common* section, and a colophon.
- A contact form posting to Web3Forms, with a `/thanks` landing page, replacing
  the bare address that had been on the page.
- `robots.txt` and `sitemap.xml`.
- Deployed as an assets-only Cloudflare Worker on the apex and on `www`, both
  as custom domains.

### Fixed

- Stopped claiming all four run in the browser — two of them don't.
- Dropped an inferred location from the page; added the publication links.
