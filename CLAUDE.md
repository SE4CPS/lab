# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Keeping this file current

**When the instructor gives an instruction, evaluate whether it's a reusable convention (applies beyond
the one slide/deck being touched right now) rather than a one-off content edit.** If it is, add it to this
file as a documented rule (GLOBAL RULE for anything meant to hold across every course deck; a scoped note
otherwise) in the same turn, without waiting to be asked separately. If it's just a one-off ("fix this
typo," "shorten this bullet"), don't. This file should always reflect the current, real conventions of the
repo, not lag behind what's actually been established.

## What this repository is

A static site of teaching and research materials for University of the Pacific courses, published via
GitHub Pages. There is no build step, package manager, or test suite for the site itself — it is served
as-is from the repository root.

- `index.html` — hand-written landing page linking out to each course/section, grouped under a
  "Teaching — Fall 2026" list (current-semester courses) and a "Past" list (older offerings). Update this
  when a course starts/finishes being taught. **GLOBAL RULE — its own `<div class="updated">Updated:
  YYYY-MM-DD HH:MM PT</div>` stamp (near the bottom of the page, same Pacific-time format as every deck's
  footer stamp) gets bumped to the current date/time on *every* edit anywhere in the repo, not only when
  `index.html` itself changes** — it's the site's single "last touched" indicator, so treat it the same way
  as a per-deck stamp: manually maintained, no build step to do it automatically, bump it in the same turn
  as any other edit rather than only when this file is the one being touched.
- `comp-051/`, `comp-153/`, `comp-163/`, `comp-175/`, `comp-233/`, `comp-263/`, `data-013/`, `javascript/`,
  `meetup/*/`, `research/` — one directory per course or talk. Each contains an `index.html` slide deck plus
  its own images, PDFs, and handout docs.
- `readme/`, `android/`, `code.html` — smaller standalone pages, same pattern.

Slide decks (e.g. `comp-263/index.html`, `comp-233/index.html`) are single HTML files built on
**reveal.js 4.3.1**, loaded from the `cdnjs`/`jsdelivr` CDN (no local/npm copy) — see the `<link>`/`<script>`
tags at the top and bottom of any `index.html`. Diagrams inside decks are authored inline as **Mermaid** or
**PlantUML** and rendered via CDN scripts as well. These files are large (20–40k lines) because every slide
is inline; when editing, jump straight to the relevant `<section>` via search rather than reading the whole
file.

