# Agentic System Notes Portal Design

## Purpose

Replace the generated repository index at the GitHub Pages root with a minimal table of contents for the public HTML notes. A first-time visitor should be able to scan the full collection and open a useful note immediately.

The portal is an index, not a promotional landing page. It will not add search, filtering, imagery, cards, animation, or new content routes.

## Content and Reading Order

The page will contain:

1. A compact masthead with the title `Agentic System Notes` and one sentence describing the collection.
2. A numbered list containing every current note.
3. A small footer linking to the GitHub repository.

Each note entry will include:

- its full title;
- a one-sentence description derived from the note;
- a concise topic label; and
- its most recent Git commit date, displayed as `Updated Oct 6, 2026`.

The five notes will be arranged as a deliberate reading path, beginning with foundational evidence architecture and moving through publication governance, evidence placement, deterministic baselines, and interoperable semantics.

## Visual Design

The portal will extend the established visual language of the notes:

- light-gray paper background;
- dark navy text;
- restrained orange accent;
- serif display headings; and
- sans-serif metadata and body copy.

The desktop layout will use a quiet editorial grid that aligns sequence numbers, titles, and metadata. On narrow screens, each entry will stack without losing reading order. The interface will avoid decorative imagery and oversized introductory content.

Hover and keyboard-focus states will make the linked entries clear without introducing animation. Main text will remain at least 16px, metadata will remain readable, and the page will support browser text enlargement without overlap or horizontal scrolling.

## Technical Architecture

The portal will be a self-contained root `index.html` using semantic HTML and embedded CSS. It will have no JavaScript, framework, package dependency, build step, or externally hosted asset.

Links to the existing notes will be relative to the repository root so they work both locally and under the GitHub Pages project path. Existing note files and URLs will remain unchanged.

The document head will include an accurate title, description, viewport configuration, canonical URL, and an embedded SVG favicon. No social-preview image will be added.

Updated dates will be taken from the latest commit affecting each note's `index.html` at implementation time and written into the static portal. When a note changes in the future, its displayed date should be updated in the same change.

## Failure Behavior

The portal has no client-side data loading or runtime dependency, so it does not require loading, empty, or retry states. If a note is moved or removed, link verification should fail before publication rather than presenting a custom runtime error.

## Verification

Implementation is complete when:

- all five note entries are present and link to their existing pages;
- each displayed title, description, label, and updated date matches its source;
- the root document has valid metadata and a favicon;
- keyboard focus is visible and the page is usable without a mouse;
- desktop and mobile layouts remain readable with no unintended horizontal overflow;
- the page remains usable at 200% browser text enlargement; and
- the published GitHub Pages root serves the new portal while existing note URLs continue to return successfully.

