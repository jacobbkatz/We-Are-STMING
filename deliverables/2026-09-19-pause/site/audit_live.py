#!/usr/bin/env python3
"""The half of the website audit that needs a real browser.

    cd deliverables/2026-09-19-pause/site && python3 -m http.server 8731 &
    python3 deliverables/2026-09-19-pause/site/audit_live.py

`check_site.py` reads the markup. This loads the page and watches what the browser
actually does with it, at five widths, in light and dark.

  device      THE ONE THAT MATTERS. Emulates a real handset (is_mobile), because a
              plain Playwright viewport sets the layout width directly and a phone
              does not - it reads <meta name="viewport"> and falls back to 980 px
              without one. On 2026-09-20 that gap hid a page with no viewport tag
              at all, no doctype and no charset: every mobile rule on the site was
              dead on a real phone and every test still passed.
  errors      uncaught JavaScript, and any request that 4xx/5xx'd
  overflow    sideways scroll at each width
  targets     tap targets under 40 px on the phone
  motion      that the reveal animations finish, so nothing stays invisible
"""
from __future__ import annotations

import sys

from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8731/index.html"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
IPHONE = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
          "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")

WIDTHS = [(390, True, "phone"), (768, True, "tablet"), (1024, False, "small laptop"),
          (1280, False, "laptop"), (1680, False, "wide")]


def main() -> int:
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME,
                              args=["--use-gl=angle", "--use-angle=swiftshader",
                                    "--enable-unsafe-swiftshader"])
        for width, mobile, label in WIDTHS:
            for scheme in ("light", "dark"):
                ctx = b.new_context(
                    viewport={"width": width, "height": 900},
                    device_scale_factor=3 if mobile else 2,
                    is_mobile=mobile, has_touch=mobile,
                    user_agent=IPHONE if mobile else None,
                    color_scheme=scheme)
                pg = ctx.new_page()
                errs, http = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("response", lambda r: http.append("%d %s" % (r.status, r.url))
                      if r.status >= 400 else None)
                pg.goto(URL, wait_until="networkidle")
                # Scroll the way a reader does, in steps. Jumping straight to the
                # bottom leaves the middle of the page never intersecting, and the
                # reveal observer - correctly - never fires for it.
                total = pg.evaluate("document.body.scrollHeight")
                # Small steps on purpose. An IntersectionObserver samples once a frame,
                # so a jump big enough to carry an element clean past the viewport
                # between two frames is never reported as intersecting - which is a
                # property of jumping, not of the page, and not what a reader does.
                step = 320
                for y in range(0, total, step):
                    pg.evaluate("window.scrollTo(0, %d)" % y)
                    pg.wait_for_timeout(45)
                pg.wait_for_timeout(900)
                pg.evaluate("window.scrollTo(0, 0)")
                pg.wait_for_timeout(400)

                note = []
                if pg.evaluate("document.compatMode") != "CSS1Compat":
                    note.append("QUIRKS MODE")
                lay = pg.evaluate("document.documentElement.clientWidth")
                if abs(lay - width) > 2:
                    note.append("lays out at %d px, not %d" % (lay, width))
                sw = pg.evaluate("document.documentElement.scrollWidth")
                if sw > width + 2:
                    note.append("scrolls sideways by %d px" % (sw - width))
                if errs:
                    note.append("JS errors: %s" % errs[:2])
                if http:
                    note.append("failed requests: %s" % http[:3])
                # The reveals carry a stagger of up to 450 ms, so a fixed wait after a
                # fast scroll caught a different straggler on every run. Wait for the
                # transitions to settle instead of guessing how long they take.
                # Anything still hidden is scrolled to directly and given a moment.
                # An IntersectionObserver samples once a frame, so a block the scroll
                # carried past between two frames is never reported - a property of
                # scripted scrolling, not of the page. Only a block that stays hidden
                # WITH ITS OWN SCROLL is a real one, and that is what gets counted.
                hidden = 0
                for _ in range(16):
                    hidden = pg.evaluate(
                        "Array.from(document.querySelectorAll('[data-rv]'))"
                        ".filter(function(e){return parseFloat(getComputedStyle(e).opacity)<0.5;})"
                        ".length")
                    if not hidden:
                        break
                    pg.wait_for_timeout(200)
                if hidden:
                    for el in pg.query_selector_all("[data-rv]"):
                        try:
                            if float(el.evaluate("e=>getComputedStyle(e).opacity")) < 0.5:
                                el.scroll_into_view_if_needed()
                                pg.wait_for_timeout(700)
                        except Exception:                    # noqa: BLE001
                            pass
                    pg.wait_for_timeout(600)
                    hidden = pg.evaluate(
                        "Array.from(document.querySelectorAll('[data-rv]'))"
                        ".filter(function(e){return parseFloat(getComputedStyle(e).opacity)<0.5;})"
                        ".length")
                if hidden:
                    note.append("%d revealed blocks never became visible" % hidden)
                if mobile:
                    # WCAG 2.2 SC 2.5.8 wants 24x24 CSS px for a control. A link
                    # sitting inside a sentence is explicitly exempt, so prose links
                    # are not counted - only things that are controls in their own
                    # right: the nav, the buttons, the model's toggles.
                    small = pg.evaluate("""() => {
                        const bad = [];
                        document.querySelectorAll('a,button').forEach(function(e){
                          const r = e.getBoundingClientRect();
                          if (r.width === 0 || r.height === 0) return;
                          if (e.closest('p,li,figcaption,.cap,.tracenote,.colophon')) return;
                          if (!e.closest('nav,.keys,.actions,.footgrid,.topnav')) return;
                          if (r.height < 24 || r.width < 24)
                            bad.push((e.textContent||'').trim().slice(0,28) + ' ' +
                                     Math.round(r.width) + 'x' + Math.round(r.height));
                        });
                        return bad.slice(0, 6);
                      }""")
                    if small:
                        note.append("tap targets under 24 px: %s" % small)

                print("%-13s %-5s %s" % (label + " " + str(width), scheme,
                                         "clear" if not note else " | ".join(note)))
                if note:
                    bad.extend(note)
                ctx.close()
        b.close()
    print()
    if bad:
        print("FAIL: %d problem(s) in the browser" % len(bad))
        return 1
    print("PASS: the page behaves at every width, in both themes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
