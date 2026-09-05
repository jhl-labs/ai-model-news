"""Frontmatter helpers shared by the collector and the site builder.

Format (each value is a JSON literal, one key per line):

    ---
    model_id: "org/name"
    title: "Name"
    ...
    ---
    (markdown body)

Only the Python standard library is used.
"""
from __future__ import annotations

import json
import re

# Fixed key order for dump_frontmatter. Every key must always be present.
KEYS = [
    "model_id",
    "title",
    "org",
    "task",
    "license",
    "params",
    "likes",
    "downloads",
    "discovered_at",
    "created_at",
    "hf_url",
    "tags",
    "reason",
]

DELIM = "---"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split *text* into (meta, body).

    Raises ValueError when the frontmatter block is missing, unterminated,
    contains a line without ``key: <json>`` shape, or a value is not valid JSON.
    """
    if not isinstance(text, str):
        raise ValueError("frontmatter text must be a string")
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r") != DELIM:
        raise ValueError("frontmatter must start with '---' on the first line")
    meta: dict = {}
    end = None
    for idx in range(1, len(lines)):
        line = lines[idx].rstrip("\r")
        if line == DELIM:
            end = idx
            break
        if not line.strip():
            raise ValueError("blank line inside frontmatter (line %d)" % (idx + 1))
        key, sep, raw = line.partition(":")
        key = key.strip()
        if not sep or not key or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError("invalid frontmatter line %d: %r" % (idx + 1, line))
        try:
            value = json.loads(raw.strip())
        except json.JSONDecodeError as exc:
            raise ValueError("invalid JSON value for key %r: %s" % (key, exc)) from exc
        meta[key] = value
    if end is None:
        raise ValueError("frontmatter is not terminated by '---'")
    body = "\n".join(lines[end + 1:])
    return meta, body


def dump_frontmatter(meta: dict, body: str) -> str:
    """Serialize *meta* (all KEYS required) followed by *body*.

    Keys are written in the fixed KEYS order; values via json.dumps.
    """
    missing = [k for k in KEYS if k not in meta]
    if missing:
        raise ValueError("missing frontmatter keys: %s" % ", ".join(missing))
    out = [DELIM]
    for key in KEYS:
        out.append("%s: %s" % (key, json.dumps(meta[key], ensure_ascii=False)))
    out.append(DELIM)
    head = "\n".join(out) + "\n"
    body = (body or "").strip("\n")
    if not body:
        return head
    return head + "\n" + body + "\n"


def slugify(model_id: str) -> str:
    """Turn ``org/name`` into the content file slug shared with build.py.

    Contract: ``/`` becomes two underscores; every other character outside
    ``A-Za-z0-9 . _ -`` becomes a single ``-``. Case is preserved.
    Example: ``meta-llama/Llama-4-Scout`` -> ``meta-llama__Llama-4-Scout``.
    """
    slug = model_id.strip().replace("/", "__")
    return re.sub(r"[^A-Za-z0-9._-]", "-", slug)
