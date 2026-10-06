# Agentic System Notes Portal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the generated GitHub Pages root with a minimal, dated table of contents for all five public notes.

**Architecture:** Add one self-contained root `index.html` with semantic markup and embedded CSS. Add one standard-library Python contract test that parses the document, validates its note inventory and metadata, and rejects runtime dependencies; visual behavior is then checked in a local browser at desktop, mobile, and enlarged-text sizes.

**Tech Stack:** HTML5, embedded CSS, Python 3 standard library (`unittest`, `html.parser`, `pathlib`, `subprocess`), GitHub Pages

**Spec:** `docs/superpowers/specs/2026-10-06-notes-portal-design.md`

## Global Constraints

- Preserve every existing file and public note URL under `notes/`.
- Use no JavaScript, framework, package dependency, build step, or externally hosted asset.
- Keep all portal styling and the SVG favicon inside root `index.html`.
- Use relative links for notes and the established gray, navy, orange, serif, and sans-serif visual language.
- Include no search, filters, imagery, cards, animation, social-preview image, or additional route.
- Main text must be at least 16px and remain usable at 200% browser text enlargement.

## Review Focus

- GitHub Pages project paths: every relative note link must resolve when the root is served at `/agentic-sys-notes/`.
- Inventory drift: adding, removing, or renaming a directory under `notes/` must make the portal contract test fail until the index is updated.
- Metadata drift: titles and displayed update dates must match the source note and its latest Git commit.
- Dependency creep: scripts, external stylesheets, remote fonts, and external image assets must remain absent.
- Narrow and enlarged layouts: long titles must wrap without clipping, overlap, or horizontal document overflow.

---

### Task 1: Portal Content Contract

**Files:**
- Create: `tests/test_portal.py`
- Create: `index.html`

**Interfaces:**
- Consumes: existing note documents at `notes/*/index.html` and their Git last-modified dates.
- Produces: a root HTML document with one ordered-list item per note; each item contains a relative link, topic label, description, and `<time datetime="YYYY-MM-DD">Updated Mon D, YYYY</time>`.

- [ ] **Step 1: Write the failing portal contract tests**

Create `tests/test_portal.py` with a small `HTMLParser` collector and a `PortalTests(unittest.TestCase)` class containing these tests:

- `test_portal_contains_exact_note_inventory`: compare normalized portal `notes/.../` hrefs with the directories returned by `Path("notes").glob("*/index.html")`; assert each note href is relative, ends with `/`, and resolves to an existing `index.html` beneath the repository root.
- `test_note_titles_and_reading_order`: assert the linked titles appear in this exact order: `Agentic Systems Need an Evidence Architecture`; `An AI-Generated Research Summary Passed Its Tests. Is It Ready to Publish?`; `Where Should Automation Evidence Live?`; `When Does AI Add Value Beyond a Deterministic Baseline?`; `Interoperable Evidence Semantics for Distributed Cyber-Physical Systems: Applying CloudEvents, SOSA/SSN, and W3C PROV`.
- `test_note_metadata`: assert topic labels and `<time>` values are respectively `Evidence architecture` / `2026-10-01`, `Publication governance` / `2026-10-02`, `System boundaries` / `2026-10-04`, `AI evaluation` / `2026-10-05`, and `Interoperability` / `2026-10-06`; use `git log -1 --format=%cs -- <note path>` to assert each `datetime` still equals the source file's latest commit date.
- `test_note_descriptions`: assert these exact descriptions in reading order: `Evidence architecture connects actions, authority, inputs, evaluation, and approval into a verifiable system of record.`; `A tested AI summary is not automatically publishable; evidence, review, and release authority remain separate decisions.`; `Automation needs a clear boundary between authoritative evidence, business transactions, and observability.`; `AI should earn its place by outperforming or extending a fair deterministic baseline on the task that matters.`; `CloudEvents, SOSA/SSN, and W3C PROV provide complementary layers for portable events, shared meaning, and evidence lineage.`
- `test_note_titles_match_source_documents`: parse each target note and assert its `<title>` equals the portal link text after trimming whitespace.
- `test_document_metadata_and_structure`: assert one `<main>`, one `<h1>` with `Agentic System Notes`, one ordered list, a meta description, canonical URL `https://andrewlyu.github.io/agentic-sys-notes/`, repository footer link, and an embedded `data:image/svg+xml` favicon.
- `test_runtime_dependencies_are_absent`: assert there are no `<script>` tags, external stylesheet links, remote font URLs, or `http(s)` image sources.

