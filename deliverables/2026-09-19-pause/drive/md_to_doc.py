#!/usr/bin/env python3
"""Turn one of this project's Markdown documents into HTML that Google Docs imports
as a typeset document rather than a wall of 11-point Arial.

    python3 deliverables/2026-09-19-pause/drive/md_to_doc.py <in.md> <out.html> ["Title"]

WHY THIS EXISTS, in plain language. The documents on Drive were uploaded as plain
Markdown, so Google converted them using its defaults: Arial everywhere, black, one
size for the body and one for every heading. They carry the same words as the
website and look nothing like it. This script writes the same words out with the
website's typography attached to every element, so that when Drive converts the
file the type, the rules, the tables and the correction banners survive.

WHAT IT WILL AND WILL NOT DO. Google Docs' importer keeps inline styles on elements
and drops stylesheets, so everything here is inline. It has no concept of a styled
blockquote, so a quotation or a correction banner is written as a one-cell table
with a background and a coloured left edge - which is how a designed Google Doc
does a callout anyway. Nothing about the words changes: this is typesetting, not
editing.

FONTS. Newsreader for headings and Inter for text, both Google fonts, so Docs has
them. If a reader's Docs is missing one it falls back to Georgia or Arial and the
document still reads.
"""
from __future__ import annotations

import html
import re
import sys

# The website's tokens, in the units Google Docs understands.
INK, INK2, MUTED = "#16191B", "#474F54", "#6A7278"
LINE, HAIR = "#E2E4E3", "#EDEFEE"
GOLD, GOLDMARK, GOLDWASH = "#8A6D22", "#C9A24B", "#FBF6E7"
SERIF = "Newsreader, Georgia, serif"
SANS = "Inter, Arial, sans-serif"
MONO = "Roboto Mono, Consolas, monospace"

BODY = ("font-family:%s;font-size:10.5pt;line-height:1.5;color:%s;"
        "margin:0 0 9pt 0;" % (SANS, INK))
H = {
    1: "font-family:%s;font-size:23pt;line-height:1.15;color:%s;font-weight:400;"
       "margin:0 0 4pt 0;" % (SERIF, INK),
    2: "font-family:%s;font-size:17pt;line-height:1.2;color:%s;font-weight:400;"
       "margin:22pt 0 5pt 0;" % (SERIF, INK),
    3: "font-family:%s;font-size:13.5pt;line-height:1.25;color:%s;font-weight:400;"
       "margin:16pt 0 4pt 0;" % (SERIF, INK),
    4: "font-family:%s;font-size:11pt;line-height:1.3;color:%s;font-weight:600;"
       "margin:13pt 0 3pt 0;" % (SANS, INK),
    5: "font-family:%s;font-size:10pt;color:%s;font-weight:600;margin:11pt 0 3pt 0;" % (SANS, INK2),
    6: "font-family:%s;font-size:10pt;color:%s;font-weight:600;margin:11pt 0 3pt 0;" % (SANS, MUTED),
}
LI = "font-family:%s;font-size:10.5pt;line-height:1.5;color:%s;margin:0 0 3pt 0;" % (SANS, INK)
TD = ("border:1px solid %s;padding:5pt 7pt;font-family:%s;font-size:9pt;"
      "line-height:1.4;color:%s;vertical-align:top;" % (LINE, SANS, INK))
TH = TD + "background-color:#F4F5F3;font-weight:600;"
RULE = '<hr style="border:none;border-top:1px solid %s;margin:16pt 0;">' % LINE


