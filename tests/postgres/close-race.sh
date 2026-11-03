#!/usr/bin/env bash
# A ballot closure is serialized against a racing write via the ballot row lock.
# CI-only PostgreSQL with synthetic fixtures; NO institutional data.
set -euo pipefail
query() { psql -X -qAt -v ON_ERROR_STOP=1 -c "$1"; }
ballot="cccccccc-cccc-4ccc-8ccc-cccccccccccc"

query "INSERT INTO conffratus_vote_lab.ballots(id,method,options,state,fixture_enabled)
 VALUES ('$ballot','nominal','[{\"id\":\"a\",\"label\":\"A\"},{\"id\":\"b\",\"label\":\"B\"}]'::jsonb,'open',true);"
query "INSERT INTO conffratus_vote_lab.fixture_voters(ballot_id,actor_ref)
 VALUES ('$ballot','closing_race_actor');"

temp="$(mktemp -d)"
trap 'rm -rf "$temp"' EXIT

# The closer updates state but holds its transaction open while sleeping.
# Poll PgSleep state instead of relying on an arbitrary unverified delay.
PGAPPNAME=conffratus-lab-closer psql -X -qAt -v ON_ERROR_STOP=1 -c \
 "BEGIN; UPDATE conffratus_vote_lab.ballots SET state='closed' WHERE id='$ballot';
 SELECT pg_sleep(5); COMMIT;" >"$temp/closer.out" 2>"$temp/closer.err" &
closer="$!"

ready=0
for i in $(seq 1 35); do
  sleeping="$(query "SELECT count(*) FROM pg_stat_activity
     WHERE application_name='conffratus-lab-closer' AND state='active' AND wait_event='PgSleep';")"
  if [[ "$sleeping" == "1" ]]; then ready=1; break; fi
  sleep 0.1
done
if [[ "$ready" != "1" ]]; then
  echo "FAIL: close transaction did not reach lock-held state" >&2
  cat "$temp/closer.err" >&2
  wait "$closer" || true
  exit 1
fi

answer="$(query "SET ROLE conffratus_lab_gateway;
 SELECT conffratus_vote_lab.record_fixture_vote(
  '$ballot','closing_race_actor',gen_random_uuid(),'{\"selected\":\"a\"}'::jsonb
 )->>'reason';")"
wait "$closer"

[[ "$answer" == "fixture_disabled_or_closed" ]] ||
 { echo "FAIL: vote entered a concurrently closing ballot: $answer" >&2; exit 1; }
[[ "$(query "SELECT state FROM conffratus_vote_lab.ballots WHERE id='$ballot';")" == "closed" ]] ||
 { echo "FAIL: closure did not commit" >&2; exit 1; }
[[ "$(query "SELECT count(*) FROM conffratus_vote_lab.votes WHERE ballot_id='$ballot';")" == "0" ]] ||
 { echo "FAIL: recorded vote while closure held row lock" >&2; exit 1; }
[[ "$(query "SELECT count(*) FROM conffratus_vote_lab.audit WHERE ballot_id='$ballot';")" == "0" ]] ||
 { echo "FAIL: audit written for a rejected vote" >&2; exit 1; }
echo "PostgreSQL close/write race PASS: ballot row lock prevents vote after closure"
