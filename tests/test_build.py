"""Tests for scripts/build.py (no network, no repo pollution)."""
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts import build  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "content"
SITE_URL = "https://example.org/base/"


class TempDirMixin:
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ai-model-news-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def build_fixtures(self, content=FIXTURES):
        out = self.tmp / "dist"
        posts = build.build(content, out, SITE_URL, "2026-09-05")
        return out, posts


class ParsePostTests(TempDirMixin, unittest.TestCase):
    def test_parse_post_ok(self):
        post = build.parse_post(FIXTURES / "sample-a.md")
        self.assertEqual(post["model_id"], "meta-llama/Llama-4-Scout-17B-16E-Instruct")
        self.assertEqual(post["likes"], 12873)
        self.assertEqual(post["tags"], ["llama", "instruct", "multimodal", "transformers"])
        self.assertEqual(post["slug"], "meta-llama__Llama-4-Scout-17B-16E-Instruct")
        self.assertTrue(post["body"].startswith("# Llama 4 Scout"))

    def test_parse_post_boundary(self):
        post = build.parse_post(FIXTURES / "sample-c.md")
        self.assertEqual(post["params"], "")
        self.assertEqual(post["created_at"], "")
        self.assertEqual(post["tags"], [])

    def test_parse_post_bad(self):
        cases = {
            "no-open.md": 'model_id: "a/b"\n---\nbody',
            "no-close.md": '---\nmodel_id: "a/b"\n',
            "bad-json.md": "---\nmodel_id: a/b\n---\n",
            "missing-key.md": '---\nmodel_id: "a/b"\n---\n',
        }
        good = build.parse_post(FIXTURES / "sample-a.md")
        for name, text in cases.items():
            with self.subTest(name):
                p = self.tmp / name
                p.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    build.parse_post(p)
        # wrong type: likes as string
        lines = ["---"]
        for k in build.REQUIRED_KEYS:
            v = "12" if k == "likes" else good[k]
            import json
            lines.append(f"{k}: {json.dumps(v)}")
        lines.append("---")
        p = self.tmp / "wrong-type.md"
        p.write_text("\n".join(lines), encoding="utf-8")
        with self.assertRaises(ValueError):
            build.parse_post(p)


class MarkdownTests(unittest.TestCase):
    def test_headings_bullets_paragraphs(self):
        out = build.markdown_to_html("# T1\n## T2\n### T3\n\npara one\nstill one\n\n- a\n- b\n\nafter")
        self.assertIn("<h1>T1</h1>", out)
        self.assertIn("<h2>T2</h2>", out)
        self.assertIn("<h3>T3</h3>", out)
        self.assertIn("<p>para one still one</p>", out)
        self.assertIn("<ul>\n<li>a</li>\n<li>b</li>\n</ul>", out)
        self.assertIn("<p>after</p>", out)

    def test_inline_markup(self):
        out = build.markdown_to_html("see [docs](https://x.y/z) and **bold** and `code<b>`")
        self.assertIn('<a href="https://x.y/z">docs</a>', out)
        self.assertIn("<strong>bold</strong>", out)
        self.assertIn("<code>code&lt;b&gt;</code>", out)

    def test_escape_xss(self):
        out = build.markdown_to_html('<script>alert(1)</script> [x](javascript:alert(1))')
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)
        self.assertNotIn("javascript:", out)


class SlugTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(build.slugify("org/name"), "org__name")
        self.assertEqual(build.slugify("a/b c:d.e-f"), "a__b-c-d.e-f")

    def test_format_count(self):
        self.assertEqual(build.format_count(999), "999")
        self.assertEqual(build.format_count(1234), "1.2k")
        self.assertEqual(build.format_count(3400000), "3.4M")
        self.assertEqual(build.format_count(1000), "1k")


