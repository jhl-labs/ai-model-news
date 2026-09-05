import unittest

from scripts.frontmatter import KEYS, dump_frontmatter, parse_frontmatter, slugify


def sample_meta():
    return {
        "model_id": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
        "title": "Llama 4 Scout 17B 16E Instruct",
        "org": "meta-llama",
        "task": "text-generation",
        "license": "llama4",
        "params": "17B",
        "likes": 1234,
        "downloads": 567890,
        "discovered_at": "2026-09-05",
        "created_at": "2026-09-01",
        "hf_url": "https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct",
        "tags": ["transformers", "safetensors", "llama4"],
        "reason": "trending, major-org",
    }


class SlugifyTests(unittest.TestCase):
    def test_org_separator_becomes_double_dash(self):
        self.assertEqual(slugify("meta-llama/Llama-4-Scout"), "meta-llama--llama-4-scout")

    def test_lowercase_and_special_chars_collapsed(self):
        self.assertEqual(slugify("Qwen/Qwen3.8_27B  (Instruct)"), "qwen--qwen3.8-27b-instruct")

    def test_strips_leading_trailing_dashes(self):
        self.assertEqual(slugify("-org-/-name-"), "org--name")


class ParseDumpTests(unittest.TestCase):
    def test_roundtrip_preserves_meta_and_body(self):
        meta = sample_meta()
        body = "## 요약\n\n설명 **굵게** `code`\n\n- 항목\n"
        text = dump_frontmatter(meta, body)
        parsed, parsed_body = parse_frontmatter(text)
        self.assertEqual(parsed, meta)
        self.assertEqual(parsed_body.strip(), body.strip())

    def test_dump_key_order_and_json_literals(self):
        text = dump_frontmatter(sample_meta(), "body")
        lines = text.split("\n")
        self.assertEqual(lines[0], "---")
        self.assertEqual([l.split(":")[0] for l in lines[1:14]], KEYS)
        self.assertEqual(lines[14], "---")
        self.assertIn('title: "Llama 4 Scout 17B 16E Instruct"', lines)
        self.assertIn("likes: 1234", lines)
        self.assertIn('tags: ["transformers", "safetensors", "llama4"]', lines)

    def test_dump_rejects_missing_keys(self):
        meta = sample_meta()
        del meta["reason"]
        with self.assertRaises(ValueError):
            dump_frontmatter(meta, "")

    def test_parse_invalid_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_frontmatter("no frontmatter here")
        with self.assertRaises(ValueError):
            parse_frontmatter("---\nmodel_id: \"x\"\n")  # unterminated
        with self.assertRaises(ValueError):
            parse_frontmatter("---\nmodel_id: not json\n---\n")

    def test_parse_handles_colon_inside_value(self):
        meta, body = parse_frontmatter('---\nhf_url: "https://huggingface.co/a/b"\n---\nhello\n')
        self.assertEqual(meta["hf_url"], "https://huggingface.co/a/b")
        self.assertEqual(body.strip(), "hello")


if __name__ == "__main__":
    unittest.main()
