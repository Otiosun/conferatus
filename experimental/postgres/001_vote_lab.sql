-- CONFFRATUS / experimental voting laboratory
-- DO NOT run against production or an Academy database.
-- Only an isolated CI PostgreSQL instance may execute this file.
-- No Academy authentication, institutional eligibility, election outcome or quorum is implied.
BEGIN;

DO $role$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'conffratus_lab_gateway') THEN
    CREATE ROLE conffratus_lab_gateway NOLOGIN;
  END IF;
END
$role$;
CREATE SCHEMA IF NOT EXISTS conffratus_vote_lab;
REVOKE ALL ON SCHEMA conffratus_vote_lab FROM PUBLIC;

CREATE TABLE IF NOT EXISTS conffratus_vote_lab.ballots (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  method text NOT NULL CHECK (method IN ('binaria','nominal','ordenada','aprovacao','escalar','cumulativa')),
  options jsonb NOT NULL CHECK (jsonb_typeof(options) = 'array'),
  state text NOT NULL DEFAULT 'draft' CHECK (state IN ('draft','open','closed')),
  -- False by default: only explicit fixture setup may enable this isolated lab.
  fixture_enabled boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS conffratus_vote_lab.fixture_voters (
  ballot_id uuid NOT NULL REFERENCES conffratus_vote_lab.ballots(id) ON DELETE RESTRICT,
  actor_ref text NOT NULL CHECK (actor_ref ~ '^[A-Za-z0-9_-]{1,64}$'),
  cumulative_quota integer CHECK (cumulative_quota BETWEEN 1 AND 1000000),
  PRIMARY KEY (ballot_id, actor_ref)
);

CREATE TABLE IF NOT EXISTS conffratus_vote_lab.votes (
  ballot_id uuid NOT NULL REFERENCES conffratus_vote_lab.ballots(id) ON DELETE RESTRICT,
  actor_ref text NOT NULL,
  request_id uuid NOT NULL,
  payload jsonb NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
  created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  PRIMARY KEY (ballot_id, actor_ref),
  UNIQUE (ballot_id, request_id),
  FOREIGN KEY (ballot_id, actor_ref)
    REFERENCES conffratus_vote_lab.fixture_voters(ballot_id, actor_ref) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS conffratus_vote_lab.audit (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ballot_id uuid NOT NULL REFERENCES conffratus_vote_lab.ballots(id) ON DELETE RESTRICT,
  actor_ref text NOT NULL,
  request_id uuid NOT NULL,
  kind text NOT NULL CHECK (kind = 'vote_recorded'),
  created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  UNIQUE (ballot_id, request_id)
);

-- Defence in depth: do not grant direct access. App-facing inserts happen in the function.
ALTER TABLE conffratus_vote_lab.ballots ENABLE ROW LEVEL SECURITY;
ALTER TABLE conffratus_vote_lab.fixture_voters ENABLE ROW LEVEL SECURITY;
ALTER TABLE conffratus_vote_lab.votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE conffratus_vote_lab.audit ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON ALL TABLES IN SCHEMA conffratus_vote_lab FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA conffratus_vote_lab FROM PUBLIC;

-- Protect accidental mutation of accepted votes and appended audit entries.
CREATE OR REPLACE FUNCTION conffratus_vote_lab.reject_mutation()
RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $body$
BEGIN
  RAISE EXCEPTION 'Accepted sample votes and audit entries cannot be updated or deleted'
    USING ERRCODE = 'check_violation';
END
$body$;
DROP TRIGGER IF EXISTS votes_no_mutation ON conffratus_vote_lab.votes;
CREATE TRIGGER votes_no_mutation
  BEFORE UPDATE OR DELETE ON conffratus_vote_lab.votes
  FOR EACH ROW EXECUTE FUNCTION conffratus_vote_lab.reject_mutation();
DROP TRIGGER IF EXISTS audit_no_mutation ON conffratus_vote_lab.audit;
CREATE TRIGGER audit_no_mutation
  BEFORE UPDATE OR DELETE ON conffratus_vote_lab.audit
  FOR EACH ROW EXECUTE FUNCTION conffratus_vote_lab.reject_mutation();

CREATE OR REPLACE FUNCTION conffratus_vote_lab.record_fixture_vote(
  p_ballot_id uuid, p_actor_ref text, p_request_id uuid, p_payload jsonb
) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = pg_catalog, conffratus_vote_lab
AS $body$
DECLARE
  b record;
  v_old record;
  v_quota integer;
  v_ids text[];
  v_count integer;
  v_key text;
  v_value jsonb;
  v_items jsonb;
  v_total bigint := 0;
  v_item record;
  v_reason text;
BEGIN
  -- The gateway role is only a synthetic test actor, never a user identity.
  IF p_ballot_id IS NULL OR p_request_id IS NULL
     OR p_actor_ref IS NULL OR p_actor_ref !~ '^[A-Za-z0-9_-]{1,64}$' THEN
    RETURN jsonb_build_object('status','invalid','reason','invalid_envelope');
  END IF;

  -- Serializes all writes to a ballot, including checks, insert and audit.
  -- Two requests racing for the same voter cannot both become accepted votes.
  SELECT * INTO b FROM conffratus_vote_lab.ballots WHERE id = p_ballot_id FOR UPDATE;
  IF NOT FOUND THEN
    RETURN jsonb_build_object('status','rejected','reason','unknown_ballot');
  END IF;

  -- Replayed successes return the original receipt, even after closing.
  SELECT actor_ref, payload INTO v_old
  FROM conffratus_vote_lab.votes
  WHERE ballot_id = p_ballot_id AND request_id = p_request_id;
  IF FOUND THEN
    IF v_old.actor_ref = p_actor_ref AND v_old.payload = p_payload THEN
      RETURN jsonb_build_object('status','replayed','request_id',p_request_id);
    END IF;
    RETURN jsonb_build_object('status','conflict','reason','request_reused');
  END IF;

  IF b.state <> 'open' OR NOT b.fixture_enabled THEN
    RETURN jsonb_build_object('status','rejected','reason','fixture_disabled_or_closed');
  END IF;

  SELECT cumulative_quota INTO v_quota
  FROM conffratus_vote_lab.fixture_voters
  WHERE ballot_id = p_ballot_id AND actor_ref = p_actor_ref;
  IF NOT FOUND THEN
    RETURN jsonb_build_object('status','rejected','reason','not_enrolled_in_fixture');
  END IF;

  IF EXISTS (
    SELECT 1 FROM conffratus_vote_lab.votes
    WHERE ballot_id = p_ballot_id AND actor_ref = p_actor_ref
  ) THEN
    -- "One vote per fixture voter" is a LAB concurrency invariant, not Academy policy.
    RETURN jsonb_build_object('status','rejected','reason','fixture_already_voted');
  END IF;

  IF jsonb_typeof(b.options) <> 'array' OR jsonb_array_length(b.options) NOT BETWEEN 2 AND 8
     OR EXISTS (
       SELECT 1 FROM jsonb_array_elements(b.options) item
       WHERE jsonb_typeof(item) IS DISTINCT FROM 'object'
         OR jsonb_typeof(item->'id') IS DISTINCT FROM 'string'
         OR (item->>'id') !~ '^[A-Za-z0-9_-]{1,40}$'
         OR jsonb_typeof(item->'label') IS DISTINCT FROM 'string'
         OR length(btrim(item->>'label')) NOT BETWEEN 1 AND 80
     ) THEN
    RETURN jsonb_build_object('status','invalid','reason','invalid_options');
  END IF;

  SELECT array_agg(item->>'id' ORDER BY ord) INTO v_ids
  FROM jsonb_array_elements(b.options) WITH ORDINALITY x(item,ord);
  v_count := cardinality(v_ids);
  IF (SELECT count(DISTINCT id) FROM unnest(v_ids) x(id)) <> v_count THEN
    RETURN jsonb_build_object('status','invalid','reason','duplicate_options');
  END IF;
  IF b.method = 'binaria'
     AND (v_count <> 2 OR NOT ('sim' = ANY(v_ids) AND 'nao' = ANY(v_ids))) THEN
    RETURN jsonb_build_object('status','invalid','reason','invalid_binary_options');
  END IF;

  IF jsonb_typeof(p_payload) IS DISTINCT FROM 'object' OR
     (SELECT count(*) FROM jsonb_object_keys(p_payload)) <> 1 THEN
    RETURN jsonb_build_object('status','invalid','reason','invalid_payload_shape');
  END IF;

  IF b.method IN ('binaria','nominal') THEN
    IF NOT (p_payload ? 'selected')
       OR jsonb_typeof(p_payload->'selected') IS DISTINCT FROM 'string'
       OR NOT (p_payload->>'selected' = ANY(v_ids)) THEN
      v_reason := 'invalid_single_choice';
    END IF;

  ELSIF b.method IN ('ordenada','aprovacao') THEN
    v_key := CASE WHEN b.method = 'ordenada' THEN 'ranking' ELSE 'approved' END;
    v_items := p_payload->v_key;
    IF jsonb_typeof(v_items) IS DISTINCT FROM 'array' THEN
      v_reason := 'invalid_array';
    ELSIF (b.method = 'ordenada' AND jsonb_array_length(v_items) <> v_count)
       OR (b.method = 'aprovacao' AND jsonb_array_length(v_items) < 1) THEN
      v_reason := 'invalid_choice_count';
    ELSIF EXISTS (
      SELECT 1 FROM jsonb_array_elements(v_items) item
      WHERE jsonb_typeof(item) IS DISTINCT FROM 'string' OR NOT (item#>>'{}' = ANY(v_ids))
    ) OR (
      SELECT count(DISTINCT item#>>'{}') <> count(*)
      FROM jsonb_array_elements(v_items) item
    ) THEN
      v_reason := 'invalid_rank_or_approval';
    END IF;

  ELSIF b.method IN ('escalar','cumulativa') THEN
    v_key := CASE WHEN b.method = 'escalar' THEN 'scores' ELSE 'allocation' END;
    v_items := p_payload->v_key;
    IF jsonb_typeof(v_items) IS DISTINCT FROM 'object' THEN
      v_reason := 'invalid_numeric_map';
    ELSIF (SELECT count(*) FROM jsonb_object_keys(v_items)) <> v_count THEN
      v_reason := 'invalid_numeric_count';
    ELSE
      FOR v_item IN SELECT key, value FROM jsonb_each(v_items)
      LOOP
        IF NOT (v_item.key = ANY(v_ids)) THEN
          v_reason := 'unknown_choice'; EXIT;
        END IF;
        IF b.method = 'escalar' THEN
          IF v_item.value::text !~ '^(10|[1-9])$' THEN
            v_reason := 'invalid_score'; EXIT;
          END IF;
        ELSE
          IF v_quota IS NULL THEN
            v_reason := 'quota_not_configured'; EXIT;
          END IF;
          IF v_item.value::text !~ '^(0|[1-9][0-9]{0,6})$' THEN
            v_reason := 'invalid_allocation'; EXIT;
          END IF;
          v_total := v_total + (v_item.value::text)::bigint;
        END IF;
      END LOOP;
      IF v_reason IS NULL AND b.method = 'cumulativa'
        AND (v_total < 1 OR v_total > v_quota) THEN
        v_reason := 'quota_exceeded_or_empty';
      END IF;
    END IF;
  END IF;

  IF v_reason IS NOT NULL THEN
    RETURN jsonb_build_object('status','invalid','reason',v_reason);
  END IF;

  INSERT INTO conffratus_vote_lab.votes (ballot_id, actor_ref, request_id, payload)
  VALUES (p_ballot_id, p_actor_ref, p_request_id, p_payload);
  INSERT INTO conffratus_vote_lab.audit (ballot_id, actor_ref, request_id, kind)
  VALUES (p_ballot_id, p_actor_ref, p_request_id, 'vote_recorded');

  RETURN jsonb_build_object('status','recorded','request_id',p_request_id);
END
$body$;

-- SECURITY DEFINER does not mean public! The role has EXECUTE only, not table access.
REVOKE ALL ON FUNCTION conffratus_vote_lab.record_fixture_vote(uuid,text,uuid,jsonb) FROM PUBLIC;
GRANT USAGE ON SCHEMA conffratus_vote_lab TO conffratus_lab_gateway;
GRANT EXECUTE ON FUNCTION conffratus_vote_lab.record_fixture_vote(uuid,text,uuid,jsonb)
  TO conffratus_lab_gateway;
COMMIT;
