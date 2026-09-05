import datetime as dt
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from email.message import Message

from scripts import collect
from scripts.frontmatter import KEYS, parse_frontmatter, slugify


def http_error(url, code, headers=None):
    msg = Message()
    for k, v in (headers or {}).items():
        msg[k] = v
    return collect.urllib.error.HTTPError(url, code, "status %d" % code, msg, None)

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


def model(model_id, likes=0, downloads=0, created=None, rank=None, pipeline="text-generation", tags=None, last_modified=None):
    m = {"id": model_id, "modelId": model_id, "likes": likes, "downloads": downloads,
         "pipeline_tag": pipeline, "tags": ["transformers"] if tags is None else tags}
    if created:
        m["createdAt"] = created + "T00:00:00.000Z"
    if last_modified:
        m["lastModified"] = last_modified + "T00:00:00.000Z"
    if rank is not None:
        m["trending_rank"] = rank
    return m


# Old enough history so that the first-run fallback is NOT used.
OLD_HISTORY = {"someone/old": {"2026-08-20": {"likes": 1, "downloads": 1}}}


class SelectFamousTests(unittest.TestCase):
    def test_trending_top30_selected_and_31st_not(self):
        cands = [model("a/top", rank=30, created="2026-08-01"), model("a/low", rank=31, created="2026-08-01")]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([(m["id"], r) for m, r in result], [("a/top", ["new", "trending"])])

    def test_major_org_recent_release(self):
        cands = [
            model("meta-llama/New", likes=20, created="2026-08-10"),   # 26 days old, >=20 likes
            model("meta-llama/Old", likes=500, created="2026-07-01"),  # 66 days old -> 신규성 게이트 제외
            model("meta-llama/Quiet", likes=5, created="2026-09-01"),  # too few likes
            model("random-user/New", likes=900, created="2026-09-01"),  # not a major org
        ]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([(m["id"], r) for m, r in result], [("meta-llama/New", ["new", "major-org"])])

    def test_first_run_surge_fallback(self):
        cands = [
            model("x/fresh-liked", likes=100, created="2026-08-30"),
            model("x/fresh-downloaded", downloads=10000, created="2026-09-01"),
            model("x/fresh-quiet", likes=99, downloads=9999, created="2026-09-01"),
            model("x/old-popular", likes=5000, downloads=1_000_000, created="2026-08-01"),
        ]
        result = collect.select_famous(cands, {}, TODAY)
        self.assertEqual(sorted(m["id"] for m, _ in result), ["x/fresh-downloaded", "x/fresh-liked"])
        self.assertTrue(all(r == ["new", "surge"] for _, r in result))

    def test_history_based_surge(self):
        history = {
            "x/likes-up": {"2026-08-28": {"likes": 100, "downloads": 500}},
            "x/dl-up": {"2026-08-29": {"likes": 10, "downloads": 6000}},
            "x/dl-up-small": {"2026-08-29": {"likes": 10, "downloads": 1000}},
            "x/flat": {"2026-08-28": {"likes": 100, "downloads": 50000}},
            "x/too-recent": {"2026-09-03": {"likes": 0, "downloads": 0}},
        }
        # createdAt 은 2년 전(신규 아님)이지만 lastModified 가 7일 이내라 갱신 게이트 통과.
        cands = [
            model("x/likes-up", likes=300, downloads=500, created="2024-09-01", last_modified="2026-08-30"),
            model("x/dl-up", likes=10, downloads=12000, created="2024-09-01", last_modified="2026-08-30"),
            model("x/dl-up-small", likes=10, downloads=5000, created="2024-09-01", last_modified="2026-08-30"),  # 5x but < 10k
            model("x/flat", likes=150, downloads=60000, created="2024-09-01", last_modified="2026-08-30"),
            model("x/too-recent", likes=900, downloads=90000, created="2024-09-01", last_modified="2026-08-30"),  # no 7-day-old snapshot
        ]
        result = collect.select_famous(cands, history, TODAY)
        self.assertEqual(sorted(m["id"] for m, _ in result), ["x/dl-up", "x/likes-up"])

    def test_exclusions_gguf_and_empty_metadata(self):
        cands = [
            model("someone/Model-GGUF", rank=1, created="2026-08-01"),
            model("Qwen/Qwen-GGUF", rank=2, created="2026-08-01"),
            model("a/no-meta", rank=3, created="2026-08-01", pipeline=None, tags=[]),
        ]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([m["id"] for m, _ in result], ["Qwen/Qwen-GGUF"])

    def test_multiple_reasons_combined_in_order(self):
        cands = [model("deepseek-ai/X", likes=500, created="2026-09-01", rank=1)]
        result = collect.select_famous(cands, {}, TODAY)
        self.assertEqual(result[0][1], ["new", "trending", "surge", "major-org"])

    def test_select_on_real_trending_fixture(self):
        trending = json.loads(load_fixture("trending.json"))
        for rank, m in enumerate(trending, start=1):
            m["trending_rank"] = rank
        result = collect.select_famous(trending, {}, TODAY)
        ids = [m["id"] for m, _ in result]
        self.assertIn("deepseek-ai/DeepSeek-V4-Flash-Vision-Exp", ids)
        self.assertNotIn("unsloth/Qwen3.8-27B-GGUF", ids)
        self.assertGreaterEqual(len(ids), 10)

    def test_new_model_gate_60_days(self):
        # createdAt 60일 정확히 -> 신규성 OK, 61일 -> 제외
        d60 = (TODAY - dt.timedelta(days=60)).isoformat()
        d61 = (TODAY - dt.timedelta(days=61)).isoformat()
        cands = [
            model("a/exactly60", rank=1, created=d60),
            model("a/over60", rank=2, created=d61),
        ]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        ids = [m["id"] for m, _ in result]
        self.assertIn("a/exactly60", ids)
        self.assertNotIn("a/over60", ids)

    def test_recent_update_gate_14_days(self):
        # lastModified 14일 -> 갱신 OK, 15일 -> 제외 (createdAt이 2년 전이어도)
        old_created = "2024-01-01"
        d14 = (TODAY - dt.timedelta(days=14)).isoformat()
        d15 = (TODAY - dt.timedelta(days=15)).isoformat()
        cands = [
            model("a/updated14", rank=1, created=old_created, last_modified=d14),
            model("a/updated15", rank=2, created=old_created, last_modified=d15),
        ]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        ids = [m["id"] for m, _ in result]
        self.assertIn("a/updated14", ids)
        self.assertNotIn("a/updated15", ids)

    def test_classic_model_excluded(self):
        # createdAt 2년 전, lastModified 30일 전 -> 신규성 게이트 제외
        cands = [model("a/classic", rank=1, likes=500, created="2024-09-01", last_modified="2026-08-06")]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([m["id"] for m, _ in result], [])

    def test_missing_dates_excluded(self):
        # createdAt/lastModified 모두 없 -> 제외
        cands = [model("a/nodates", rank=1, likes=500)]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        self.assertEqual([m["id"] for m, _ in result], [])

    def test_reason_includes_new_or_updated(self):
        # 선정된 모델의 reason에 "new" 또는 "updated" 포함
        cands = [
            model("a/new-one", rank=1, created="2026-09-01"),
            model("a/updated-old", rank=2, created="2024-01-01", last_modified="2026-09-01"),
        ]
        result = collect.select_famous(cands, OLD_HISTORY, TODAY)
        for _, reasons in result:
            self.assertTrue("new" in reasons or "updated" in reasons,
                            "reason must include new or updated: %s" % reasons)


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
        readme = load_fixture("readme_deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md")
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

    def test_extract_summary_drops_badge_links_wrapping_images(self):
        readme = "# T\n\n[![badge](https://img.shields.io/x.svg)](https://example.com/a) [![b](https://x/y.png)](https://example.com/b)\n\n" \
                 "Granite is a family of open-source large language models developed by IBM.\n"
        summary = collect.extract_summary(readme)
        self.assertEqual(summary, "Granite is a family of open-source large language models developed by IBM.")

    def test_extract_summary_empty_readme(self):
        self.assertEqual(collect.extract_summary(""), "모델 카드에 설명이 없습니다.")
        self.assertEqual(collect.extract_summary("---\nlicense: mit\n---\n# only heading\n"), "모델 카드에 설명이 없습니다.")

    def test_render_post_contains_all_keys_and_sections(self):
        detail = json.loads(load_fixture("detail_Qwen__Qwen3.8-27B.json"))
        readme = load_fixture("readme_Qwen__Qwen3.8-27B.md")
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
        for section in ("## 왜 주목받는가", "## 핵심 스펙", "## 요약", "## 라이선스",
                        "## 관련 모델", "| 라이선스 | apache-2.0 |"):
            self.assertIn(section, body)
        self.assertNotRegex(body, r"<[a-zA-Z]+[^>]*>")

    def test_why_paragraph_contains_reason(self):
        detail = json.loads(load_fixture("detail_Qwen__Qwen3.8-27B.json"))
        text = collect.render_post(detail, ["trending"], "2026-09-05", "")
        _, body = parse_frontmatter(text)
        why_start = body.index("## 왜 주목받는가")
        why_end = body.index("## 핵심 스펙")
        section = body[why_start:why_end]
        self.assertIn("트렌딩 상위", section)

    def test_why_paragraph_contains_stats(self):
        detail = json.loads(load_fixture("detail_Qwen__Qwen3.8-27B.json"))
        text = collect.render_post(detail, ["trending"], "2026-09-05", "")
        _, body = parse_frontmatter(text)
        why_start = body.index("## 왜 주목받는가")
        why_end = body.index("## 핵심 스펙")
        section = body[why_start:why_end]
        self.assertIn("좋아요 13,948개", section)
        self.assertIn("다운로드 5,739,341회", section)
        self.assertIn("2026-09-05", section)

    def test_spec_table(self):
        detail = json.loads(load_fixture("detail_Qwen__Qwen3.8-27B.json"))
        text = collect.render_post(detail, ["trending"], "2026-09-05", "")
        _, body = parse_frontmatter(text)
        spec_start = body.index("## 핵심 스펙")
        spec_end = body.index("## 요약")
        table = body[spec_start:spec_end]
        # 6 data rows (excluding header + separator)
        self.assertEqual(table.count("\n| "), 8)  # 2 header/sep + 6 data rows
        for label in ("태스크", "파라미터", "라이선스", "최초 등록일", "좋아요", "다운로드"):
            self.assertIn("| %s |" % label, table)

    def test_license_commercial(self):
        self.assertEqual(collect.commercial_status("apache-2.0"), "상업 이용 가능")
        self.assertEqual(collect.commercial_status("mit"), "상업 이용 가능")
        self.assertEqual(collect.commercial_status("unknown"), "라이선스 정보 없음 — 원문 확인 필요")
        self.assertEqual(collect.commercial_status(""), "라이선스 정보 없음 — 원문 확인 필요")
        self.assertEqual(collect.commercial_status("proprietary"), "상업 이용 제한 또는 확인 필요")

    def test_related_models_same_org(self):
        published = {"models": {
            "Qwen/Qwen3.8-27B": {"slug": "Qwen__Qwen3.8-27B", "published_at": "2026-09-05"},
            "Qwen/Qwen3.8-Flash-Next": {"slug": "Qwen__Qwen3.8-Flash-Next", "published_at": "2026-09-05"},
        }}
        meta = {"org": "Qwen", "task": "image-text-to-text", "model_id": "Qwen/Qwen3.8-27B",
                "slug": "Qwen__Qwen3.8-27B"}
        related = collect.build_related_models(meta, published, None)
        self.assertIn("Qwen3.8 Flash Next", related)
        self.assertIn("../Qwen__Qwen3.8-Flash-Next/", related)
        self.assertNotIn("Qwen__Qwen3.8-27B", related)

    def test_related_models_empty_when_no_sibling(self):
        published = {"models": {
            "Qwen/Qwen3.8-27B": {"slug": "Qwen__Qwen3.8-27B", "published_at": "2026-09-05"},
        }}
        meta = {"org": "Qwen", "task": "image-text-to-text", "model_id": "Qwen/Qwen3.8-27B",
                "slug": "Qwen__Qwen3.8-27B"}
        related = collect.build_related_models(meta, published, None)
        self.assertEqual(related, "아직 관련 모델이 발행되지 않았습니다.")

    def test_regenerate_local(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        posts = root / "content" / "models"
        posts.mkdir(parents=True)
        data = root / "data"
        data.mkdir()
        # 기존 구조 글 작성
        old_post = (
            '---\n'
            'model_id: "Qwen/Qwen3.8-27B"\n'
            'title: "Qwen3.8 27B"\n'
            'org: "Qwen"\n'
            'task: "image-text-to-text"\n'
            'license: "apache-2.0"\n'
            'params: "27.8B"\n'
            'likes: 13948\n'
            'downloads: 5739341\n'
            'discovered_at: "2026-09-05"\n'
            'created_at: "2026-08-05"\n'
            'hf_url: "https://huggingface.co/Qwen/Qwen3.8-27B"\n'
            'tags: ["transformers"]\n'
            'reason: "trending"\n'
            '---\n\n'
            '## 요약\n\n이전 본문의 요약 문단입니다.\n\n## 모델 정보\n\n- 구 정보\n'
        )
        (posts / "Qwen__Qwen3.8-27B.md").write_text(old_post, encoding="utf-8")
        (data / "published.json").write_text(json.dumps({"models": {
            "Qwen/Qwen3.8-27B": {"slug": "Qwen__Qwen3.8-27B", "published_at": "2026-09-05"},
        }}))
        rewritten = collect.regenerate_local(posts, data / "published.json")
        self.assertEqual(len(rewritten), 1)
        new_text = (posts / "Qwen__Qwen3.8-27B.md").read_text(encoding="utf-8")
        meta, body = parse_frontmatter(new_text)
        # frontmatter 보존
        self.assertEqual(meta["model_id"], "Qwen/Qwen3.8-27B")
        # 새 구조 헤더
        for section in ("## 왜 주목받는가", "## 핵심 스펙", "## 요약", "## 라이선스",
                        "## 관련 모델"):
            self.assertIn(section, body)
        # 기존 요약 보존
        self.assertIn("이전 본문의 요약 문단입니다.", body)
        # 구 '## 모델 정보' 는 제거
        self.assertNotIn("## 모델 정보", body)
        self.assertNotIn("## 선정 이유", body)
        self.assertIn("상업 이용 가능", body)

    def test_fetch_json_retries_once_then_raises(self):
        calls = []

        def flaky(url):
            calls.append(url)
            raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            collect.fetch_json("https://example.invalid/x", flaky)
        self.assertEqual(len(calls), 1)  # retry lives in default_fetcher, injected fetchers are called once
        sleep = mock.Mock()
        with mock.patch.object(collect.urllib.request, "urlopen", side_effect=OSError("down")) as opener:
            with self.assertRaises(RuntimeError):
                collect.default_fetcher("https://example.invalid/y", sleep=sleep)
        self.assertEqual(opener.call_count, collect.RETRY_MAX + 1)  # transient OSError is retried
        self.assertEqual(sleep.call_count, collect.RETRY_MAX)

    def test_default_fetcher_retries_429_with_backoff_then_succeeds(self):
        url = "https://example.invalid/429"
        body = mock.MagicMock()
        body.__enter__.return_value.read.return_value = b'{"ok": true}'
        responses = [
            http_error(url, 429), http_error(url, 503), http_error(url, 500), body,
        ]
        sleep = mock.Mock()
        err = io.StringIO()
        with mock.patch.object(collect.urllib.request, "urlopen", side_effect=responses) as opener, \
                mock.patch("sys.stderr", err):
            self.assertEqual(collect.default_fetcher(url, sleep=sleep), '{"ok": true}')
        self.assertEqual(opener.call_count, 4)
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [1.0, 2.0, 4.0])
        self.assertEqual(err.getvalue().count("warning: retry"), 3)

    def test_default_fetcher_honours_retry_after_header_with_cap(self):
        url = "https://example.invalid/ra"
        body = mock.MagicMock()
        body.__enter__.return_value.read.return_value = b"[]"
        responses = [
            http_error(url, 429, {"Retry-After": "7"}),
            http_error(url, 503, {"Retry-After": "120"}),
            http_error(url, 429, {"Retry-After": "not-a-number"}),
            body,
        ]
        sleep = mock.Mock()
        with mock.patch.object(collect.urllib.request, "urlopen", side_effect=responses), \
                mock.patch("sys.stderr", io.StringIO()):
            self.assertEqual(collect.default_fetcher(url, sleep=sleep), "[]")
        # header wins over backoff, is capped at RETRY_MAX_SECONDS, unparsable falls back to backoff
        self.assertEqual([c.args[0] for c in sleep.call_args_list],
                         [7.0, collect.RETRY_MAX_SECONDS, 4.0])

    def test_default_fetcher_does_not_retry_404(self):
        url = "https://example.invalid/missing"
        sleep = mock.Mock()
        with mock.patch.object(collect.urllib.request, "urlopen", side_effect=http_error(url, 404)) as opener:
            with self.assertRaises(RuntimeError) as ctx:
                collect.default_fetcher(url, sleep=sleep)
        self.assertEqual(opener.call_count, 1)
        sleep.assert_not_called()
        self.assertIn("404", str(ctx.exception))

    def test_default_fetcher_gives_up_after_retry_max(self):
        url = "https://example.invalid/502"
        sleep = mock.Mock()
        with mock.patch.object(collect.urllib.request, "urlopen", side_effect=http_error(url, 502)) as opener, \
                mock.patch("sys.stderr", io.StringIO()):
            with self.assertRaises(RuntimeError):
                collect.default_fetcher(url, sleep=sleep)
        self.assertEqual(opener.call_count, collect.RETRY_MAX + 1)
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [1.0, 2.0, 4.0, 8.0])

    def test_fetch_readme_returns_empty_on_fetch_error(self):
        def missing(url):
            raise RuntimeError("fetch failed: %s (HTTP 404)" % url)
        err = io.StringIO()
        with mock.patch("sys.stderr", err):
            self.assertEqual(collect.fetch_readme("a/b", missing), "")
        self.assertIn("README unavailable", err.getvalue())

    def test_gather_candidates_merges_listings_and_ranks_trending(self):
        def fetcher(url):
            if "sort=trendingScore" in url:
                return json.dumps([model("t/one"), model("t/two")])
            if "sort=likes" in url:
                return json.dumps([model("t/one", likes=999), model("l/only")])
            if "sort=downloads" in url:
                raise RuntimeError("offline")
            if "author=" in url:
                return json.dumps([model("o/only")]) if "author=Qwen" in url else "[]"
            raise RuntimeError("unexpected url %s" % url)
        err = io.StringIO()
        with mock.patch("sys.stderr", err):
            seen = collect.gather_candidates(fetcher, collect.DEFAULT_CONFIG)
        by_id = {m["id"]: m for m in seen}
        self.assertEqual(sorted(by_id), ["l/only", "o/only", "t/one", "t/two"])
        self.assertEqual(by_id["t/one"]["trending_rank"], 1)
        self.assertEqual(by_id["t/one"]["likes"], 0)  # trending entry wins over later listings
        self.assertNotIn("trending_rank", by_id["l/only"])
        self.assertIn("top-downloads listing failed", err.getvalue())


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
        self.assertFalse((self.content / "deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md").exists())

    def test_dedup_via_existing_file_is_not_overwritten(self):
        self.content.mkdir(parents=True)
        existing = self.content / "deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md"
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

    def test_run_skips_model_whose_detail_fails_and_records_history_for_all(self):
        target = "deepseek-ai/DeepSeek-V4-Flash-Vision-Exp"

        def fetcher(url):
            if url == "%s/%s" % (collect.HF_API, target):
                raise RuntimeError("fetch failed: %s (HTTP 500)" % url)
            return fixture_fetcher(url)
        err = io.StringIO()
        with mock.patch("sys.stderr", err), redirect_stdout(io.StringIO()):
            new = collect.run(self.content, self.data, 25, False, TODAY, fetcher=fetcher)
        self.assertNotIn(target, new)
        self.assertGreater(len(new), 0)
        self.assertIn("skipping %s" % target, err.getvalue())
        history = json.loads((self.data / "stats_history.json").read_text())
        self.assertIn(target, history)  # history covers every candidate, not only published ones