- [ ] **Step 2: Run the tests and verify the missing portal fails**

Run: `rtk test python3 -m unittest tests/test_portal.py -v`

Expected: FAIL because root `index.html` does not exist.

- [ ] **Step 3: Create the semantic portal content**

Create `index.html` with the approved masthead, ordered list, descriptions, topic labels, exact dates above, and repository footer. Use extensionless relative note links such as `notes/evidence-architecture-for-agentic-systems/` so local and GitHub Pages routing agree.

- [ ] **Step 4: Run the content contract tests**

Run: `rtk test python3 -m unittest tests/test_portal.py -v`

Expected: PASS for inventory, reading order, titles, dates, document structure, and dependency constraints.

- [ ] **Step 5: Commit the content contract**

Run: `rtk git add index.html tests/test_portal.py && rtk git commit -m "feat: add notes portal content"`

### Task 2: Minimal Responsive Presentation

**Files:**
- Modify: `index.html`
- Modify: `tests/test_portal.py`

**Interfaces:**
- Consumes: the semantic portal structure from Task 1.
- Produces: embedded CSS tokens and responsive rules that present the same document as an editorial grid on desktop and a stacked list on narrow screens.

- [ ] **Step 1: Add failing visual-contract tests**

Add `test_visual_contract` assertions for these CSS requirements: the exact color tokens `#f5f5f5`, `#2d3142`, and `#eb6c36`; a main text base size of at least `16px`; a visible `:focus-visible` rule; a narrow-screen media query; wrapping safeguards (`overflow-wrap` or `word-break`); and no declaration that disables focus outlines without supplying a replacement.

- [ ] **Step 2: Run the visual-contract test and verify it fails**

Run: `rtk test python3 -m unittest tests.test_portal.PortalTests.test_visual_contract -v`

Expected: FAIL because the presentation tokens and responsive rules are not complete.

- [ ] **Step 3: Implement the embedded visual system**

Style the masthead and numbered list as the approved quiet editorial grid. Use system serif and sans-serif stacks, an orange top rule or link accent, generous row spacing, high-contrast text, and a mobile breakpoint that stacks sequence number, title, description, and metadata. Add restrained hover and keyboard-focus states without transitions or animation.

- [ ] **Step 4: Run the complete automated suite**

Run: `rtk test python3 -m unittest tests/test_portal.py -v`

Expected: all tests PASS.

- [ ] **Step 5: Serve and inspect the page**

Run: `rtk proxy python3 -m http.server 8000 --directory .`

Inspect `http://localhost:8000/` at approximately 1440×900 and 390×844, then repeat at 200% browser zoom. Confirm the first viewport shows the collection, all long titles wrap cleanly, focus remains visible, every row is usable by keyboard, and there is no unintended horizontal scrolling.

- [ ] **Step 6: Commit the responsive presentation**

Run: `rtk git add index.html tests/test_portal.py && rtk git commit -m "style: finish minimal notes portal"`

### Task 3: Publication Verification

**Files:**
- Verify only: `index.html`, `notes/*/index.html`

**Interfaces:**
- Consumes: the verified static portal from Tasks 1 and 2.
- Produces: a published GitHub Pages root with unchanged note URLs.

- [ ] **Step 1: Run final local checks**

Run: `rtk test python3 -m unittest tests/test_portal.py -v`

Run: `rtk git diff --check`

Expected: all tests PASS and `git diff --check` reports no errors.

- [ ] **Step 2: Publish through the repository's existing GitHub Pages flow**

Push the implementation commits to the configured `main` remote after the branch-finishing review approves them.

- [ ] **Step 3: Verify the public portal and preserved notes**

Check that `https://andrewlyu.github.io/agentic-sys-notes/` serves the new title and that each of the five existing note URLs returns HTTP 200. Confirm the displayed titles and updated dates match the locally tested index.
