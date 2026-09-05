#!/usr/bin/env python3
"""AI Model News static site generator.

Reads ``content/models/*.md`` (front matter + markdown subset) and writes a
complete static site (index, model detail pages, about, RSS, sitemap) into an
output directory. Python standard library only.

Usage::

    python3 scripts/build.py --content-dir content/models --out dist \
        [--site-url https://example.org/base/] [--build-date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
from email.utils import format_datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if __package__ in (None, ""):
    # Allow `python3 scripts/build.py` from the repository root.
    sys.path.insert(0, str(ROOT))

from scripts.frontmatter import slugify as _slugify  # noqa: E402

if __package__ in (None, ""):
    # Allow `python3 scripts/build.py` from the repository root.
    sys.path.insert(0, str(ROOT))

from scripts.frontmatter import slugify  # noqa: E402  (single slug contract shared with collect.py)
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"

SITE_NAME = "AI Model News"
SITE_TAGLINE = "Hugging Face 에서 주목받는 모델 소식"
SITE_DESCRIPTION = (
    "Hugging Face 에서 트렌딩·급상승·주요 기관 신작으로 주목받는 AI 모델 소식을 "
    "매일 자동으로 수집해 전하는 기술 블로그"
)
DEFAULT_SITE_URL = "https://jhl-labs.github.io/ai-model-news/"
REPO_URL = "https://github.com/jhl-labs/ai-model-news"
FEED_LIMIT = 50

REQUIRED_KEYS: dict[str, tuple[type, ...]] = {
    "model_id": (str,),
    "title": (str,),
    "org": (str,),
    "task": (str,),
    "license": (str,),
    "params": (str,),
    "likes": (int,),
    "downloads": (int,),
    "discovered_at": (str,),
    "created_at": (str,),
    "hf_url": (str,),
    "tags": (list,),
    "reason": (str,),
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------
# Front matter parsing
# --------------------------------------------------------------------------
def parse_post(path: Path | str) -> dict[str, Any]:
    """Parse a content file into a dict. Raises ValueError on bad input."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing opening '---'")
    meta: dict[str, Any] = {}
    end = None
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            end = i
            break
        if not line.strip():
            continue
        key, sep, raw = line.partition(":")
        key = key.strip()
        if not sep or not key:
            raise ValueError(f"{path}:{i + 1}: expected 'key: <json>'")
        try:
            meta[key] = json.loads(raw.strip())
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{i + 1}: invalid JSON for {key!r}: {exc}") from exc
    if end is None:
        raise ValueError(f"{path}: missing closing '---'")

    missing = [k for k in REQUIRED_KEYS if k not in meta]
    if missing:
        raise ValueError(f"{path}: missing keys: {', '.join(missing)}")
    for key, types in REQUIRED_KEYS.items():
        value = meta[key]
        if isinstance(value, bool) or not isinstance(value, types):
            raise ValueError(f"{path}: key {key!r} has wrong type {type(value).__name__}")
    if not all(isinstance(t, str) for t in meta["tags"]):
        raise ValueError(f"{path}: 'tags' must be a list of strings")
    if not DATE_RE.match(meta["discovered_at"]):
        raise ValueError(f"{path}: 'discovered_at' must be YYYY-MM-DD")
    if meta["created_at"] and not DATE_RE.match(meta["created_at"]):
        raise ValueError(f"{path}: 'created_at' must be YYYY-MM-DD or empty")
    if not meta["model_id"]:
        raise ValueError(f"{path}: 'model_id' must not be empty")

    post = dict(meta)
    post["body"] = "\n".join(lines[end + 1:]).strip("\n")
    post["slug"] = slugify(post["model_id"])
    post["source"] = str(path.name)
    return post


# --------------------------------------------------------------------------
# Minimal markdown converter (escape first, then apply markup)
# --------------------------------------------------------------------------
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def _safe_href(url: str) -> str:
    """Allow only http(s), mailto, relative and anchor URLs."""
    lowered = url.strip().lower()
    if lowered.startswith(("http://", "https://", "mailto:", "/", "#", "./", "../")):
        return url
    return "#"


def render_inline(text: str) -> str:
    """Escape *text* and then convert inline markdown markup."""
    escaped = html.escape(text, quote=True)
    # Inline code first so that markup inside code is left untouched.
    parts = []
    last = 0
    for m in _INLINE_CODE_RE.finditer(escaped):
        parts.append(_render_inline_rest(escaped[last:m.start()]))
        parts.append(f"<code>{m.group(1)}</code>")
        last = m.end()
    parts.append(_render_inline_rest(escaped[last:]))
    return "".join(parts)


