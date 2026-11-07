import { isDeliberationMethod, searchKey } from './rules.js';
import type { DeliberationMethod } from './types.js';
import { isRichTextRuns } from './rich-text.js';
import type { RichTextRun } from './rich-text.js';

export type ProposalType = 'PDR' | 'PR' | 'Ofício';
export type PreviewChoice = { id: string; label: string };

export type Draft = {
  id: string;
  title: string;
  body: string;
  /** Optional safe formatting, always mirrored by the plain body. */
  bodyRuns?: RichTextRun[];
  sectionId: string;
  type: ProposalType;
  authorComplete: boolean;
  partners: { id: string; complete: boolean }[];
  status: 'redacao' | 'revisao' | 'concluida';
};

export type Deliberation = {
  id: string;
  title: string;
  objective: string;
  proposalId: string;
  sectionId: string;
  start: string;
  end: string;
  type: string;
  method?: DeliberationMethod;
  choices?: PreviewChoice[];
  status: 'programada' | 'cancelada';
};

/** Local fixture references only, never Academy authorization. */
export type WorkflowValidationContext = {
  memberIds: ReadonlySet<string>;
  deliberativeSectionIds: ReadonlySet<string>;
  authorId?: string;
};

/** Validate the labels and stable option IDs used by the existing preview editor. */
export function isValidPreviewChoices(value: unknown): value is PreviewChoice[] {
  if (!Array.isArray(value) || value.length < 2 || value.length > 8) return false;

  const labels = new Set<string>();
  return value.every((choice, index) => {
    if (!choice || typeof choice !== 'object' || Array.isArray(choice)) return false;

    const item = choice as Record<string, unknown>;
    if (item.id !== 'opt-' + String(index + 1) ||
        typeof item.label !== 'string' ||
        !item.label.trim() ||
        item.label !== item.label.trim() ||
        item.label.length > 80) return false;

    const key = searchKey(item.label);
    if (labels.has(key)) return false;
    labels.add(key);
    return true;
  });
}

/** Restored data is untrusted, including older or partially written records. */
export function isSavedDraft(value: unknown, context: WorkflowValidationContext): value is Draft {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;

  const draft = value as Record<string, unknown>;
  if (typeof draft.id !== 'string' || !draft.id ||
      typeof draft.title !== 'string' || typeof draft.body !== 'string' ||
      (draft.bodyRuns !== undefined && !isRichTextRuns(draft.bodyRuns, draft.body)) ||
      typeof draft.sectionId !== 'string' ||
      !['PDR', 'PR', 'Ofício'].includes(String(draft.type)) ||
      typeof draft.authorComplete !== 'boolean' ||
      !['redacao', 'revisao', 'concluida'].includes(String(draft.status)) ||
      !Array.isArray(draft.partners)) return false;

  const partners = draft.partners as unknown[];
  const validPartners = partners.every(partner => {
    if (!partner || typeof partner !== 'object' || Array.isArray(partner)) return false;
    const data = partner as Record<string, unknown>;
    return typeof data.id === 'string' && context.memberIds.has(data.id) &&
      typeof data.complete === 'boolean';
  });
  if (!validPartners) return false;

  const signatures = partners as { id: string; complete: boolean }[];
  if (new Set(signatures.map(partner => partner.id)).size !== signatures.length ||
      signatures.some(partner => partner.id === context.authorId)) return false;

  if (draft.status !== 'redacao' &&
      (draft.title.trim().length < 3 ||
       draft.body.trim().length < 20 ||
       !context.deliberativeSectionIds.has(draft.sectionId))) return false;

  // An older record cannot claim completion with missing signatures.
  return draft.status !== 'concluida' ||
    (draft.authorComplete && signatures.every(partner => partner.complete));
}

/** Only the documented synthetic fields are safe to export or restore. */
export function cleanDraftRecord(draft: Draft): Draft {
  return {
    id: draft.id,
    title: draft.title,
    body: draft.body,
    ...(isRichTextRuns(draft.bodyRuns, draft.body)
      ? { bodyRuns: draft.bodyRuns.map(run => ({text: run.text, marks: [...run.marks]})) }
      : {}),
    sectionId: draft.sectionId,
    type: draft.type,
    authorComplete: draft.authorComplete,
    partners: draft.partners.map(partner => ({ id: partner.id, complete: partner.complete })),
    status: draft.status
  };
}

export function cleanScheduleRecord(item: Deliberation): Deliberation {
  return {
    id: item.id,
    title: item.title,
    objective: item.objective,
    proposalId: item.proposalId,
    sectionId: item.sectionId,
    start: item.start,
    end: item.end,
    type: item.type,
    ...(item.method ? { method: item.method } : {}),
    ...(item.choices ? { choices: item.choices.map(choice => ({ id: choice.id, label: choice.label })) } : {}),
    status: item.status
  };
}

export function isSavedSchedule(value: unknown): value is Deliberation {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;

  const item = value as Record<string, unknown>;
  return typeof item.id === 'string' && !!item.id &&
    typeof item.title === 'string' && typeof item.objective === 'string' &&
    typeof item.proposalId === 'string' && typeof item.sectionId === 'string' &&
    typeof item.start === 'string' && typeof item.end === 'string' &&
    !Number.isNaN(Date.parse(item.start)) && !Number.isNaN(Date.parse(item.end)) &&
    Date.parse(item.start) < Date.parse(item.end) &&
    ['PDR', 'PR', 'Ofício'].includes(String(item.type)) &&
    (item.method === undefined || isDeliberationMethod(item.method)) &&
    (item.choices === undefined || isValidPreviewChoices(item.choices)) &&
    (item.choices === undefined || item.method !== 'binaria') &&
    ['programada', 'cancelada'].includes(String(item.status));
}

/** Never restore an active schedule that points to a draft still awaiting signoff. */
export function isRestorableSchedule(
  value: unknown,
  candidateDrafts: readonly Draft[],
  deliberativeSectionIds: ReadonlySet<string>
): value is Deliberation {
  return isSavedSchedule(value) && (
    value.status === 'cancelada' ||
    (deliberativeSectionIds.has(value.sectionId) &&
     !candidateDrafts.some(draft => draft.id === value.proposalId && draft.status !== 'concluida'))
  );
}

/** Preserve the first valid instance of an ID; quarantine every rejected entry. */
export function uniqueSavedRecords<T extends { id: string }>(
  items: readonly unknown[],
  valid: (value: unknown) => value is T
): { accepted: T[]; rejected: unknown[] } {
  const seen = new Set<string>();
  const accepted: T[] = [];
  const rejected: unknown[] = [];

  for (const item of items) {
    if (valid(item) && !seen.has(item.id)) {
      seen.add(item.id);
      accepted.push(item);
    } else {
      rejected.push(item);
    }
  }
  return { accepted, rejected };
}

/** Local opaque IDs must not collide, even within a single clock tick. */
export function nextLocalRecordId(
  prefix: 'draft' | 'sched',
  records: readonly { id: string }[],
  timestamp = Date.now()
): string {
  const base = prefix + '-' + timestamp.toString(36);
  let candidate = base;
  let suffix = 1;
  while (records.some(record => record.id === candidate)) {
    candidate = base + '-' + String(suffix++);
  }
  return candidate;
}
