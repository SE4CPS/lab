"""Estimate slide-frame overflow risk for the RISE seminar deck.

The RISE seminar deck (research/rise-seminar/Fall2026/index.html) is a
single long vertical stack: one bare outer <section> containing every
real content slide as a nested <section data-chapter="N">. That matches
this repo's own `.reveal .slides > section > section { max-height: 680px;
overflow-y: auto; }` cap, so every one of these is a "leaf slide" subject
to that budget. This is a heuristic estimate, not a real renderer (this
repo has no browser/screenshot tool available): treat every finding as
"worth a second look," not an automatic verdict, per the same spirit as
scripts/audit_svg_text.py.

Usage:
    python scripts/audit_rise_slide_height.py [path/to/index.html]
Defaults to research/rise-seminar/Fall2026/index.html.
"""
import re
import sys
import html as htmllib

PATH = sys.argv[1] if len(sys.argv) > 1 else "research/rise-seminar/Fall2026/index.html"
CAP = 680          # .reveal .slides > section > section max-height
WARN_AT = 600      # flag with margin before the hard cap
BASE_FONT = 25     # .reveal base font-size, px (1em)
LINE_HEIGHT = 1.35
GLYPH_W = 0.52     # proportional-text width factor (same heuristic as audit_svg_text.py)
# Effective content width per "column" in px, at a plausible large
# presentation viewport. Full-width content uses FULL_W; a .twocol
# child uses HALF_W (minus inter-column gap and this deck's own padding).
FULL_W = 1400
HALF_W = 660

with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

section_re = re.compile(r'<section\s+data-chapter="(\d+)"([^>]*)>(.*?)</section>', re.S)


