#!/usr/bin/env python3
"""Collect notable Hugging Face models and write one markdown post per model.

Standard library only (urllib.request, json, re, datetime, pathlib, argparse).
The Hugging Face API is used anonymously; no token is ever sent.

Selection criteria (kept as module constants so README can quote them):

  (0) novelty gate - applied to every candidate first. A model must have
      createdAt within NEW_MODEL_DAYS (60) OR lastModified within
      RECENT_UPDATE_DAYS (14). Models failing this gate (e.g. years-old
      classics such as gpt2/bert-base-uncased) are excluded regardless of
      any other criterion. Passing models get "new" and/or "updated" in
      their reason list.
  (A) trending  - within the top TRENDING_TOP_N of
                  /api/models?sort=trendingScore
  (B) surge     - compared with the snapshot taken >= SURGE_WINDOW_DAYS ago in
                  data/stats_history.json: likes grew by >= SURGE_LIKES_DELTA,
                  or downloads grew >= SURGE_DOWNLOAD_RATIO x (and the absolute
                  download count is >= SURGE_MIN_DOWNLOADS).
                  When no history reaches back that far (first run), a model
                  created within FIRST_RUN_NEW_DAYS with likes >= FIRST_RUN_LIKES
                  or downloads >= FIRST_RUN_DOWNLOADS counts as a surge.
  (C) major-org - published by one of MAJOR_ORGS within MAJOR_ORG_DAYS and
                  likes >= MAJOR_ORG_MIN_LIKES.

Exclusions: GGUF re-uploads by non-major orgs; models with neither a
pipeline_tag nor tags.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

if __package__ in (None, ""):
    # Allow `python3 scripts/collect.py` from the repository root.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.frontmatter import KEYS, dump_frontmatter, parse_frontmatter, slugify  # noqa: E402

HF_API = "https://huggingface.co/api/models"
HF_WEB = "https://huggingface.co"
USER_AGENT = "ai-model-news-collector/1.0 (+https://github.com/jhl-labs/ai-model-news)"
TIMEOUT = 30
# Retry policy for default_fetcher: HTTP 429/5xx and transient network errors
# are retried with exponential backoff (1s, 2s, 4s, 8s); a Retry-After header
# takes precedence but is capped at RETRY_MAX_SECONDS.
RETRY_MAX = 4
RETRY_BASE_SECONDS = 1.0
RETRY_MAX_SECONDS = 30.0
RETRY_STATUSES = (429, 500, 502, 503, 504)

# --- selection constants ---------------------------------------------------
TRENDING_TOP_N = 30
SURGE_WINDOW_DAYS = 7
SURGE_LIKES_DELTA = 200
SURGE_DOWNLOAD_RATIO = 2.0
SURGE_MIN_DOWNLOADS = 10_000
FIRST_RUN_NEW_DAYS = 7
FIRST_RUN_LIKES = 100
FIRST_RUN_DOWNLOADS = 10_000
MAJOR_ORG_DAYS = 30
MAJOR_ORG_MIN_LIKES = 20
HISTORY_KEEP_DAYS = 14
NEW_MODEL_DAYS = 60      # createdAt이 이 기간 이내면 "신규"
RECENT_UPDATE_DAYS = 14  # lastModified가 이 기간 이내면 "갱신"
MAJOR_ORGS = [
    "meta-llama", "google", "mistralai", "Qwen", "deepseek-ai", "openai",
    "microsoft", "nvidia", "stabilityai", "black-forest-labs", "apple",
    "ibm-granite", "allenai", "CohereLabs", "zai-org", "moonshotai",
    "xai-org", "HuggingFaceTB", "nari-labs", "tencent",
]

DEFAULT_CONFIG = {
    "trending_top_n": TRENDING_TOP_N,
    "surge_window_days": SURGE_WINDOW_DAYS,
    "surge_likes_delta": SURGE_LIKES_DELTA,
    "surge_download_ratio": SURGE_DOWNLOAD_RATIO,
    "surge_min_downloads": SURGE_MIN_DOWNLOADS,
    "first_run_new_days": FIRST_RUN_NEW_DAYS,
    "first_run_likes": FIRST_RUN_LIKES,
    "first_run_downloads": FIRST_RUN_DOWNLOADS,
    "major_org_days": MAJOR_ORG_DAYS,
    "major_org_min_likes": MAJOR_ORG_MIN_LIKES,
    "major_orgs": MAJOR_ORGS,
    "new_model_days": NEW_MODEL_DAYS,
    "recent_update_days": RECENT_UPDATE_DAYS,
}

SUMMARY_MAX_CHARS = 600
MIN_PARAGRAPH_CHARS = 30  # shorter blocks ("Notes:") are not meaningful summaries
MAX_TAGS = 30


# --- HTTP -------------------------------------------------------------------
# Exceptions a fetcher/JSON decode step can raise: RuntimeError from
# default_fetcher, OSError from sockets, ValueError from json.loads.
FETCH_ERRORS = (RuntimeError, OSError, ValueError)
# Additionally, a malformed API payload can break rendering.
POST_ERRORS = FETCH_ERRORS + (KeyError, TypeError, AttributeError)


def _retry_after_seconds(exc: urllib.error.HTTPError) -> float | None:
    """Parse a numeric Retry-After header; None when absent or not a number."""
    value = exc.headers.get("Retry-After") if exc.headers is not None else None
    if value is None:
        return None
    try:
        return max(0.0, float(value.strip()))
    except ValueError:
        return None  # HTTP-date form is rare on the HF API; fall back to backoff


def _retry_delay(attempt: int, exc: Exception) -> float:
    """Seconds to wait before retry number *attempt* (0-based)."""
    delay = RETRY_BASE_SECONDS * (2 ** attempt)
    if isinstance(exc, urllib.error.HTTPError):
        hinted = _retry_after_seconds(exc)
        if hinted is not None:
            delay = hinted
    return min(delay, RETRY_MAX_SECONDS)


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in RETRY_STATUSES
    # URLError (DNS, refused, timeout) and other socket-level OSErrors are transient.
    return isinstance(exc, OSError)


def default_fetcher(url: str, sleep=None) -> str:
    """GET *url* and return the body as text.

    HTTP 429/500/502/503/504 and transient network errors are retried up to
    RETRY_MAX times with exponential backoff (Retry-After honoured, capped).
    Other 4xx responses fail immediately. *sleep* is injectable for tests.
    """
    sleep = sleep or time.sleep
    last_exc: Exception | None = None
    for attempt in range(RETRY_MAX + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as exc:
            last_exc = exc
            if not _is_retryable(exc) or attempt >= RETRY_MAX:
                break
            delay = _retry_delay(attempt, exc)
            print("warning: retry %d/%d for %s in %.0fs (%s)"
                  % (attempt + 1, RETRY_MAX, url, delay, exc), file=sys.stderr)
            sleep(delay)
    raise RuntimeError("fetch failed: %s (%s)" % (url, last_exc))


def fetch_json(url: str, fetcher):
    """GET *url* with *fetcher* (always passed explicitly; see run())."""
    return json.loads(fetcher(url))


def list_trending(fetcher, limit: int = 50) -> list:
    return fetch_json("%s?sort=trendingScore&direction=-1&limit=%d" % (HF_API, limit), fetcher)


def list_top(fetcher, sort: str, limit: int = 100) -> list:
    return fetch_json("%s?sort=%s&direction=-1&limit=%d" % (HF_API, sort, limit), fetcher)


def list_recent_by_org(org: str, fetcher, limit: int = 20) -> list:
    return fetch_json("%s?author=%s&sort=lastModified&direction=-1&limit=%d" % (HF_API, org, limit), fetcher)


def fetch_model_detail(model_id: str, fetcher) -> dict:
    return fetch_json("%s/%s" % (HF_API, model_id), fetcher)


def fetch_readme(model_id: str, fetcher) -> str:
    try:
        return fetcher("%s/%s/raw/main/README.md" % (HF_WEB, model_id))
    except FETCH_ERRORS as exc:  # README is optional
        print("warning: README unavailable for %s: %s" % (model_id, exc), file=sys.stderr)
        return ""


# --- helpers ----------------------------------------------------------------
def parse_date(value) -> dt.date | None:
    """'2026-08-31T06:16:18.000Z' -> date(2026, 8, 31); None when missing."""
    if not value or not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value[:10])
    except ValueError:
        return None


def model_org(model_id: str) -> str:
    return model_id.split("/", 1)[0] if "/" in model_id else ""


def model_name(model_id: str) -> str:
    return model_id.split("/", 1)[1] if "/" in model_id else model_id


def title_from_id(model_id: str) -> str:
    return re.sub(r"[-_]+", " ", model_name(model_id)).strip()


def humanize_params(n) -> str:
    """304646824126 -> '304.6B', 350000000 -> '350M', None/0 -> ''."""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return ""
    if n <= 0:
        return ""
    for unit, size in (("T", 10 ** 12), ("B", 10 ** 9), ("M", 10 ** 6), ("K", 10 ** 3)):
        if n >= size:
            value = n / size
            text = "%.1f" % value
            if text.endswith(".0"):
                text = text[:-2]
            return text + unit
    return str(n)


def params_from_detail(detail: dict) -> str:
    st = detail.get("safetensors") or {}
    total = st.get("total")
    if not total and isinstance(st.get("parameters"), dict):
        total = sum(v for v in st["parameters"].values() if isinstance(v, (int, float)))
    return humanize_params(total)


def license_from_detail(detail: dict) -> str:
    lic = (detail.get("cardData") or {}).get("license")
    if isinstance(lic, list):
        lic = lic[0] if lic else None
    if isinstance(lic, str) and lic.strip():
        return lic.strip()
    return "unknown"


# --- summary extraction -----------------------------------------------------
_HTML_LINE = re.compile(r"^\s*<[^>]*>?.*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        m = re.search(r"^---\s*$", text[3:], flags=re.M)
        if m:
            return text[3 + m.end():]
    return text


def _clean_line(line: str) -> str:
    line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)       # images
    line = re.sub(r"<!--.*?-->", "", line)                  # html comments
    line = re.sub(r"<[^>]+>", "", line)                     # inline html tags
    line = re.sub(r"\[!\w+\]", "", line)                    # [!Note] admonitions
    line = re.sub(r"^\s*>\s?", "", line)                    # blockquote prefix
    line = re.sub(r"\[([^\]]*)\]\((?:https?://img\.shields\.io|[^)]*badge)[^)]*\)", "", line)
    line = re.sub(r"\[\s*\]\([^)]*\)", "", line)                  # links left empty after image removal
    return line.strip()


def extract_summary(readme_text: str) -> str:
    """Return the first 1-3 meaningful paragraphs after the frontmatter.

    Headings, tables, code fences, HTML/badge/image lines are dropped; the
    result is cut to SUMMARY_MAX_CHARS with a trailing ellipsis.
    """
    text = _strip_frontmatter(readme_text or "")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    paragraphs: list[str] = []
    current: list[str] = []
    in_fence = False

    def flush():
        if current:
            para = " ".join(current).strip()
            if len(para) >= MIN_PARAGRAPH_CHARS:
                paragraphs.append(para)
            current.clear()

    for raw in text.split("\n"):
        if _FENCE.match(raw):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        s = line.strip()
        if s.startswith("#") or s.startswith("|") or _HTML_LINE.match(s) or s.startswith("!["):
            flush()
            continue
        cleaned = _clean_line(line)
        if not cleaned or re.fullmatch(r"[-*_=\s]+", cleaned):
            continue
        current.append(cleaned)
        if len(paragraphs) >= 3:
            break
    flush()
    paragraphs = paragraphs[:3]
    if not paragraphs:
        return "모델 카드에 설명이 없습니다."
    summary = "\n\n".join(paragraphs)
    if len(summary) > SUMMARY_MAX_CHARS:
        summary = summary[:SUMMARY_MAX_CHARS].rstrip() + "…"
    return summary


# --- selection --------------------------------------------------------------
def is_excluded(model: dict, config: dict) -> bool:
    model_id = model.get("id") or model.get("modelId") or ""
    org = model_org(model_id)
    if "gguf" in model_id.lower() and org not in config["major_orgs"]:
        return True
    if not model.get("pipeline_tag") and not model.get("tags"):
        return True
    return False


def _snapshot_before(history_entry: dict, cutoff: dt.date) -> dict | None:
    """Latest snapshot dated on/before *cutoff*."""
    best_date, best = None, None
    for date_str, snap in (history_entry or {}).items():
        d = parse_date(date_str)
        if d is None or d > cutoff:
            continue
        if best_date is None or d > best_date:
            best_date, best = d, snap
    return best


def history_reaches_back(history: dict, cutoff: dt.date) -> bool:
    for entry in history.values():
        for date_str in entry:
            d = parse_date(date_str)
            if d is not None and d <= cutoff:
                return True
    return False


def select_famous(candidates: list, history: dict, now: dt.date, config: dict | None = None) -> list:
    """Return [(model, [reasons...])] for candidates meeting any criterion.

    *candidates* are HF listing dicts; a candidate coming from the trending
    list should carry ``"trending_rank"`` (1-based). *history* is
    {model_id: {"YYYY-MM-DD": {"likes": int, "downloads": int}}}.
    """
    cfg = dict(DEFAULT_CONFIG)
    if config:
        cfg.update(config)
    cutoff = now - dt.timedelta(days=cfg["surge_window_days"])
    # First run (or history too young): there is nothing to compare against,
    # so brand-new models with clear traction are treated as surging.
    first_run = not history_reaches_back(history, cutoff)
    selected = []
    seen = set()
    for model in candidates:
        model_id = model.get("id") or model.get("modelId") or ""
        if not model_id or model_id in seen or is_excluded(model, cfg):
            continue
        seen.add(model_id)
        reasons = []
        likes = int(model.get("likes") or 0)
        downloads = int(model.get("downloads") or 0)
        created = parse_date(model.get("createdAt"))
        modified = parse_date(model.get("lastModified"))
        age = (now - created).days if created else None
        modified_age = (now - modified).days if modified else None

        # --- 신규성 게이트: createdAt 60일 이내 또는 lastModified 14일 이내 ---
        # 둘 다 없거나 둘 다 기한 밖이면 선정 제외 (trending/surge/major-org 어떤 경로든).
        # 게이트 통과 시 "new"/"updated" 태그를 reason에 포함한다.
        is_new = age is not None and age <= cfg["new_model_days"]
        is_updated = modified_age is not None and modified_age <= cfg["recent_update_days"]
        if not is_new and not is_updated:
            continue
        novelty_reasons = []
        if is_new:
            novelty_reasons.append("new")
        if is_updated:
            novelty_reasons.append("updated")

        rank = model.get("trending_rank")
        if isinstance(rank, int) and 1 <= rank <= cfg["trending_top_n"]:
            reasons.append("trending")

        surge = False
        if first_run:
            if age is not None and age <= cfg["first_run_new_days"] and (
                likes >= cfg["first_run_likes"] or downloads >= cfg["first_run_downloads"]
            ):
                surge = True
        else:
            prev = _snapshot_before(history.get(model_id, {}), cutoff)
            if prev:
                prev_likes = int(prev.get("likes") or 0)
                prev_dl = int(prev.get("downloads") or 0)
                if likes - prev_likes >= cfg["surge_likes_delta"]:
                    surge = True
                elif downloads >= cfg["surge_min_downloads"] and downloads >= prev_dl * cfg["surge_download_ratio"]:
                    surge = True
        if surge:
            reasons.append("surge")

        if model_org(model_id) in cfg["major_orgs"] and age is not None \
                and age <= cfg["major_org_days"] and likes >= cfg["major_org_min_likes"]:
            reasons.append("major-org")

        if reasons:
            # 신규성 게이트를 통과한 모델만 여기 도달. new/updated 태그를
            # 기존 선정 사유 앞에 붙여 reason 리스트를 구성한다.
            selected.append((model, novelty_reasons + reasons))
    return selected


def update_history(history: dict, models: list, today: dt.date, keep_days: int = HISTORY_KEEP_DAYS) -> dict:
    """Record today's likes/downloads and drop snapshots older than keep_days."""
    today_str = today.isoformat()
    oldest = today - dt.timedelta(days=keep_days)
    for model in models:
        model_id = model.get("id") or model.get("modelId")
        if not model_id:
            continue
        history.setdefault(model_id, {})[today_str] = {
            "likes": int(model.get("likes") or 0),
            "downloads": int(model.get("downloads") or 0),
        }
    for model_id in list(history):
        entry = history[model_id]
        for date_str in list(entry):
            d = parse_date(date_str)
            if d is None or d < oldest:
                del entry[date_str]
        if not entry:
            del history[model_id]
    return history


