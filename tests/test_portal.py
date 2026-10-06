from __future__ import annotations

import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PORTAL = ROOT / "index.html"

NOTES = [
    {
        "href": "notes/evidence-architecture-for-agentic-systems/",
        "title": "Agentic Systems Need an Evidence Architecture",
        "description": (
            "Evidence architecture connects actions, authority, inputs, evaluation, "
            "and approval into a verifiable system of record."
        ),
        "topic": "Evidence architecture",
        "date": "2026-10-01",
    },
    {
        "href": "notes/ai-summary-publication-evidence/",
        "title": (
            "An AI-Generated Research Summary Passed Its Tests. "
            "Is It Ready to Publish?"
        ),
        "description": (
            "A tested AI summary is not automatically publishable; evidence, review, "
            "and release authority remain separate decisions."
        ),
        "topic": "Publication governance",
        "date": "2026-10-02",
    },
    {
        "href": "notes/automation-evidence-placement/",
        "title": "Where Should Automation Evidence Live?",
        "description": (
            "Automation needs a clear boundary between authoritative evidence, "
            "business transactions, and observability."
        ),
        "topic": "System boundaries",
        "date": "2026-10-04",
    },
    {
        "href": "notes/ai-value-beyond-deterministic-baseline/",
        "title": "When Does AI Add Value Beyond a Deterministic Baseline?",
        "description": (
            "AI should earn its place by outperforming or extending a fair "
            "deterministic baseline on the task that matters."
        ),
        "topic": "AI evaluation",
        "date": "2026-10-05",
    },
    {
        "href": "notes/interoperable-evidence-semantics-cyber-physical-systems/",
        "title": (
            "Interoperable Evidence Semantics for Distributed Cyber-Physical Systems: "
            "Applying CloudEvents, SOSA/SSN, and W3C PROV"
        ),
        "description": (
            "CloudEvents, SOSA/SSN, and W3C PROV provide complementary layers for "
            "portable events, shared meaning, and evidence lineage."
        ),
        "topic": "Interoperability",
        "date": "2026-10-06",
    },
]


def normalized_text(parts: list[str]) -> str:
    return " ".join("".join(parts).split())


class PortalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tag_counts: dict[str, int] = {}
        self.elements: list[tuple[str, dict[str, str]]] = []
        self.entries: list[dict[str, str]] = []
        self.h1 = ""
        self._entry: dict[str, str] | None = None
        self._capture: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
        self.elements.append((tag, attributes))

        classes = set(attributes.get("class", "").split())
        if tag == "li" and "note-entry" in classes:
            self._entry = {}
        elif tag == "h1":
            self._begin_capture("h1")
        elif self._entry is not None and tag == "a" and "note-link" in classes:
            self._entry["href"] = attributes.get("href", "")
            self._begin_capture("title")
        elif self._entry is not None and "note-description" in classes:
            self._begin_capture("description")
        elif self._entry is not None and "note-topic" in classes:
            self._begin_capture("topic")
        elif self._entry is not None and tag == "time":
            self._entry["date"] = attributes.get("datetime", "")
            self._begin_capture("date_text")

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        capture_tags = {
            "h1": "h1",
            "a": "title",
            "p": "description",
            "span": "topic",
            "time": "date_text",
        }
        if self._capture == capture_tags.get(tag):
            value = normalized_text(self._text)
            if self._capture == "h1":
                self.h1 = value
            elif self._entry is not None:
                self._entry[self._capture] = value
            self._capture = None
            self._text = []

        if tag == "li" and self._entry is not None:
            self.entries.append(self._entry)
            self._entry = None

    def _begin_capture(self, field: str) -> None:
        self._capture = field
        self._text = []


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._inside_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title" and not self.title:
            self._inside_title = True

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.title += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False


class PortalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(PORTAL.is_file(), "root index.html should exist")
        self.source = PORTAL.read_text(encoding="utf-8")
        self.parser = PortalParser()
        self.parser.feed(self.source)

    def test_portal_contains_exact_note_inventory(self) -> None:
        actual_hrefs = [entry["href"] for entry in self.parser.entries]
        discovered_hrefs = sorted(
            f"notes/{path.parent.name}/" for path in (ROOT / "notes").glob("*/index.html")
        )

        self.assertEqual(sorted(actual_hrefs), discovered_hrefs)
        for href in actual_hrefs:
            parsed = urlsplit(href)
            self.assertFalse(parsed.scheme or parsed.netloc or href.startswith("/"))
            self.assertTrue(href.endswith("/"))
            self.assertTrue((ROOT / href / "index.html").is_file())

    def test_note_titles_and_reading_order(self) -> None:
        self.assertEqual(
            [entry["title"] for entry in self.parser.entries],
            [note["title"] for note in NOTES],
        )

    def test_note_metadata(self) -> None:
        self.assertEqual(
            [(entry["topic"], entry["date"]) for entry in self.parser.entries],
            [(note["topic"], note["date"]) for note in NOTES],
        )

        for note, entry in zip(NOTES, self.parser.entries):
            note_path = f"{note['href']}index.html"
            git_date = subprocess.run(
                ["git", "log", "-1", "--format=%cs", "--", note_path],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            self.assertEqual(entry["date"], git_date)

    def test_note_descriptions(self) -> None:
        self.assertEqual(
            [entry["description"] for entry in self.parser.entries],
            [note["description"] for note in NOTES],
        )

    def test_note_titles_match_source_documents(self) -> None:
        for note, entry in zip(NOTES, self.parser.entries):
            parser = TitleParser()
            parser.feed((ROOT / note["href"] / "index.html").read_text(encoding="utf-8"))
            self.assertEqual(entry["title"], normalized_text([parser.title]))

    def test_document_metadata_and_structure(self) -> None:
        self.assertEqual(self.parser.tag_counts.get("main"), 1)
        self.assertEqual(self.parser.tag_counts.get("h1"), 1)
        self.assertEqual(self.parser.tag_counts.get("ol"), 1)
        self.assertEqual(self.parser.h1, "Agentic System Notes")

        metas = [attrs for tag, attrs in self.parser.elements if tag == "meta"]
        self.assertIn(
            {
                "name": "description",
                "content": "Public architecture notes on building, reviewing, and operating agentic systems.",
            },
            metas,
        )

        links = [attrs for tag, attrs in self.parser.elements if tag == "link"]
        self.assertIn(
            {
                "rel": "canonical",
                "href": "https://andrewlyu.github.io/agentic-sys-notes/",
            },
            links,
        )
        self.assertTrue(
            any(
                "icon" in attrs.get("rel", "").split()
                and attrs.get("href", "").startswith("data:image/svg+xml")
                for attrs in links
            )
        )

        anchors = [attrs for tag, attrs in self.parser.elements if tag == "a"]
        self.assertTrue(
            any(
                attrs.get("class") == "repository-link"
                and attrs.get("href") == "https://github.com/andrewlyu/agentic-sys-notes"
                for attrs in anchors
            )
        )

    def test_runtime_dependencies_are_absent(self) -> None:
        self.assertEqual(self.parser.tag_counts.get("script", 0), 0)
        links = [attrs for tag, attrs in self.parser.elements if tag == "link"]
        self.assertFalse(any("stylesheet" in attrs.get("rel", "").split() for attrs in links))
        self.assertNotIn("fonts.googleapis.com", self.source)
        images = [attrs for tag, attrs in self.parser.elements if tag == "img"]
        self.assertFalse(
            any(attrs.get("src", "").startswith(("http://", "https://")) for attrs in images)
        )


if __name__ == "__main__":
    unittest.main()
