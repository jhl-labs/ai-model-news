// Dependency-free regression tests for the actual browser script.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../static/app.js'), 'utf8');

function app(hash = '') {
  const element = (attrs = {}) => ({
    value: '', hidden: false, attrs, handlers: {},
    getAttribute(k) { return this.attrs[k]; },
    setAttribute(k, v) { this.attrs[k] = v; },
    classList: {toggle() {}}, focus() {},
    addEventListener(k, handler) { this.handlers[k] = handler; },
    fire(k) { this.handlers[k](); }
  });
  const cards = [
    element({'data-task': 'text', 'data-org': 'a', 'data-search': 'alpha'}),
    element({'data-task': 'image', 'data-org': 'b', 'data-search': 'beta'})
  ];
  const chips = ['', 'text', 'image'].map(task => element({'data-task': task}));
  const ids = Object.fromEntries(['cards', 'filters', 'org-filter', 'search',
    'reset-filters', 'no-match', 'stat-visible'].map(id => [id, element()]));
  ids.cards.querySelectorAll = () => cards;
  ids.filters.querySelectorAll = () => chips;
  const listeners = {}, timers = new Map();
  let nextTimer = 0;
  const window = {location: {hash, pathname: '/', search: ''},
    history: {replaceState(_state, _title, url) { window.location.hash = url.includes('#') ? url.slice(url.indexOf('#')) : ''; }},
    addEventListener(k, fn) { listeners[k] = fn; }};
  vm.runInNewContext(source, {window,
    document: {documentElement: element(), getElementById: id => ids[id] || null},
    setTimeout(fn) { const id = ++nextTimer; timers.set(id, fn); return id; },
    clearTimeout(id) { timers.delete(id); }
  });
  return {ids, chips, cards, window,
    type(q) { ids.search.value = q; ids.search.fire('input'); },
    flush() { const callbacks = [...timers.values()]; timers.clear(); callbacks.forEach(fn => fn()); },
    hash(value) { window.location.hash = value; listeners.hashchange(); }};
}

test('typing then immediately selecting a task preserves the query', () => {
  const a = app(); a.type('alpha'); a.chips[1].fire('click'); a.flush();
  assert.equal(a.ids.search.value, 'alpha');
  assert.equal(a.window.location.hash, '#task=text&q=alpha');
  assert.deepEqual(a.cards.map(card => card.hidden), [false, true]);
});

test('typing then immediately selecting an organization preserves the query', () => {
  const a = app(); a.type('alpha'); a.ids['org-filter'].value = 'a'; a.ids['org-filter'].fire('change'); a.flush();
  assert.equal(a.ids.search.value, 'alpha');
  assert.deepEqual(a.cards.map(card => card.hidden), [false, true]);
});

test('reset cancels pending search', () => {
  const a = app(); a.type('alpha'); a.ids['reset-filters'].fire('click'); a.flush();
  assert.equal(a.ids.search.value, '');
  assert.equal(a.window.location.hash, '');
  assert(a.cards.every(card => !card.hidden));
});

test('hash navigation replaces pending search', () => {
  const a = app(); a.type('alpha'); a.hash('#q=beta'); a.flush();
  assert.equal(a.ids.search.value, 'beta');
  assert.deepEqual(a.cards.map(card => card.hidden), [true, false]);
});

test('unknown shared task falls back to all tasks', () => {
  const a = app('#task=removed');
  assert(a.cards.every(card => !card.hidden));
  assert.equal(a.chips[0].attrs['aria-pressed'], 'true');
});