def _render_inline_rest(s: str) -> str:
    s = _LINK_RE.sub(
        lambda m: f'<a href="{html.escape(_safe_href(html.unescape(m.group(2))), quote=True)}">{m.group(1)}</a>',
        s,
    )
    s = _BOLD_RE.sub(r"<strong>\1</strong>", s)
    return s


def markdown_to_html(md: str) -> str:
    """Convert the supported markdown subset to HTML."""
    out: list[str] = []
    paragraph: list[str] = []
    in_list = False

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + " ".join(render_inline(l) for l in paragraph) + "</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in md.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            out.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            continue
        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet:
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{render_inline(bullet.group(1))}</li>")
            continue
        close_list()
        paragraph.append(stripped)
    flush_paragraph()
    close_list()
    return "\n".join(out)


def summarize(md: str, limit: int = 200) -> str:
    """Plain-text summary: first paragraph, markup stripped."""
    for block in re.split(r"\n\s*\n", md.strip()):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines or lines[0].startswith("#"):
            continue
        text = " ".join(lines)
        text = re.sub(r"^[-*]\s+", "", text)
        text = _LINK_RE.sub(r"\1", text)
        text = text.replace("**", "").replace("`", "")
        if len(text) > limit:
            text = text[: limit - 1].rstrip() + "…"
        return text
    return ""


# --------------------------------------------------------------------------
# Template helpers
# --------------------------------------------------------------------------
_TEMPLATE_CACHE: dict[str, str] = {}