def inline(t: str) -> str:
    """Bold, italic, strikethrough, code and links, in that order of nesting."""
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`",
               lambda m: '<span style="font-family:%s;font-size:9.5pt;'
                         'background-color:#F1F2F0;color:%s">%s</span>'
                         % (MONO, INK2, m.group(1)), t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: '<a href="%s" style="color:%s;text-decoration:underline">%s</a>'
                         % (html.escape(m.group(2), quote=True), GOLD, m.group(1)), t)
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r'<b><i>\1</i></b>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r'<b>\1</b>', t)
    t = re.sub(r"~~(.+?)~~", r'<span style="text-decoration:line-through;color:%s">\1</span>' % MUTED, t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"<i>\1</i>", t)
    return t


def callout(inner: str, tone: str = "gold") -> str:
    """A quotation or a correction banner. Docs has no styled blockquote, so this is
    a single-cell table, which is what a hand-made Google Doc uses for the same job."""
    bg, edge = (GOLDWASH, GOLDMARK) if tone == "gold" else ("#F5F6F4", LINE)
    return ('<table style="border-collapse:collapse;width:100%%;margin:11pt 0"><tr>'
            '<td style="border:none;border-left:3px solid %s;background-color:%s;'
            'padding:8pt 11pt">%s</td></tr></table>' % (edge, bg, inner))


def table(rows, align):
    out = ['<table style="border-collapse:collapse;width:100%;margin:11pt 0">']
    for i, row in enumerate(rows):
        out.append("<tr>")
        for j, cell in enumerate(row):
            a = align[j] if j < len(align) else "left"
            style = (TH if i == 0 else TD) + "text-align:%s;" % a
            out.append('<td style="%s">%s</td>' % (style, inline(cell.strip())))
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)


def convert(md: str, title: str | None = None) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out, i, n = [], 0, len(lines)
    first_h1_used = False

    def flush_quote(buf):
        if not buf:
            return
        inner = convert_fragment("\n".join(buf))
        out.append(callout(inner))

    while i < n:
        ln = lines[i]

        # fenced code
        if ln.startswith("```"):
            i += 1
            code = []
            while i < n and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            out.append('<table style="border-collapse:collapse;width:100%%;margin:11pt 0"><tr>'
                       '<td style="border:1px solid %s;background-color:#F7F8F6;padding:8pt 10pt">'
                       '<span style="font-family:%s;font-size:9pt;line-height:1.45;color:%s;'
                       'white-space:pre-wrap">%s</span></td></tr></table>'
                       % (LINE, MONO, INK2, html.escape("\n".join(code)).replace("\n", "<br>")))
            continue

        # blockquote run
        if ln.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            flush_quote(buf)
            continue

        # table
        if "|" in ln and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            head = [c for c in ln.strip().strip("|").split("|")]
            spec = [c.strip() for c in lines[i + 1].strip().strip("|").split("|")]
            align = ["center" if s.startswith(":") and s.endswith(":")
                     else "right" if s.endswith(":") else "left" for s in spec]
            rows = [head]
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append([c for c in lines[i].strip().strip("|").split("|")]); i += 1
            out.append(table(rows, align))
            continue

        # rule
        if re.match(r"^\s*(---+|\*\*\*+|___+)\s*$", ln):
            out.append(RULE); i += 1; continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lvl, text = len(m.group(1)), m.group(2).strip()
            if lvl == 1 and not first_h1_used:
                first_h1_used = True
            out.append("<h%d style=\"%s\">%s</h%d>" % (lvl, H[lvl], inline(text), lvl))
            i += 1
            continue

        # list run (bullets and numbers, one level of nesting)
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", ln):
            items, i = [], i
            while i < n and (re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i])
                             or (lines[i].startswith("  ") and lines[i].strip()
                                 and items)):
                cur = lines[i]
                mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", cur)
                if mm:
                    items.append((len(mm.group(1)), mm.group(2), mm.group(3)))
                else:
                    d, mark, txt = items[-1]
                    items[-1] = (d, mark, txt + " " + cur.strip())
                i += 1
            ordered = bool(re.match(r"\d", items[0][1]))
            tag = "ol" if ordered else "ul"
            out.append('<%s style="margin:0 0 9pt 0;padding-left:20pt">' % tag)
            depth = 0
            for d, mark, txt in items:
                want = 1 if d >= 2 else 0
                while want > depth:
                    out.append('<%s style="margin:3pt 0;padding-left:18pt">'
                               % ("ol" if re.match(r"\d", mark) else "ul")); depth += 1
                while want < depth:
                    out.append("</ul>" if not ordered else "</ol>"); depth -= 1
                out.append('<li style="%s">%s</li>' % (LI, inline(txt)))
            while depth > 0:
                out.append("</ul>" if not ordered else "</ol>"); depth -= 1
            out.append("</%s>" % tag)
            continue

        # blank
        if not ln.strip():
            i += 1; continue

        # paragraph run
        para = [ln]
        i += 1
        while (i < n and lines[i].strip() and not lines[i].startswith(">")
               and not lines[i].startswith("#") and not lines[i].startswith("```")
               and not re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i])
               and not re.match(r"^\s*(---+|\*\*\*+|___+)\s*$", lines[i])
               and "|" not in lines[i]):
            para.append(lines[i]); i += 1
        out.append('<p style="%s">%s</p>' % (BODY, inline(" ".join(para))))

    return "".join(out)


def convert_fragment(md: str) -> str:
    """Inside a callout: same rules, tighter spacing, no nested callouts."""
    body = convert(md)
    return body.replace("margin:0 0 9pt 0;", "margin:0 0 6pt 0;")


def wrap(body: str, title: str, subtitle: str) -> str:
    head = ('<h1 style="%s">%s</h1>' % (H[1], html.escape(title)))
    if subtitle:
        head += ('<p style="font-family:%s;font-size:10pt;color:%s;margin:0 0 4pt 0">%s</p>'
                 % (SANS, MUTED, subtitle))
    head += RULE
    return ("<!doctype html><html><head><meta charset=\"utf-8\"><title>%s</title></head>"
            "<body style=\"font-family:%s;font-size:10.5pt;color:%s\">%s%s</body></html>"
            % (html.escape(title), SANS, INK, head, body))


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    md = open(src, encoding="utf-8").read()
    # The file's own first H1 becomes the document title and is not repeated.
    m = re.match(r"^\s*#\s+(.+?)\s*$", md, re.M)
    title = sys.argv[3] if len(sys.argv) > 3 else (m.group(1) if m else src)
    if m and m.start() == 0:
        md = md[m.end():]
    sub = ("We Are STMing · Jacob Katz and Nuh Shaheer · "
           "the working record, as written. github.com/jacobbkatz/We-Are-STMING")
    open(dst, "w", encoding="utf-8").write(wrap(convert(md), title, sub))
    print("wrote %s  (%d bytes from %d)" % (dst, len(open(dst, encoding="utf-8").read()), len(md)))


if __name__ == "__main__":
    main()