class BuildTests(TempDirMixin, unittest.TestCase):
    def test_empty_content(self):
        empty = self.tmp / "empty"
        empty.mkdir()
        out, posts = self.build_fixtures(empty)
        self.assertEqual(posts, [])
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertIn("아직 수집된 모델이 없습니다", html)
        for name in ("feed.xml", "sitemap.xml", "robots.txt", "404.html", ".nojekyll",
                     "assets/style.css", "assets/app.js", "about/index.html"):
            self.assertTrue((out / name).exists(), name)
        ET.fromstring((out / "feed.xml").read_text(encoding="utf-8"))

    def test_missing_content_dir(self):
        out, posts = self.build_fixtures(self.tmp / "does-not-exist")
        self.assertEqual(posts, [])
        self.assertTrue((out / "index.html").exists())

    def test_index_cards(self):
        out, posts = self.build_fixtures()
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('<article class="card"'), 3)
        self.assertIn('data-task="text-generation"', html)
        self.assertIn('data-task="image-text-to-text"', html)
        self.assertIn('data-org="indie-lab"', html)
        self.assertIn('href="models/google__gemma-3-27b-it/"', html)
        self.assertIn('href="assets/style.css"', html)
        self.assertIn("12.9k", html)
        self.assertIn("3.4M", html)
        self.assertIn("&lt;beta&gt;", html)
        self.assertNotIn("<beta>", html)
        self.assertIn('<meta name="viewport"', html)
        self.assertIn('<meta name="color-scheme" content="light dark">', html)
        self.assertIn('type="application/rss+xml"', html)
        self.assertIn(f'<link rel="canonical" href="{SITE_URL}">', html)
        self.assertNotIn("아직 수집된 모델이 없습니다</p>", html.replace(' hidden', 'HIDDEN'))

    def test_detail_pages(self):
        out, posts = self.build_fixtures()
        for p in posts:
            page = out / "models" / p["slug"] / "index.html"
            self.assertTrue(page.exists(), page)
            html = page.read_text(encoding="utf-8")
            self.assertIn(f'href="{p["hf_url"]}"', html)
            self.assertIn('target="_blank" rel="noopener"', html)
            self.assertIn('href="../../assets/style.css"', html)
        c = (out / "models" / "indie-lab__tiny-tts-v2" / "index.html").read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", c)
        self.assertNotIn("<script>alert(1)", c)
        self.assertIn("<td>—</td>", c)  # empty params / created_at
        a = (out / "models" / posts[0]["slug"] / "index.html").read_text(encoding="utf-8")
        self.assertIn('rel="next"', a)
        self.assertIn(f'href="../{posts[1]["slug"]}/"', a)

    def test_feed(self):
        out, posts = self.build_fixtures()
        root = ET.fromstring((out / "feed.xml").read_text(encoding="utf-8"))
        items = root.findall("./channel/item")
        self.assertEqual(len(items), 3)
        for item in items:
            pub = item.findtext("pubDate")
            parsedate_to_datetime(pub)  # RFC-822 parse
            self.assertRegex(pub, r"^[A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2} [+-]\d{4}$")
            link = item.findtext("link")
            self.assertTrue(link.startswith(SITE_URL + "models/"))
            self.assertEqual(item.findtext("guid"), link)
            self.assertTrue(item.findtext("description"))
        self.assertIn("<h1>Gemma 3 27B</h1>", items[0].findtext("description"))
        self.assertIn("<h1>Llama 4 Scout</h1>", items[1].findtext("description"))

    def test_sitemap_and_robots(self):
        out, posts = self.build_fixtures()
        root = ET.fromstring((out / "sitemap.xml").read_text(encoding="utf-8"))
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [u.text for u in root.findall("./s:url/s:loc", ns)]
        self.assertEqual(len(locs), 2 + len(posts))
        self.assertIn(SITE_URL, locs)
        self.assertIn(SITE_URL + "about/", locs)
        robots = (out / "robots.txt").read_text(encoding="utf-8")
        self.assertIn(f"Sitemap: {SITE_URL}sitemap.xml", robots)

    def test_sort_order(self):
        out, posts = self.build_fixtures()
        ids = [p["model_id"] for p in posts]
        # 2026-09-04: gemma (20481 likes) > llama (12873); then 2026-08-30 tiny-tts
        self.assertEqual(ids, ["google/gemma-3-27b-it",
                               "meta-llama/Llama-4-Scout-17B-16E-Instruct",
                               "indie-lab/tiny-tts:v2"])
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertLess(html.index("google__gemma-3-27b-it"), html.index("meta-llama__Llama-4"))
        self.assertLess(html.index("meta-llama__Llama-4"), html.index("indie-lab__tiny-tts-v2"))

    def test_cli(self):
        out = self.tmp / "cli"
        rc = build.main(["--content-dir", str(FIXTURES), "--out", str(out),
                         "--site-url", SITE_URL, "--build-date", "2026-09-05"])
        self.assertEqual(rc, 0)
        self.assertTrue((out / "index.html").exists())
        self.assertEqual(build.main(["--content-dir", str(FIXTURES), "--out", str(out),
                                     "--build-date", "bad"]), 1)


if __name__ == "__main__":
    unittest.main()
