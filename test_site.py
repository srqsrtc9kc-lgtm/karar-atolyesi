from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTICLE_DIR = ROOT / "rehberler"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.titles: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.titles.append(data.strip())


class SiteTests(unittest.TestCase):
    def test_exactly_ten_substantive_guides(self) -> None:
        articles = sorted(ARTICLE_DIR.glob("*.html"))
        self.assertEqual(len(articles), 10)
        for article in articles:
            raw = article.read_text(encoding="utf-8")
            visible = re.sub(r"<[^>]+>", " ", raw)
            words = re.findall(r"\b[\wÇĞİÖŞÜçğıöşü'-]+\b", visible)
            self.assertGreaterEqual(len(words), 350, f"{article.name} yeterince kapsamlı değil")

    def test_internal_links_resolve(self) -> None:
        for page in list(ROOT.glob("*.html")) + list(ARTICLE_DIR.glob("*.html")):
            parser = LinkParser()
            parser.feed(page.read_text(encoding="utf-8"))
            for href in parser.hrefs:
                if href.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = (page.parent / href.split("#", 1)[0]).resolve()
                self.assertTrue(target.exists(), f"Bozuk bağlantı: {page.name} -> {href}")

    def test_titles_are_unique(self) -> None:
        titles: list[str] = []
        for page in list(ROOT.glob("*.html")) + list(ARTICLE_DIR.glob("*.html")):
            parser = LinkParser()
            parser.feed(page.read_text(encoding="utf-8"))
            self.assertEqual(len(parser.titles), 1, page.name)
            titles.extend(parser.titles)
        self.assertEqual(len(titles), len(set(titles)))

    def test_no_secrets_or_premature_affiliate_claim(self) -> None:
        forbidden = [
            r"@gmail\.com",
            r"password\s*[:=]",
            r"credential\s*[:=]",
            r"secret\s*[:=]",
            r"api[_-]?key\s*[:=]",
            r"BEGIN [A-Z ]*PRIVATE KEY",
        ]
        candidates = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts]
        for path in candidates:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in forbidden:
                self.assertIsNone(re.search(pattern, text, re.IGNORECASE), f"Yasak veri: {path.name}")
            premature_claim = "Amazon " + "Gelir Ortağı olarak"
            self.assertNotIn(premature_claim, text, f"Erken ortaklık beyanı: {path.name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