# --- rendering --------------------------------------------------------------
REASON_TEXT = {
    "trending": "Hugging Face 트렌딩 상위 %d위 안에 들었습니다" % TRENDING_TOP_N,
    "surge": "최근 %d일 사이 좋아요·다운로드가 급증했습니다" % SURGE_WINDOW_DAYS,
    "major-org": "주요 기관이 최근 %d일 안에 공개한 신작입니다" % MAJOR_ORG_DAYS,
    "new": "최근 %d일 내 최초 공개된 신규 모델입니다" % NEW_MODEL_DAYS,
    "updated": "최근 %d일 내 의미 있는 갱신이 있었습니다" % RECENT_UPDATE_DAYS,
}


def reason_sentence(reasons: list) -> str:
    """One sentence per matched criterion, followed by a closing sentence."""
    parts = [REASON_TEXT.get(r, r) for r in reasons]
    if not parts:
        return "선정 기준에 해당하여 소개합니다."
    return " ".join(p if p.endswith(".") else p + "." for p in parts) + " 이 기준에 해당해 선정했습니다."


def build_meta(detail: dict, reasons: list, discovered_at: str) -> dict:
    model_id = detail.get("id") or detail.get("modelId") or ""
    tags = [t for t in (detail.get("tags") or []) if isinstance(t, str)][:MAX_TAGS]
    created = parse_date(detail.get("createdAt"))
    return {
        "model_id": model_id,
        "title": title_from_id(model_id),
        "org": model_org(model_id),
        "task": detail.get("pipeline_tag") or "other",
        "license": license_from_detail(detail),
        "params": params_from_detail(detail),
        "likes": int(detail.get("likes") or 0),
        "downloads": int(detail.get("downloads") or 0),
        "discovered_at": discovered_at,
        "created_at": created.isoformat() if created else "",
        "hf_url": "%s/%s" % (HF_WEB, model_id),
        "tags": tags,
        "reason": ", ".join(reasons),
    }


