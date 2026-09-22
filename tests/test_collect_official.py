import datetime as dt
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest

from scripts import build, collect, collect_official as official
from scripts.frontmatter import parse_frontmatter

TODAY = dt.date(2026, 9, 23)
# Synthetic markup mirrors the official dated heading/paragraph structure.
NOTES = '''<h3>September 22, 2026</h3>
<p><b>Claude Opus 5.5 launch</b></p>
<p>Compare with Claude Opus 5. Future Claude Sonnet 5.5 will follow.
<a href="https://www.anthropic.com/claude-opus-5-5">Announcement</a></p>
<h3>September 15, 2026</h3><p>Launching Salesforce in Claude (beta)</p>
<h3>September 1, 2026</h3><p>Claude Fable 5.1 and Claude Mythos 5.1 launch</p>
<p><a href="https://www.anthropic.com/news/example">Announcement</a></p>
<h3>July 1, 2026</h3><p>Claude Opus 5 launch</p>
<h3>October 1, 2026</h3><p>Claude Sonnet 5.5 launch</p>'''


class OfficialTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.content = self.root / 'content'
        self.data = self.root / 'data'

    def run_collector(self, **kwargs):
        with redirect_stdout(io.StringIO()):
            return official.run(self.content, self.data, TODAY, fetcher=lambda url: NOTES, **kwargs)

    def test_only_dated_launch_titles_are_models(self):
        records = official.parse_launches(NOTES, TODAY)
        self.assertEqual([r['title'] for r in records],
                         ['Claude Opus 5.5', 'Claude Fable 5.1', 'Claude Mythos 5.1'])
        self.assertEqual(records[0]['date'], '2026-09-22')
        self.assertEqual(records[0]['url'], 'https://www.anthropic.com/claude-opus-5-5')

    def test_no_dated_entries_is_a_visible_failure(self):
        with self.assertRaises(ValueError):
            official.parse_launches('<html>Access denied</html>', TODAY)

    def test_future_announcement_heading_not_a_release(self):
        text = '<h3>September 22, 2026</h3><p>Claude Opus 6 will launch</p>'
        self.assertEqual(official.parse_launches(text, TODAY), [])

    def test_external_link_not_trusted(self):
        records = official.parse_launches(NOTES.replace('https://www.anthropic.com/claude-opus-5-5',
                                                       'https://www.anthropic.com.evil.test/x'), TODAY)
        self.assertEqual(records[0]['url'], official.SOURCE_URL)

    def test_dry_run_does_not_write(self):
        self.assertEqual(len(self.run_collector(dry_run=True)), 3)
        self.assertFalse(self.content.exists())
        self.assertFalse(self.data.exists())

    def test_dedup_and_shared_history_preserved(self):
        self.data.mkdir()
        original = {'hf/model': {'slug': 'hf__model', 'published_at': '2026-09-20'}}
        collect.save_json(self.data / 'published.json', {'models': original})
        self.assertEqual(len(self.run_collector()), 3)
        self.assertEqual(self.run_collector(), [])
        models = json.loads((self.data / 'published.json').read_text())['models']
        self.assertEqual(models['hf/model'], original['hf/model'])
        self.assertEqual(len(models), 4)

    def test_recovers_history_after_interrupted_state_write(self):
        self.run_collector()
        (self.data / 'published.json').unlink()
        self.assertEqual(self.run_collector(), [])
        state = json.loads((self.data / 'published.json').read_text())
        self.assertEqual(len(state['models']), 3)

    def test_cap(self):
        self.assertEqual(len(self.run_collector(max_new=1)), 1)
        self.assertEqual(len(list(self.content.glob('*.md'))), 1)

    def test_build_and_regenerate_preserve_official_source(self):
        self.run_collector()
        path = self.content / 'Anthropic__claude-opus-5-5.md'
        before = path.read_text()
        meta, _ = parse_frontmatter(before)
        self.assertEqual(meta['source'], 'official')
        self.assertEqual(meta['hf_url'], '')
        collect.regenerate_local(self.content, self.data / 'published.json')
        self.assertEqual(path.read_text(), before)
        output = self.root / 'dist'
        build.build(self.content, output, build_date='2026-09-23')
        detail = (output / 'models/Anthropic__claude-opus-5-5/index.html').read_text()
        self.assertIn('공식 발표 보기', detail)
        self.assertIn('https://www.anthropic.com/claude-opus-5-5', detail)
        self.assertNotIn('Hugging Face 에서 보기', detail)
        self.assertIn('<td>미제공</td>', detail)
        index = (output / 'index.html').read_text()
        self.assertIn('공식 발표', index)
        self.assertIn('♥ —', index)
        self.assertIn('Claude Opus 5.5', (output / 'feed.xml').read_text())


if __name__ == '__main__':
    unittest.main()
