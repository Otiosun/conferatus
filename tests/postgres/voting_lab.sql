-- Executed ONLY on CI's disposable PostgreSQL service. All IDs/data are synthetic.
\set ON_ERROR_STOP on

INSERT INTO conffratus_vote_lab.ballots (id,method,options,state,fixture_enabled) VALUES
 ('11111111-1111-4111-8111-111111111111','nominal',
 '[{"id":"a","label":"Alternativa A"},{"id":"b","label":"Alternativa B"},{"id":"c","label":"Alternativa C"}]','open',true),
 ('22222222-2222-4222-8222-222222222222','binaria',
 '[{"id":"sim","label":"Sim"},{"id":"nao","label":"Não"}]','open',true),
 ('33333333-3333-4333-8333-333333333333','ordenada',
 '[{"id":"a","label":"A"},{"id":"b","label":"B"},{"id":"c","label":"C"}]','open',true),
 ('44444444-4444-4444-8444-444444444444','aprovacao',
 '[{"id":"a","label":"A"},{"id":"b","label":"B"},{"id":"c","label":"C"}]','open',true),
 ('55555555-5555-4555-8555-555555555555','escalar',
 '[{"id":"a","label":"A"},{"id":"b","label":"B"},{"id":"c","label":"C"}]','open',true),
 ('66666666-6666-4666-8666-666666666666','cumulativa',
 '[{"id":"a","label":"A"},{"id":"b","label":"B"},{"id":"c","label":"C"}]','open',true),
 ('77777777-7777-4777-8777-777777777777','nominal',
 '[{"id":"a","label":"A"},{"id":"b","label":"B"}]','open',false),
 ('88888888-8888-4888-8888-888888888888','nominal',
 '[{"id":"a","label":"A"},{"id":"b","label":"B"}]','open',true);

INSERT INTO conffratus_vote_lab.fixture_voters (ballot_id,actor_ref,cumulative_quota) VALUES
 ('11111111-1111-4111-8111-111111111111','nominal_one',NULL),
 ('11111111-1111-4111-8111-111111111111','nominal_two',NULL),
 ('22222222-2222-4222-8222-222222222222','binary_one',NULL),
 ('33333333-3333-4333-8333-333333333333','rank_one',NULL),
 ('44444444-4444-4444-8444-444444444444','approval_one',NULL),
 ('55555555-5555-4555-8555-555555555555','scalar_one',NULL),
 ('66666666-6666-4666-8666-666666666666','quota_one',4),
 ('66666666-6666-4666-8666-666666666666','quota_missing',NULL),
 ('77777777-7777-4777-8777-777777777777','disabled_one',NULL),
 ('88888888-8888-4888-8888-888888888888','race_one',NULL),
 ('88888888-8888-4888-8888-888888888888','race_two',NULL);

DO $checks$
DECLARE
  result jsonb;
  nominal uuid := '11111111-1111-4111-8111-111111111111';
  binary_ballot uuid := '22222222-2222-4222-8222-222222222222';
  rank_ballot uuid := '33333333-3333-4333-8333-333333333333';
  approval_ballot uuid := '44444444-4444-4444-8444-444444444444';
  scalar_ballot uuid := '55555555-5555-4555-8555-555555555555';
  quota_ballot uuid := '66666666-6666-4666-8666-666666666666';
  disabled_ballot uuid := '77777777-7777-4777-8777-777777777777';
  request_one uuid := 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
