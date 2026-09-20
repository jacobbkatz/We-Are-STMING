#!/usr/bin/env python3
"""Turn poster.html into poster.pdf (the print file) and poster_preview.png.

    python3 deliverables/2026-09-19-pause/poster/render.py

WHAT IT DOES, in plain language. It opens poster.html in a headless copy of the Chrome
browser - the same engine your laptop uses - and asks it to print the page to PDF at
exactly the page size set in poster.html, then to take one screenshot of the whole
thing so you can look at it without opening a PDF reader.

  poster.pdf          -> send this to the printer. 48 x 36 inches, landscape.
  poster_preview.png  -> open this to check the layout. Same thing, as a picture.

IF IT FAILS. The usual cause is that the browser is not where this script expects it:
it looks at /opt/pw-browsers/chromium. On a different machine, install the Python
package `playwright` and then run `python3 -m playwright install chromium`, and this
script will find the browser on its own.

PAGE SIZE. The size is read out of poster.html itself (the `@page` rule), so there is
only one place to change it. **48 x 36 in landscape, confirmed by Jacob on 2026-09-20.**
It was carried as provisional until then because no event specification exists anywhere
in the project files and none was invented.
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "poster.html")
PDF = os.path.join(HERE, "poster.pdf")
PNG = os.path.join(HERE, "poster_preview.png")

# Where the browser lives in this environment. A plain `chromium` on the PATH, or a
# playwright-installed one, is used instead if this is missing.
CHROMIUM = "/opt/pw-browsers/chromium"


def page_size_from_html(path):
    """Read `@page { size: <w>in <h>in; }` out of the stylesheet. One source of truth."""
    css = open(path, encoding="utf-8").read()
    m = re.search(r"@page\s*\{[^}]*size:\s*([0-9.]+)in\s+([0-9.]+)in", css)
    if not m:
        raise SystemExit("Could not find the @page size rule in %s" % path)
    return float(m.group(1)), float(m.group(2))


def main():
    from playwright.sync_api import sync_playwright

    w_in, h_in = page_size_from_html(HTML)
    # CSS inches are exactly 96 CSS pixels, so this is the pixel size of the page.
    w_px, h_px = int(round(w_in * 96)), int(round(h_in * 96))
    print("page: %g x %g in  (%d x %d css px)" % (w_in, h_in, w_px, h_px))

    launch = {}
    if os.path.exists(CHROMIUM):
        launch["executable_path"] = CHROMIUM

    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": w_px, "height": h_px},
                                device_scale_factor=1)
        page.goto("file://" + HTML)
        page.wait_for_load_state("networkidle")

        # Wait until the typeface AND every picture are really in place. Without
        # this the page is sometimes measured and printed half-loaded, which comes
        # out as missing pictures and text in the wrong font - it has happened.
        page.wait_for_function("document.fonts.status === 'loaded'", timeout=60000)
        page.wait_for_function(
            "Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)",
            timeout=60000)
        page.evaluate("""() => Promise.all(
            Array.from(document.images).map(i => i.decode().catch(() => null)))""")
        # Every picture must also have been given a size on the page, and the
        # layout has to stop changing between two looks 400 ms apart.
        last = None
        for _ in range(12):
            page.wait_for_timeout(400)
            now = page.evaluate("""() => Array.from(document.images)
                .map(i => Math.round(i.getBoundingClientRect().height)).join(',')""")
            if now == last and "0" not in now.split(","):
                break
            last = now
        else:
            print("WARNING: the page never settled - check the preview carefully")

        # Report anything that did not fit, so a layout problem is caught here rather
        # than at the printer. A panel hides whatever will not fit inside it, which is
        # what stops one panel printing on top of the next - but it means a sentence
        # can be cut off in silence. This check finds that: every number should be 0.
        over = page.evaluate("""() => {
            const p = document.body;
            const out = {page: [p.scrollWidth - p.clientWidth, p.scrollHeight - p.clientHeight],
                         panels: []};
            document.querySelectorAll('.panel, .hero, .numbers, .ctx, .call, .foot')
              .forEach(el => {
                const over = el.scrollHeight - el.clientHeight;
                if (over > 1) {
                  const h = el.querySelector('h2, h3, h1');
                  out.panels.push([(h ? h.textContent : el.className).trim().slice(0, 46),
                                   over]);
                }
              });
            return out;
        }""")
        if over["page"][0] > 1 or over["page"][1] > 1:
            print("WARNING: the whole page overflows by %d x %d css px (%.2f x %.2f in)"
                  % (over["page"][0], over["page"][1],
                     over["page"][0] / 96, over["page"][1] / 96))
        for name, px in over["panels"]:
            print("WARNING: text is being cut off in \"%s\" - it is %.2f in too tall"
                  % (name, px / 96))
        if not over["panels"] and over["page"][1] <= 1:
            print("fit: every panel's text fits inside it")

        page.pdf(path=PDF, width="%gin" % w_in, height="%gin" % h_in,
                 print_background=True, prefer_css_page_size=True,
                 margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        page.screenshot(path=PNG, full_page=False)
        browser.close()

    for p in (PDF, PNG):
        print("wrote %s  (%.1f MB)" % (p, os.path.getsize(p) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
