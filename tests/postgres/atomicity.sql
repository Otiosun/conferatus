-- CI-only fault injection: force the second INSERT (audit) to fail, then assert
-- that PostgreSQL automatically rolls back the preceding vote INSERT.
-- The deliberately orphaned audit row exists only in the disposable test DB.
\set ON_ERROR_STOP on
INSERT INTO conffratus_vote_lab.ballots(id,method,options,state,fixture_enabled)
VALUES (
 '99999999-1111-4999-8999-999999999999','nominal',
 '[{"id":"a","label":"A"},{"id":"b","label":"B"}]','open',true
);
INSERT INTO conffratus_vote_lab.fixture_voters(ballot_id,actor_ref)
VALUES ('99999999-1111-4999-8999-999999999999','fault_one');

-- Synthetic pre-existing unique index collision, inserted with privileged CI setup.
INSERT INTO conffratus_vote_lab.audit(ballot_id,actor_ref,request_id,kind)
VALUES(
 '99999999-1111-4999-8999-999999999999','fault_one',
 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','vote_recorded'
);

DO $fault$
DECLARE
 fault_ballot_id uuid := '99999999-1111-4999-8999-999999999999';
 request_key uuid := 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb';
BEGIN
 BEGIN
   PERFORM conffratus_vote_lab.record_fixture_vote(fault_ballot_id,'fault_one',request_key,'{"selected":"a"}');
   RAISE EXCEPTION 'Audit collision did not reject transaction';
 EXCEPTION WHEN unique_violation THEN
   -- The audit unique index rejected the same request_id after vote insertion.
   NULL;
 END;

 IF EXISTS (SELECT 1 FROM conffratus_vote_lab.votes WHERE ballot_id=fault_ballot_id) THEN
   RAISE EXCEPTION 'Atomicity violated: vote survived audit insert failure';
 END IF;
 IF (SELECT count(*) FROM conffratus_vote_lab.audit WHERE ballot_id=fault_ballot_id) <> 1 THEN
   RAISE EXCEPTION 'Audit count unexpected after controlled fault';
 END IF;

 -- A new clean request can succeed; failed request did not consume actor's vote.
 IF (conffratus_vote_lab.record_fixture_vote(
   fault_ballot_id,'fault_one',gen_random_uuid(),'{"selected":"b"}'
 ))->>'status' <> 'recorded' THEN
   RAISE EXCEPTION 'Atomicity violated: valid retry after rollback was denied';
 END IF;
 IF (SELECT count(*) FROM conffratus_vote_lab.votes WHERE ballot_id=fault_ballot_id) <> 1 THEN
   RAISE EXCEPTION 'Valid retry should record exactly one accepted vote';
 END IF;
 RAISE NOTICE 'Audit-insert fault injection: complete vote rollback and subsequent retry PASS';
END
$fault$;
