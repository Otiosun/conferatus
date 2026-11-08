import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeRichTextRuns } from '../dist/domain/rich-text.js';
import {
  isRichBlockDocument,
  migrateLegacyRichText,
  projectRichBlocksToLegacy,
  insertHorizontalRule,
  removeHorizontalRule,
  renderRichBlockDocument
} from '../dist/domain/rich-blocks.js';

const text = 'Cabeçalho\n\nFórmula H2O\nReferência segura.';
const href = 'https://example.com/material';
const runs = [
  { text: 'Cabeçalho', marks: ['bold'] },
  { text: '\n\nFórmula H', marks: [] },
  { text: '2', marks: ['subscript'] },
  { text: 'O\n', marks: [] },
  { text: 'Referência segura.', marks: ['italic'], href }
];
const layout = { align: 'justify', left: 16, right: 32, lineHeight: 2 };

test('legacy migration preserves text, empty paragraphs, formatting, URL and whole layout', () => {
  const legacy = { body: text, bodyRuns: runs, bodyLayout: layout };
  const converted = migrateLegacyRichText(legacy);
  assert.equal(converted.ok, true, JSON.stringify(converted));
  const doc = converted.value;
  assert.equal(isRichBlockDocument(doc), true);
  assert.deepEqual(doc.blocks.map(block => block.type),
    ['paragraph', 'paragraph', 'paragraph', 'paragraph']);
  assert.equal(doc.blocks[1].text, '');
  assert.notEqual(doc.layout, layout);
  const restored = projectRichBlocksToLegacy(doc);
  assert.equal(restored.ok, true);
  assert.equal(restored.value.body, text);
  assert.deepEqual(restored.value.bodyLayout, layout);
  assert.deepEqual(normalizeRichTextRuns(restored.value.bodyRuns), normalizeRichTextRuns(runs));
  assert.notEqual(restored.value.bodyRuns[0].marks, runs[0].marks);
});

test('legacy migration preserves trailing newlines and text-only drafts', () => {
  for (const body of ['', 'A', '\n', 'A\n', '\nA\n\n', 'A\r\nB']) {
    const migrated = migrateLegacyRichText({ body });
    assert.equal(migrated.ok, true);
    const restored = projectRichBlocksToLegacy(migrated.value);
    assert.deepEqual(restored, { ok: true, value: { body } });
  }
});

test('reject formatted newlines and excessive paragraphs rather than drop data', () => {
  assert.deepEqual(
    migrateLegacyRichText({ body: 'A\nB', bodyRuns: [{ text: 'A\nB', marks: ['bold'] }] }),
    { ok: false, reason: 'formatted-line-break' }
  );
  assert.deepEqual(
    migrateLegacyRichText({ body: 'x\n'.repeat(1024) }),
    { ok: false, reason: 'document-too-large' }
  );
  assert.deepEqual(
    migrateLegacyRichText({ body: 'ok', bodyRuns: [{ text: 'oops', marks: [] }] }),
    { ok: false, reason: 'invalid-legacy' }
  );
});

test('horizontal rule inserts and removes immutably with no silent downgrade', () => {
  const source = migrateLegacyRichText({ body: 'Antes\nDepois' }).value;
  const inserted = insertHorizontalRule(source, 0);
  assert.equal(inserted.ok, true);
  assert.deepEqual(inserted.value.blocks.map(block => block.type),
    ['paragraph', 'horizontalRule', 'paragraph']);
  assert.deepEqual(projectRichBlocksToLegacy(inserted.value),
    { ok: false, reason: 'structural-blocks' });
  assert.equal(source.blocks.length, 2);
  const encoded = JSON.stringify(inserted.value);
  const decoded = JSON.parse(encoded);
  assert.equal(isRichBlockDocument(decoded), true);
  assert.match(renderRichBlockDocument(decoded), /<p>Antes<\/p><hr><p>Depois<\/p>/);
  assert.deepEqual(insertHorizontalRule(decoded, 0),
    { ok: false, reason: 'invalid-position' });
  const removed = removeHorizontalRule(decoded, 1);
  assert.equal(removed.ok, true);
  assert.deepEqual(projectRichBlocksToLegacy(removed.value),
    { ok: true, value: { body: 'Antes\nDepois' } });
  assert.deepEqual(removeHorizontalRule(decoded, 0),
    { ok: false, reason: 'invalid-position' });
});

test('strict versioned blocks reject injected HTML, CSS, nodes and malformed positions', () => {
  const valid = { version: 1, blocks: [
    { type: 'paragraph', text: '<script>test()</script> & texto' },
    { type: 'horizontalRule' },
    { type: 'paragraph', text: 'Depois' }
  ]};
  assert.equal(isRichBlockDocument(valid), true);
  const safeHTML = renderRichBlockDocument(valid);
  assert.equal(safeHTML.includes('<script>'), false);
  assert.match(safeHTML, /&lt;script&gt;/);
  for (const invalid of [
    { ...valid, version: 2 },
    { ...valid, onload: 'alert(1)' },
    { ...valid, layout: { align: 'left', left: 0, right: 0, lineHeight: '1;evil()' } },
    { version: 1, blocks: [{ type: 'horizontalRule' }] },
    { version: 1, blocks: [{ type: 'paragraph', text: 'A' }, { type: 'horizontalRule' }] },
    { version: 1, blocks: [{ type: 'horizontalRule' }, { type: 'paragraph', text: 'B' }] },
    { version: 1, blocks: [
      { type: 'paragraph', text: 'A' }, { type: 'horizontalRule' },
      { type: 'horizontalRule' }, { type: 'paragraph', text: 'B' }
    ] },
    { version: 1, blocks: [{ type: 'table', rows: [['X']] }] },
    { version: 1, blocks: [{ type: 'paragraph', text: 'A', onclick: 'evil()' }] },
    { version: 1, blocks: [{ type: 'paragraph', text: 'A\nB' }] },
    { version: 1, blocks: [{ type: 'paragraph', text: 'A',
      runs: [{ text: 'A', marks: [], href: 'javascript:alert(1)' }] }] }
  ]) {
    assert.equal(isRichBlockDocument(invalid), false, JSON.stringify(invalid));
    assert.equal(renderRichBlockDocument(invalid), undefined);
    assert.deepEqual(projectRichBlocksToLegacy(invalid),
      { ok: false, reason: 'invalid-document' });
  }
});

test('migration and mutation never change caller-owned arrays', () => {
  const input = { body: 'A\nB', bodyRuns: [
    { text: 'A', marks: ['bold'] },
    { text: '\nB', marks: [] }
  ]};
  const original = structuredClone(input);
  const migrated = migrateLegacyRichText(input);
  assert.equal(migrated.ok, true);
  const transformed = insertHorizontalRule(migrated.value, 0);
  assert.equal(transformed.ok, true);
  transformed.value.blocks[0].text = 'altered elsewhere';
  assert.deepEqual(input, original);
  assert.equal(migrated.value.blocks[0].text, 'A');
});

test('projecting a rule cannot be hidden by adding unrelated formatting', () => {
  const doc = {
    version: 1,
    blocks: [
      { type: 'paragraph', text: 'A', runs: [{ text: 'A', marks: ['bold'] }] },
      { type: 'horizontalRule' },
      { type: 'paragraph', text: 'B', runs: [{ text: 'B', marks: ['italic'] }] }
    ],
    layout
  };
  assert.equal(isRichBlockDocument(doc), true);
  assert.deepEqual(projectRichBlocksToLegacy(doc),
    { ok: false, reason: 'structural-blocks' });
  assert.match(renderRichBlockDocument(doc), /text-align:justify/);
});