COMMERCIAL_LICENSES = {
    "apache-2.0", "mit", "bsd-3-clause", "bsd-2-clause", "cc-by-4.0",
    "cc-by-sa-4.0", "openrail++", "openrail", "llama3.1", "llama3.2",
    "qwen", "qwen-license",
}


def commercial_status(license_id: str) -> str:
    """라이선스의 상업 이용 가능 여부를 한 줄로 반환 (사실 기반)."""
    if not license_id or license_id == "unknown":
        return "라이선스 정보 없음 — 원문 확인 필요"
    key = license_id.strip().lower()
    if key in COMMERCIAL_LICENSES:
        return "상업 이용 가능"
    return "상업 이용 제한 또는 확인 필요"


def build_why_paragraph(meta: dict, reasons: list, published: dict | None = None) -> str:
    """'왜 주목받는가' 문단을 조립한다.

    *meta* 는 build_meta 결과. *published* 는 published.json 의 {"models": {...}}.
    같은 org 의 발행된 다른 모델이 있으면 그 모델과의 비교 문장을,
    없으면 '비교 제공 불가' 안내를 덧붙인다. 모든 정보는 HF API 필드 또는
    published.json 에서만 도출하며, 추정은 붙이지 않는다.
    """
    likes = int(meta.get("likes", 0))
    downloads = int(meta.get("downloads", 0))
    discovered_at = meta.get("discovered_at", "")
    parts = [reason_sentence(reasons)]
    parts.append("좋아요 %s개, 다운로드 %s회(수집 시점 %s)."
                 % (format(likes, ","), format(downloads, ","), discovered_at))
    org = meta.get("org", "")
    self_id = meta.get("model_id", "")
    sibling = None
    if published and org:
        models = published.get("models", {}) if isinstance(published, dict) else {}
        for mid, info in models.items():
            if mid == self_id:
                continue
            if model_org(mid) == org:
                sibling = (mid, info)
                break
    if sibling is not None:
        parts.append("같은 기관(%s)의 다른 발행 모델 %s 와 함께 살펴보세요."
                     % (org, sibling[0]))
    else:
        parts.append("같은 기관의 이전 모델과의 비교는 발행 이력이 부족해 제공하지 않습니다.")
    return " ".join(parts)


