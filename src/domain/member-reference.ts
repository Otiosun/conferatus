import type { Member } from './types.js';

/**
 * An ACDM ID is an opaque directory reference, not proof of an Academy session.
 * Never infer roles, eligibility, identity ownership or voting permissions here.
 */
export type MemberReferenceResult =
  | Readonly<{ state: 'found'; member: Member }>
  | Readonly<{ state: 'not-found' | 'ambiguous' }>;

export function resolveMemberReference(directory: readonly Member[], reference: string): MemberReferenceResult {
  // The preview already uses these characters for synthetic identifiers.
  // Real Academy formats must be supplied by its owner, not guessed here.
  if (!/^[A-Za-z0-9_-]{3,40}$/.test(reference)) return { state: 'not-found' };
  const matches = directory.filter(member => member.acdmId === reference);
  if (matches.length > 1) return { state: 'ambiguous' };
  const member = matches[0];
  return member ? { state: 'found', member } : { state: 'not-found' };
}
