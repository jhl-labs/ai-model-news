import datetime as dt
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from scripts import collect
from scripts.frontmatter import KEYS, parse_frontmatter, slugify

FIXTURES = Path(__file__).parent / "fixtures" / "hf"
TODAY = dt.date(2026, 9, 5)


def load_fixture(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


def fixture_fetcher(url: str) -> str:
    """Serve HF API urls from tests/fixtures/hf without network access."""
    if url.startswith(collect.HF_API + "?"):
        query = url.split("?", 1)[1]
        if "sort=trendingScore" in query:
            return load_fixture("trending.json")
        if "author=" in query:
            org = query.split("author=", 1)[1].split("&", 1)[0]
            path = FIXTURES / ("by_org_%s.json" % org)
            return path.read_text(encoding="utf-8") if path.exists() else "[]"
        return "[]"  # likes / downloads listings
    if url.startswith(collect.HF_API + "/"):
        model_id = url[len(collect.HF_API) + 1:]
        path = FIXTURES / ("detail_%s.json" % slugify(model_id))
        if path.exists():
            return path.read_text(encoding="utf-8")
        # Minimal synthetic detail for models that have no fixture.
        for m in json.loads(load_fixture("trending.json")):
            if m["id"] == model_id:
                return json.dumps(m)
        raise RuntimeError("fetch failed: %s (HTTP 404)" % url)
    if url.startswith(collect.HF_WEB + "/") and url.endswith("/raw/main/README.md"):
        model_id = url[len(collect.HF_WEB) + 1:-len("/raw/main/README.md")]
        path = FIXTURES / ("readme_%s.md" % slugify(model_id))
        return path.read_text(encoding="utf-8") if path.exists() else ""
    raise RuntimeError("unexpected url %s" % url)


def model(model_id, likes=0, downloads=0, created=None, rank=None, pipeline="text-generation", tags=None):
    m = {"id": model_id, "modelId": model_id, "likes": likes, "downloads": downloads,
         "pipeline_tag": pipeline, "tags": ["transformers"] if tags is None else tags}
    if created:
        m["createdAt"] = created + "T00:00:00.000Z"
    if rank is not None:
        m["trending_rank"] = rank
    return m


# Old enough history so that the first-run fallback is NOT used.
OLD_HISTORY = {"someone/old": {"2026-08-20": {"likes": 1, "downloads": 1}}}


class SelectFamousTests(unittest.TestCase):
    def test_trending_top30_selected_and_31st_not(self):
        cands = [model("a/top", rank=30, created="2025-01-01"), model("a/low", rank=31, created="2025-01-01")]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([(m["id"], r) for m, r in result], [("a/top", ["trending"])])

    def test_major_org_recent_release(self):
        cands = [
            model("meta-llama/New", likes=20, created="2026-08-10"),   # 26 days old, >=20 likes
            model("meta-llama/Old", likes=500, created="2026-07-01"),  # too old
            model("meta-llama/Quiet", likes=5, created="2026-09-01"),  # too few likes
            model("random-user/New", likes=900, created="2026-09-01"),  # not a major org
        ]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([(m["id"], r) for m, r in result], [("meta-llama/New", ["major-org"])])

    def test_first_run_surge_fallback(self):
        cands = [
            model("x/fresh-liked", likes=100, created="2026-08-30"),
            model("x/fresh-downloaded", downloads=10000, created="2026-09-01"),
            model("x/fresh-quiet", likes=99, downloads=9999, created="2026-09-01"),
            model("x/old-popular", likes=5000, downloads=1_000_000, created="2026-08-01"),
        ]
        result = collect.select_famous(cands, {}, TODAY)
        self.assertEqual(sorted(m["id"] for m, _ in result), ["x/fresh-downloaded", "x/fresh-liked"])
        self.assertTrue(all(r == ["surge"] for _, r in result))

    def test_history_based_surge(self):
        history = {
            "x/likes-up": {"2026-08-28": {"likes": 100, "downloads": 500}},
            "x/dl-up": {"2026-08-29": {"likes": 10, "downloads": 6000}},
            "x/dl-up-small": {"2026-08-29": {"likes": 10, "downloads": 1000}},
            "x/flat": {"2026-08-28": {"likes": 100, "downloads": 50000}},
            "x/too-recent": {"2026-09-03": {"likes": 0, "downloads": 0}},
        }
        cands = [
            model("x/likes-up", likes=300, downloads=500, created="2025-01-01"),
            model("x/dl-up", likes=10, downloads=12000, created="2025-01-01"),
            model("x/dl-up-small", likes=10, downloads=5000, created="2025-01-01"),  # 5x but < 10k
            model("x/flat", likes=150, downloads=60000, created="2025-01-01"),
            model("x/too-recent", likes=900, downloads=90000, created="2025-01-01"),  # no 7-day-old snapshot
        ]
        result = collect.select_famous(cands, history, TODAY)
        self.assertEqual(sorted(m["id"] for m, _ in result), ["x/dl-up", "x/likes-up"])

    def test_exclusions_gguf_and_empty_metadata(self):
        cands = [
            model("someone/Model-GGUF", rank=1, created="2025-01-01"),
            model("Qwen/Qwen-GGUF", rank=2, created="2025-01-01"),
            model("a/no-meta", rank=3, created="2025-01-01", pipeline=None, tags=[]),
        ]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([m["id"] for m, _ in result], ["Qwen/Qwen-GGUF"])

    def test_multiple_reasons_combined_in_order(self):
        cands = [model("deepseek-ai/X", likes=500, created="2026-09-01", rank=1)]
        result = collect.select_famous(cands, {}, TODAY)
        self.assertEqual(result[0][1], ["trending", "surge", "major-org"])

    def test_select_on_real_trending_fixture(self):
        trending = json.loads(load_fixture("trending.json"))
        for rank, m in enumerate(trending, start=1):
            m["trending_rank"] = rank
        result = collect.select_famous(trending, {}, TODAY)
        ids = [m["id"] for m, _ in result]
        self.assertIn("deepseek-ai/DeepSeek-V4-Flash-Vision-Exp", ids)
        self.assertNotIn("unsloth/Qwen3.8-27B-GGUF", ids)
        self.assertGreaterEqual(len(ids), 10)


class HistoryTests(unittest.TestCase):
    def test_update_history_prunes_older_than_14_days(self):
        history = {"a/b": {"2026-08-01": {"likes": 1, "downloads": 1}, "2026-08-25": {"likes": 2, "downloads": 2}}}
        collect.update_history(history, [model("a/b", likes=3, downloads=4)], TODAY)
        self.assertEqual(sorted(history["a/b"]), ["2026-08-25", "2026-09-05"])
        self.assertEqual(history["a/b"]["2026-09-05"], {"likes": 3, "downloads": 4})


class HelperTests(unittest.TestCase):
    def test_humanize_params_boundaries(self):
        self.assertEqual(collect.humanize_params(None), "")
        self.assertEqual(collect.humanize_params(0), "")
        self.assertEqual(collect.humanize_params(999), "999")
        self.assertEqual(collect.humanize_params(1000), "1K")
        self.assertEqual(collect.humanize_params(350_000_000), "350M")
        self.assertEqual(collect.humanize_params(999_999_999), "1000M")
        self.assertEqual(collect.humanize_params(1_000_000_000), "1B")
        self.assertEqual(collect.humanize_params(7_200_000_000), "7.2B")
        self.assertEqual(collect.humanize_params(1_500_000_000_000), "1.5T")

    def test_params_from_safetensors_parameters_sum(self):
        detail = {"safetensors": {"parameters": {"BF16": 6_000_000_000, "F32": 1_200_000_000}}}
        self.assertEqual(collect.params_from_detail(detail), "7.2B")
        self.assertEqual(collect.params_from_detail({}), "")

    def test_license_from_card_data(self):
        self.assertEqual(collect.license_from_detail({"cardData": {"license": "mit"}}), "mit")
        self.assertEqual(collect.license_from_detail({"cardData": {"license": ["llama4", "other"]}}), "llama4")
        self.assertEqual(collect.license_from_detail({"cardData": {}}), "unknown")
        self.assertEqual(collect.license_from_detail({}), "unknown")

    def test_extract_summary_skips_frontmatter_html_and_badges(self):
        readme = load_fixture("readme_deepseek-ai--deepseek-v4-flash-vision-exp.md")
        summary = collect.extract_summary(readme)
        self.assertTrue(summary.startswith("We are excited to introduce"))
        self.assertNotIn("license: mit", summary)
        self.assertNotIn("<", summary)
        self.assertNotIn("img.shields.io", summary)
        self.assertNotIn("| Benchmark", summary)

    def test_extract_summary_truncates_to_600_chars(self):
        readme = "---\nlicense: mit\n---\n\n# T\n\n" + ("가나다라 " * 300)
        summary = collect.extract_summary(readme)
        self.assertTrue(summary.endswith("…"))
        self.assertLessEqual(len(summary), collect.SUMMARY_MAX_CHARS + 1)

    def test_extract_summary_empty_readme(self):
        self.assertEqual(collect.extract_summary(""), "모델 카드에 설명이 없습니다.")
        self.assertEqual(collect.extract_summary("---\nlicense: mit\n---\n# only heading\n"), "모델 카드에 설명이 없습니다.")

    def test_render_post_contains_all_keys_and_sections(self):
        detail = json.loads(load_fixture("detail_qwen--qwen3.8-27b.json"))
        readme = load_fixture("readme_qwen--qwen3.8-27b.md")
        text = collect.render_post(detail, ["trending", "major-org"], "2026-09-05", readme)
        meta, body = parse_frontmatter(text)
        self.assertEqual(list(meta), KEYS)
        self.assertEqual(meta["model_id"], "Qwen/Qwen3.8-27B")
        self.assertEqual(meta["title"], "Qwen3.8 27B")
        self.assertEqual(meta["org"], "Qwen")
        self.assertEqual(meta["license"], "apache-2.0")
        self.assertEqual(meta["params"], "27.8B")
        self.assertEqual(meta["created_at"], "2026-08-05")
        self.assertEqual(meta["reason"], "trending, major-org")
        self.assertEqual(meta["hf_url"], "https://huggingface.co/Qwen/Qwen3.8-27B")
        for section in ("## 요약", "## 모델 정보", "## 선정 이유", "- 라이선스: apache-2.0"):
            self.assertIn(section, body)
        self.assertNotRegex(body, r"<[a-zA-Z]+[^>]*>")

    def test_fetch_json_retries_once_then_raises(self):
        calls = []

        def flaky(url):
            calls.append(url)
            raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            collect.fetch_json("https://example.invalid/x", flaky)
        self.assertEqual(len(calls), 1)  # retry lives in default_fetcher, injected fetchers are called once
        with mock.patch.object(collect.urllib.request, "urlopen", side_effect=OSError("down")) as opener:
            with self.assertRaises(RuntimeError):
                collect.default_fetcher("https://example.invalid/y")
        self.assertEqual(opener.call_count, 2)


class RunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.content = root / "content" / "models"
        self.data = root / "data"

    def tearDown(self):
        self.tmp.cleanup()

    def run_collect(self, **kw):
        out = io.StringIO()
        with redirect_stdout(out):
            new = collect.run(self.content, self.data, kw.pop("max_new", 25), kw.pop("dry_run", False),
                              TODAY, fetcher=fixture_fetcher, **kw)
        return new, out.getvalue()

    def test_first_run_writes_posts_and_state(self):
        new, out = self.run_collect()
        self.assertGreaterEqual(len(new), 10)
        files = sorted(self.content.glob("*.md"))
        self.assertEqual(len(files), len(new))
        published = json.loads((self.data / "published.json").read_text())
        self.assertEqual(sorted(published["models"]), sorted(new))
        history = json.loads((self.data / "stats_history.json").read_text())
        self.assertIn("2026-09-05", history["deepseek-ai/DeepSeek-V4-Flash-Vision-Exp"])
        meta, _ = parse_frontmatter(files[0].read_text(encoding="utf-8"))
        self.assertEqual(list(meta), KEYS)
        self.assertEqual(out.strip().count("\n") + 1, len(new))

    def test_dedup_via_published_json(self):
        self.data.mkdir(parents=True)
        (self.data / "published.json").write_text(json.dumps({"models": {
            "deepseek-ai/DeepSeek-V4-Flash-Vision-Exp": {"slug": "x", "published_at": "2026-09-01"}}}))
        new, _ = self.run_collect()
        self.assertNotIn("deepseek-ai/DeepSeek-V4-Flash-Vision-Exp", new)
        self.assertFalse((self.content / "deepseek-ai--deepseek-v4-flash-vision-exp.md").exists())

    def test_dedup_via_existing_file_is_not_overwritten(self):
        self.content.mkdir(parents=True)
        existing = self.content / "deepseek-ai--deepseek-v4-flash-vision-exp.md"
        existing.write_text("KEEP", encoding="utf-8")
        new, _ = self.run_collect()
        self.assertNotIn("deepseek-ai/DeepSeek-V4-Flash-Vision-Exp", new)
        self.assertEqual(existing.read_text(encoding="utf-8"), "KEEP")

    def test_second_run_reports_no_new_models(self):
        self.run_collect()
        new, out = self.run_collect()
        self.assertEqual(new, [])
        self.assertIn("No new models", out)

    def test_dry_run_writes_nothing(self):
        new, out = self.run_collect(dry_run=True)
        self.assertGreater(len(new), 0)
        self.assertFalse(self.content.exists())
        self.assertFalse(self.data.exists())
        self.assertIn("deepseek-ai/DeepSeek-V4-Flash-Vision-Exp", out)

    def test_max_new_cap(self):
        new, _ = self.run_collect(max_new=3)
        self.assertEqual(len(new), 3)
        self.assertEqual(len(list(self.content.glob("*.md"))), 3)

    def test_main_exit_code_1_when_trending_unavailable(self):
        def broken(url):
            raise RuntimeError("offline")
        err = io.StringIO()
        with mock.patch.object(collect, "default_fetcher", broken), \
                mock.patch("sys.stderr", err):
            code = collect.main(["--content-dir", str(self.content), "--data-dir", str(self.data),
                                 "--today", "2026-09-05"])
        self.assertEqual(code, 1)
        self.assertIn("collection failed", err.getvalue())


if __name__ == "__main__":
    unittest.main()
