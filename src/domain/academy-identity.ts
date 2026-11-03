/**
 * Integration boundary for the Academy's existing authentication system.
 * An ACDM ID is a reference to an institutional record, NEVER a login token
 * or evidence that the holder may vote or manage a deliberation.
 */
export type AcademyIdentity =
  | Readonly<{ state: 'unavailable' }>
  | Readonly<{ state: 'identified'; acdmId: string }>;

export interface AcademyIdentityProvider {
  currentIdentity(): Promise<AcademyIdentity>;
}

/** Offline CONFFRATUS has no Academy login and must never invent one. */
export class UnconnectedAcademyIdentityProvider implements AcademyIdentityProvider {
  async currentIdentity(): Promise<AcademyIdentity> {
    return { state: 'unavailable' };
  }
}

/**
 * Identity is deliberately NOT an authorization result. An integrated server
 * must separately validate its own session, section eligibility and grants.
 * This is also safe for a mock provider in contract tests.
 */
export function identityReference(identity: AcademyIdentity): string | null {
  return identity.state === 'identified' ? identity.acdmId : null;
}