class WriteSummaryTests(unittest.TestCase):
    def test_write_summary_format(self):
        md = collect.write_summary({
            "today": "2026-09-05", "candidates": 50, "new_posts": 3,
            "excluded": 12, "total_published": 47,
        })
        self.assertIn("## 수집 실행 요약", md)
        self.assertIn("| 항목 | 값 |", md)
        self.assertIn("| 수집 일시 | 2026-09-05 |", md)
        self.assertIn("| 후보 모델 수 | 50 |", md)
        self.assertIn("| 신규 발행 | 3 |", md)
        self.assertIn("| 제외(신규성 게이트) | 12 |", md)
        self.assertIn("| 누적 발행 모델 | 47 |", md)
        self.assertTrue(md.endswith("\n"))

    def test_write_summary_to_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "summary.md"
            md = collect.write_summary({
                "today": "2026-09-05", "candidates": 10, "new_posts": 0,
                "excluded": 5, "total_published": 20,
            }, path=p)
            self.assertTrue(p.exists())
            self.assertEqual(p.read_text(encoding="utf-8"), md)
            collect.write_summary({
                "today": "2026-09-06", "candidates": 11, "new_posts": 1,
                "excluded": 6, "total_published": 21,
            }, path=p)
            text = p.read_text(encoding="utf-8")
            self.assertEqual(text.count("## 수집 실행 요약"), 2)
            self.assertIn("2026-09-05", text)
            self.assertIn("2026-09-06", text)

    def test_write_summary_defaults_for_missing_keys(self):
        md = collect.write_summary({})
        self.assertIn("| 수집 일시 |  |", md)
        self.assertIn("| 후보 모델 수 | 0 |", md)


class ZeroResultsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.content = root / "content" / "models"
        self.data = root / "data"

    def tearDown(self):
        self.tmp.cleanup()

    def test_zero_results_no_failure(self):
        def empty_fetcher(url: str) -> str:
            if url.startswith(collect.HF_API + "?"):
                if "sort=trendingScore" in url:
                    return "[]"
                return "[]"
            if url.startswith(collect.HF_API + "/"):
                return "{}"
            return ""
        err = io.StringIO()
        out = io.StringIO()
        with mock.patch("sys.stderr", err), redirect_stdout(out):
            new = collect.run(self.content, self.data, 25, False, TODAY, fetcher=empty_fetcher)
        self.assertEqual(new, [])
        self.assertIn("No new models", out.getvalue())

    def test_zero_results_dry_run_no_failure(self):
        def empty_fetcher(url: str) -> str:
            if url.startswith(collect.HF_API + "?"):
                return "[]"
            return ""
        out = io.StringIO()
        with redirect_stdout(out):
            new = collect.run(self.content, self.data, 25, True, TODAY, fetcher=empty_fetcher)
        self.assertEqual(new, [])
        self.assertIn("No new models", out.getvalue())


if __name__ == "__main__":
    unittest.main()


def _write_post(posts_dir: Path, meta: dict) -> None:
    """테스트용 최소 글 파일(frontmatter + 빈 요약)을 쓴다."""
    from scripts.frontmatter import dump_frontmatter
    full = {
        "model_id": meta["model_id"], "title": meta["model_id"].split("/")[-1],
        "org": meta["model_id"].split("/")[0], "task": meta.get("task", "other"),
        "license": meta.get("license", "unknown"), "params": meta.get("params", ""),
        "likes": meta.get("likes", 0), "downloads": meta.get("downloads", 0),
        "discovered_at": meta.get("discovered_at", "2026-09-01"),
        "created_at": meta.get("created_at", "2026-08-01"),
        "hf_url": "https://huggingface.co/" + meta["model_id"], "tags": [],
        "reason": meta.get("reason", "major-org"),
    }
    (posts_dir / (slugify(meta["model_id"]) + ".md")).write_text(
        dump_frontmatter(full, "## 요약\n\n요약."), encoding="utf-8")


