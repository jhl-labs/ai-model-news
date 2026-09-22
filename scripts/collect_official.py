#!/usr/bin/env python3
"""Collect model launches from Anthropic's official, dated release notes."""
from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.collect import atomic_write_text, default_fetcher, load_json, save_json
from scripts.frontmatter import dump_frontmatter, parse_frontmatter, slugify

SOURCE_URL = "https://support.claude.com/en/articles/12138966-release-notes"
MODEL_NAME = re.compile(r"Claude\s+([A-Z][A-Za-z]+)\s+(\d+(?:\.\d+)*)")


class ReleaseNotesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.current = None
        self.tag = None
        self.text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h3", "p"):
            self.tag, self.text, self.links = tag, [], []
        if tag == "a" and self.tag:
            url = dict(attrs).get("href", "")
            parsed = urlparse(url)
            if parsed.scheme == "https" and parsed.hostname in ("www.anthropic.com", "anthropic.com"):
                self.links.append(url)

    def handle_data(self, data):
        if self.tag:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag != self.tag:
            return
        text = " ".join("".join(self.text).split())
        if tag == "h3":
            try:
                date = dt.datetime.strptime(text, "%B %d, %Y").date()
            except ValueError:
                self.current = None
            else:
                self.current = {"date": date, "paragraphs": [], "links": []}
                self.entries.append(self.current)
        elif self.current is not None:
            self.current["paragraphs"].append(text)
            self.current["links"].extend(self.links)
        self.tag = None


def parse_launches(text: str, today: dt.date) -> list[dict]:
    parser = ReleaseNotesParser()
    parser.feed(text)
    if not parser.entries:
        raise ValueError("official release notes have no dated entries; check source format")
    launches = {}
    for entry in parser.entries:
        if not 0 <= (today - entry["date"]).days <= 60:
            continue
        # Only the release heading identifies models. Body comparisons and future
        # roadmap mentions must never be treated as launches.
        paragraphs = [p for p in entry["paragraphs"] if p]
        launch_title = MODEL_NAME.pattern + r"(?: and " + MODEL_NAME.pattern + r")* launch"
        if not paragraphs or not re.fullmatch(launch_title, paragraphs[0]):
            continue
        for family, version in MODEL_NAME.findall(paragraphs[0]):
            mid = "Anthropic/claude-" + family.lower() + "-" + version.replace(".", "-")
            record = {"model_id": mid, "title": f"Claude {family} {version}",
                      "date": entry["date"].isoformat(),
                      "url": entry["links"][0] if entry["links"] else SOURCE_URL}
            # Prefer the original launch if a later entry repeats the model.
            if mid not in launches or record["date"] < launches[mid]["date"]:
                launches[mid] = record
    return sorted(launches.values(), key=lambda record: record["date"], reverse=True)


def render_launch(record: dict, today: dt.date) -> str:
    meta = dict(model_id=record["model_id"], title=record["title"], org="Anthropic",
                task="text-generation", license="unknown", params="", likes=0, downloads=0,
                discovered_at=today.isoformat(), created_at=record["date"], hf_url="",
                tags=["Claude", "official-release"], reason="new, official-release",
                source="official", source_url=record["url"])
    body = (f"## 공식 출시\n\nAnthropic 공식 릴리스 노트의 {record['date']} 출시 항목에서 "
            f"**{record['title']}** 발표를 확인했습니다.\n\n"
            "## 확인된 정보\n\n"
            f"| 항목 | 값 |\n| --- | --- |\n| 모델 | {record['title']} |\n"
            f"| 발표 기관 | Anthropic |\n| 공식 발표일 | {record['date']} |\n\n"
            "## 이용 정보\n\n제공 채널, 요금, 이용 조건과 모델 사양은 아래 공식 발표에서 확인할 수 있습니다. "
            "이 글에는 Hugging Face 다운로드·좋아요 통계를 적용하지 않습니다.\n\n"
            f"## 출처\n\n- [공식 발표]({record['url']})\n"
            f"- [Anthropic 공식 릴리스 노트]({SOURCE_URL})\n")
    return dump_frontmatter(meta, body)


def run(content_dir: Path, data_dir: Path, today: dt.date, *, fetcher=default_fetcher,
        dry_run: bool = False, max_new: int = 25) -> list[str]:
    if max_new < 0:
        raise ValueError("--max-new must be non-negative")
    launches = parse_launches(fetcher(SOURCE_URL), today)
    state_path = data_dir / "published.json"
    state = load_json(state_path, {"models": {}})
    new = []
    for record in launches:
        if len(new) >= max_new:
            break
        mid = record["model_id"]
        slug = slugify(mid)
        path = content_dir / (slug + ".md")
        if mid in state["models"]:
            continue
        if path.exists():
            meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
            if meta.get("model_id") != mid or meta.get("source") != "official":
                raise ValueError(f"existing content conflicts with official model: {mid}")
            if not dry_run:
                state["models"][mid] = {"slug": slug, "published_at": meta["discovered_at"],
                                        "source": "official"}
                save_json(state_path, state)
            continue
        if not dry_run:
            atomic_write_text(path, render_launch(record, today))
            state["models"][mid] = {"slug": slug, "published_at": today.isoformat(), "source": "official"}
            save_json(state_path, state)
        new.append(mid)
        print(path)
    print(f"Official releases: {len(launches)} detected, {len(new)} new")
    return new


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--content-dir", type=Path, default=Path("content/models"))
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-new", type=int, default=25)
    args = ap.parse_args(argv)
    try:
        run(args.content_dir, args.data_dir, dt.datetime.now(dt.timezone.utc).date(),
            dry_run=args.dry_run, max_new=args.max_new)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: official collection failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
