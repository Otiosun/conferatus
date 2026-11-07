/**
 * Text is authoritative. Formatting is an optional, strictly typed view of it.
 * Never store untrusted HTML in a proposal or restore it from a backup.
 */
export const INLINE_MARKS = ['bold', 'italic', 'underline', 'strike'] as const;
export type InlineMark = typeof INLINE_MARKS[number];
export type RichTextRun = { text: string; marks: InlineMark[] };

const markOrder = (marks: readonly InlineMark[]): InlineMark[] =>
  INLINE_MARKS.filter(mark => marks.includes(mark));

/** Collapse neighboring runs without changing the exact plain-text body. */
export function normalizeRichTextRuns(runs: readonly RichTextRun[]): RichTextRun[] {
  const output: RichTextRun[] = [];
  for (const run of runs) {
    if (!run.text) continue;
    const marks = markOrder(run.marks);
    const previous = output[output.length - 1];
    if (previous && previous.marks.join('|') === marks.join('|')) {
      previous.text += run.text;
    } else {
      output.push({text: run.text, marks});
    }
  }
  return output;
}

/** Check restored session/archive formatting as untrusted JSON. */
export function isRichTextRuns(value: unknown, body: string): value is RichTextRun[] {
  if (!Array.isArray(value) || value.length > 2048 || body.length > 200000) return false;
  let text = '';
  for (const item of value) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) return false;
    const run = item as Record<string, unknown>;
    if (typeof run.text !== 'string' || !run.text || !Array.isArray(run.marks) || run.marks.length > 4) return false;
    if (!run.marks.every(mark => typeof mark === 'string' && INLINE_MARKS.includes(mark as InlineMark))) return false;
    if (new Set(run.marks).size !== run.marks.length) return false;
    text += run.text;
    if (text.length > body.length) return false;
  }
  return text === body;
}

const safeText = (text: string) => text.replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
})[char] ?? char);

const tagByMark: Record<InlineMark, string> = {
  bold: 'strong', italic: 'em', underline: 'u', strike: 's'
};

/** Render only text and four hardcoded semantic tags; no raw HTML is trusted. */
export function renderRichText(body: string, runs?: unknown): string {
  if (!isRichTextRuns(runs, body)) return safeText(body);
  return runs.map(run => {
    let html = safeText(run.text);
    for (const mark of markOrder(run.marks)) {
      const tag = tagByMark[mark];
      html = '<' + tag + '>' + html + '</' + tag + '>';
    }
    return html;
  }).join('');
}
