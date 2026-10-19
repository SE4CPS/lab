#!/usr/bin/env python3
"""Audit every hand-authored SVG diagram's background card for a size
that doesn't actually match its own content -- the "no overflow, no
underflow" GLOBAL RULE in CLAUDE.md.

A diagram card is a <rect> that spans (approximately) the full
viewBox -- this is what distinguishes it from a small decorative or
satellite box inside a hub-style diagram, which would otherwise produce
false positives. For each real card found:

  - OVERFLOW: some <text>/<tspan> OR some other <rect> (a stacked box,
    not just its label) sits past the card's own bottom edge (a
    hardcoded viewBox/card height picked without checking whether the
    last entry's content actually fits inside it). A box can overflow
    with its own label text still sitting safely inside it, so box
    bottoms and text positions are checked independently -- checking
    only text position missed two real instances in comp-175 Module 9
    (2026-10) where the box itself, not its label, clipped the card.
  - UNDERFLOW: the card is much taller than its content needs (a
    hardcoded height copied from a different diagram's math, or picked
    up front and never revisited once the diagram's real content was
    filled in) -- flagged when the empty gap below the last piece of
    content exceeds both an absolute (25px) and a relative (35% of card
    height) threshold, to avoid flagging ordinary comfortable padding.

This is a heuristic over raw markup, not a real renderer -- it can flag
a legitimate design (e.g. a single big icon in a deliberately simple
card) as underflow. Treat every finding as "worth a second look," the
same caveat as audit_svg_text.py, and confirm with an actual screenshot
before deciding whether to resize anything.

Usage:
    python scripts/audit_svg_card_fill.py path/to/deck.html [...]
"""
import re
import sys

CARD_FILLS = {"#2a2a2a", "#1e1e1e", "#0d0d0d"}
UNDERFLOW_REL_THRESHOLD = 0.35
UNDERFLOW_ABS_THRESHOLD = 25


def audit_svg(svg, offset, label="svg"):
    issues = []
    m = re.match(r'<svg\b[^>]*viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not m:
        return issues
    vw, vh = float(m.group(1)), float(m.group(2))

    rects = re.findall(
        r'<rect x="([\-\d.]+)" y="([\-\d.]+)" width="([\d.]+)" height="([\d.]+)"[^>]*fill="(#[0-9a-fA-F]{3,6})"',
        svg,
    )
    if not rects:
        return issues
    cardx, cardy, cardw, cardh, fill = rects[0]
    cardx, cardy, cardw, cardh = float(cardx), float(cardy), float(cardw), float(cardh)
    # the card must span (approximately) the full viewBox, near the origin --
    # otherwise this is a small satellite/decorative box, not a background card
    if cardw < 0.9 * vw or cardx > 5 or cardy > 5:
        return issues
    if fill.lower() not in CARD_FILLS:
        return issues

    card_bottom = cardy + cardh
    ys_text = [float(y) for y in re.findall(r'<(?:text|tspan)[^>]*\sy="([\-\d.]+)"', svg)]
    max_text_y = max(ys_text) if ys_text else cardy

    # other rects (stacked boxes, not just their labels) -- a box can
    # overflow the card while its own label text still sits safely
    # inside it, so this has to be checked independently of text position
    rect_bottoms = [float(ry) + float(rh) for _, ry, _, rh, _ in rects[1:]]
    max_rect_y = max(rect_bottoms) if rect_bottoms else cardy

    content_bottom = max(max_text_y, max_rect_y)
    if not ys_text and not rect_bottoms:
        return issues

    if max_rect_y > card_bottom + 1:
        issues.append(
            f"{label} (offset {offset}): OVERFLOW -- viewBox {vw:.0f}x{vh:.0f}, "
            f"card bottom={card_bottom:.1f}, a box extends to y={max_rect_y:.1f} "
            f"({max_rect_y - card_bottom:.1f}px past the card)"
        )
    elif max_text_y > card_bottom + 1:
        issues.append(
            f"{label} (offset {offset}): OVERFLOW -- viewBox {vw:.0f}x{vh:.0f}, "
            f"card bottom={card_bottom:.1f}, text extends to y={max_text_y:.1f} "
            f"({max_text_y - card_bottom:.1f}px past the card)"
        )

    # underflow: how far does content (any other rect, plus every text/tspan)
    # actually reach, versus how far the card goes
    gap = card_bottom - content_bottom
    if cardh > 0 and gap > UNDERFLOW_ABS_THRESHOLD and gap / cardh > UNDERFLOW_REL_THRESHOLD:
        issues.append(
            f"{label} (offset {offset}): UNDERFLOW -- viewBox {vw:.0f}x{vh:.0f}, "
            f"content ends at y={content_bottom:.1f} but card goes to {card_bottom:.1f} "
            f"({gap:.1f}px / {gap / cardh * 100:.0f}% of card height unused)"
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
            issues = audit_svg(m.group(0), m.start(), label=f"  SVG#{i}")
            for iss in issues:
                print(iss)
            file_issues += len(issues)
        print(f"  {file_issues} possible issue(s)\n")
        total += file_issues
    print(f"Total across {len(paths)} file(s): {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python scripts/audit_svg_card_fill.py <deck.html> [...]")
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
