import type { Member, OptionResult, GovernanceChange } from './types.js';

export function totalVotes(options: OptionResult[]): number {
  return options.reduce((sum, option) => sum + option.votes, 0);
}
export function resultPercentage(votes: number, total: number): number {
  if (!Number.isFinite(votes) || !Number.isFinite(total) || total <= 0) return 0;
  return Math.max(0, Math.min(100, Math.round((votes / total) * 100)));
}
/** Preview-only member association editor. Historical activity is deliberately untouched. */
export function updateSectionAssignment(member: Member, sectionId: string, assigned: boolean): {
  member: Member;
  change: GovernanceChange;
} {
  const before = [...member.sectionIds];
  const after = assigned ? [...new Set([...before, sectionId])] : before.filter(id => id !== sectionId);
  const updated = { ...member, sectionIds: after };
  return {
    member: updated,
    change: {
      kind: assigned ? 'vinculo' : 'rebaixamento',
      memberId: member.id,
      sectionId,
      previousSectionIds: before,
      nextSectionIds: after,
    },
  };
}
export function escapeHTML(value: string): string {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

/** Flexible directory lookup that does not depend on accent or case. */
export function searchKey(value: string): string {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR').trim();
}

/** Apply only known, valid demo members and sections; never trust browser storage. */
export function restoreDemoMembers(members: Member[], validSectionIds: string[], stored: unknown): void {
  if (!Array.isArray(stored)) return;
  const allowedSections = new Set(validSectionIds);
  const known = new Map(members.map(member => [member.id, member]));
  const usedIds = new Set(members.map(m => m.acdmId).filter((id): id is string => Boolean(id)));
  for (const entry of stored) {
    if (!entry || typeof entry !== 'object' || typeof entry.id !== 'string') continue;
    const member = known.get(entry.id);
    if (!member) continue;
    if (Array.isArray(entry.sectionIds)) {
      member.sectionIds = [...new Set<string>((entry.sectionIds as unknown[]).filter(
        (id: unknown): id is string => typeof id === 'string' && allowedSections.has(id)
      ))];
    }
    if (typeof entry.acdmId === 'string') {
      const candidate = entry.acdmId.toUpperCase();
      if (/^[A-Z0-9_-]{3,40}$/.test(candidate) &&
          (candidate === member.acdmId || !usedIds.has(candidate))) {
        if (member.acdmId) usedIds.delete(member.acdmId);
        member.acdmId = candidate;
        usedIds.add(candidate);
      }
    }
  }
}
