import type { Member, OptionResult, GovernanceChange, Ballot, Section } from './types.js';

export function totalVotes(options: OptionResult[]): number {
  return options.reduce((sum, option) => sum + option.votes, 0);
}
export function resultPercentage(votes: number, total: number): number {
  if (!Number.isFinite(votes) || !Number.isFinite(total) || total <= 0) return 0;
  return Math.max(0, Math.min(100, Math.round((votes / total) * 100)));
}
export function canRecordVote(ballot: Ballot): boolean {
  return ballot.status === 'aberta';
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
      kind: assigned ? 'vinculo' : 'desvinculo',
      memberId: member.id,
      sectionId,
      previousSectionIds: before,
      nextSectionIds: after,
      previousRole: member.role,
      nextRole: updated.role,
    },
  };
}
/** Rebaixamento de função preserva atividades e indicadores anteriores. */
export function demoteToCommonMember(member: Member, commonSectionId = 'membros'): {member: Member; change: GovernanceChange} {
 const before = [...member.sectionIds];
 const updated: Member = {...member, role:'membro', sectionIds:[commonSectionId], hadDeliberativeHistory:member.hadDeliberativeHistory === true || member.sectionIds.some(id=>id!==commonSectionId)};
 return {member:updated,change:{kind:'rebaixamento',memberId:member.id,sectionId:commonSectionId,previousSectionIds:before,nextSectionIds:[commonSectionId],previousRole:member.role,nextRole:'membro'}};
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
    if (entry.role === 'diretor' || entry.role === 'membro') member.role = entry.role;
    if (entry.hadDeliberativeHistory === true) member.hadDeliberativeHistory = true;
    if (entry.hadDeliberativeHistory === false) member.hadDeliberativeHistory = false;
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

/** Voting eligibility and administrative role are independent. */
export function isDeliberativeMember(member: Member, sections: Section[]): boolean {
 const eligible = new Set(sections.filter(s=>s.category==='deliberativa').map(s=>s.id));
 return member.sectionIds.some(id=>eligible.has(id));
}
/** Existing votes remain available after a deliberative member's demotion. */
export function hasPersonalVoteHistory(member: Member, sections: Section[]): boolean {
 return member.hadDeliberativeHistory===true || isDeliberativeMember(member,sections);
}