def load_template(name: str) -> str:
    if name not in _TEMPLATE_CACHE:
        _TEMPLATE_CACHE[name] = (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    return _TEMPLATE_CACHE[name]


_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


def render(template: str, **ctx: Any) -> str:
    """Replace ``{{name}}`` placeholders. Values are inserted verbatim, so callers
    must escape untrusted text themselves (use :func:`esc`)."""

    def sub(m: re.Match[str]) -> str:
        key = m.group(1)
        if key not in ctx:
            raise KeyError(f"template placeholder {{{{{key}}}}} not provided")
        return str(ctx[key])

    return _PLACEHOLDER_RE.sub(sub, template)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def format_count(n: int) -> str:
    """1234 -> 1.2k, 3400000 -> 3.4M."""
    n = int(n)
    for unit, div in (("B", 1_000_000_000), ("M", 1_000_000), ("k", 1_000)):
        if n >= div:
            val = n / div
            s = f"{val:.1f}".rstrip("0").rstrip(".")
            return f"{s}{unit}"
    return str(n)


def join_url(base: str, rel: str) -> str:
    if not base.endswith("/"):
        base += "/"
    return base + rel.lstrip("/")


def sort_posts(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(posts, key=lambda p: (p["discovered_at"], p["likes"]), reverse=True)


def load_posts(content_dir: Path) -> list[dict[str, Any]]:
    posts = []
    if content_dir.is_dir():
        for path in sorted(content_dir.glob("*.md")):
            posts.append(parse_post(path))
    return sort_posts(posts)


# --------------------------------------------------------------------------
# Page rendering
# --------------------------------------------------------------------------
def render_page(*, rel: str, title: str, description: str, canonical: str,
                body: str, site_url: str, build_date: str, page_class: str = "") -> str:
    """Wrap *body* into the base layout. *rel* is the relative prefix to the
    site root ('' for index, '../../' for detail pages)."""
    return render(
        load_template("base.html"),
        rel=rel,
        site_name=esc(SITE_NAME),
        site_tagline=esc(SITE_TAGLINE),
        page_title=esc(title),
        page_description=esc(description),
        canonical=esc(canonical),
        feed_url=esc(join_url(site_url, "feed.xml")),
        repo_url=esc(REPO_URL),
        body=body,
        build_date=esc(build_date),
        page_class=esc(page_class),
    )


def relative_date(date_str: str, build_date: str) -> str:
    d = dt.date.fromisoformat(date_str)
    b = dt.date.fromisoformat(build_date)
    delta = (b - d).days
    if delta <= 0:
        return "오늘"
    if delta == 1:
        return "1일 전"
    return f"{delta}일 전"


def card_badges(post: dict[str, Any], build_date: str) -> list[tuple[str, str]]:
    """Return [(css_class, label), ...] for a post card."""
    badges: list[tuple[str, str]] = []
    reasons = [r.strip() for r in post.get("reason", "").split(",") if r.strip()]
    if "new" in reasons:
        badges.append(("badge-new", "신규"))
    if "updated" in reasons:
        badges.append(("badge-updated", "갱신"))
    if "surge" in reasons:
        badges.append(("badge-surge", "급상승"))
    # "new" 가 reason 에 없으면 created_at 으로 유추(60일 이내).
    if "new" not in reasons and post.get("created_at"):
        try:
            created = dt.date.fromisoformat(post["created_at"])
            bdate = dt.date.fromisoformat(build_date)
            if 0 <= (bdate - created).days <= 60:
                badges.append(("badge-new", "신규"))
        except ValueError:
            pass
    return badges


def render_card(post: dict[str, Any], build_date: str = "") -> str:
    search = " ".join([post["model_id"], post["title"], *post["tags"]]).lower()
    reasons = [r.strip() for r in post["reason"].split(",") if r.strip()]
    reason_html = "".join(f'<span class="tag tag-reason">{esc(r)}</span>' for r in reasons)
    params = esc(post["params"]) if post["params"] else "—"
    badges = card_badges(post, build_date) if build_date else []
    badges_html = "".join(
        f'<span class="badge {cls}">{esc(label)}</span>' for cls, label in badges
    )
    rel = relative_date(post["discovered_at"], build_date) if build_date else post["discovered_at"]
    return render(
        load_template("card.html"),
        slug=esc(post["slug"]),
        org=esc(post["org"]),
        task=esc(post["task"]),
        search=esc(search),
        title=esc(post["title"]),
        model_id=esc(post["model_id"]),
        params=params,
        license=esc(post["license"]),
        likes=esc(format_count(post["likes"])),
        likes_full=esc(f"{post['likes']:,}"),
        downloads=esc(format_count(post["downloads"])),
        downloads_full=esc(f"{post['downloads']:,}"),
        discovered_at=esc(post["discovered_at"]),
        relative_date=esc(rel),
        badges=badges_html,
        reasons=reason_html,
    )


def render_index(posts: list[dict[str, Any]], site_url: str, build_date: str) -> str:
    task_counts: dict[str, int] = {}
    orgs: dict[str, int] = {}
    for p in posts:
        task_counts[p["task"]] = task_counts.get(p["task"], 0) + 1
        orgs[p["org"]] = orgs.get(p["org"], 0) + 1

    chips = [
        f'<button type="button" class="chip is-active" data-task="" aria-pressed="true">'
        f'전체 <span class="chip-count">{len(posts)}</span></button>'
    ]
    for task, n in sorted(task_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        chips.append(
            f'<button type="button" class="chip" data-task="{esc(task)}" aria-pressed="false">'
            f'{esc(task)} <span class="chip-count">{n}</span></button>'
        )
    org_options = ['<option value="">모든 기관</option>']
    for org, n in sorted(orgs.items(), key=lambda kv: (-kv[1], kv[0].lower())):
        org_options.append(f'<option value="{esc(org)}">{esc(org)} ({n})</option>')

    # 하이라이트: discovered_at 이 build_date 기준 3일(72시간) 이내, likes 상위 3개.
    bdate = dt.date.fromisoformat(build_date)
    highlight_pool = [
        p for p in posts
        if 0 <= (bdate - dt.date.fromisoformat(p["discovered_at"])).days <= 3
    ]
    highlight_posts = sorted(highlight_pool, key=lambda p: p["likes"], reverse=True)[:3]

    # 급상승: reason 에 "surge" 포함, likes 상위 5개(하이라이트와 중복 허용).
    surge_posts = [
        p for p in posts
        if "surge" in [r.strip() for r in p.get("reason", "").split(",")]
    ]
    surge_posts = sorted(surge_posts, key=lambda p: p["likes"], reverse=True)[:5]

    if posts:
        cards = "\n".join(render_card(p, build_date) for p in posts)
        last_update = max(p["discovered_at"] for p in posts)
    else:
        cards = ""
        last_update = "—"

    highlights_html = "\n".join(render_card(p, build_date) for p in highlight_posts)
    surges_html = "\n".join(render_card(p, build_date) for p in surge_posts)

    body = render(
        load_template("index.html"),
        site_tagline=esc(SITE_TAGLINE),
        model_count=len(posts),
        last_update=esc(last_update),
        chips="\n".join(chips),
        org_options="\n".join(org_options),
        cards=cards,
        highlights=highlights_html,
        surges=surges_html,
        highlights_hidden="" if highlight_posts else " hidden",
        surges_hidden="" if surge_posts else " hidden",
        empty_hidden="" if not posts else " hidden",
        filters_hidden=" hidden" if not posts else "",
    )
    return render_page(
        rel="",
        title=f"{SITE_NAME} — {SITE_TAGLINE}",
        description=SITE_DESCRIPTION,
        canonical=site_url if site_url.endswith("/") else site_url + "/",
        body=body,
        site_url=site_url,
        build_date=build_date,
        page_class="page-index",
    )


def render_detail(post: dict[str, Any], prev_post: dict[str, Any] | None,
                  next_post: dict[str, Any] | None, site_url: str, build_date: str) -> str:
    rel = "../../"
    tags_html = "".join(f'<li class="tag">{esc(t)}</li>' for t in post["tags"]) or \
        '<li class="tag tag-muted">태그 없음</li>'
    reasons = [r.strip() for r in post["reason"].split(",") if r.strip()]
    reason_html = "".join(f'<span class="tag tag-reason">{esc(r)}</span>' for r in reasons)

    def nav_link(p: dict[str, Any] | None, cls: str, label: str) -> str:
        if p is None:
            return f'<span class="pager-link is-disabled {cls}"><span class="pager-label">{label}</span><span class="pager-title">없음</span></span>'
        return (
            f'<a class="pager-link {cls}" href="../{esc(p["slug"])}/" rel="{"prev" if cls == "pager-prev" else "next"}">'
            f'<span class="pager-label">{label}</span><span class="pager-title">{esc(p["title"])}</span></a>'
        )

    body = render(
        load_template("detail.html"),
        title=esc(post["title"]),
        model_id=esc(post["model_id"]),
        org=esc(post["org"]),
        task=esc(post["task"]),
        params=esc(post["params"]) if post["params"] else "—",
        license=esc(post["license"]),
        likes=esc(f"{post['likes']:,}"),
        downloads=esc(f"{post['downloads']:,}"),
        created_at=esc(post["created_at"]) if post["created_at"] else "—",
        discovered_at=esc(post["discovered_at"]),
        hf_url=esc(_safe_href(post["hf_url"])),
        content=markdown_to_html(post["body"]) or "<p>본문이 없습니다.</p>",
        tags=tags_html,
        reasons=reason_html,
        prev_link=nav_link(prev_post, "pager-prev", "이전 모델"),
        next_link=nav_link(next_post, "pager-next", "다음 모델"),
    )
    desc = summarize(post["body"]) or f"{post['org']} 의 {post['task']} 모델 {post['model_id']}"
    return render_page(
        rel=rel,
        title=f"{post['title']} — {SITE_NAME}",
        description=desc,
        canonical=join_url(site_url, f"models/{post['slug']}/"),
        body=body,
        site_url=site_url,
        build_date=build_date,
        page_class="page-detail",
    )


def render_about(site_url: str, build_date: str) -> str:
    body = render(load_template("about.html"), repo_url=esc(REPO_URL))
    return render_page(
        rel="../",
        title=f"About — {SITE_NAME}",
        description="AI Model News 의 목적과 '유명 모델' 선정 기준, 데이터 출처를 설명합니다.",
        canonical=join_url(site_url, "about/"),
        body=body,
        site_url=site_url,
        build_date=build_date,
        page_class="page-about",
    )


def render_404(site_url: str, build_date: str) -> str:
    body = render(load_template("404.html"), site_root=esc(site_url))
    # 404.html is served from arbitrary depth on GitHub Pages, so use absolute asset URLs.
    page = render_page(
        rel=site_url if site_url.endswith("/") else site_url + "/",
        title=f"페이지를 찾을 수 없습니다 — {SITE_NAME}",
        description="요청한 페이지가 존재하지 않습니다.",
        canonical=join_url(site_url, "404.html"),
        body=body,
        site_url=site_url,
        build_date=build_date,
        page_class="page-404",
    )
    return page


# --------------------------------------------------------------------------
# Feeds
# --------------------------------------------------------------------------
def _rfc822(date_str: str) -> str:
    d = dt.date.fromisoformat(date_str)
    return format_datetime(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc))


def render_feed(posts: list[dict[str, Any]], site_url: str, build_date: str) -> str:
    items = []
    for p in posts[:FEED_LIMIT]:
        url = join_url(site_url, f"models/{p['slug']}/")
        summary_html = markdown_to_html(p["body"]) or f"<p>{esc(p['title'])}</p>"
        summary_html = summary_html.replace("]]>", "]]]]><![CDATA[>")
        items.append(
            "    <item>\n"
            f"      <title>{esc(p['title'])}</title>\n"
            f"      <link>{esc(url)}</link>\n"
            f'      <guid isPermaLink="true">{esc(url)}</guid>\n'
            f"      <pubDate>{_rfc822(p['discovered_at'])}</pubDate>\n"
            f"      <category>{esc(p['task'])}</category>\n"
            f"      <category>{esc(p['org'])}</category>\n"
            f"      <description><![CDATA[{summary_html}]]></description>\n"
            "    </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{esc(SITE_NAME)}</title>\n"
        f"    <link>{esc(site_url)}</link>\n"
        f"    <description>{esc(SITE_TAGLINE)}</description>\n"
        "    <language>ko</language>\n"
        f"    <lastBuildDate>{_rfc822(build_date)}</lastBuildDate>\n"
        f'    <atom:link href="{esc(join_url(site_url, "feed.xml"))}" rel="self" type="application/rss+xml"/>\n'
        + ("\n".join(items) + "\n" if items else "")
        + "  </channel>\n</rss>\n"
    )


def render_sitemap(posts: list[dict[str, Any]], site_url: str, build_date: str) -> str:
    entries = [(site_url if site_url.endswith("/") else site_url + "/", build_date),
               (join_url(site_url, "about/"), build_date)]
    entries += [(join_url(site_url, f"models/{p['slug']}/"), p["discovered_at"]) for p in posts]
    urls = "".join(
        f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{esc(mod)}</lastmod>\n  </url>\n"
        for loc, mod in entries
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n"
    )


def render_robots(site_url: str) -> str:
    return f"User-agent: *\nAllow: /\nSitemap: {join_url(site_url, 'sitemap.xml')}\n"


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def build(content_dir: Path, out: Path, site_url: str = DEFAULT_SITE_URL,
          build_date: str | None = None) -> list[dict[str, Any]]:
    if not site_url.endswith("/"):
        site_url += "/"
    build_date = build_date or dt.date.today().isoformat()
    if not DATE_RE.match(build_date):
        raise ValueError("--build-date must be YYYY-MM-DD")

    posts = load_posts(Path(content_dir))
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)

    (out / "index.html").write_text(render_index(posts, site_url, build_date), encoding="utf-8")
    models_dir = out / "models"
    models_dir.mkdir(exist_ok=True)
    for i, p in enumerate(posts):
        prev_post = posts[i - 1] if i > 0 else None       # newer
        next_post = posts[i + 1] if i + 1 < len(posts) else None  # older
        d = models_dir / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            render_detail(p, prev_post, next_post, site_url, build_date), encoding="utf-8")
    about_dir = out / "about"
    about_dir.mkdir(exist_ok=True)
    (about_dir / "index.html").write_text(render_about(site_url, build_date), encoding="utf-8")
    (out / "404.html").write_text(render_404(site_url, build_date), encoding="utf-8")
    (out / "feed.xml").write_text(render_feed(posts, site_url, build_date), encoding="utf-8")
    (out / "sitemap.xml").write_text(render_sitemap(posts, site_url, build_date), encoding="utf-8")
    (out / "robots.txt").write_text(render_robots(site_url), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    assets = out / "assets"
    assets.mkdir(exist_ok=True)
    for name in ("style.css", "app.js"):
        shutil.copyfile(STATIC_DIR / name, assets / name)
    return posts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the AI Model News static site.")
    ap.add_argument("--content-dir", default="content/models", type=Path)
    ap.add_argument("--out", default="dist", type=Path)
    ap.add_argument("--site-url", default=DEFAULT_SITE_URL)
    ap.add_argument("--build-date", default=None, help="YYYY-MM-DD (default: today)")
    args = ap.parse_args(argv)
    try:
        posts = build(args.content_dir, args.out, args.site_url, args.build_date)
    except ValueError as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1
    print(f"built {len(posts)} model page(s) into {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
