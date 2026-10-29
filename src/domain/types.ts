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
}
export interface Section {
  id: SectionId;
  name: string;
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
  kind: 'rebaixamento' | 'restauracao' | 'vinculo';
  memberId: MemberId;
  sectionId: SectionId;
  previousSectionIds: SectionId[];
  nextSectionIds: SectionId[];
}
