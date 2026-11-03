import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveMemberReference } from '../dist/domain/member-reference.js';
import { members } from '../dist/data/fixtures.js';

test('ACDM ID resolves one synthetic profile without authorizing anything', () => {
  const result = resolveMemberReference(members, 'DEMO-0002');
  assert.equal(result.state, 'found');
  assert.equal(result.member?.id, 'm02');
  assert.equal('canVote' in result, false);
  assert.equal('role' in result, false);
  assert.equal('session' in result, false);
});

test('missing, malformed, unknown and ambiguous reference never resolve a profile', () => {
  for (const id of ['', 'x', 'DEMO-UNLISTED', '../profile/m02', 'A'.repeat(100)]) {
    assert.equal(resolveMemberReference(members, id).state, 'not-found');
  }
  const duplicates = [{...members[0],acdmId:'REF-42'}, {...members[1],acdmId:'REF-42'}];
  assert.equal(resolveMemberReference(duplicates, 'REF-42').state, 'ambiguous');
});

test('ACDM ID is an opaque, exact reference rather than a normalized credential', () => {
  assert.equal(resolveMemberReference(members,'DEMO-0002').state,'found');
  assert.equal(resolveMemberReference(members,'demo-0002').state,'not-found');
  assert.equal(resolveMemberReference(members,' DEMO-0002 ').state,'not-found');
});
