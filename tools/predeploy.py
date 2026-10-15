#!/usr/bin/env python3
"""Runs before every `npm run deploy` (npm's `predeploy` hook). Two jobs.

1. Stamp the masthead. The Version comes from package.json and the Version date is
   today, written into site/index.html, so neither depends on someone remembering.
   1.10.3 shipped on 2026-10-15 with the previous day's date because the date was
   a hand edit.

2. Refuse a deploy that is not newer than what is live. The live masthead version
   is fetched, and package.json must be strictly greater. A branch cut from a main
   that lags the last deploy carries the same or an older version number, so this
   is the check that catches it. That happened on 2026-10-15: teaching-line had been
   deployed as 1.10.3 without being merged, a branch from main shipped as 1.10.3
   too, and it put the uncorrected CV and resume back on the site.

Bump the version with `npm version patch --no-git-tag-version` (or minor), then deploy.
"""
import datetime
import json
import pathlib
import re
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "site" / "index.html"
LIVE = "https://tonydefazio.com/"

VERSION_RE = re.compile(r'(<span class="lbl">Version</span> <span class="val">)([0-9.]+)(</span>)')
DATE_RE = re.compile(
    r'(<span class="lbl">Version date</span> <time class="val" datetime=")'
    r'([0-9-]+)(">)([0-9-]+)(</time>)')


def parse(v):
    return tuple(int(x) for x in v.split("."))


def main():
    version = json.loads((ROOT / "package.json").read_text())["version"]
    today = datetime.date.today().isoformat()

    url = f"{LIVE}?predeploy={int(time.time())}"
    # Cloudflare answers Python's default User-Agent with 403.
    req = urllib.request.Request(url, headers={"User-Agent": "tonydefazio.com predeploy"})
    with urllib.request.urlopen(req, timeout=20) as r:
        live_html = r.read().decode("utf-8")
    m = VERSION_RE.search(live_html)
    if not m:
        sys.exit(f"predeploy: no Version found in the live masthead at {LIVE}; not deploying.")
    live = m.group(2)
    if parse(version) <= parse(live):
        sys.exit(
            f"predeploy: package.json is {version} but {live} is live; not deploying.\n"
            f"  Either the version was not bumped, or this branch is behind the last deploy.\n"
            f"  Check that the live version's commit is in this branch, then\n"
            f"  `npm version patch --no-git-tag-version` and deploy again.")

    html = PAGE.read_text()
    html, nv = VERSION_RE.subn(lambda m: m.group(1) + version + m.group(3), html)
    html, nd = DATE_RE.subn(
        lambda m: m.group(1) + today + m.group(3) + today + m.group(5), html)
    if nv != 1 or nd != 1:
        sys.exit(f"predeploy: expected one Version and one Version date in {PAGE.name}, "
                 f"found {nv} and {nd}; not deploying.")
    PAGE.write_text(html)
    print(f"predeploy: masthead stamped {version}, {today}; live is {live}.")


if __name__ == "__main__":
    main()
