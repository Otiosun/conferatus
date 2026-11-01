export type MemberId = string;
export type SectionId = string;
export type Role = 'diretor' | 'membro';
export type BallotStatus = 'aberta' | 'encerrada';
export interface Member {
  id: MemberId;
  name: string;
  acdmId?: string;
  subtitle: string;
  totalVotes: number;
  proposals: number;
  approved: number;
  collaborations: number;
  sectionIds: SectionId[];
  role: Role;
  /** Previous deliberative participation remains on record after a demotion. */
  hadDeliberativeHistory?: boolean;
}
export interface Section {
  id: SectionId;
  name: string;
  category: 'deliberativa' | 'comum';
  places?: number;
}
export interface OptionResult {
  id: string;
  label: string;
  votes: number;
}
export interface Ballot {
  id: string;
  title: string;
  section: string;
  description: string;
  status: BallotStatus;
  options: OptionResult[];
}
export interface Activity {
  id: string;
  memberId: MemberId;
  type: 'voto' | 'proposicao';
  title: string;
  section: string;
  code: string;
  summary: string;
  approved: boolean;
  votes: number;
  percentage: number;
}
export interface GovernanceChange {
  kind: 'rebaixamento' | 'desvinculo' | 'vinculo';
  memberId: MemberId;
  sectionId: SectionId;
  previousSectionIds: SectionId[];
  nextSectionIds: SectionId[];
  previousRole: Role;
  nextRole: Role;
}

// Planned model for the eventual authenticated voting system; not yet stored on a server.
export interface PersonalVoteRecord {
  ballotId: string;
  memberId: MemberId;
  optionId: string;
  recordedAt: string;
}
