import test from 'node:test';
import assert from 'node:assert/strict';
import { UnconnectedAcademyIdentityProvider, identityReference } from '../dist/domain/academy-identity.js';

test('offline preview has no institutional identity, even when asked repeatedly', async () => {
 const provider = new UnconnectedAcademyIdentityProvider();
 for (let i=0;i<3;i++) {
  const session = await provider.currentIdentity();
  assert.deepEqual(session, {state:'unavailable'});
  assert.equal(identityReference(session), null);
  assert.equal('role' in session, false);
  assert.equal('token' in session, false);
 }
});

test('external identity adapter contract exposes reference only, not roles or voting permission', async () => {
 const fakeAdapter = {async currentIdentity() {return {state:'identified',acdmId:'ACDM-SAMPLE'};}};
 const identity = await fakeAdapter.currentIdentity();
 assert.equal(identityReference(identity), 'ACDM-SAMPLE');
 assert.equal('role' in identity, false);
 assert.equal('canVote' in identity, false);
});
