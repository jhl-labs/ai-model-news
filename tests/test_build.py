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
        self.assertIn('<p class="empty" id="empty-state">', html)
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
        # 전체 카드(하이라이트/급상승 중복 포함)가 아닌 #cards 섹션 안의 카드만 카운트.
        cards_section = html[html.index('id="cards"'):]
        self.assertEqual(cards_section.count('<article class="card"'), 3)
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
        # 모델이 있으면 빈 상태 안내는 hidden 속성으로 숨겨야 한다(CSS 는 [hidden] 만 숨김).
        self.assertIn('<p class="empty" id="empty-state" hidden>', html)

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


def _make_post(model_id="org/test-1", title="Test", org="org", task="text-generation",
               license="mit", params="7B", likes=100, downloads=1000,
               discovered_at="2026-09-04", created_at="2026-09-01",
               hf_url="https://huggingface.co/org/test-1",
               tags=["t"], reason="trending"):
    return {
        "model_id": model_id, "title": title, "org": org, "task": task,
        "license": license, "params": params, "likes": likes, "downloads": downloads,
        "discovered_at": discovered_at, "created_at": created_at,
        "hf_url": hf_url, "tags": tags, "reason": reason,
        "body": "", "slug": build.slugify(model_id), "source": model_id + ".md",
    }


class HighlightSurgeTests(unittest.TestCase):
    def test_highlight_section(self):
        posts = [
            _make_post(model_id="a/new-high", likes=500, discovered_at="2026-09-04",
                        created_at="2026-09-01", reason="trending"),
            _make_post(model_id="b/new-mid", likes=300, discovered_at="2026-09-03",
                        created_at="2026-09-01", reason="trending"),
            _make_post(model_id="c/old", likes=9999, discovered_at="2026-08-01",
                        created_at="2026-06-01", reason="trending"),
        ]
        html = build.render_index(posts, SITE_URL, "2026-09-05")
        self.assertIn('aria-label="오늘의 하이라이트"', html)
        # 하이라이트 섹션은 highlight-cards 부터 다음 섹션(surge) 전까지.
        hi_start = html.index('class="highlight-cards"')
        hi_end = html.index('class="surge', hi_start)
        hi_section = html[hi_start:hi_end]
        self.assertIn("a__new-high", hi_section)
        self.assertIn("b__new-mid", hi_section)
        self.assertNotIn("c__old", hi_section)

    def test_highlight_empty_hidden(self):
        posts = [_make_post(model_id="c/old", likes=9999, discovered_at="2026-08-01",
                            created_at="2026-06-01")]
        html = build.render_index(posts, SITE_URL, "2026-09-05")
        self.assertIn("highlights hidden", html)

    def test_surge_section(self):
        posts = [
            _make_post(model_id="a/surge", likes=400, discovered_at="2026-09-04",
                        reason="surge, trending"),
            _make_post(model_id="b/normal", likes=9999, discovered_at="2026-09-04",
                        reason="trending"),
        ]
        html = build.render_index(posts, SITE_URL, "2026-09-05")
        self.assertIn('aria-label="이번 주 급상승"', html)
        # surge 섹션은 surge-cards 부터 다음 섹션(filters) 전까지.
        sg_start = html.index('class="surge-cards"')
        sg_end = html.index('class="filters', sg_start)
        sg_section = html[sg_start:sg_end]
        self.assertIn("a__surge", sg_section)
        self.assertNotIn("b__normal", sg_section)

    def test_surge_empty_hidden(self):
        posts = [_make_post(model_id="b/normal", likes=9999, reason="trending")]
        html = build.render_index(posts, SITE_URL, "2026-09-05")
        self.assertIn("surge hidden", html)

    def test_relative_date(self):
        self.assertEqual(build.relative_date("2026-09-05", "2026-09-05"), "오늘")
        self.assertEqual(build.relative_date("2026-09-04", "2026-09-05"), "1일 전")
        self.assertEqual(build.relative_date("2026-09-01", "2026-09-05"), "4일 전")
        self.assertEqual(build.relative_date("2026-09-06", "2026-09-05"), "오늘")

    def test_badges_new_from_reason(self):
        post = _make_post(reason="new, trending", created_at="2026-08-01")
        badges = build.card_badges(post, "2026-09-05")
        classes = [b[0] for b in badges]
        self.assertIn("badge-new", classes)

    def test_badges_new_inferred_from_created_at(self):
        post = _make_post(reason="trending", created_at="2026-09-01")
        badges = build.card_badges(post, "2026-09-05")
        classes = [b[0] for b in badges]
        self.assertIn("badge-new", classes)

    def test_badges_new_not_inferred_old_created(self):
        post = _make_post(reason="trending", created_at="2026-01-01")
        badges = build.card_badges(post, "2026-09-05")
        classes = [b[0] for b in badges]
        self.assertNotIn("badge-new", classes)

    def test_badges_surge(self):
        post = _make_post(reason="surge, trending")
        badges = build.card_badges(post, "2026-09-05")
        classes = [b[0] for b in badges]
        self.assertIn("badge-surge", classes)

    def test_badges_updated(self):
        post = _make_post(reason="updated, trending")
        badges = build.card_badges(post, "2026-09-05")
        classes = [b[0] for b in badges]
        self.assertIn("badge-updated", classes)

    def test_badges_empty(self):
        post = _make_post(reason="trending", created_at="2026-01-01")
        badges = build.card_badges(post, "2026-09-05")
        self.assertEqual(badges, [])

    def test_360px_stack(self):
        posts = [_make_post(discovered_at="2026-09-04", reason="surge")]
        html = build.render_index(posts, SITE_URL, "2026-09-05")
        # grid 클래스가 존재하고 1fr 기본값(미디어쿼리에서 확장)은 CSS 에서 처리.
        self.assertIn("highlight-cards", html)
        self.assertIn("surge-cards", html)
        css = (ROOT / "static" / "style.css").read_text(encoding="utf-8")
        self.assertIn("grid-template-columns: 1fr", css)


if __name__ == "__main__":
    unittest.main()