def build_related_models(meta: dict, published: dict | None = None, posts_dir: Path | None = None) -> str:
    """같은 org / 같은 task 의 발행된 모델 링크 목록을 마크다운으로 반환.

    *published* 는 published.json {"models": {model_id: {"slug": ..., ...}}}.
    *posts_dir* 는 글 파일이 있는 디렉터리(선택). slug 가 published.json 에 없으면
    파일 존재 여부로 보강한다. 자기 자신과 중복은 제거하고 최대 org 3 + task 3 개.
    """
    if published is None:
        return "아직 관련 모델이 발행되지 않았습니다."
    models = published.get("models", {}) if isinstance(published, dict) else {}
    org = meta.get("org", "")
    task = meta.get("task", "")
    self_id = meta.get("model_id", "")
    self_slug = meta.get("slug") or slugify(self_id)

    def link_for(mid: str, info: dict) -> str | None:
        if mid == self_id:
            return None
        slug = (info or {}).get("slug") or slugify(mid)
        if posts_dir is not None and not (posts_dir / ("%s.md" % slug)).exists():
            return None
        if slug == self_slug:
            return None
        title = title_from_id(mid)
        return "- [%s](../%s/)" % (title, slug)

    seen: set[str] = set()
    lines: list[str] = []

    # 같은 org
    for mid, info in models.items():
        if len(lines) >= 3:
            break
        if model_org(mid) != org:
            continue
        ln = link_for(mid, info)
        if ln and ln not in seen:
            seen.add(ln)
            lines.append(ln)

    # 같은 task
    task_count = 0
    for mid, info in models.items():
        if task_count >= 3:
            break
        ln = link_for(mid, info)
        if ln is None or ln in seen:
            continue
        # task 정보는 published.json 에 없으므로 파일에서 frontmatter를 읽어야 한다.
        if posts_dir is not None:
            slug = (info or {}).get("slug") or slugify(mid)
            p = posts_dir / ("%s.md" % slug)
            if not p.exists():
                continue
            try:
                text = p.read_text(encoding="utf-8")
                fm, _ = parse_frontmatter(text)
                if fm.get("task") != task:
                    continue
            except Exception:
                continue
        else:
            # posts_dir 이 없으면 task 비교를 건너뛴다(과도한 추정 방지).
            continue
        seen.add(ln)
        lines.append(ln)
        task_count += 1

    if not lines:
        return "아직 관련 모델이 발행되지 않았습니다."
    return "\n".join(lines)


