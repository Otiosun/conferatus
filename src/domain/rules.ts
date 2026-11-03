import type { Member, OptionResult, GovernanceChange, Ballot, Section, DeliberationMethod } from './types.js';

/** Definitions supplied by Megalos on 03/11/2026. Vote counting is not yet institutional. */
export const DELIBERATION_METHODS: readonly {id: DeliberationMethod; label: string; detail: string}[] = [
  {id:'binaria',label:'Binária',detail:'Sim ou Não para aprovar uma proposição'},
  {id:'nominal',label:'Nominal',detail:'Uma opção da lista; a mais votada vence'},
  {id:'ordenada',label:'Ordenada',detail:'Ranqueamento das opções, da primeira à última'},
  {id:'aprovacao',label:'Por aprovação',detail:'Todas as opções consideradas aceitáveis'},
  {id:'escalar',label:'Escalar',detail:'Nota de 1 a 10 para cada opção'},
  {id:'cumulativa',label:'Cumulativa',detail:'Distribuição de uma cota proporcional de votos entre opções'},
];
export function isDeliberationMethod(value: unknown): value is DeliberationMethod {
  return typeof value==='string' && DELIBERATION_METHODS.some(method=>method.id===value);
}
/** A cumulative allocation is a positive whole number, never inferred from a title or section. */
export function isPositiveCumulativeVoteWeight(value: unknown): value is number {
  return typeof value==='number' && Number.isSafeInteger(value) && value>0;
}


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

/** Changes a section link only; this is not a role demotion. */
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
/** Move a member to the common member category, retaining all past activity. */
export function demoteToCommonMember(member: Member, commonSectionId = 'membros'): {
  member: Member;
  change: GovernanceChange;
} {
  const before = [...member.sectionIds];
  const updated: Member = { ...member, role: 'membro', sectionIds: [commonSectionId],
  hadDeliberativeHistory: member.hadDeliberativeHistory === true || member.sectionIds.some(id => id !== commonSectionId) };
  return {
    member: updated,
    change: {
      kind: 'rebaixamento', memberId: member.id, sectionId: commonSectionId,
      previousSectionIds: before, nextSectionIds: [commonSectionId],
      previousRole: member.role, nextRole: updated.role,
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
    if (entry.role === 'diretor' || entry.role === 'membro') member.role = entry.role;
    if (entry.hadDeliberativeHistory === true) member.hadDeliberativeHistory = true;
    if (entry.hadDeliberativeHistory === false) member.hadDeliberativeHistory = false;
    if (isPositiveCumulativeVoteWeight(entry.cumulativeVoteWeight)) {
      member.cumulativeVoteWeight = entry.cumulativeVoteWeight;
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

/** Institutional voting membership is separate from administrative access. */
export function isDeliberativeMember(member: Member, sections: Section[]): boolean {
 const eligibleSections = new Set(sections.filter(section => section.category === 'deliberativa').map(section => section.id));
 return member.sectionIds.some(sectionId => eligibleSections.has(sectionId));
}

/** Past deliberative votes remain visible after a member is demoted. */
export function hasPersonalVoteHistory(member: Member, sections: Section[]): boolean {
 return member.hadDeliberativeHistory === true || isDeliberativeMember(member, sections);
}


/** Self-contained fixture choices for the opt-in voting laboratory. Never official ballots. */
export const PREVIEW_BINARY_OPTIONS = [
  {id:'sim', label:'Sim'}, {id:'nao', label:'Não'},
] as const;
export const PREVIEW_LIST_OPTIONS = [
  {id:'a', label:'Alternativa A'}, {id:'b', label:'Alternativa B'},
  {id:'c', label:'Alternativa C'},
] as const;

export type PreviewVote =
  | {method:'binaria'|'nominal'; selected:string}
  | {method:'ordenada'; ranking:string[]}
  | {method:'aprovacao'; approved:string[]}
  | {method:'escalar'; scores:Record<string,number>}
  | {method:'cumulativa'; allocation:Record<string,number>; weight:number};

export type PreviewVoteValidation =
  | {ok:true; vote:PreviewVote}
  | {ok:false; error:string};

/** Validate a single in-memory sample, not eligibility, authentication or an institutional tally. */
export function validatePreviewVote(method: DeliberationMethod, payload: unknown, cumulativeWeight?: number): PreviewVoteValidation {
  if(!isDeliberationMethod(method) || !payload || typeof payload!=='object' || Array.isArray(payload))
    return {ok:false,error:'Preencha um voto de demonstração válido.'};
  const data=payload as Record<string,unknown>;
  const choices=method==='binaria'?PREVIEW_BINARY_OPTIONS:PREVIEW_LIST_OPTIONS;
  const ids=choices.map(option=>option.id);
  const validId=(id:unknown):id is string=>typeof id==='string'&&ids.includes(id);
  const exactList=(items:unknown):items is string[]=>Array.isArray(items)&&
    items.every(validId)&&new Set(items).size===items.length;
  const numericChoices=(value:unknown,min:number,max:number):value is Record<string,number>=>{
    if(!value||typeof value!=='object'||Array.isArray(value))return false;
    const record=value as Record<string,unknown>;
    return Object.keys(record).length===ids.length &&
      ids.every(id=>Object.prototype.hasOwnProperty.call(record,id)&&
        typeof record[id]==='number'&&Number.isSafeInteger(record[id])&&
        (record[id] as number)>=min&&(record[id] as number)<=max);
  };
  if(method==='binaria'||method==='nominal') {
    if(!validId(data.selected))return {ok:false,error:'Selecione exatamente uma alternativa.'};
    return {ok:true,vote:{method,selected:data.selected}};
  }
  if(method==='ordenada') {
    if(!exactList(data.ranking)||data.ranking.length!==ids.length)
      return {ok:false,error:'Ordene todas as alternativas sem repetir posições.'};
    return {ok:true,vote:{method,ranking:[...data.ranking]}};
  }
  if(method==='aprovacao') {
    if(!exactList(data.approved)||data.approved.length===0)
      return {ok:false,error:'Marque pelo menos uma alternativa aceitável, sem repetições.'};
    return {ok:true,vote:{method,approved:[...data.approved]}};
  }
  if(method==='escalar') {
    if(!numericChoices(data.scores,1,10))
      return {ok:false,error:'Atribua uma nota inteira de 1 a 10 para cada alternativa.'};
    return {ok:true,vote:{method,scores:{...data.scores}}};
  }
  if(!isPositiveCumulativeVoteWeight(cumulativeWeight))
    return {ok:false,error:'Configure primeiro uma quantidade de votos para este membro.'};
  if(!numericChoices(data.allocation,0,cumulativeWeight))
    return {ok:false,error:'Distribua quantidades inteiras, sem valores negativos.'};
  const used=Object.values(data.allocation).reduce((total,value)=>total+value,0);
  if(!Number.isSafeInteger(used)||used===0||used>cumulativeWeight)
    return {ok:false,error:'Distribua pelo menos um voto, sem exceder a cota disponível.'};
  // Partial use of the quota is allowed ONLY in this sandbox; Academy policy remains undefined.
  return {ok:true,vote:{method:'cumulativa',allocation:{...data.allocation},weight:cumulativeWeight}};
}
