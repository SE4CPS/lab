#!/usr/bin/env python3
"""Audit every inline SVG in a deck for text that overflows its own box.

For each <text> element inside an SVG, estimate its rendered width
(char_count * font-size * an empirical glyph-width factor) and check it
against the nearest box (<rect>) whose y-range contains the text's baseline
AND whose x-range at least partially overlaps the text's estimated
x-range. Text with no such box is assumed to be a legitimate standalone
label/caption (not meant to be "inside" anything) and is not flagged.

This is a heuristic, not an exact renderer -- it exists to catch gross
overflows (a box sized without checking its own longest label) that are
easy to introduce and easy to miss by eye in a 5000+ line deck, per the
GLOBAL RULE on verifying diagram slides. It will not catch every subtle
case and can occasionally flag a false positive; treat findings as "worth
a second look," not an automatic verdict.

Usage:
    python scripts/audit_svg_text.py path/to/deck.html [...]
"""
import re
import sys
import html

CHAR_WIDTH_MONO = 0.62    # Consolas/monospace: each glyph is close to this fraction of font-size
CHAR_WIDTH_PROP = 0.52    # Segoe UI/Arial/proportional: narrower on average -- using the mono
                          # factor here overestimates width and produces false positives


def char_width_factor(font_family):
    return CHAR_WIDTH_MONO if "Consolas" in font_family or "monospace" in font_family else CHAR_WIDTH_PROP


def audit_svg(svg, label="svg"):
    issues = []
    rects = []
    for m in re.finditer(r"<rect\s+([^/>]*)/>", svg):
        attrs = dict(re.findall(r'([a-zA-Z\-]+)="([^"]*)"', m.group(1)))
        try:
            x, y, w, h = (float(attrs[k]) for k in ("x", "y", "width", "height"))
        except (KeyError, ValueError):
            continue
        rects.append((x, y, w, h))
    if not rects:
        return issues

    # the largest rect is almost always the outer card background, not a content box
    areas = sorted(range(len(rects)), key=lambda i: rects[i][2] * rects[i][3], reverse=True)
    card_idx = areas[0] if len(rects) > 1 else None
    boxes = [r for i, r in enumerate(rects) if i != card_idx]

    for m in re.finditer(r"<text\s+([^>]*)>(.*?)</text>", svg, re.S):
        attrs = dict(re.findall(r'([a-zA-Z\-]+)="([^"]*)"', m.group(1)))
        raw = m.group(2)
        lines = re.findall(r"<tspan[^>]*>(.*?)</tspan>", raw, re.S) or [raw]
        try:
            tx, ty, fs = float(attrs.get("x", 0)), float(attrs.get("y", 0)), float(attrs.get("font-size", 12))
        except ValueError:
            continue
        anchor = attrs.get("text-anchor", "start")
        factor = char_width_factor(attrs.get("font-family", ""))

        for line in lines:
            text = html.unescape(re.sub(r"<[^>]+>", "", line)).strip()
            # SVG (like HTML) collapses runs of whitespace -- including a raw
            # newline plus indentation inside a <text> with no <tspan> -- down
            # to a single space when actually rendered, so measure it that
            # way too or a wrapped source line inflates the estimated width.
            text = re.sub(r"\s+", " ", text)
            if not text:
                continue
            est_w = len(text) * fs * factor
            if anchor == "middle":
                tx1, tx2 = tx - est_w / 2, tx + est_w / 2
            elif anchor == "end":
                tx1, tx2 = tx - est_w, tx
            else:
                tx1, tx2 = tx, tx + est_w

            y_boxes = [b for b in boxes if b[1] - 2 <= ty <= b[1] + b[3] + 2]
            if not y_boxes:
                continue
            overlapping = []
            for b in y_boxes:
                bx1, by1, bw, bh = b
                bx2 = bx1 + bw
                ox = min(tx2, bx2) - max(tx1, bx1)
                if ox > 0:
                    overlapping.append(b)
            if not overlapping:
                continue

            fits = any(b[0] - 1 <= tx1 and tx2 <= b[0] + b[2] + 1 for b in overlapping)
            if not fits:
                b = min(overlapping, key=lambda r: r[2])
                bx1, by1, bw, bh = b
                issues.append(
                    f"{label}: text '{text[:40]}' est x-range [{tx1:.0f},{tx2:.0f}] "
                    f"exceeds nearest box x-range [{bx1:.0f},{bx1 + bw:.0f}]"
                )
    return issues


def main(paths):
    total = 0
    for path in paths:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        print(f"=== {path} ===")
        file_issues = 0
        for i, m in enumerate(re.finditer(r"<svg[^>]*>(.*?)</svg>", content, re.S)):
            issues = audit_svg(m.group(0), label=f"  SVG#{i} (offset {m.start()})")
            for iss in issues:
                print(iss)
            file_issues += len(issues)
        print(f"  {file_issues} possible issue(s)\n")
        total += file_issues
    print(f"Total across {len(paths)} file(s): {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python scripts/audit_svg_text.py <deck.html> [...]")
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
