/**
 * Isolated, versioned document-block experiment. NOT connected to the live editor.
 *
 * The current draft's body/bodyRuns remain authoritative until a tested and
 * approved migration covers editing, undo, import/export and signatures.
 */
import {
  isRichTextRuns, normalizeRichTextRuns, renderRichText,
  isRichLayout, richLayoutStyle
} from './rich-text.js';
import type { RichTextRun, RichBodyLayout } from './rich-text.js';

export type ParagraphBlock = {
  type: 'paragraph';
  text: string;
  runs?: RichTextRun[];
};

export type HorizontalRuleBlock = { type: 'horizontalRule' };
export type RichBlock = ParagraphBlock | HorizontalRuleBlock;

export type RichBlockDocumentV1 = {
  version: 1;
  blocks: RichBlock[];
  /** Existing layout applies to the whole document, not individual paragraphs. */
  layout?: RichBodyLayout;
};

export type LegacyText = {
  body: string;
  bodyRuns?: RichTextRun[];
  bodyLayout?: RichBodyLayout;
};

type MigrationFailure = 'invalid-legacy' | 'formatted-line-break' | 'document-too-large';
type ProjectionFailure = 'invalid-document' | 'structural-blocks' | 'legacy-limit';
type Result<T, Reason extends string> =
  | { ok: true; value: T }
  | { ok: false; reason: Reason };

const MAX_BLOCKS = 1024;
const MAX_RUNS = 2048;
const MAX_TEXT_LENGTH = 200_000;
const EXACT_DOCUMENT_KEYS = new Set(['version', 'blocks', 'layout']);
const EXACT_PARAGRAPH_KEYS = new Set(['type', 'text', 'runs']);

