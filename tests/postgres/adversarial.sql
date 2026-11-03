-- CI-only adversarial payload and schema-gate tests on an isolated PostgreSQL service.
\set ON_ERROR_STOP on
DO $role$ BEGIN
 IF NOT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='conffratus_lab_guest') THEN
  CREATE ROLE conffratus_lab_guest NOLOGIN;
 END IF;
END $role$;

INSERT INTO conffratus_vote_lab.fixture_voters(ballot_id,actor_ref,cumulative_quota) VALUES
 ('33333333-3333-4333-8333-333333333333','rank_edge',NULL),
 ('44444444-4444-4444-8444-444444444444','approve_edge',NULL),
 ('55555555-5555-4555-8555-555555555555','score_edge',NULL),
 ('66666666-6666-4666-8666-666666666666','quota_edge',4);

INSERT INTO conffratus_vote_lab.ballots(id,method,options,state,fixture_enabled) VALUES
 ('aaaaaaa1-1111-4111-8111-111111111111','nominal',
  '[{"id":"a","label":"A"},{"id":"a","label":"Duplicated"}]','open',true),
 ('aaaaaaa2-2222-4222-8222-222222222222','nominal',
  '[{"id":"a","label":"A"},{"id":"b"}]','open',true),
 ('aaaaaaa3-3333-4333-8333-333333333333','binaria',
  '[{"id":"a","label":"A"},{"id":"b","label":"B"}]','open',true);
INSERT INTO conffratus_vote_lab.fixture_voters(ballot_id,actor_ref)
VALUES
 ('aaaaaaa1-1111-4111-8111-111111111111','bad_options_one'),
 ('aaaaaaa2-2222-4222-8222-222222222222','bad_options_two'),
 ('aaaaaaa3-3333-4333-8333-333333333333','bad_binary');

DO $adversarial$
DECLARE
  result jsonb;
  rank_id uuid := '33333333-3333-4333-8333-333333333333';
  approval_id uuid := '44444444-4444-4444-8444-444444444444';
  scalar_id uuid := '55555555-5555-4555-8555-555555555555';
  cumulative_id uuid := '66666666-6666-4666-8666-666666666666';
BEGIN
  result:=conffratus_vote_lab.record_fixture_vote(rank_id,'rank_edge',gen_random_uuid(),'{}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'Missing ranking accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(rank_id,'rank_edge',gen_random_uuid(),'{"ranking":null}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'NULL ranking accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(rank_id,'rank_edge',gen_random_uuid(),'{"ranking":["a",3,"c"]}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'Numeric ranking accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(approval_id,'approve_edge',gen_random_uuid(),'{"approved":null}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'NULL approval accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(approval_id,'approve_edge',gen_random_uuid(),'{"approved":["a","a"]}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'Duplicate approvals accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(scalar_id,'score_edge',gen_random_uuid(),'{"scores":{"a":1,"b":"2","c":3}}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'String score accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(scalar_id,'score_edge',gen_random_uuid(),'{"scores":{"a":1,"b":2,"c":1000000000000000000000000000000}}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'Huge score accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(cumulative_id,'quota_edge',gen_random_uuid(),'{"allocation":{"a":1,"b":-1,"c":0}}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'Negative quota accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(cumulative_id,'quota_edge',gen_random_uuid(),'{"allocation":{"a":10000000000000000000000,"b":0,"c":0}}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'Overflow quota not safely rejected: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(cumulative_id,'quota_edge',gen_random_uuid(),'{"allocation":{"a":1.5,"b":0,"c":0}}');
  IF result->>'status'<>'invalid' THEN RAISE EXCEPTION 'Fraction quota accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote(cumulative_id,'x'';DROP TABLE votes;--',gen_random_uuid(),'{"allocation":{"a":1,"b":0,"c":0}}');
  IF result->>'reason'<>'invalid_envelope' THEN RAISE EXCEPTION 'Unsafe synthetic actor accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote('aaaaaaa1-1111-4111-8111-111111111111','bad_options_one',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'reason'<>'duplicate_options' THEN RAISE EXCEPTION 'Duplicate option IDs not rejected: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote('aaaaaaa2-2222-4222-8222-222222222222','bad_options_two',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'reason'<>'invalid_options' THEN RAISE EXCEPTION 'Missing option label accepted: %',result; END IF;

  result:=conffratus_vote_lab.record_fixture_vote('aaaaaaa3-3333-4333-8333-333333333333','bad_binary',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'reason'<>'invalid_binary_options' THEN RAISE EXCEPTION 'Wrong binary option set accepted: %',result; END IF;

  IF (SELECT count(*) FROM conffratus_vote_lab.votes)<>6 THEN
    RAISE EXCEPTION 'Malformed payloads changed accepted vote counts';
  END IF;
  IF (SELECT count(*) FROM conffratus_vote_lab.audit)<>6 THEN
    RAISE EXCEPTION 'Malformed payloads created audit records';
  END IF;
  RAISE NOTICE 'Malicious, malformed and overflow inputs rejected without writes: PASS';
END
$adversarial$;