def render_post(detail: dict, reasons: list, discovered_at: str, readme_text: str = "",
                published: dict | None = None, posts_dir: Path | None = None) -> str:
    meta = build_meta(detail, reasons, discovered_at)
    assert all(k in meta for k in KEYS)
    params = meta["params"] or "정보 없음"
    created_at = meta["created_at"] or "정보 없음"
    why = build_why_paragraph(meta, reasons, published)
    related = build_related_models(meta, published, posts_dir)
    license_line = "%s — %s" % (meta["license"], commercial_status(meta["license"]))
    spec_rows = [
        ("태스크", "`%s`" % meta["task"]),
        ("파라미터", params),
        ("라이선스", meta["license"]),
        ("최초 등록일", created_at),
        ("좋아요", format(meta["likes"], ",")),
        ("다운로드", format(meta["downloads"], ",")),
    ]
    spec_table = "| 항목 | 값 |\n| --- | --- |\n" + "\n".join("| %s | %s |" % r for r in spec_rows)
    body = "\n".join([
        "## 왜 주목받는가",
        "",
        why,
        "",
        "## 핵심 스펙",
        "",
        spec_table,
        "",
        "## 요약",
        "",
        extract_summary(readme_text),
        "",
        "## 라이선스",
        "",
        license_line,
        "",
        "## 관련 모델",
        "",
        related,
    ])
    return dump_frontmatter(meta, body)