def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = htmllib.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def est_text_lines(text, width_px):
    if not text.strip():
        return 0
    chars_per_line = max(10, int(width_px / (BASE_FONT * GLYPH_W)))
    return max(1, -(-len(text) // chars_per_line))  # ceil division


def est_block_height(inner_html, width_px):
    line_px = BASE_FONT * LINE_HEIGHT
    total = 0
    notes = []

    # SVGs come in two real shapes in this deck: a fixed-size icon
    # (explicit width="N" height="N" HTML attrs, e.g. every .structicon
    # glyph) that renders at exactly that pixel size regardless of
    # viewBox or container width, and a responsive diagram
    # (style="width:100%;max-width:Npx;height:auto") that scales to the
    # container/max-width, height derived from the viewBox aspect
    # ratio. Conflating the two (treating every svg as the responsive
    # kind) produced a wildly wrong estimate for every small icon.
    for svg in re.finditer(r'<svg\b([^>]*)>(.*?)</svg>', inner_html, re.S):
        attrs = svg.group(1)
        fixed_w = re.search(r'\bwidth="(\d+)"', attrs)
        fixed_h = re.search(r'\bheight="(\d+)"', attrs)
        if fixed_w and fixed_h and 'width="100%"' not in attrs:
            svg_h = float(fixed_h.group(1))
            total += svg_h
            notes.append("svg(fixed) ~%dpx" % svg_h)
            continue
        vb = re.search(r'viewBox="[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', attrs)
        style_w = re.search(r'max-width:\s*(\d+)px', attrs)
        render_w = min(width_px, int(style_w.group(1))) if style_w else width_px
        if vb:
            w, h = float(vb.group(1)), float(vb.group(2))
            svg_h = render_w * (h / w) if w else 0
            total += svg_h
            notes.append("svg(scaled,%dw) ~%dpx" % (render_w, svg_h))
    body_no_svg = re.sub(r'<svg\b.*?</svg>', '', inner_html, flags=re.S)

    for m in re.finditer(r'<h([234])[^>]*>(.*?)</h\1>', body_no_svg, re.S):
        level, txt = m.group(1), strip_tags(m.group(2))
        size_em = {'2': 1.7, '3': 1.3, '4': 1.05}[level]
        lines = est_text_lines(txt, width_px)
        h = lines * BASE_FONT * size_em * 1.15 + 10  # + margin
        total += h
        notes.append("h%s(%dc)~%dpx" % (level, len(txt), h))

    for m in re.finditer(r'<p\b[^>]*>(.*?)</p>', body_no_svg, re.S):
        txt = strip_tags(m.group(1))
        lines = est_text_lines(txt, width_px)
        h = lines * line_px + 8  # + margin
        total += h
        if len(txt) > 40:
            notes.append("p(%dc,%dl)~%dpx" % (len(txt), lines, h))

    li_count = 0
    for m in re.finditer(r'<li\b[^>]*>(.*?)</li>', body_no_svg, re.S):
        txt = strip_tags(m.group(1))
        lines = est_text_lines(txt, width_px)
        total += lines * line_px * 0.85 + 4
        li_count += 1
    if li_count:
        notes.append("%d li" % li_count)

    tr_count = len(re.findall(r'<tr\b', body_no_svg))
    if tr_count:
        row_h = BASE_FONT * 0.62 * 1.35 + 11  # table font is 0.62em, plus row padding
        total += tr_count * row_h
        notes.append("%d tr~%dpx" % (tr_count, tr_count * row_h))

    return total, notes


def first_heading(inner_html):
    m = re.search(r'<h[234][^>]*>(.*?)</h[234]>', inner_html, re.S)
    return strip_tags(m.group(1))[:70] if m else "(no heading)"


results = []
for m in section_re.finditer(src):
    chapter, attrs, inner = m.group(1), m.group(2), m.group(3)
    line_no = src[:m.start()].count("\n") + 1

    if 'qbox-grid' in inner:
        # A real CSS grid (grid-template-columns: repeat(5, 1fr)), not a
        # vertically-stacked list of paragraphs. This heuristic's
        # per-<p> stacking model doesn't apply and would wildly
        # overestimate height (e.g. 18 short boxes in 4 rows of 5, not
        # 18 stacked lines). Skipped rather than modeled.
        results.append((line_no, chapter, first_heading(inner), None,
                         ["qbox-grid: not audited, real CSS grid not stacked rows"]))
        continue

    if 'display:flex' in inner and inner.count('<svg') > 1:
        # A row of small side-by-side figures (see the running
        # release-distribution-by-time-interval example): flex children
        # share the row's width, not each one individually stretching
        # full-width. Not modeled generically; skipped so it isn't
        # wrongly flagged as if the figures were stacked.
        results.append((line_no, chapter, first_heading(inner), None,
                         ["flex row of figures: not audited, side by side not stacked"]))
        continue

    if '<div class="twocol">' in inner:
        # Two columns side by side, each roughly HALF_W wide.
        tw = re.search(r'<div class="twocol">(.*?)</div>\s*</section>|<div class="twocol">(.*)$', inner, re.S)
        body = (tw.group(1) or tw.group(2)) if tw else inner
        col_re = re.compile(r'<div>(.*?)</div>\s*(?=<div>|$)', re.S)
        cols = [c.group(1) for c in col_re.finditer(body)] or [body]
        pre_twocol = inner[:inner.index('<div class="twocol">')]
        h_pre, notes_pre = est_block_height(pre_twocol, FULL_W)
        col_results = [est_block_height(c, HALF_W) for c in cols]
        col_heights = [h for h, _ in col_results]
        est = h_pre + (max(col_heights) if col_heights else 0)
        notes = notes_pre + ["COL%d:%s" % (i, n) for i, (_, n) in enumerate(col_results)]
    else:
        est, notes = est_block_height(inner, FULL_W)

    results.append((line_no, chapter, first_heading(inner), est, notes))

skipped = [r for r in results if r[3] is None]
flagged = [r for r in results if r[3] is not None and r[3] >= WARN_AT]
print("Total leaf slides audited: %d (%d skipped as not modeled)" % (len(results), len(skipped)))
print("Flagged (estimated >= %dpx, cap %dpx): %d\n" % (WARN_AT, CAP, len(flagged)))
for line_no, chapter, heading, est, notes in flagged:
    tag = "OVER CAP" if est > CAP else "near cap"
    print("[%s] line %d (chapter=%s) ~%dpx :: %s" % (tag, line_no, chapter, est, heading))
    print("    " + " | ".join(notes))
if skipped:
    print("\nSkipped (not modeled; review manually if ever touched again):")
    for line_no, chapter, heading, est, notes in skipped:
        print("  line %d (chapter=%s) :: %s : %s" % (line_no, chapter, heading, notes[0]))