Because each deck is a single self-contained HTML file, there's no shared component/template system across
courses — copy patterns from a similar existing slide in the same deck (or another course's deck) rather
than inventing new structure.

## A few standalone code samples live in this repo (not part of the site build)

These are course examples/demos, each independent, with no root-level `package.json` tying them together:

- **`comp-233/`** — has its own `package.json` (`sensor-user-authentication`, Express app; `npm start` runs
  `app.js` — note `app.js` isn't currently checked in) and `be.py`, a separate Flask + MongoDB dashboard
  backend (`python be.py`, serves on port 5001).
- **`ollama-agent/`** — small Node/Python examples (`sensor.js`, `agent.py`) with hand-rolled test files
  (`sensor.test.js`, `legal.test.js`) that use Node's built-in `assert` and run directly, e.g.
  `node ollama-agent/sensor.test.js` — there is no test runner (Jest/Mocha) configured, and no
  `package.json` in this directory.
- **`comp-153/`** and **`comp-163/`** — `postgress-*.py` scripts (ping/print/crud/webserver) demonstrating
  Postgres access, plus a Flask template (`templates/flowers.html`) and a SQLite DB (`flowers.db`) used in
  labs.

Treat each of these as an isolated example tied to its course folder, not a shared library — don't assume
changes in one propagate to another, even when the logic looks duplicated (e.g. `postgress-*.py` is
duplicated near-identically between `comp-153/` and `comp-163/`).

## Conventions for a new/updated course deck

These apply to any course folder, not just one course in particular:

- **Fixed-position chrome, not a real footer.** Reveal.js slides don't share a DOM footer, so persistent
  elements (university seal, quick links) are `position: fixed` `<img>`/`<a>` tags placed directly in
  `<body>`, before `<div class="reveal">`, so they render above every slide. Seal goes top-right; quick
  links (e.g. `Canvas`, `Syllabus`) go bottom-left as small pill-style `<a>` tags in a flex container —
  copy the existing markup/styling rather than reinventing it.
- **Every deck shows a slide counter and a last-updated stamp.** The counter must count **horizontal
  slides only** (`c/t` = current/total across top-level `<section>`s), not flatten vertical sub-slides into
  the same count — reveal.js's built-in `slideNumber: 'c/t'` counts every slide including nested verticals,
  which isn't what we want. Instead set `slideNumber: false` and, in `Reveal.initialize({...}).then(...)`,
  install a small custom counter: read `Reveal.getIndices()` for `{h, v}`, count `.reveal > .slides >
  section` for the horizontal total, and if the current horizontal slide has more than one direct `section`
  child, append a second `(v+1/vTotal)` count next to the main one — so a module with a vertical stack shows
  both "this module's position among modules" and "position within that module." Fixed bottom-right,
  `pointer-events: none`. Applies to every deck. The "Updated" stamp lives **inside the bottom-left quick-link
  footer, as its last element** (after `Home`/`Canvas`/`Syllabus`, whichever exist) — a plain `<span>` (not a
  link) styled like
  the pill `<a>` tags next to it: `Updated: YYYY-MM-DD HH:MM PT` in **Pacific time** (this repo is a Pacific
  university's course site; Pacific time regardless of where the edit is made). If a deck has no left-side
  footer yet, create one (`position: fixed; bottom: 10px; left: 10px; display: flex; gap: 8px;`) containing
  just this span. **Whenever you edit a deck's slide content, bump the stamp to the date/time of the
  edit** — it's manually maintained, not computed, since this repo has no build step to stamp it
  automatically.
- **Syllabus content is its own vertical stack.** Wrap syllabus-type slides (course description, learning
  objectives, grading, policies, project milestones) in one outer `<section id="syllabus">` containing
  nested `<section>`s, the same nesting pattern used for module stacks (`<section id="module-N">` with
  inner `<section>`s) — keeps them reachable by pressing down, off to the side of the main horizontal flow.
- **Reusing another course's public materials:** when asked to build a course off a prior public offering
  (e.g. a department course-archive site) or a colleague's syllabus doc, leave an HTML comment near the top
  of `<body>` naming the source and summarizing what was changed/omitted (e.g. swapped a cloud provider for
  local VMs, dropped instructor-identifying details like name/office/email). Don't invent
  dates/policies/deliverables that aren't in a source or given by the instructor — mark them
  `TBD`/flag in a comment instead (e.g. exact holiday breaks beyond fixed federal holidays, final exam
  time/room) rather than guessing.
- **Root `index.html`'s course list** should reflect who's teaching what *now*: current-semester courses
  under a "Teaching — <Term Year>" heading, everything else under "Past".
- **Reading a `.docx` in this repo:** the Read tool can't open it directly, and this environment doesn't
  have `pandoc`/`python-docx`. Unzip it and strip tags from `word/document.xml` (e.g. via `unzip` + a small
  Python regex pass) to pull out plain text.
- **Writing a `.docx` in this repo:** same missing-dependency problem in reverse. Build one by hand with
  Python's stdlib `zipfile` (no external package needed) — a `.docx` is just a zip of a handful of OOXML
  parts: `[Content_Types].xml`, `_rels/.rels`, `docProps/core.xml`, `word/document.xml`,
  `word/styles.xml`, `word/_rels/document.xml.rels`. Keep it minimal (paragraph/heading/table helpers that
  emit `<w:p>`/`<w:tbl>` XML) and don't reference styles, numbering, or rels IDs you haven't actually
  defined in the corresponding part — Word will prompt to repair the file on a dangling reference. Validate
  before calling it done: reopen with `zipfile.testzip()` and parse every `.xml`/`.rels` part with
  `xml.etree.ElementTree` to confirm they're well-formed. See `comp-175/CourseSyllabus175-Fall2026.docx`
  and the script that generated it for the working pattern.
- **Bullet length cap:** every `<li>` in a slide deck must be **30 characters or fewer** of visible text
  (tags/entities don't count). Applies deck-wide, not just to whichever slide is being edited — when adding
  or editing any bullet, write it short from the start rather than shortening later. When auditing an
  existing deck, extract `<li>` text with a small Python regex pass (strip tags, `html.unescape`, collapse
  whitespace, check length) rather than eyeballing it — this repo's decks are 20k+ lines, too long to scan
  by hand reliably. **Enforcement is going-forward only**, not retroactive: comp-051 and data-013 predate
  this rule and are 44%/56% non-compliant across 1,000+ existing bullets each — don't mass-rewrite old
  content to fix this on its own; only bring a bullet into compliance when you're already touching that
  slide for another reason.
- **No em dashes/hyphens used for emphasis.** Don't write `"clause — clause"` as a rhetorical aside; split
  into two sentences or use a colon/comma instead. Legitimate uses stay: numeric/date ranges (`&ndash;`, e.g.
  `Aug 24–Dec 11`, `1–2 PM`) and plain compound-word hyphens (`long-term`, `Type-2`) are fine — only the
  dash-as-emphasis construction goes.
- **Keep slide content technical, not motivational filler.** Cut generic "wisdom summary" / reflection
  slides (recaps that just restate a vibe, open-ended "discuss" prompts with no technical content). Concrete,
  sourced facts (a real CVE, a cited statistic with a source) are fine to keep even if introduced for
  motivation — the test is whether a bullet teaches or cites something concrete, not whether the slide has
  an inspirational framing.
- **GLOBAL RULE — slide `<h4>`/`<h3>`/`<h2>` headings are technical/descriptive, not catchy or
  rhetorical.** Write the heading as a plain noun phrase naming what the slide actually shows (`Admin and
  User Scale`, `Package Manager: Real Examples`), not a punchy tagline built around a rhetorical contrast or
  wordplay (`The Same Job, Very Different Scale`). Applies to every deck, every heading level, going
  forward — when in doubt, prefer the shorter, flatter, more literal phrasing over the more "interesting"
  one. A caption/note under a diagram that just restates what the diagram already visually shows (not a
  warning or risk) should be cut entirely rather than kept for flavor — see the `.note-below` rule above,
  which already covers this for fragment notes specifically; the same judgment applies to any plain
  descriptive `<p>` caption too, warning-only or gone.
- **Any URL shown as visible slide text must be a clickable link** (`<a href="..." target="_blank"
  rel="noopener">`), not bare text — applies to citations, footers, syllabus references, everywhere.
- **Diagrams are hand-authored inline SVG, not Mermaid, in any deck built/edited after 2026-08.** Mermaid
  inside reveal.js only renders reliably for whichever slide happens to be visible at page load — every
  other `.mermaid` block sits in a `display:none` section and fails to measure/render correctly, so it
  silently breaks for anything but the first slide. Build diagrams as plain inline SVG (rects/text/lines,
  a shared arrowhead `<marker>`, a small `box()`/`arrow()`/`svg()` helper set is enough) — guaranteed to
  render regardless of which slide is showing. See `comp-175/index.html` for the established helper pattern.
  - **Minimum 4px gap** between any two boxes in the same diagram (no touching/near-touching edges) —
    audit programmatically (parse `<rect>` x/y/width/height, check pairwise overlap+gap) rather than eyeballing;
    this repo's diagrams are dense enough that visual review misses violations. The audit must flag two
    separate failure modes: boxes that overlap on **both** axes at once (a true collision — check this
    case explicitly, a gap-only check silently misses it) and boxes with **less than 4px** gap on the one
    axis where they don't overlap.
  - **Scale to fill the available space**: set `max-width` high enough that the SVG actually uses the column
    it's placed in (twocol right pane, or full slide width for a concept diagram) rather than rendering small
    with wasted whitespace around it; keep SVG text a bit larger than the deck's base look-and-feel to stay
    readable at that size. This only works if the diagram's own wrapper actually participates in the
    `.twocol` flex layout — a `<div class="diagram">` sibling of `.col` needs `flex:1` too (comp-175's
    `.twocol .col, .twocol .diagram { flex: 1; min-width: 0; }` covers both), otherwise raising `max-width`
    on the SVG does nothing visible: the wrapper still sizes to its own content instead of stretching to
    fill its half of the row, leaving dead space beside a diagram that looks small no matter how high the
    ceiling is raised. If a deck ever introduces its own `.diagram` wrapper class, give it this same rule.
  - **Raising `max-width` only helps a landscape diagram — a tall/portrait one (height > width in its
    `viewBox`) needs the opposite caution.** Since sizing is `width:100%;height:auto`, scaling the width up
    scales the height up by the same ratio, and reveal.js slides have a fixed height with no scroll — a
    portrait diagram pushed too wide overflows off the top/bottom of the slide instead of getting more
    legible. Before bumping a diagram's `max-width`, check its `viewBox` aspect ratio first; for a portrait
    one, leave it at (or size it around) whatever value already renders without clipping rather than
    applying the same percentage bump used for the wide ones. comp-175's recurring 16-module position
    diagram (`viewBox="0 0 288 502"`) is the example this bit — it overflowed at `max-width:440px` and is
    now standardized back to `310px` across every slide that uses it.
  - **GLOBAL RULE — any label that appears in both the TOC and a recurring diagram (this module-position
    stack being the concrete case) is stored once, in one JS object, and both consumers render from it —
    never hand-duplicated in N places.** Before this was fixed, this diagram's 16 module names were
    hardcoded inline in the SVG markup of *every* slide that showed it (21 copies in comp-175), and had
    drifted out of sync with the TOC's own Topic column, which uses different, more current wording. The
    fix: a `moduleTopics` object (module number &rarr; topic string, matching the TOC's Topic column
    exactly) defined once in the deck's footer `<script>`; the TOC's Topic `<td>` cells carry a matching
    `data-module="N"` attribute so the same object can also set/verify their text; and the diagram itself
    is reduced to a placeholder — `<div class="module-nav" data-current="N"></div>` — that a
    `buildNavSVG(current)` function renders into on page load, reading labels from `moduleTopics`. Changing
    a module's topic name now means editing `moduleTopics` in one place; the TOC row and every diagram
    instance picks it up automatically. **This mechanism is wired up in both comp-175 and comp-051** — the
    same `moduleTopics`/`topicFull`/`topicShort`/`buildNavSVG`/`.module-nav` IIFE, in each deck's own footer
    `<script>`, reading each deck's own topics. comp-051's version adds one wrinkle worth copying if another
    deck needs it: when a TOC topic is a long, multi-part description (comp-051's Week 1 is three phrases
    joined by commas) that doesn't fit the diagram's box width, `moduleTopics[n]` holds both a `full` string
    (goes to the TOC) and an optional `short` one (goes to the diagram only, falls back to `full` when
    absent) — don't shorten what's actually shown in the TOC just to make it fit a 260px SVG box. Any future
    deck with a similar "same list of names shown in multiple places" situation should follow this same
    pattern rather than hand-duplicating text.
  - **GLOBAL RULE — reordering or renaming which topic occupies a given module number is *not* a
    one-line `moduleTopics` edit; it touches several places `moduleTopics` doesn't reach, and all of them
    must be updated in the same turn.** `moduleTopics` only auto-propagates to the TOC's Topic column and
    the `.module-nav` diagram — it does **not** touch: (1) that module's own `<h2>Module N</h2><h3>Title</h3>`
    heading and its stub/real Agenda content (module wrappers keep a fixed `id="module-N"` position; swapping
    two modules' topics means swapping the *content* inside two `id="module-N"` wrappers, not renumbering
    the wrappers); (2) any "Looking Ahead: Module N" transition slide at the end of the *previous* module,
    which names what's coming next in prose and will describe the old topic if left untouched; (3) a
    syllabus-page "Topics" list, if one enumerates topics in module order; (4) any other prose anywhere in
    the deck that names a module by topic rather than by number. Treat `moduleTopics` as step one of a
    checklist, not the whole fix — after editing it, `grep` the deck for the old and new topic names/module
    numbers to find what else needs updating rather than assuming the JS object alone covers it. **Also
    audit every *other* module's own `<h3>` against `moduleTopics[n]` at the same time, not just the two
    being reordered** — a script-driven check across comp-175 (parse each `<!-- MODULE N -->` block's
    `<h3>` and diff it against `moduleTopics[n]`) found 12 of 15 modules already mismatched, unrelated to
    the module-2/3 swap itself (stale stub titles like `<h3>Dynamic Host Config (DHCP)</h3>` next to a
    `moduleTopics` entry of `'Network Configuration'`) — these drift silently any time `moduleTopics` gets
    refined without a matching sweep back through the `<h3>` titles, so fixing only the two modules being
    actively reordered leaves a deck that still looks inconsistent to a reader paging through it. This was
    the actual gap caught when comp-175's Module 2 (File Systems) and Module 3 (Command-Line & Permissions)
    were swapped: `moduleTopics` was updated first, but the module wrappers' own headings/agendas, the
    Module 1 "Looking Ahead: Module 2" slide, and the syllabus Topics list all still described the old
    ordering until fixed by hand. Applies to every deck, any time modules get reordered or retopicked.
  - **Text sitting directly on a solid `#FF671D` fill uses dark text, never white** — see the dedicated
    GLOBAL RULE on this further down for the full explanation and exceptions.
  - **UOP orange (`#FF671D`, Pantone 165 C — the brand's current primary orange) is the one highlight/accent
    color** across diagrams and CSS alike: the "current item" fill in a diagram, `.highlight` text color,
    stat-bar fills, accent icons. Don't introduce a second accent color for the same "this one matters" role.
  - **GLOBAL RULE — a hand-drawn "star"/hub-spoke diagram (one central circle with several satellite boxes
    arranged around it, e.g. "What Does an OS Actually Do?" or "Advantages of Virtualization" in comp-175)
    has no connecting edges** — no radiating `<line>`/arrow spokes between the hub and its satellite boxes.
    The circular arrangement itself already reads as "these all relate to the center"; adding lines on top
    clutters a layout that's already dense with 6+ boxes and their own text, without adding information the
    positioning didn't already convey. Remove the `<line>` elements (and their now-unused arrowhead
    `<marker>` in `<defs>`, if nothing else in that SVG references it) between the hub and satellites, but
    keep both the hub circle and the satellite boxes themselves. Applies to this diagram shape specifically
    (a central hub + radiating satellites) — the linear stacked-box diagrams elsewhere (e.g. compile
    pipelines, layer stacks) still keep their connecting arrows, since those actually show a sequence/flow,
    not just a "these relate to one center" grouping.
- **GLOBAL RULE — no scrollable code blocks, ever.** A `<pre><code>` long enough to need a scrollbar in
  reveal.js means a viewer can't see the whole thing at once during a live talk — that's a failure of the
  slide, not something a scrollbar fixes. Split it into two side-by-side blocks in a flex/twocol row instead
  (each with its own `<pre><code>`, a smaller inline `font-size` like `14pt` if needed) so the full listing
  is visible without scrolling. Only trim/omit code as a last resort if splitting still doesn't fit; don't
  reach for `overflow-y:auto` as the solution.
- **GLOBAL RULE — a large decorative heading (e.g. `<h2><span class="highlight">...</span></h2>` at the
  reveal.js theme's default large size) wrapping onto 2+ lines inside a narrow twocol column eats vertical
  space fast, and bullets below it can get pushed off the bottom of the slide with no scroll to recover
  them.** Before using the theme's default heading size for a phrase longer than a couple words inside a
  narrow column, either give it an explicit smaller `font-size` (comp-051's "Before Operating Systems" slide
  needed `font-size:1.7rem` to stop wrapping 3x) or shorten the phrase. This compounds with long bullets —
  when a heading is already tall, keep that slide's bullets to single lines (see the bullet-length rule)
  rather than letting both problems stack.
- **A lone, narrow, left-aligned block of content (a short code sample, a couple of links) with nothing
  beside it reads as "half-empty slide," even though reveal.js is just doing its normal text-align:center
  default.** Pair it with a companion visual in a real twocol layout — for a short code sample, a small
  diagram showing where it fits in a larger pipeline/concept works well (see comp-051's "C Code" → "Assembly"
  slide pair, each paired with the same compile pipeline diagram, current stage highlighted per slide) —
  rather than leaving it centered alone with no image, matching the concept→existing-software→implementation
  pattern's usual visual density. **Caveat, stated plainly:** this can only be checked by actually reading
  each slide's markup (there's no browser/screenshot tool available to render and inspect a deck visually),
  so a "no empty space anywhere in this deck" sweep is done incrementally, slide by slide, as instances are
  found or flagged — not as a one-shot guarantee across an entire 10k+-line deck.
- **GLOBAL RULE — once a module actually has real content, its second slide is an Agenda slide**, right
  after the module's own heading/title slide and before its first real content (e.g. before the
  chronological-motivation timeline slide). Two-column: left is an `<ol style="line-height: 1.8;">` of ~6-8
  condensed topic items covering the whole module (module-specific, not per-slide-exhaustive); right is a
  real technical figure that matches the module's subject, following the same hotlink-and-credit pattern as
  "Real product screenshots" below — search for a genuine diagram from a reputable source, actually fetch
  and verify it renders as a real image before using it (don't guess a URL), and prefer one that's actually
  legible at slide scale (a huge multi-thousand-pixel infographic looks impressive in search results but is
  unusable on a slide — a small set of individually-verified official logos or a properly-proportioned
  diagram beats one giant unreadable poster). Credit it in a `.source-line`. See Module 1 in any deck for
  the pattern. **A bare stub module (title slide only, `[not yet built]`, no real content yet) does NOT
  get a placeholder Agenda slide** — a plain `<h4>Agenda</h4>` + `<ol>` with no figure and nothing to
  preview is dead weight, not a real second slide; it was tried in comp-175's Modules 2-16 and removed once
  it became clear an agenda for a module with zero other slides doesn't preview anything. A stub module is
  just its title slide (`<h2>Module N</h2><h3>Title</h3>` + the `.module-nav` diagram) until the module
  actually gets built out with real content — the Agenda slide gets added as part of that build-out, not
  before. Applies to every module, every deck.
- **Module content follows concept → existing software → implementation.** For a topic-per-module course
  deck, open with a very conceptual, mostly-diagram slide (what the idea is and why it's called that — no
  product names yet), then a slide on real existing software/tools that implement the concept, then the
  hands-on technical implementation (actual commands, config, or URLs). Keep the diagram-only concept slide
  full-slide width, not two-column, so it reads as "big idea" before the two-column technical slides that
  follow it.
- **GLOBAL RULE — every larger topic, in every module, in every course deck, opens with a
  chronological-motivation slide, before its concept slide.** Not specific to one course; applies the moment
  any module (new or existing) introduces a named topic (a language feature, a role, a technology, a
  command family — whatever the module's own topic-per-module or concept-per-topic breakdown is). Jumping
  straight from one topic's wrap-up into the next topic's concept slide (e.g. from "the sysadmin role" to
  "what is virtualization") reads as an abrupt jump with no bridge — the timeline slide is that bridge, and
  it comes *before* the concept → existing software → implementation sequence above, not instead of it.
  Two-column, standard 50/50 split: **left column is just the module heading** (`<h2>Module N</h2>` +
  `<h3>Title</h3>`, the same heading every other opening slide in that module uses — this is each module's
  actual first slide, so it must still say which module you're in), **right column is the chronological
  timeline** (5-6 dated milestones, vertical line with a dot per entry, most-recent entry in UOP orange)
  answering "when/why did this topic/role/technology first come to exist, and how did it get to today" (e.g.
  "when was the sysadmin role founded" → 1950s computer operators → 1969 UNIX → 1980s the job title appears →
  today's DevOps/SRE). No code example or figure alongside the timeline — heading left, timeline right, that's
  the whole slide; the concept → existing software → implementation sequence that follows is where real
  examples belong. Get the dates right — these are real historical facts appearing in front of students, not
  filler, so verify anything you're not certain of rather than guessing a plausible-sounding year. Applies to
  every module in every course deck (already built out across all of comp-051/index.html's and
  data-013/index.html's substantive modules, and comp-175/index.html's Module 1) — see any of those
  for the pattern.
- **Scatter real CLI-command slides right after the concept they implement**, not bunched at the end.
  Two-column, standard 50/50 split. The `.terminal` block is a **plain `<div class="terminal">` styled with
  `white-space: pre`** holding raw text only — no `<pre>`, no `<code>`, no `<span>` wrappers, no `#`-comment
  lines (clutter, not signal, on a slide). This is a hard requirement, not a style preference: RevealHighlight
  (loaded for syntax highlighting) auto-processes every `<pre><code>` on the page, and re-escapes any HTML
  tags nested inside it (e.g. a `<span class="prompt">`) into literal visible text. Keeping `.terminal` as a
  plain text-only div sidesteps that entirely and stays simpler to author. Only the first line of a
  backslash-wrapped multi-line command gets a `$` prefix; continuation lines are plain indented text, not a
  repeated `$`. Prefer a real cross-platform CLI (e.g. VirtualBox's `VBoxManage`) over GUI-only steps
  precisely because it's the same commands on Windows/macOS/Linux; call that out explicitly in a small note
  under the bullets rather than assuming one host OS.
- **Small aside notes go below the two-column split, not inside a column.** A caveat/context sentence that
  would otherwise sit under a `<ul>` inside one `.col` (e.g. "same command on every host OS") instead goes
  as its own `<p class="fragment note-below">` directly after the closing `</div>` of `.twocol`, full slide
  width. `.note-below` is a larger, more readable size than the old inline small-print treatment; `fragment`
  means it's click-to-reveal rather than dumped on the slide immediately with everything else.
- **GLOBAL RULE — `.note-below` (the fragment/click-to-reveal note) is for warnings and risks only, never
  plain supplementary info.** Before writing one, ask whether it's cautioning against a real mistake,
  misconception, or risk (a default password left unchanged, a rule that will hard-reject your input, a
  common "people think X but it's actually Y" mix-up, a practice that's actually counterproductive). If the
  draft note is really just restating/elaborating what the slide already shows — a fact, a definition, a
  "yes, and here's how" answer — either reframe it as an actual warning or drop it entirely; don't keep it
  just because it seems informative. A citation is not a warning either — see the next rule.
- **GLOBAL RULE — citations/sources get their own always-visible `.source-line`, never bundled into a
  `.note-below` fragment.** A source shouldn't be hidden behind a click (citations need to stay visible for
  integrity, not treated as a dramatic reveal) and shouldn't be diluted into a warning-style note. `.source-line`
  (~1.1rem, ~0.85 opacity, centered) is a plain non-fragment `<p>` placed after any `.note-below` on
  the same slide. When the software/tool being cited has a genuine public GitHub repository (verify it's
  real and actually theirs before linking — org pages like `github.com/proxmox`, `github.com/xcp-ng`, not a
  guess), link it alongside the official source rather than only the vendor site.
- **GLOBAL RULE — a figure's `.source-line` always sits directly below that figure, inside the same
  column/wrapper as the `<img>`/`<svg>` itself — never dropped after the whole `.twocol` closes, where it
  renders full-width and reads as floating in the middle of the slide, disconnected from whichever figure it
  actually credits.** This drifted inconsistently in comp-175: some figures already did it right (source
  right after the `<img>`, inside its own `.col`), others had the source-line placed after `</div>` closing
  `.twocol` — harmless for a single-figure slide (nothing else to disambiguate from), but wrong the moment a
  slide has two figures side by side, since one combined source line below both can't tell a reader which
  credit belongs to which image. Fixed instances: the Unix/Linux logos (was one combined line below both
  columns; now split into two, each directly under its own logo), the two W3Techs charts (Growth Over Time,
  Market Position), and the VMware/VirtualBox toolset logos (was after the comparison table; moved to right
  after the logo row, before the table). Applies to every deck, not just comp-175.
- **GLOBAL RULE — every figure hotlinked from the web (any `<img>` whose `src` points off-repo), and every
  table whose *data* (not just page-chrome styling) came from an external source, gets a short plain-text
  caption directly below it, on the same `.source-line` as its source, with only the source part in
  parentheses** — one paragraph, not two: `<p class="source-line">Type 1 vs. Type 2 hypervisor architecture
  (Source: <a ...>Medium</a>)</p>`, placed right after the `</table>`/`</img>` inside that element's own
  column, never after the whole `.twocol` closes (see the placement rule above — the same reasoning applies
  to tables: comp-175's "Top 5 Hypervisors" table had its source as a bare `"Source"` link floating below
  the entire two-column row, disconnected from the table it credited; fixed by moving it into the table's
  own `.col`, right after `</table>`, with a caption: `"Popular hypervisor comparison, ranked (Source: <a
  ...>virtualizationhowto.com</a>)"`). The caption itself is never wrapped in its own parentheses/brackets;
  only the trailing `(Source: ...)` is. One to a handful of words describing what the figure/table actually
  shows — not a repeat of the slide's own heading, and not the alt text verbatim (alt text is for
  accessibility, the caption is for a reader glancing at the slide). For a labeled pair of figures the
  caption also disambiguates which is which (`"apt: Debian, Ubuntu (Source: ...)"` / `"pacman: Arch Linux
  (Source: ...)"`) — see comp-175's Bash/Package-Manager "Real Examples" slides for the pattern, and the
  Agenda hypervisor diagram, Unix/Linux logos, distro grid, W3Techs charts, toolset logos, VirtualBox manual
  screenshots, password table, release-cycle chart, login screen, and Top 5 Hypervisors table for further
  examples. **A table populated entirely from course-authored content (grading breakdown, lab specs,
  policies, project schedule) needs no source line at all** — this only applies when the table's numbers/
  facts were pulled from an external source. Applies to every deck going forward. **Not retroactive to
  pre-existing hotlinked images added before this rule existed** — comp-051 alone still has roughly four
  dozen web images from before this session's citation conventions with no `.source-line` at all (not just a
  missing caption, no attribution whatsoever); per the same going-forward precedent as the bullet-length cap,
  don't mass-retrofit those without reading each slide's context first — only bring one into compliance when
  already touching that slide for another reason.
- **GLOBAL RULE — text sitting directly on a solid `fill="#FF671D"` shape uses dark text (`#1a1a1a`),
  never white; text on the dark `fill="#3a1f0a"` "highlighted concept" box (the one with the `#FF671D`
  *outline*, not fill) keeps white text as before.** These are two different, easily-confused box styles
  in this repo's diagrams and each needs the opposite text color:
  - **Solid bright fill** (`fill="#FF671D"`) — `.stat-fill` bars, a bar-chart value label, a "current item"
    box in a nav diagram — background is bright, so text must be dark. White-on-`#FF671D` is genuinely
    low-contrast (roughly 2.8:1, below WCAG AA); dark text on the same orange is close to 7:1.
  - **Dark fill with orange outline** (`fill="#3a1f0a" stroke="#FF671D"`) — the "final answer" / key-concept
    callout box used throughout (e.g. "= A Distribution", "VM Ready to Boot") — background is *dark*, so it
    still needs light text; giving this one dark text (a real mistake made and caught in this repo) makes
    it nearly invisible.
  Neither of these is the same as orange used as *text* color directly on the deck's page background
  (`.highlight`, `.term-pill`, a `.stat-label`, a timeline's "Today" marker) — that direction already has
  good contrast on its own and doesn't need either fix. Before styling any new box+text pair, check which
  of the two fills it actually uses rather than assuming. `.note-below` and `.source-line` live in
  `assets/deck-chrome.css`; `.stat-fill` (where a deck uses it, currently comp-175 only) is defined in that
  deck's own `<style>` block.
- **Definition/word-origin slides get a "Terminology" tag, as a diagonal corner ribbon at the true top-left
  of the page** (GitHub's classic "Fork me" ribbon look, not a pill badge) — pinned to the page itself like
  `.seal` is pinned top-right, not inset into whichever slide happens to be showing. A slide's own `<section>`
  can't just get `position:relative` for this: reveal.js only expands the *current* section to fill `.slides`,
  and even then its content is centered inside it, so anything absolutely-positioned inside ends up inset from
  the real corner rather than flush with it. Instead there is exactly **one** shared ribbon element, created once
  by the counter/footer `<script>` block at the bottom of the page and shown/hidden by reading the current
  slide's `data-tag` attribute on `Reveal.on('slidechanged', ...)` — the same mechanism that script already uses
  for the slide counter. To tag a slide: add `data-tag="terminology"` to its `<section>` (no wrapper markup
  needed inside the slide itself). The CSS (`.tag-ribbon-wrap` clipping box + `.tag-terminology` rotated ribbon)
  lives in `assets/deck-chrome.css`; the JS (element creation + the `tagColors` map + the `slidechanged`
  listener) lives in each deck's own footer `<script>`, right after the existing slide-counter IIFE. See
  comp-175's "Word Origin: 'Hypervisor'" slide in Module 1 for the pattern. More tag kinds reuse the same
  ribbon element — just add another `data-tag` value and a color to that script's `tagColors` map. **This
  ribbon mechanism (the CSS in `assets/deck-chrome.css` plus the JS IIFE in the footer `<script>`) is a
  GLOBAL property of every course deck** — wire it up in any deck that has the shared-chrome `<link>`, even
  before that deck has any `data-tag`-ed slides yet, so the mechanism is ready the moment a Terminology slide
  gets added.
- **GLOBAL RULE — never place two `data-tag="terminology"` slides back-to-back**, in any module, in any
  course deck. Not every term in a module needs its own Terminology slide (pick genuinely worthwhile ones,
  not an exhaustive glossary of every word used) — but whichever ones a module gets must have at least one
  regular (non-terminology) slide between any two of them, module content or otherwise. This applies across
  module boundaries too: check the slide immediately before/after a module's own boundary, not just within
  that module, before inserting one near the edge of a module's vertical stack. Verify by listing every
  `data-tag="terminology"` section's line number (`grep -n 'data-tag="terminology"'`) and confirming none
  are adjacent siblings — comp-051's Module 1 ("Algorithm") through Module 12 ("Recursion") and comp-175's
  Module 1 (ten terms: "GNU," "Bash," "Package," "Distro," "Virtualization," "Hypervisor," "Host / Guest,"
  "Virtual Machine," "Kernel," "Snapshot") already follow this; use their spacing as the reference pattern.
- **GLOBAL RULE — once a module has enough slides to support it, aim for at least 10 terminology slides**,
  not just "a handful." A module with 40+ regular slides across a concept→existing-software→implementation
  spread genuinely uses far more than 2-3 named terms worth a dedicated etymology slide — comp-175's Module 1
  went from 3 to 10 once every real candidate term already present in its own content (kernel, GNU, bash,
  package, distro, host/guest, VM, plus the original virtualization/hypervisor/snapshot) was given one,
  rather than stopping at the first few obvious picks. This doesn't relax the quality bar from the rule
  above (still real, sourced, historically-accurate word origins tied to content the module actually
  covers, never invented or padded just to hit a count) — it only says don't under-shoot by picking 2-3 and
  calling it done when a module's own content actually supports several times that many. A short module
  (a handful of slides total) has no obligation to reach 10 — the target scales with how much the module
  actually covers, not a fixed quota applied regardless of size.
- **GLOBAL RULE — every module that contains at least one `data-tag="terminology"` slide gets a "Module N:
  Terminology" recap slide**, and that slide's term list is **built automatically at page load, not
  hand-authored**. Every `data-tag="terminology"` slide must also carry `data-term="..."` (the bare term
  itself, decoupled from whatever the slide's own `<h4>` says, e.g. `<section data-tag="terminology"
  data-term="Hypervisor">`). The recap slide itself is just a shell, **no `<h4>` title** — just the terms
  themselves fill the slide: `<section class="term-recap"><div class="term-pill-container"></div></section>`.
  Nothing inside `.term-pill-container` is written by hand. A third IIFE in each deck's footer `<script>`
  (right after the counter and ribbon-toggle
  ones, inside the same `Reveal.initialize().then(...)`) runs once on page load: it walks every
  `.reveal > .slides > section[id^="module-"]` to get module order, collects every `[data-tag="terminology"][data-term]`
  slide's term + which module it lives in (via `.closest('section[id^="module-"]')`), then for each
  `.term-recap` slide appends a `<span>` per term whose module comes at or before that recap's own module —
  `.term-pill` (orange, highlighted) if the term's module *is* this recap's module, `.term-pill-muted`
  (gray) if it's from an earlier one. **Only the current module's own terms are ever highlighted; every
  other term shown is muted, no other color distinction is drawn.** A module with no earlier terms (e.g.
  Module 1) ends up with only `.term-pill` entries, nothing muted — that falls out of the algorithm on its
  own, not a special case to author.
  **GLOBAL RULE — size varies independently of that color tier, via a `.w1`/`.w2`/`.w3` modifier class
  (smallest to largest) assigned per term by a deterministic hash of the term string** (`weightClass()` in
  the same IIFE), so the slide genuinely reads as a word cloud rather than a flat list of same-size
  highlighted words. Without this, a module's *own* terms (the common case — nothing has scrolled off into
  the muted tier yet, especially true for a module's first-ever recap) all shared one identical `.term-pill`
  font-size, so the "cloud" was really just a uniform row of orange text — this was caught and fixed after
  comp-175's Module 1 recap (all 10 of its own terms, nothing muted yet) rendered exactly that way. The hash
  is deterministic (not `Math.random()`) so a term's size stays stable across every recap slide it appears
  on and across page reloads, without hand-authoring a weight per term. Placement: **the module's own last
  slide**, appended as the final vertical
  sub-slide right before that module's wrapper `</section>` closes. In a module that already ends on a "Key
  Terms" word-cloud slide, `.term-recap` **takes over that slide's own position** instead of sitting next to
  it — a module never has both a `.term-recap` and a static `Module N: Key Terms` word cloud at once, since
  that's exactly the duplicate this rule replaces. In a module with no such slide (comp-051 and data-013's
  modules don't have a "Key Terms"/"Looking Ahead" convention the way comp-175 does), `.term-recap` is simply
  appended as the new last slide. **If a module has zero `data-tag="terminology"` slides, do not add a
  `.term-recap` section for it** — conditional per module, not a blanket requirement like the word cloud;
  such a module keeps whatever it already had (a static word cloud, or nothing) unchanged.
  **This is a GLOBAL RULE applying to every module, in every Fall 2026 course deck** (comp-051, comp-175,
  data-013) — the three-IIFE footer script (counter, ribbon-toggle, term-recap auto-build) should be wired up
  in every one of them regardless of whether that specific deck currently has any tagged slides, so the
  mechanism is a no-op until a module earns a slide, not something to retrofit later. As of this writing
  comp-051 has 11 tagged modules (Module 1 "Algorithm" through Module 12 "Recursion," skipping Module 9) each
  with its own `.term-recap`, comp-175 has one (Module 1, ten terms), and
  data-013 has zero tagged slides and therefore zero `.term-recap` sections — its footer script is still
  wired up and ready.
- **Real product screenshots are welcome alongside hand-drawn SVGs, as their own slides.** When an official
  manual has a genuinely useful figure (e.g. `virtualbox.org/manual`'s VM-creation wizard screenshots, its
  component-architecture diagram), embed it directly (`<img src="https://...">`, hotlinked, not downloaded
  into the repo) as the right-hand `.col` of a two-column slide, with a small `Source: <a ...>` credit line
  underneath. These are additional slides alongside the concept/software/implementation ones, not
  replacements for the hand-drawn diagrams.
- **GLOBAL RULE — whenever two figures are shown side by side (a left/right image pair, or a same-row
  logo grid), normalize their containers to identical width and height** so the pair reads as a matched
  set rather than drifting apart because each image has its own native aspect ratio. Sizing each image by
  only one dimension (`width:110px;height:auto`, or `height:26px;width:auto`) looks fine when both images
  happen to share an aspect ratio, but silently mismatches the moment they don't (a circular icon vs. a
  wide wordmark logo, a 4:3 screenshot vs. a 16:9 one) — this actually happened in comp-175 (a 32px-tall
  UNIX logo next to a 44px-tall Tux, and a 110px-wide Ubuntu icon next to an equally-110px-wide but much
  shorter VirtualBox wordmark). Fix: wrap each image in `<div class="fig-box" style="width:Wpx;height:Hpx;">`
  (same W/H on every box in that pair/grid) with the bare `<img>` inside, no per-image `width`/`height`
  styling of its own. `.fig-box` lives in `assets/deck-chrome.css` — `display:flex; align-items:center;
  justify-content:center;` on the box, `max-width:100%; max-height:100%; width:auto; height:auto;` on the
  img inside it, so each image scales down to fit the shared box regardless of its own aspect ratio. Applies
  to small inline logos next to a heading, a 2-up or 4-up logo grid, and full-size screenshot pairs alike
  (just pick a box size appropriate to that slide's content — a few dozen px for inline logos, ~200-230px
  tall for a screenshot pair). See comp-175's Unix/Linux, Bash Real Examples, Package Manager Real
  Examples, Main Distributions, Our Toolset, and Practical Lab: Download slides for the pattern.
  **Never put `margin: 0 auto` on `.fig-box` itself** — it's shared by every use, and on the uses where a
  `.fig-box` sits next to other content inside another flex row (a vendor logo beside its heading, e.g.
  comp-175's "Unix"/"Linux" slide), an item-level `margin:0 auto` is read as an **auto margin**, which
  consumes all the flex row's free space and shoves the box away from its sibling instead of sitting flush
  against it — this actually happened (the Unix/Tux logos drifted far from their "Unix"/"Linux" headings,
  well off from the left-aligned bullets below). Center a `.fig-box` through its *container* instead —
  `text-align:center` on a block wrapper, `justify-content:center` on a flex row, `justify-items:center` on
  a grid (see the Main Distributions 4-logo grid) — never through margin on the box itself.
- **GLOBAL RULE — a vendor/product logo shown directly beside its heading (the "logo + text" combo used for
  first-mention vendor logos) is left-aligned flush with the column's own left-aligned body text below it,
  with a tight gap between icon and heading** (`display:flex; align-items:center; justify-content:flex-start;
  gap:8px;` — `justify-content:flex-start` stated explicitly even though it's the flex default, so the
  intent is unambiguous on re-read) **— never centered floating away from the text column.** A centered or
  drifted logo+heading row reads as visually disconnected from the bullets underneath it, which are always
  left-aligned per `.twocol`'s own `text-align:left`. This is usually a symptom of the `.fig-box` auto-margin
  mistake above, but keep both rules in mind: even with `.fig-box` fixed, don't add centering back on
  purpose for this pattern specifically.
- **GLOBAL RULE — the first time a named vendor/product (Linux, Unix, Ubuntu, VMware, VirtualBox,
  Windows, macOS, etc.) is formally introduced in a module, put its real logo next to that first
  mention.** "Formally introduced" means the slide that actually defines/contrasts/compares it (a
  concept slide, a toolset/comparison slide) — not every passing text mention afterward; once a term has
  its logo on its introducing slide, later mentions in that module don't need it repeated. Verify the logo
  actually loads as a real image before using it (Wikipedia/Wikimedia Commons infobox logos are usually the
  easiest reliable source; vendor sites work too if directly hotlinkable), size it modestly (small, inline
  next to the heading it labels — `height:26-44px` alongside an `<h4>`, or centered above a comparison table
  — never a huge hero image), and credit it in a `.source-line`. If a slide is bullets-vs-bullets already
  contrasting two named things (e.g. "Unix" left / "Linux" right), put each one's own logo next to its own
  heading, one per side. Applies to every course deck — comp-175's "Unix"/"Linux" and "Our Toolset: VMware
  & VirtualBox" slides are the reference examples; comp-051 currently has no branded vendor/product
  mentions to apply this to (it's language/concept-focused, not tool-focused), so there's nothing to add
  there yet — revisit if that changes.
- **Close a module with a real hands-on lab sequence**, not a recap slide: download → create/configure →
  install → verify (a CLI-verify slide showing the actual check commands), immediately followed by a
  deliverables/checklist slide, then the module's word-cloud slide (below), then the "Looking Ahead"
  transition into the next module.
- **The second-to-last slide of every module is a word cloud** of the terminology introduced in that
  module — full-slide (not two-column), just an `<h4>` title (`Module N: Key Terms`) and the cloud. Build
  it with a small `word_cloud_svg(terms)` helper: `terms` is a list of `(word, weight)` pairs, weight 1-3
  driving font size (3 = largest/most central, 1 = smallest); flow the words left-to-right into rows sized
  to the slide width, centering each row, and pick weight-3 terms in UOP orange bold, weight-2 in light
  gray, weight-1 in muted gray. This is a hand-rolled layout (no external word-cloud library), so keep it
  to roughly 20-25 terms per module — more than that gets cluttered at slide scale. Always the second-to-last
  slide, immediately before "Looking Ahead," regardless of how the rest of the module is organized.
  **Superseded by `.term-recap` in any module that has one** (see the Terminology-recap GLOBAL RULE below):
  once a module has at least one `data-tag="terminology"` slide, its auto-built `.term-recap` slide takes
  over this exact position and role — same visual language (weighted plain-text terms, orange/gray, flowed
  centered rows), just populated automatically instead of hand-listed, and it fully replaces the static
  word-cloud slide rather than sitting alongside it as a duplicate. Modules with zero `data-tag="terminology"`
  slides keep the plain hand-built `word_cloud_svg` word cloud exactly as described above — this only changes
  once a module actually has terminology-tagged content.
- **Graded assignment slides (Lab-N / Homework-N) get an anchor id** — `<section id="lab-N">` / `<section
  id="homework-N">` — and the schedule/TOC table links to that id directly (`./#/lab-N`), the same pattern
  already used for `./#/module-N`. Only add the schedule-table link once the target anchor actually exists;
  for assignment numbers not built yet, note the planned due date as plain text (or in an HTML comment) so
  the page never ships a dead link. Every assignment slide states, explicitly, not just "see syllabus": the
  point value, the exact due date/time (with timezone), where to submit, the group-work policy, and the AI
  policy (AI use allowed but must be disclosed per-part, distinguishing what was and wasn't AI-assisted) —
  as `<p class="fragment note-below">` lines below the two-column split, not folded into the bullet list.
  When the assignment isn't built yet, use the standard scaffold instead of inventing values: `<h2>Lab
  N</h2>`, `<h3>TBD</h3>`, then two `note-below` fragments — one with `Points: TBD. Due: TBD (Pacific
  time).`, one with the standing default policy text (`Submit via Canvas. Groups OK, but by submitting
  you're confirming you personally understand the work. AI is fine to use, but clearly state which parts
  used AI and which parts you did without it.`) — see `comp-051/index.html`'s `lab-1`..`lab-7` or
  `data-013/index.html`'s `lab-1`..`lab-6` for the pattern. Only the point value and due date are
  actually unknown; the policy sentence is the repo's real standing default, not a guess, so state it
  outright rather than marking it TBD too.
- **GLOBAL RULE — schedule/TOC tables link to `#module-N`, never to a date-specific anchor.** A specific
  calendar date (`id="Aug27"`, `id="sept-3"`, `id="oct-13"`, etc.) is only valid for the one semester it was
  computed for — the moment the class meets on a different date next term, every link built on it is wrong
  and needs another mass rename (comp-051 alone needed 25 of these renamed once already, see the Fall 2026
  semester calendar section above). `#module-N` doesn't have that problem: the module number is stable
  across semesters even when the calendar underneath it isn't. So: don't give individual day/date slides
  their own `id`; the module wrapper's `id="module-N"` is the only anchor the schedule table should ever
  link to, and it already resolves to that module's first slide (which, per the chronological-motivation
  rule above, is always the timeline slide). Applies to every module in every course deck — comp-051's day
  anchors (`Aug27`, `sept-3`, `oct-13`, `finalsPrep`, …) have already been removed and its TOC repointed at
  `#module-N`; data-013 and comp-175 never had date anchors to begin with.

## Standardizing chrome across decks

Every deck's fixed-position chrome (seal, quick-links footer, counter) should read the same way across
courses, not just follow the same *structural* pattern. Current canonical link order, left to right:
**TOC → Email → Office Hours (span) → Syllabus → [course-specific docs/tools, e.g. a `.docx` mirror or an
external compiler] → Zoom → Canvas → Updated (always last)**. `comp-051/index.html`,
`comp-175/index.html`, and `data-013/index.html` all follow this order as of Fall 2026 — copy
whichever is closest to the new deck's link set rather than re-deriving the order. Internal same-page
anchors (TOC, Syllabus when it's an in-deck `id="syllabus"` section) use `target="_self"`; genuinely
external links (Canvas, Zoom, a `.docx` download, a third-party compiler) keep `target="_blank"
rel="noopener"`.

**Shared CSS file:** the actual chrome rules (`.seal`, `.quick-links`, `.footer-link`/`.footer-link:hover`,
`.highlight`, and the `.slides { width: 90% !important; }` override) live in one place, `assets/deck-chrome.css`
at the repo root, not copy-pasted per deck. Every course deck links to it with a relative path from its own
folder: `<link rel="stylesheet" href="../assets/deck-chrome.css">`, placed after the reveal.js/theme/plugin
CDN `<link>` tags and before the deck's own `<style>` block, so deck-specific rules can still override it if a
deck ever genuinely needs to (none currently do). Canonical values baked into that file: seal `width:120px;
top:18px; right:18px; opacity:0.92`; footer-link `color:#aaa; font-size:0.82rem; padding:4px 10px;
background:rgba(0,0,0,0.25)` — deliberately subtle/low-contrast against the page rather than a bright
attention-grabbing pill, since it's chrome that should recede, not compete with slide content; highlight
`color:#bf4a12; font-weight:bold` plus the yellow-tinted background/padding/border-radius/outline (this is
the repo's actual `.highlight` treatment — note it doesn't match the UOP-orange-only wording above; the
merged bf4a12-plus-yellow-highlight style is what's actually in use and is the one to keep matching). Markup
in each deck should use `class="seal"` on the seal `<img>` (no wrapping `<div>` or inline `style` needed) and
`class="quick-links"` / `class="footer-link"` on the footer container and each link/span inside it, not inline
`style="..."` attributes repeated per element — inline styles on this chrome silently drift out of sync
between decks over time (this happened: comp-051 was on `height:100px` while comp-175/data-013 were on
`width:120px` before this was consolidated). When adding a **new** Fall 2026 deck, link the shared file and
use the class-based markup from the start rather than inlining chrome styles again.

**Fall 2026 Canvas course shells** (use these exact course IDs for every Canvas link in a deck — the
top quick-link "Canvas" pill, any in-deck "Syllabus" link that points at Canvas's syllabus page, and
anywhere else a course-specific Canvas URL is needed — don't reuse an older/different course ID left
over from a prior semester):

| Course | Canvas URL |
|---|---|
| COMP-051 | https://pacific.instructure.com/courses/148497 |
| COMP-175 | https://pacific.instructure.com/courses/146243 |
| DATA-013 | https://pacific.instructure.com/courses/148388 |

Office hours for Fall 2026, all three courses: **Tuesday, Thursday 2:00–3:00 PM, CTC 117.**

Module-opening slides across all decks use the same two-line heading, not a single combined line:
`<h2>Module N</h2>` followed by `<h3>Title</h3>` (title only, no "Module N -" prefix repeated in the h3).
Applies to the syllabus's own module slide too when syllabus content is wrapped as `<section
id="module-N">` per the vertical-stack convention above (e.g. `<h2>Module 17</h2>` / `<h3>Syllabus</h3>`).

## Validating a deck

`scripts/validate_deck.py` (`pip install html5lib lxml` once) checks a deck's `<section>`/`<div>` tag
balance, does a full HTML5 structural parse (catches things a simple tag-count misses, like a stray
orphaned closing tag that silently truncates the slide tree, or unescaped `<`/`>` in a raw code sample
being misread as a bogus tag — both have been found this way in this repo already, invisibly broken on
the live site for a while before being caught), and reports bullet-length/em-dash/bare-URL/Mermaid/chrome
status. Run it after any structural edit (module restructuring, moving slides between sections, bulk
find-and-replace across a 10k+-line deck) before considering the change done:

```
python scripts/validate_deck.py comp-051/index.html comp-175/index.html data-013/index.html
```

Exit code is non-zero only on real structural errors; bullet-length/em-dash/bare-URL counts are printed
for awareness but don't fail the run (see the bullet-length policy above — those are advisory, not
blocking).

## Fall 2026 semester calendar

Official University of the Pacific dates for Fall 2026, Semester Programs (covers Benerd College, College
of the Pacific, Conservatory of Music, Eberhardt School of Business, School of Engineering and Computer
Science, and Pre-Pharm) — source: [Academic Calendars 2026-2027 PDF](https://catalog.pacific.edu/uop/generalinformation/academiccalendar/academiccalendar.pdf).
Use these, not a prior year's dates, whenever building or auditing a Fall 2026 course deck's schedule table:

| Description | Date(s) |
|---|---|
| Classes Begin | Monday, August 24 |
| Labor Day (holiday, no classes) | Monday, September 7 |
| Census Date | Friday, September 18 |
| Fall Student Break (no classes) | Friday, October 2 |
| Last Day to Withdraw | Friday, October 30 |
| Thanksgiving Break | Wednesday–Friday, November 25–27 |
| Classes Resume | Monday, November 30 |
| Classes End | Friday, December 4 |
| Final Examination Period | Monday–Friday, December 7–11 |
| Deadline for Faculty to Submit Final Grades | Tuesday, December 15 |

For a **Tuesday/Thursday** course starting the week of Aug 24, the correct weekly meeting dates are:

| Week | Tue | Thu | Notes |
|---|---|---|---|
| 1 | Aug 25 | Aug 27 | |
| 2 | Sep 1 | Sep 3 | |
| 3 | Sep 8 | Sep 10 | |
| 4 | Sep 15 | Sep 17 | |
| 5 | Sep 22 | Sep 24 | |
| 6 | Sep 29 | Oct 1 | |
| 7 | Oct 6 | Oct 8 | |
| 8 | Oct 13 | Oct 15 | |
| 9 | Oct 20 | Oct 22 | |
| 10 | Oct 27 | Oct 29 | |
| 11 | Nov 3 | Nov 5 | |
| 12 | Nov 10 | Nov 12 | |
| 13 | Nov 17 | Nov 19 | |
| 14 | Nov 24 | *(no class)* | Thanksgiving Break Nov 25–27 falls on the Thursday |
| 15 | Dec 1 | Dec 3 | |
| 16 | *(no regular class — classes end Dec 4)* | | Final exam scheduled within Dec 7–11 per the registrar's grid |

A **Monday/Wednesday** course instead runs Aug 24/26, Aug 31/Sep 2, Sep 8 (Sep 7 Labor Day Monday makes that
week Wed-only), … — derive similarly by shifting from Aug 24, not by reusing a prior semester's dates.

## Spring 2026 semester calendar

Official University of the Pacific dates for Spring 2026, Semester Programs (same program group as the Fall
2026 table above) — source: [2025-26 Semester Programs academic calendar](https://catalog.pacific.edu/previouscatalogs/2025-26/stocktongeneral/academiccalendar/).
Needed when shifting/importing a prior Spring course's content (e.g. a Canvas course-copy date shift) into a
Fall 2026 course, or when auditing a deck that still carries leftover Spring dates:

| Description | Date(s) |
|---|---|
| Classes Begin | Monday, January 12 |
| Martin Luther King, Jr. Day (holiday, no classes) | Monday, January 19 |
| Census Date | Friday, February 6 |
| Presidents' Day (holiday, no classes) | Monday, February 16 |
| Spring Break | Monday–Friday, March 9–13 |
| Last Day to Withdraw | Friday, March 27 |
| Classes End | Tuesday, April 28 |
| Final Examination Period | Thursday, April 30 – Wednesday, May 6 |
| Commencement (Stockton) | Saturday, May 9 |

**Watch out for McGeorge School of Law's calendar** — `pacific.edu` publishes a *separate* academic calendar
just for McGeorge (different program, different dates: e.g. its Spring 2026 term begins the same Jan 12 by
coincidence, but its Fall term, holidays, and finals period don't match the Semester Programs table above at
all). A search for "University of the Pacific academic calendar" surfaces both; confirm any fetched PDF/page
is explicitly for Semester Programs (the group covering Benerd College, College of the Pacific, Conservatory
of Music, Eberhardt School of Business, School of Engineering and Computer Science, School of Health
Sciences, Pre-Pharm) before using its dates — not the McGeorge-specific one.

## Reusable prompts (course-independent)

Prompt patterns worth reusing as-is (with the bracketed parts swapped) for any course, any semester:

- **New semester, update the landing page:**
  "In Fall/Spring <YEAR> I'm teaching <COURSE 1>, <COURSE 2>, ... — update the existing folder or create a
  new one for each, with a table of contents." → triggers the root `index.html` Teaching/Past split plus,
  for any course with no folder yet, a new reveal.js skeleton (see [Conventions](#conventions-for-a-newupdated-course-deck)).
- **New course, no material yet — reuse a real source instead of inventing content:**
  "For <COURSE>, go through <URL to a public course page / prior offering> and reuse as much as possible.
  Do not reuse <specific tech, e.g. AWS/cloud> — we'll use <replacement, e.g. local VM>. Also add syllabus
  slides following that example." → fetch the source, keep description/objectives/grading/schedule/lab
  structure, swap out only the named tech, and add a syllabus vertical stack.
- **Merging in a second source (e.g. a colleague's syllabus doc):**
  "I added another syllabus from a colleague in the <COURSE> folder, reuse as much as useful." → read it
  (see the `.docx` note above), and where it conflicts with what's already there (e.g. a different grading
  breakdown), ask which one to use rather than silently overwriting — the rest (institutional policy
  boilerplate: Honor Code, accommodations, recording/nondiscrimination notices, program outcomes) is
  usually safe to fold in without asking, minus the other instructor's personal details.
- **Quick-link footer:**
  "Add a link to <Canvas/other resource URL> in the page footer for <COURSE>." → fixed-position pill link,
  bottom-left, next to any existing ones (see Conventions above).
- **Readability pass:**
  "Increase font size and slide space used" → bump the deck's base `section`/`li`/`table`/`code` font sizes
  and any small inline `rem` overrides in syllabus-style content blocks; widen constrained-width tables.
- **After any of the above:** if the change introduces a pattern that isn't course-specific, add it to the
  Conventions section here rather than letting it live only in one course's HTML comments.

## Deployment

`.github/workflows/static.yml` deploys the **entire repository** to GitHub Pages on every push to `main`
(via `actions/upload-pages-artifact` with `path: '.'`). There is no CI build/test/lint step — anything
pushed to `main` goes live as-is, so verify HTML/links locally (e.g. open the file directly in a browser)
before pushing.