# --- persistence ------------------------------------------------------------
def load_json(path: Path, default):
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")


def _extract_summary_section(body: str) -> str:
    """기존 글 본문에서 '## 요약' 섹션의 내용을 추출한다.

    새 구조의 '## 요약' 헤더부터 다음 '## ' 헤더까지의 텍스트를 반환한다.
    예전 구조(## 요약 → ## 모델 정보 → ## 선정 이유)와 새 구조 모두에서
    요약 블록만 떼어낸다.
    """
    if not body:
        return "모델 카드에 설명이 없습니다."
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## 요약":
            start = i + 1
            break
    if start is None:
        return "모델 카드에 설명이 없습니다."
    block: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        block.append(line)
    text = "\n".join(block).strip("\n")
    return text or "모델 카드에 설명이 없습니다."


def regenerate_local(posts_dir: Path, published_path: Path) -> list[str]:
    """네트워크 없이 기존 글을 새 본문 구조로 재작성한다.

    각 content/models/*.md 의 frontmatter 는 그대로 두고 본문만 교체한다.
    '## 요약' 섹션은 기존 본문에서 추출해 재사용하고, '왜 주목받는가'·
    '핵심 스펙'·'라이선스'·'관련 모델' 은 frontmatter 메타 + published.json
    으로 다시 만든다. HF API 호출은 일절 하지 않는다.
    """
    published = load_json(published_path, {"models": {}})
    published.setdefault("models", {})
    posts_dir = Path(posts_dir)
    rewritten: list[str] = []
    for post_path in sorted(posts_dir.glob("*.md")):
        text = post_path.read_text(encoding="utf-8")
        try:
            meta, body = parse_frontmatter(text)
        except ValueError as exc:
            print("warning: skip %s: %s" % (post_path.name, exc), file=sys.stderr)
            continue
        reasons = [r.strip() for r in (meta.get("reason") or "").split(",") if r.strip()]
        # frontmatter 에는 slug 가 없으므로 model_id 로부터 복원.
        meta_for_render = dict(meta)
        meta_for_render["slug"] = slugify(meta.get("model_id", ""))
        summary_text = _extract_summary_section(body)
        why = build_why_paragraph(meta_for_render, reasons, published)
        related = build_related_models(meta_for_render, published, posts_dir)
        license_line = "%s — %s" % (meta.get("license", "unknown"),
                                   commercial_status(meta.get("license", "unknown")))
        params = meta.get("params") or "정보 없음"
        created_at = meta.get("created_at") or "정보 없음"
        spec_rows = [
            ("태스크", "`%s`" % meta.get("task", "other")),
            ("파라미터", params),
            ("라이선스", meta.get("license", "unknown")),
            ("최초 등록일", created_at),
            ("좋아요", format(int(meta.get("likes") or 0), ",")),
            ("다운로드", format(int(meta.get("downloads") or 0), ",")),
        ]
        spec_table = "| 항목 | 값 |\n| --- | --- |\n" + "\n".join(
            "| %s | %s |" % r for r in spec_rows)
        new_body = "\n".join([
            "## 왜 주목받는가",
            "",
            why,
            "",
            "## 핵심 스펙",
            "",
            spec_table,
            "",
            "## 요약",
            "",
            summary_text,
            "",
            "## 라이선스",
            "",
            license_line,
            "",
            "## 관련 모델",
            "",
            related,
        ])
        new_text = dump_frontmatter(meta, new_body)
        post_path.write_text(new_text, encoding="utf-8")
        rewritten.append(post_path.name)
    return rewritten