BEGIN
  result := conffratus_vote_lab.record_fixture_vote(disabled_ballot,'disabled_one',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'reason' <> 'fixture_disabled_or_closed' THEN RAISE EXCEPTION 'Default-closed policy failed: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(nominal,'outsider',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'reason' <> 'not_enrolled_in_fixture' THEN RAISE EXCEPTION 'Unlisted actor accepted: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_one',gen_random_uuid(),'{}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Empty payload accepted: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_one',gen_random_uuid(),'{"selected":"a","junk":1}');
  IF result->>'reason' <> 'invalid_payload_shape' THEN RAISE EXCEPTION 'Unexpected field allowed: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_one',request_one,'{"selected":"b"}');
  IF result->>'status' <> 'recorded' THEN RAISE EXCEPTION 'Nominal vote failed: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_one',request_one,'{"selected":"b"}');
  IF result->>'status' <> 'replayed' THEN RAISE EXCEPTION 'Idempotent retry failed: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_one',request_one,'{"selected":"a"}');
  IF result->>'reason' <> 'request_reused' THEN RAISE EXCEPTION 'Idempotency conflict not detected: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_two',request_one,'{"selected":"b"}');
  IF result->>'reason' <> 'request_reused' THEN RAISE EXCEPTION 'Cross-actor request reuse allowed: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_one',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'reason' <> 'fixture_already_voted' THEN RAISE EXCEPTION 'Second vote allowed: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(binary_ballot,'binary_one',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Unknown binary option accepted'; END IF;
  result := conffratus_vote_lab.record_fixture_vote(binary_ballot,'binary_one',gen_random_uuid(),'{"selected":"sim"}');
  IF result->>'status' <> 'recorded' THEN RAISE EXCEPTION 'Binary vote failed: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(rank_ballot,'rank_one',gen_random_uuid(),'{"ranking":["a","a","c"]}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Duplicate rank accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(rank_ballot,'rank_one',gen_random_uuid(),'{}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Missing rank accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(rank_ballot,'rank_one',gen_random_uuid(),'{"ranking":["b","a","c"]}');
  IF result->>'status' <> 'recorded' THEN RAISE EXCEPTION 'Ranked vote failed: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(approval_ballot,'approval_one',gen_random_uuid(),'{"approved":[]}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Empty approval accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(approval_ballot,'approval_one',gen_random_uuid(),'{"approved":["a","a"]}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Duplicate approval accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(approval_ballot,'approval_one',gen_random_uuid(),'{"approved":["a","c"]}');
  IF result->>'status' <> 'recorded' THEN RAISE EXCEPTION 'Approval vote failed: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(scalar_ballot,'scalar_one',gen_random_uuid(),'{"scores":{"a":0,"b":4,"c":10}}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Scalar zero accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(scalar_ballot,'scalar_one',gen_random_uuid(),'{"scores":{"a":1,"b":5,"c":"9"}}');
  IF result->>'status' <> 'invalid' THEN RAISE EXCEPTION 'Scalar string accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(scalar_ballot,'scalar_one',gen_random_uuid(),'{"scores":{"a":1,"b":5,"c":10}}');
  IF result->>'status' <> 'recorded' THEN RAISE EXCEPTION 'Scalar vote failed: %',result; END IF;

  result := conffratus_vote_lab.record_fixture_vote(quota_ballot,'quota_missing',gen_random_uuid(),'{"allocation":{"a":1,"b":0,"c":0}}');
  IF result->>'reason' <> 'quota_not_configured' THEN RAISE EXCEPTION 'Unconfigured quota accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(quota_ballot,'quota_one',gen_random_uuid(),'{"allocation":{"a":3,"b":2,"c":0}}');
  IF result->>'reason' <> 'quota_exceeded_or_empty' THEN RAISE EXCEPTION 'Excess quota accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(quota_ballot,'quota_one',gen_random_uuid(),'{"allocation":{"a":0,"b":0,"c":0}}');
  IF result->>'reason' <> 'quota_exceeded_or_empty' THEN RAISE EXCEPTION 'Empty quota accepted: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(quota_ballot,'quota_one',gen_random_uuid(),'{"allocation":{"a":3,"b":1,"c":0}}');
  IF result->>'status' <> 'recorded' THEN RAISE EXCEPTION 'Cumulative vote failed: %',result; END IF;

  IF (SELECT count(*) FROM conffratus_vote_lab.votes) <> 6 THEN
    RAISE EXCEPTION 'Expected precisely 6 accepted votes';
  END IF;
  IF (SELECT count(*) FROM conffratus_vote_lab.audit) <> 6 THEN
    RAISE EXCEPTION 'Audit not atomic with vote writes';
  END IF;

  UPDATE conffratus_vote_lab.ballots SET state='closed' WHERE id=nominal;
  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_one',request_one,'{"selected":"b"}');
  IF result->>'status' <> 'replayed' THEN RAISE EXCEPTION 'Replay after close failed: %',result; END IF;
  result := conffratus_vote_lab.record_fixture_vote(nominal,'nominal_two',gen_random_uuid(),'{"selected":"a"}');
  IF result->>'reason' <> 'fixture_disabled_or_closed' THEN RAISE EXCEPTION 'Closed ballot accepted: %',result; END IF;

  BEGIN
    UPDATE conffratus_vote_lab.votes SET payload='{}' WHERE ballot_id=nominal;
    RAISE EXCEPTION 'Mutation trigger absent';
  EXCEPTION WHEN check_violation THEN NULL;
  END;
  BEGIN
    DELETE FROM conffratus_vote_lab.audit WHERE ballot_id=nominal;
    RAISE EXCEPTION 'Audit deletion trigger absent';
  EXCEPTION WHEN check_violation THEN NULL;
  END;
  IF (SELECT count(*) FROM conffratus_vote_lab.audit) <> 6 THEN
    RAISE EXCEPTION 'Audit changed after mutation attempt';
  END IF;
  RAISE NOTICE 'Six voting modalities and fail-closed/idempotent/immutable checks passed';
END
$checks$;