class ComparisonTests(unittest.TestCase):
    """같은 기관·같은 태스크 이전 모델 대비 수치 비교와 급상승 증분 문장."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.posts = Path(tmp.name)
        self.published = {"models": {}}

    def _publish(self, model_id, published_at, **meta):
        meta["model_id"] = model_id
        meta.setdefault("discovered_at", published_at)
        _write_post(self.posts, meta)
        self.published["models"][model_id] = {"slug": slugify(model_id), "published_at": published_at}

    def test_parse_params(self):
        self.assertEqual(collect.parse_params("27.8B"), 27_800_000_000)
        self.assertEqual(collect.parse_params("350M"), 350_000_000)
        self.assertEqual(collect.parse_params("1.2T"), 1_200_000_000_000)
        self.assertIsNone(collect.parse_params(""))
        self.assertIsNone(collect.parse_params("정보 없음"))

    def test_previous_model_requires_same_org_and_task(self):
        self._publish("Qwen/Qwen3-8B", "2026-08-20", task="text-generation", params="8B")
        self._publish("Qwen/Qwen-VL", "2026-08-25", task="image-text-to-text", params="7B")
        self._publish("google/gemma-9b", "2026-08-30", task="text-generation", params="9B")
        meta = {"model_id": "Qwen/Qwen3-32B", "org": "Qwen", "task": "text-generation"}
        prev = collect.find_previous_model(meta, self.published, self.posts)
        self.assertEqual(prev["model_id"], "Qwen/Qwen3-8B")

    def test_previous_model_picks_most_recent_and_skips_self(self):
        self._publish("Qwen/Qwen3-8B", "2026-08-20", task="text-generation")
        self._publish("Qwen/Qwen3-14B", "2026-08-28", task="text-generation")
        self._publish("Qwen/Qwen3-32B", "2026-09-05", task="text-generation")
        meta = {"model_id": "Qwen/Qwen3-32B", "org": "Qwen", "task": "text-generation"}
        prev = collect.find_previous_model(meta, self.published, self.posts)
        self.assertEqual(prev["model_id"], "Qwen/Qwen3-14B")

    def test_previous_model_none_when_no_match(self):
        self._publish("Qwen/Qwen-VL", "2026-08-25", task="image-text-to-text")
        meta = {"model_id": "Qwen/Qwen3-32B", "org": "Qwen", "task": "text-generation"}
        self.assertIsNone(collect.find_previous_model(meta, self.published, self.posts))
        self.assertIsNone(collect.find_previous_model(meta, self.published, None))

    def test_compare_sentence_with_numbers(self):
        prev = {"model_id": "Qwen/Qwen3-8B", "params": "8B", "downloads": 1000, "license": "apache-2.0"}
        meta = {"model_id": "Qwen/Qwen3-32B", "params": "32B", "downloads": 500, "license": "apache-2.0"}
        s = collect.compare_sentence(meta, prev)
        self.assertIn("이전 모델 Qwen/Qwen3-8B(파라미터 8B, 다운로드 1,000)", s)
        self.assertIn("파라미터 300.0% 증가", s)
        self.assertIn("다운로드 50.0% 감소", s)
        self.assertIn("라이선스 동일(apache-2.0)", s)

    def test_compare_sentence_marks_missing_params(self):
        prev = {"model_id": "a/b", "params": "", "downloads": 0, "license": "mit"}
        meta = {"model_id": "a/c", "params": "3B", "downloads": 10, "license": "other"}
        s = collect.compare_sentence(meta, prev)
        self.assertIn("파라미터 비교 정보 없음", s)
        self.assertIn("다운로드 0→10(비율 산출 불가)", s)
        self.assertIn("라이선스 mit→other", s)

    def test_compare_sentence_none_is_first_publication(self):
        self.assertEqual(collect.compare_sentence({"model_id": "a/c"}, None),
                         "같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).")

    def test_surge_sentence_with_snapshot(self):
        history = {"a/c": {"2026-08-28": {"likes": 100, "downloads": 1000},
                           "2026-09-04": {"likes": 180, "downloads": 1500}}}
        meta = {"model_id": "a/c", "likes": 200, "downloads": 3000}
        s = collect.surge_sentence(meta, history, TODAY)
        self.assertEqual(s, "급상승 근거(7일 전 2026-08-28 스냅샷 대비): 좋아요 100→200(+100.0%), 다운로드 1,000→3,000(+200.0%).")

    def test_surge_sentence_without_snapshot(self):
        history = {"a/c": {"2026-09-04": {"likes": 180, "downloads": 1500}}}
        meta = {"model_id": "a/c", "likes": 200, "downloads": 3000}
        self.assertEqual(collect.surge_sentence(meta, history, TODAY),
                         "급상승 근거: 7일 전 스냅샷 정보 없음(수집 이력 부족).")
        self.assertEqual(collect.surge_sentence(meta, {}, TODAY),
                         "급상승 근거: 7일 전 스냅샷 정보 없음(수집 이력 부족).")

    def test_why_paragraph_includes_comparison_and_surge(self):
        self._publish("Qwen/Qwen3-8B", "2026-08-20", task="text-generation", params="8B", downloads=1000)
        history = {"Qwen/Qwen3-32B": {"2026-08-27": {"likes": 10, "downloads": 100}}}
        meta = {"model_id": "Qwen/Qwen3-32B", "org": "Qwen", "task": "text-generation",
                "params": "16B", "likes": 30, "downloads": 400, "license": "apache-2.0",
                "discovered_at": "2026-09-05"}
        why = collect.build_why_paragraph(meta, ["trending", "surge"], self.published,
                                          posts_dir=self.posts, history=history, today=TODAY)
        self.assertIn("이전 모델 Qwen/Qwen3-8B", why)
        self.assertIn("파라미터 100.0% 증가", why)
        self.assertIn("좋아요 10→30(+200.0%)", why)
        self.assertNotIn("함께 살펴보세요", why)

    def test_why_paragraph_no_surge_sentence_without_surge_reason(self):
        meta = {"model_id": "Qwen/Qwen3-32B", "org": "Qwen", "task": "text-generation",
                "params": "16B", "likes": 30, "downloads": 400, "license": "apache-2.0",
                "discovered_at": "2026-09-05"}
        why = collect.build_why_paragraph(meta, ["trending"], self.published,
                                          posts_dir=self.posts, history={}, today=TODAY)
        self.assertNotIn("급상승 근거", why)
        self.assertIn("비교 대상 없음(최초 발행)", why)

    def test_compare_sentence_equal_params_says_same(self):
        prev = {"model_id": "a/b", "params": "321.3B", "downloads": 100, "license": "mit"}
        meta = {"model_id": "a/c", "params": "321.3B", "downloads": 100, "license": "mit"}
        s = collect.compare_sentence(meta, prev)
        self.assertIn("파라미터 동일(321.3B)", s)
        self.assertIn("다운로드 동일(100)", s)
