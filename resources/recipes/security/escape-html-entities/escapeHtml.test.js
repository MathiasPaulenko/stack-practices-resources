/**
 * Tests for escapeHtml.js — run with: node --test escapeHtml.test.js
 * Uses the built-in node:test runner, no dependencies required.
 */

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { escapeHtml, safeJsonInScript, safeUrl } = require('./escapeHtml.js');

test('escapeHtml escapes a script payload', () => {
  assert.equal(
    escapeHtml('<script>alert("xss")</script>'),
    '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'
  );
});

test('escapeHtml escapes all five critical characters', () => {
  assert.equal(escapeHtml('<>&"\''), '&lt;&gt;&amp;&quot;&#x27;');
});

test('escapeHtml leaves plain text unchanged', () => {
  assert.equal(escapeHtml('Hello, world!'), 'Hello, world!');
});

test('safeJsonInScript neutralizes script breakout', () => {
  const out = safeJsonInScript({
    name: 'x</script><script>alert(1)</script>'
  });
  assert.ok(!out.includes('</script>'));
  assert.ok(out.includes('\\u003c'));
});

test('safeJsonInScript output still parses as JSON', () => {
  const data = { user: 'Alice & Bob', n: 42 };
  const out = safeJsonInScript(data);
  assert.deepEqual(JSON.parse(out), data);
});

test('safeUrl rejects javascript: protocol', () => {
  assert.equal(safeUrl('javascript:alert(1)'), '');
});

test('safeUrl rejects data: protocol', () => {
  assert.equal(safeUrl('data:text/html,<script>alert(1)</script>'), '');
});

test('safeUrl accepts https URLs', () => {
  assert.equal(
    safeUrl('https://example.com/path?q=1'),
    'https://example.com/path?q=1'
  );
});

test('safeUrl resolves relative URLs against the base', () => {
  assert.equal(
    safeUrl('/docs/guide', 'https://example.com'),
    'https://example.com/docs/guide'
  );
});
