import type { Member, MemberId, Section } from './types.js';
import { members, sections } from '../data/fixtures.js';

/** A real Academy member adapter can replace this without modifying pages. */
export interface MemberProvider {
  listMembers(): Promise<Member[]>;
  getMember(id: MemberId): Promise<Member | undefined>;
  listSections(): Promise<Section[]>;
}
export class FixtureMemberProvider implements MemberProvider {
  async listMembers() { return members.map(m => ({ ...m, sectionIds: [...m.sectionIds] })); }
  async getMember(id: MemberId) { return (await this.listMembers()).find(m => m.id === id); }
  async listSections() { return [...sections]; }
}
