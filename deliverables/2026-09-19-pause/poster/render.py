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
only one place to change it. **That size, 48 x 36 in, is PROVISIONAL and was never
checked against an event specification - see the note at the top of poster.html.**
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
        # Wait for the fonts and every image, so nothing is rendered half-loaded.
        page.evaluate("document.fonts.ready")
        page.wait_for_function(
            "Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
        page.wait_for_timeout(600)

        # Report anything that did not fit, so a layout problem is caught here rather
        # than at the printer. Both numbers should be zero.
        over = page.evaluate("""() => {
            const p = document.querySelector('.poster');
            return {w: p.scrollWidth - p.clientWidth, h: p.scrollHeight - p.clientHeight};
        }""")
        if over["w"] or over["h"]:
            print("WARNING: content overflows the page by %d x %d css px "
                  "(%.2f x %.2f in) - fix poster.html before printing"
                  % (over["w"], over["h"], over["w"] / 96, over["h"] / 96))
        else:
            print("fit: content sits inside the page")

        page.pdf(path=PDF, width="%gin" % w_in, height="%gin" % h_in,
                 print_background=True, prefer_css_page_size=True,
                 margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        page.screenshot(path=PNG, full_page=False)
        browser.close()

    for p in (PDF, PNG):
        print("wrote %s  (%.1f MB)" % (p, os.path.getsize(p) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
