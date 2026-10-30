#!/usr/bin/env python3
"""Focused release checks for the public bilingual handbook."""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_site import ROOT, LOCALES, SOURCES, SITE_URL, home_page, page, public_pdf_links, safe_url, markdown_to_html


class Document(HTMLParser):
    def __init__(self, value: str):
        super().__init__()
        self.ids, self.links, self.resources = [], [], []
        self.section_labels, self.downloads = [], []
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
            if "download" in attrs:
                self.downloads.append(attrs.get("href", ""))
        if tag == "section" and "aria-labelledby" in attrs:
            self.section_labels.append(attrs["aria-labelledby"])
        if tag in ("img", "script"):
            self.resources.append(attrs.get("src", ""))
        if tag == "link" and attrs.get("rel") in ("icon", "stylesheet"):
            self.resources.append(attrs.get("href", ""))


class ReleaseTests(unittest.TestCase):
    def test_pages_match_canonical_manuscripts_and_current_downloads(self):
        for locale, (stem, _) in LOCALES.items():
            manuscript = (ROOT / SOURCES[locale]).read_text(encoding="utf-8")
            self.assertEqual(len(markdown_to_html(manuscript, locale)[1]), 27)
            for name, expected in ((stem + ".html", page(manuscript, locale)),
                                   ("english.html" if locale == "en" else "index.html", home_page(manuscript, locale))):
                content = (ROOT / name).read_text(encoding="utf-8")
                self.assertEqual(content, expected)
                self.assertIn("v1.1", content)
                self.assertIn(f'downloads/ai-butler-handbook_v1.1_{locale}.pdf', content)
                self.assertNotRegex(content, r"noindex|v1\.0|local-preview|/Users/|file://|本機修訂稿|local revision")
                self.assertIn('rel="canonical"', content)
                self.assertNotRegex(content, r"(?:@import|url\s*\(|goatcounter|https://gc\.)")
        self.assertEqual((ROOT / "linkedin.html").read_bytes(), (ROOT / "english.html").read_bytes())

    def test_every_live_local_link_resource_and_anchor(self):
        for name in ("index.html", "english.html", "linkedin.html", "read.html", "read-en.html"):
            content = (ROOT / name).read_text(encoding="utf-8")
            doc = Document(content)
            self.assertEqual(len(doc.ids), len(set(doc.ids)))
            for resource in doc.resources:
                self.assertFalse(urlsplit(resource).scheme)
                self.assertFalse(resource.startswith("//"))
            for url in doc.links + doc.resources:
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc:
                    continue
                target = (ROOT / unquote(parsed.path)).resolve() if parsed.path else ROOT / name
                self.assertTrue(target.is_relative_to(ROOT))
                self.assertTrue(target.is_file(), url)
                if parsed.fragment and target.suffix == ".html":
                    self.assertIn(unquote(parsed.fragment), Document(target.read_text(encoding="utf-8")).ids)

    def test_reader_appendices_and_interactions_preserved(self):
        for stem, _ in LOCALES.values():
            content = (ROOT / (stem + ".html")).read_text(encoding="utf-8")
            self.assertEqual(content.count('class="toc-group"'), 12)
            self.assertIn('class="chapter-number" aria-hidden="true">A</span>', content)
            self.assertIn('class="chapter-number" aria-hidden="true">D</span>', content)
            self.assertIn('src="assets/reader.js" defer', content)
        self.assertIn('prefers-reduced-motion:no-preference', (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn("負責人與期限：待確認", (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn("Owner and deadline: to confirm.", (ROOT / "english.html").read_text(encoding="utf-8"))

    def test_homepage_narrative_and_reading_entries(self):
        for name, reader, locale in (("index.html", "read.html", "zh"),
                                     ("english.html", "read-en.html", "en")):
            content = (ROOT / name).read_text(encoding="utf-8")
            doc = Document(content)
            self.assertEqual(doc.section_labels, ["worksheet-title", "questions-title",
                "route-title", "outcomes-title", "audience-title", "invitation-title"])
            self.assertGreaterEqual(doc.links.count(reader), 3)
            pdf = f"downloads/ai-butler-handbook_v1.1_{locale}.pdf"
            self.assertEqual(doc.downloads.count(pdf), 3)
            takeaways = re.search(r'<dl class="takeaways">(.*?)</dl>', content, re.S)
            self.assertIsNotNone(takeaways)
            self.assertEqual(takeaways.group(1).count("<dt>"), 4)

    def test_reject_unsafe_urls_and_escape_markup(self):
        for url in ("javascript:alert(1)", "file:///private/example", "../../../outside"):
            with self.assertRaises(ValueError):
                safe_url(url)
        with self.assertRaises(ValueError):
            safe_url("https://example.com/image.svg", image=True)
        value, _ = markdown_to_html("# Test\n## 1. Start\n<script>not executable</script>")
        self.assertNotIn("<script>", value)
        self.assertIn("&lt;script&gt;", value)

    def test_homepage_controls_are_progressive_and_local(self):
        for name in ("index.html", "english.html", "linkedin.html"):
            content = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('src="assets/home.js" defer', content)
            self.assertNotIn('sheet-focus', content)
            self.assertNotIn('aria-pressed', content)
            self.assertNotIn('<button', content)
            self.assertEqual(content.count('class="takeaway-card"'), 4)
            self.assertNotIn('book-arrive', content)
            self.assertIn('prefers-reduced-motion:no-preference', content)
            for number in (1, 2):
                self.assertIn(f'id="sheet-row-{number}"', content)
            self.assertIn('href="#worksheet-title"', content)
            self.assertNotIn('ribbon-arrive', content)

    @unittest.skipUnless(shutil.which("node"), "Interaction state checks need existing Node.js")
    def test_homepage_interaction_states(self):
        subprocess.run(["node", str(ROOT / "scripts/test_home.js")], check=True,
                       capture_output=True, text=True)

    def test_pdf_annotation_rewrite_preserves_offsets_and_fails_closed(self):
        with tempfile.TemporaryDirectory(prefix="handbook-link-test-") as directory:
            target = Path(directory) / "synthetic.pdf"
            original = b"prefix /URI (file:///" + b"example/" * 20 + b"meeting-loop-zh.svg) suffix"
            target.write_bytes(original)
            self.assertEqual(public_pdf_links(target), 1)
            public = target.read_bytes()
            self.assertEqual(len(original), len(public))
            self.assertEqual(original.index(b" suffix"), public.index(b" suffix"))
            self.assertIn((SITE_URL + "assets/meeting-loop-zh.svg").encode(), public)
            self.assertNotIn(b"file:", public)
            self.assertEqual(public_pdf_links(target), 0)
            for value in (b"/URI (file:///unknown.svg)", b"/URI (file:///meeting-loop-en.svg)"):
                target.write_bytes(value)
                before = hashlib.sha256(value).hexdigest()
                with self.assertRaises(ValueError):
                    public_pdf_links(target)
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)

    @unittest.skipUnless(shutil.which("pdfinfo"), "PDF annotation validation needs existing Poppler")
    def test_release_pdfs_have_only_public_uri_annotations(self):
        for locale in LOCALES:
            target = ROOT / f"downloads/ai-butler-handbook_v1.1_{locale}.pdf"
            urls = subprocess.run(["pdfinfo", "-url", str(target)], capture_output=True, text=True, check=True).stdout
            self.assertNotRegex(urls, r"file:|/Users/")
            self.assertIn(SITE_URL + f"assets/meeting-loop-{locale}.svg", urls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
