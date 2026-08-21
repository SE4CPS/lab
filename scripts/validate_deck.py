#!/usr/bin/env python3
"""Validate a reveal.js course deck against this repo's CLAUDE.md conventions.

Checks performed:
  - <section>/<div> tag balance (fast, parser-agnostic lexical scan)
  - Full HTML5 structural parse via html5lib (catches things like stray/orphaned
    closing tags and unescaped "<" in code samples that silently corrupt the
    real DOM tree even when tag counts look balanced -- see comp-051's
    "orphaned </div>" bug and data-013's stray "5555" token, both found by
    this exact check and invisible to a simple tag-count pass)
  - Bullet length cap (<=30 visible chars per <li>, per CLAUDE.md)
  - Em dash usage in *visible* text (comments are exempt -- flagging emphasis
    dashes in invisible authoring notes is noise, not signal)
  - Bare (non-linked) URLs in visible text
  - Mermaid usage (should be inline SVG in any deck built/edited after 2026-08)
  - Presence of the required chrome: slideNumber:false + custom counter using
    the exact ".reveal > .slides > section" selector, seal image, "Updated:"
    stamp

Usage:
    python scripts/validate_deck.py <path/to/index.html> [more paths...]

Exit code is 0 if every deck passes with zero *serious* issues (HTML5
structural errors); bullet-length/em-dash/bare-URL counts are reported but do
not fail the run, since those are advisory (see CLAUDE.md's "going forward
only" bullet-length policy) rather than hard requirements.

Requires: html5lib, lxml (``pip install html5lib lxml``).
"""
import html
import re
import sys

try:
    import html5lib
except ImportError:
    print("This script requires html5lib + lxml: pip install html5lib lxml", file=sys.stderr)
    raise

TAG_RE = {
    "section": re.compile(r"<section\b[^>]*>|</section\s*>"),
    "div": re.compile(r"<div\b[^>]*>|</div\s*>"),
}
LI_RE = re.compile(r"<li\b[^>]*>(.*?)</li>", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
URL_RE = re.compile(r"https?://[^\s\"'<>]+")


def strip_comments(text):
    return COMMENT_RE.sub("", text)


def tag_balance(text, tag):
    # Strip comments first -- an authoring comment that merely *mentions* a
    # tag name in prose (e.g. "...on the slide's <section>) that...") would
    # otherwise be miscounted as a real open/close, producing a false alarm.
    text = strip_comments(text)
    depth = 0
    min_depth = 0
    for m in TAG_RE[tag].finditer(text):
        depth += -1 if m.group().startswith("</") else 1
        min_depth = min(min_depth, depth)
    return depth, min_depth


def bullet_length_report(text):
    total = 0
    over = 0
    for m in LI_RE.finditer(text):
        total += 1
        plain = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        plain = re.sub(r"\s+", " ", plain)
        if len(plain) > 30:
            over += 1
    return total, over


def bare_url_count(visible_text):
    count = 0
    for m in URL_RE.finditer(visible_text):
        pre = visible_text[max(0, m.start() - 10) : m.start()]
        if 'href="' not in pre and 'src="' not in pre and "xmlns=" not in pre:
            count += 1
    return count


def validate(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    print(f"\n=== {path} ===")
    ok = True

    for tag in ("section", "div"):
        depth, min_depth = tag_balance(text, tag)
        status = "OK" if depth == 0 and min_depth >= 0 else "MISMATCH"
        if status != "OK":
            ok = False
        print(f"  {tag} balance: final={depth} min={min_depth} [{status}]")

    parser = html5lib.HTMLParser(
        tree=html5lib.treebuilders.getTreeBuilder("lxml"), debug=True
    )
    parser.parse(text)
    serious = [
        e
        for e in parser.errors
        if e[1]
        in ("end-tag-too-early", "unexpected-end-tag", "expected-closing-tag-but-got-eof")
    ]
    print(f"  HTML5 structural errors: {len(serious)}")
    if serious:
        ok = False
        for e in serious[:10]:
            print(f"    {e}")

    doc = html5lib.parse(text, treebuilder="lxml", namespaceHTMLElements=False)
    root = doc.getroot()
    top_level = root.cssselect(".reveal > .slides > section")
    print(f"  Top-level (horizontal) slides: {len(top_level)}")

    visible_text = strip_comments(text)
    total_li, over_li = bullet_length_report(visible_text)
    pct = 100 * over_li / max(total_li, 1)
    print(f"  Bullets over 30 chars: {over_li}/{total_li} ({pct:.0f}%) [advisory]")

    em_dash = visible_text.count("—")
    print(f"  Em dashes in visible text: {em_dash} [advisory -- check for emphasis misuse]")

    mermaid = len(re.findall(r"mermaid", text, re.I))
    print(f"  Mermaid mentions: {mermaid}" + (" [should be inline SVG]" if mermaid else ""))

    bare = bare_url_count(visible_text)
    print(f"  Bare URLs in visible text: {bare}" + (" [should be <a> links]" if bare else ""))

    has_counter = ".reveal > .slides > section" in text and "slideNumber: false" in text
    has_seal = "University_of_the_Pacific_seal" in text
    has_stamp = "Updated:" in text
    print(
        f"  Chrome: counter={'OK' if has_counter else 'MISSING'} "
        f"seal={'OK' if has_seal else 'MISSING'} "
        f"stamp={'OK' if has_stamp else 'MISSING'}"
    )

    return ok


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    all_ok = True
    for path in argv:
        if not validate(path):
            all_ok = False
    print("\n" + ("PASS" if all_ok else "FAIL (see structural errors above)"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