# --- main -------------------------------------------------------------------
def gather_candidates(fetcher, config: dict) -> list:
    """Return every model seen across all listings. Raises when even trending is unavailable."""
    trending = list_trending(fetcher, limit=50)
    by_id: dict = {}
    for rank, model in enumerate(trending, start=1):
        model = dict(model)
        model["trending_rank"] = rank
        by_id[model["id"]] = model

    def merge(models):
        for model in models:
            mid = model.get("id")
            if not mid:
                continue
            if mid in by_id:
                for k, v in model.items():
                    by_id[mid].setdefault(k, v)
            else:
                by_id[mid] = dict(model)

    for sort in ("likes", "downloads"):
        try:
            merge(list_top(fetcher, sort, limit=100))
        except FETCH_ERRORS as exc:
            print("warning: top-%s listing failed: %s" % (sort, exc), file=sys.stderr)
    for org in config["major_orgs"]:
        try:
            merge(list_recent_by_org(org, fetcher, limit=20))
        except FETCH_ERRORS as exc:
            print("warning: listing for %s failed: %s" % (org, exc), file=sys.stderr)
    return list(by_id.values())


def write_summary(stats: dict, path: Path | None = None) -> str:
    """실행 요약 마크다운을 반환하고 path가 주어지면 파일에 추가 기록."""
    lines = [
        "## 수집 실행 요약",
        "",
        "| 항목 | 값 |",
        "| --- | --- |",
        f"| 수집 일시 | {stats.get('today','')} |",
        f"| 후보 모델 수 | {stats.get('candidates',0)} |",
        f"| 신규 발행 | {stats.get('new_posts',0)} |",
        f"| 제외(신규성 게이트) | {stats.get('excluded',0)} |",
        f"| 누적 발행 모델 | {stats.get('total_published',0)} |",
    ]
    md = "\n".join(lines) + "\n"
    if path is not None:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(md)
    return md