function hasOnlyKeys(value: Record<string, unknown>, keys: ReadonlySet<string>): boolean {
  return Object.keys(value).every(key => keys.has(key));
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/** A divider is a structural leaf, never HTML buried in a text run. */
export function isRichBlockDocument(value: unknown): value is RichBlockDocumentV1 {
  if (!isRecord(value) || !hasOnlyKeys(value, EXACT_DOCUMENT_KEYS) ||
      value.version !== 1 || !Array.isArray(value.blocks) ||
      value.blocks.length < 1 || value.blocks.length > MAX_BLOCKS ||
      (value.layout !== undefined && !isRichLayout(value.layout))) {
    return false;
  }

  let length = 0;
  let paragraphCount = 0;
  let runCount = 0;
  const blocks = value.blocks as unknown[];
  for (let index = 0; index < blocks.length; index++) {
    const block = blocks[index];
    if (!isRecord(block)) return false;

    if (block.type === 'horizontalRule') {
      const previous = blocks[index - 1];
      const next = blocks[index + 1];
      if (Object.keys(block).length !== 1 ||
          index === 0 || index === blocks.length - 1 ||
          !isRecord(previous) || previous.type !== 'paragraph' ||
          !isRecord(next) || next.type !== 'paragraph') {
        return false;
      }
      continue;
    }

    if (block.type !== 'paragraph' || !hasOnlyKeys(block, EXACT_PARAGRAPH_KEYS) ||
        typeof block.text !== 'string' || block.text.includes('\n') ||
        (block.runs !== undefined && !isRichTextRuns(block.runs, block.text))) {
      return false;
    }

    length += block.text.length + (paragraphCount++ > 0 ? 1 : 0);
    runCount += Array.isArray(block.runs) ? block.runs.length : 0;
    if (length > MAX_TEXT_LENGTH || runCount > MAX_RUNS) return false;
  }

  return true;
}

function copyRuns(runs: readonly RichTextRun[]): RichTextRun[] {
  return runs.map(({ text, marks, font, size, color, highlight, href }) => ({
    text,
    marks: [...marks],
    ...(font ? { font } : {}),
    ...(size !== undefined ? { size } : {}),
    ...(color ? { color } : {}),
    ...(highlight ? { highlight } : {}),
    ...(href ? { href } : {})
  }));
}

function cloneBlock(block: RichBlock): RichBlock {
  if (block.type === 'horizontalRule') return { type: 'horizontalRule' };
  return {
    type: 'paragraph',
    text: block.text,
    ...(block.runs ? { runs: copyRuns(block.runs) } : {})
  };
}

function styledLineBreak(run: RichTextRun): boolean {
  return run.text.includes('\n') && (
    run.marks.length > 0 || Boolean(run.font || run.size || run.color ||
    run.highlight || run.href)
  );
}

/**
 * Convert an existing draft without writing to storage. Styled newline
 * characters cannot be represented by paragraph boundaries, so reject them
 * rather than silently removing their styles.
 */
export function migrateLegacyRichText(input: LegacyText):
  Result<RichBlockDocumentV1, MigrationFailure> {
  if (!input || typeof input.body !== 'string' ||
      input.body.length > MAX_TEXT_LENGTH ||
      (input.bodyRuns !== undefined && !isRichTextRuns(input.bodyRuns, input.body)) ||
      (input.bodyLayout !== undefined && !isRichLayout(input.bodyLayout))) {
    return { ok: false, reason: 'invalid-legacy' };
  }

  const paragraphs = input.body.split('\n');
  if (paragraphs.length > MAX_BLOCKS) {
    return { ok: false, reason: 'document-too-large' };
  }

  const runs = input.bodyRuns;
  if (runs?.some(styledLineBreak)) {
    return { ok: false, reason: 'formatted-line-break' };
  }

  const intervals: { start: number; end: number; run: RichTextRun }[] = [];
  let runOffset = 0;
  for (const run of runs ?? []) {
    intervals.push({ start: runOffset, end: runOffset + run.text.length, run });
    runOffset += run.text.length;
  }

  const blocks: ParagraphBlock[] = [];
  let position = 0;
  for (const text of paragraphs) {
    const start = position;
    const end = position + text.length;
    const pieces: RichTextRun[] = [];
    for (const interval of intervals) {
      const from = Math.max(start, interval.start);
      const to = Math.min(end, interval.end);
      if (to > from) {
        const segment = copyRuns([interval.run])[0];
        if (!segment) continue;
        segment.text = interval.run.text.slice(from - interval.start, to - interval.start);
        pieces.push(segment);
      }
    }
    const normalized = normalizeRichTextRuns(pieces);
    blocks.push({
      type: 'paragraph',
      text,
      ...(runs && text ? { runs: normalized } : {})
    });
    position = end + 1;
  }

  const document: RichBlockDocumentV1 = {
    version: 1,
    blocks,
    ...(input.bodyLayout ? { layout: { ...input.bodyLayout } } : {})
  };
  return isRichBlockDocument(document)
    ? { ok: true, value: document }
    : { ok: false, reason: 'document-too-large' };
}

/** Reject structural blocks when projecting back to the older text-only API. */
export function projectRichBlocksToLegacy(value: unknown):
  Result<LegacyText, ProjectionFailure> {
  if (!isRichBlockDocument(value)) return { ok: false, reason: 'invalid-document' };
  if (value.blocks.some(block => block.type === 'horizontalRule')) {
    return { ok: false, reason: 'structural-blocks' };
  }

  const paragraphs = value.blocks as ParagraphBlock[];
  const body = paragraphs.map(paragraph => paragraph.text).join('\n');
  const hasFormatting = paragraphs.some(paragraph => paragraph.runs !== undefined);
  const flatRuns: RichTextRun[] = [];

  if (hasFormatting) {
    paragraphs.forEach((paragraph, index) => {
      if (index > 0) flatRuns.push({ text: '\n', marks: [] });
      if (paragraph.runs) flatRuns.push(...copyRuns(paragraph.runs));
      else if (paragraph.text) flatRuns.push({ text: paragraph.text, marks: [] });
    });
  }

  const bodyRuns = hasFormatting ? normalizeRichTextRuns(flatRuns) : undefined;
  if (body.length > MAX_TEXT_LENGTH ||
      (bodyRuns && !isRichTextRuns(bodyRuns, body))) {
    return { ok: false, reason: 'legacy-limit' };
  }

  return { ok: true, value: {
    body,
    ...(bodyRuns ? { bodyRuns } : {}),
    ...(value.layout ? { bodyLayout: { ...value.layout } } : {})
  }};
}

/** Immutable operation; only between two adjacent paragraph blocks. */
export function insertHorizontalRule(
  value: unknown, afterBlockIndex: number
): Result<RichBlockDocumentV1, 'invalid-document' | 'invalid-position'> {
  if (!isRichBlockDocument(value)) return { ok: false, reason: 'invalid-document' };
  const left = value.blocks[afterBlockIndex];
  const right = value.blocks[afterBlockIndex + 1];
  if (!Number.isInteger(afterBlockIndex) ||
      !left || left.type !== 'paragraph' || !right || right.type !== 'paragraph' ||
      value.blocks.length + 1 > MAX_BLOCKS) {
    return { ok: false, reason: 'invalid-position' };
  }
  return { ok: true, value: {
    version: 1,
    blocks: [
      ...value.blocks.slice(0, afterBlockIndex + 1).map(cloneBlock),
      { type: 'horizontalRule' },
      ...value.blocks.slice(afterBlockIndex + 1).map(cloneBlock)
    ],
    ...(value.layout ? { layout: { ...value.layout } } : {})
  }};
}

/** Immutable removal proves a divider can be reversed without losing text. */
export function removeHorizontalRule(
  value: unknown, blockIndex: number
): Result<RichBlockDocumentV1, 'invalid-document' | 'invalid-position'> {
  if (!isRichBlockDocument(value)) return { ok: false, reason: 'invalid-document' };
  if (!Number.isInteger(blockIndex) ||
      value.blocks[blockIndex]?.type !== 'horizontalRule') {
    return { ok: false, reason: 'invalid-position' };
  }
  return { ok: true, value: {
    version: 1,
    blocks: value.blocks.filter((_, index) => index !== blockIndex).map(cloneBlock),
    ...(value.layout ? { layout: { ...value.layout } } : {})
  }};
}

/** Prototype renderer: never output imported HTML, CSS, or arbitrary attributes. */
export function renderRichBlockDocument(value: unknown): string | undefined {
  if (!isRichBlockDocument(value)) return undefined;
  const html = value.blocks.map(block => {
    if (block.type === 'horizontalRule') return '<hr>';
    return '<p>' + renderRichText(block.text, block.runs) + '</p>';
  }).join('');
  const style = richLayoutStyle(value.layout);
  return '<div class="workflow-block-preview"' +
    (style ? ' style="' + style + '"' : '') + '>' + html + '</div>';
}


/**
 * Cursor offsets are UTF-16; a split is allowed only at an extended grapheme
 * boundary. Unicode sequences such as "e" + combining accent, flag pairs and
 * ZWJ emoji are indivisible even when their surrogate pairs are individually valid.
 * Fail closed on older engines: never guess an interior boundary.
 */
function isGraphemeBoundary(text: string, offset: number): boolean {
  if (offset === 0 || offset === text.length) return true;
  if (typeof Intl.Segmenter !== 'function') return false;
  return new Intl.Segmenter('pt-BR', { granularity: 'grapheme' })
    .segment(text).containing(offset)?.index === offset;
}

/** Copy arbitrary slices of inline marks without creating a dangling URL or style. */
function sliceParagraphRuns(
  paragraph: ParagraphBlock, start: number, end: number
): RichTextRun[] | undefined {
  if (!paragraph.runs || end === start) return undefined;
  const result: RichTextRun[] = [];
  let position = 0;
  for (const run of paragraph.runs) {
    const from = Math.max(position, start);
    const to = Math.min(position + run.text.length, end);
    if (from < to) {
      result.push({
        ...copyRuns([run])[0]!,
        text: run.text.slice(from - position, to - position)
      });
    }
    position += run.text.length;
  }
  return normalizeRichTextRuns(result);
}

/**
 * Split a paragraph at a valid cursor offset. Existing marks are retained on
 * each side; the newline becomes a structural boundary, not an inline mark.
 */
export function splitRichParagraph(
  value: unknown, blockIndex: number, offset: number
): Result<RichBlockDocumentV1, 'invalid-document' | 'invalid-position' | 'limit-exceeded'> {
  if (!isRichBlockDocument(value)) return { ok: false, reason: 'invalid-document' };
  const block = value.blocks[blockIndex];
  if (!Number.isInteger(blockIndex) || !block || block.type !== 'paragraph' ||
      !Number.isInteger(offset) || offset < 0 || offset > block.text.length ||
      !isGraphemeBoundary(block.text, offset)) {
    return { ok: false, reason: 'invalid-position' };
  }

  const left: ParagraphBlock = {
    type: 'paragraph', text: block.text.slice(0, offset),
    ...(sliceParagraphRuns(block, 0, offset) ?
      { runs: sliceParagraphRuns(block, 0, offset) } : {})
  };
  const right: ParagraphBlock = {
    type: 'paragraph', text: block.text.slice(offset),
    ...(sliceParagraphRuns(block, offset, block.text.length) ?
      { runs: sliceParagraphRuns(block, offset, block.text.length) } : {})
  };
  const next: RichBlockDocumentV1 = {
    version: 1,
    blocks: [
      ...value.blocks.slice(0, blockIndex).map(cloneBlock),
      left, right,
      ...value.blocks.slice(blockIndex + 1).map(cloneBlock)
    ],
    ...(value.layout ? { layout: { ...value.layout } } : {})
  };
  return isRichBlockDocument(next)
    ? { ok: true, value: next } : { ok: false, reason: 'limit-exceeded' };
}

/** Backspace at a paragraph boundary may merge paragraphs, never erase a rule. */
export function joinRichParagraphs(
  value: unknown, leftIndex: number
): Result<RichBlockDocumentV1, 'invalid-document' | 'invalid-position' | 'limit-exceeded'> {
  if (!isRichBlockDocument(value)) return { ok: false, reason: 'invalid-document' };
  const left = value.blocks[leftIndex];
  const right = value.blocks[leftIndex + 1];
  if (!Number.isInteger(leftIndex) || !left || left.type !== 'paragraph' ||
      !right || right.type !== 'paragraph') {
    return { ok: false, reason: 'invalid-position' };
  }

  const needsRuns = left.runs !== undefined || right.runs !== undefined;
  const combined = needsRuns ? normalizeRichTextRuns([
    ...(left.runs ? copyRuns(left.runs) :
       left.text ? [{ text: left.text, marks: [] }] : []),
    ...(right.runs ? copyRuns(right.runs) :
       right.text ? [{ text: right.text, marks: [] }] : [])
  ]) : undefined;
  const merged: ParagraphBlock = {
    type: 'paragraph',
    text: left.text + right.text,
    ...(combined && combined.length ? { runs: combined } : {})
  };
  const next: RichBlockDocumentV1 = {
    version: 1,
    blocks: [
      ...value.blocks.slice(0, leftIndex).map(cloneBlock),
      merged,
      ...value.blocks.slice(leftIndex + 2).map(cloneBlock)
    ],
    ...(value.layout ? { layout: { ...value.layout } } : {})
  };
  return isRichBlockDocument(next)
    ? { ok: true, value: next } : { ok: false, reason: 'limit-exceeded' };
}