def run(content_dir: Path, data_dir: Path, max_new: int, dry_run: bool, today: dt.date,
        fetcher=None, config: dict | None = None) -> list:
    fetcher = fetcher or default_fetcher
    cfg = dict(DEFAULT_CONFIG)
    if config:
        cfg.update(config)
    history_path = data_dir / "stats_history.json"
    published_path = data_dir / "published.json"
    history = load_json(history_path, {})
    published = load_json(published_path, {"models": {}})
    published.setdefault("models", {})

    candidates = gather_candidates(fetcher, cfg)
    selected = select_famous(candidates, history, today, cfg)

    new_posts = []
    for model, reasons in selected:
        if len(new_posts) >= max_new:
            break
        model_id = model["id"]
        slug = slugify(model_id)
        post_path = content_dir / ("%s.md" % slug)
        if model_id in published["models"] or post_path.exists():
            continue
        if dry_run:
            print("%s\t%s\t%s" % (model_id, ", ".join(reasons), post_path))
            new_posts.append(model_id)
            continue
        try:
            detail = fetch_model_detail(model_id, fetcher)
            readme = fetch_readme(model_id, fetcher)
            text = render_post(detail, reasons, today.isoformat(), readme,
                               published=published, posts_dir=content_dir)
        except POST_ERRORS as exc:
            print("warning: skipping %s: %s" % (model_id, exc), file=sys.stderr)
            continue
        content_dir.mkdir(parents=True, exist_ok=True)
        post_path.write_text(text, encoding="utf-8")
        published["models"][model_id] = {"slug": slug, "published_at": today.isoformat()}
        new_posts.append(model_id)
        print(post_path)

    if not dry_run:
        update_history(history, candidates, today)
        save_json(history_path, history)
        save_json(published_path, published)
    if not new_posts:
        print("No new models")

    stats = {
        "today": today.isoformat(),
        "candidates": len(candidates),
        "new_posts": len(new_posts),
        "excluded": len(candidates) - len(selected),
        "total_published": len(published["models"]),
    }
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        try:
            write_summary(stats, Path(summary_path))
        except OSError as exc:
            print("warning: failed to write step summary: %s" % exc, file=sys.stderr)

    return new_posts


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Collect notable Hugging Face models into markdown posts.")
    parser.add_argument("--content-dir", default="content/models")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--max-new", type=int, default=25)
    parser.add_argument("--dry-run", action="store_true", help="print the selection without writing files")
    parser.add_argument("--today", default=None, help="override today's date (YYYY-MM-DD)")
    parser.add_argument("--regenerate", action="store_true",
                        help="rewrite existing content/models/*.md in the new body layout (no network)")
    args = parser.parse_args(argv)
    if args.regenerate:
        return 0 if regenerate_local(Path(args.content_dir), Path(args.data_dir) / "published.json") else 1
    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.timezone.utc).date()
    try:
        run(Path(args.content_dir), Path(args.data_dir), args.max_new, args.dry_run, today)
    except Exception as exc:  # noqa: BLE001 - CLI boundary: any failure must become exit code 1
        print("error: collection failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
