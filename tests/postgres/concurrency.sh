#!/usr/bin/env bash
# Disposable CI database only; no Academy identities or real votes.
set -euo pipefail
cd "$(dirname "$0")/../.."
query() { psql -X -qAt -v ON_ERROR_STOP=1 -c "$1"; }
ballot="88888888-8888-4888-8888-888888888888"
request="99999999-9999-4999-8999-999999999999"
temp_dir="$(mktemp -d)"
trap 'rm -rf "$temp_dir"' EXIT

# The gateway may call a secured function, never inspect raw ballots directly.
if query 'SET ROLE conffratus_lab_gateway; SELECT count(*) FROM conffratus_vote_lab.votes;' >"$temp_dir/denied.out" 2>"$temp_dir/denied.err"; then
  echo "FAIL: gateway unexpectedly has direct vote-table access" >&2
  exit 1
fi
if query "SET ROLE conffratus_lab_guest; SELECT conffratus_vote_lab.record_fixture_vote(
  '$ballot','race_one','$request','{\"selected\":\"a\"}'::jsonb
)->>'status';" >"$temp_dir/guest.out" 2>"$temp_dir/guest.err"; then
  echo "FAIL: unprivileged test role invoked voting gateway" >&2
  exit 1
fi
if ! grep -qi "permission denied" "$temp_dir/guest.err"; then
  echo "FAIL: guest denial had unexpected error" >&2
  cat "$temp_dir/guest.err" >&2
  exit 1
fi
if ! grep -qi "permission denied" "$temp_dir/denied.err"; then
  echo "FAIL: expected permission error" >&2
  cat "$temp_dir/denied.err" >&2
  exit 1
fi

pids=""
for i in $(seq 1 12); do
  (
    query "SET ROLE conffratus_lab_gateway; SELECT conffratus_vote_lab.record_fixture_vote(
      '$ballot', 'race_one', '$request', '{\"selected\":\"a\"}'::jsonb
    )->>'status';"
  ) >"$temp_dir/$i.out" 2>"$temp_dir/$i.err" &
  pids="$pids $!"
done
for pid in $pids; do wait "$pid"; done

recorded=0
replayed=0
for i in $(seq 1 12); do
  result="$(tr -d '[:space:]' < "$temp_dir/$i.out")"
  case "$result" in
    recorded) recorded=$((recorded+1)) ;;
    replayed) replayed=$((replayed+1)) ;;
    *) echo "FAIL: concurrent request $i returned '$result'" >&2; cat "$temp_dir/$i.err" >&2; exit 1 ;;
  esac
done
[[ "$recorded" -eq 1 && "$replayed" -eq 11 ]] ||
  { echo "FAIL: expected 1 recorded + 11 replays; got $recorded / $replayed" >&2; exit 1; }

pids=""
for i in $(seq 1 6); do
  query "SET ROLE conffratus_lab_gateway; SELECT conffratus_vote_lab.record_fixture_vote(
    '$ballot', 'race_one', gen_random_uuid(), '{\"selected\":\"b\"}'::jsonb
  )->>'reason';" >"$temp_dir/new-$i.out" &
  pids="$pids $!"
done
for pid in $pids; do wait "$pid"; done
for i in $(seq 1 6); do
  [[ "$(tr -d '[:space:]' < "$temp_dir/new-$i.out")" == "fixture_already_voted" ]] ||
    { echo "FAIL: new request was not blocked" >&2; exit 1; }
done

conflict="$(query "SET ROLE conffratus_lab_gateway; SELECT conffratus_vote_lab.record_fixture_vote(
 '$ballot', 'race_two', '$request', '{\"selected\":\"a\"}'::jsonb
)->>'reason';")"
[[ "$conflict" == "request_reused" ]] || { echo "FAIL: cross-actor token reuse allowed" >&2; exit 1; }

votes="$(query "SELECT count(*) FROM conffratus_vote_lab.votes WHERE ballot_id='$ballot';")"
audits="$(query "SELECT count(*) FROM conffratus_vote_lab.audit WHERE ballot_id='$ballot';")"
[[ "$votes" == "1" && "$audits" == "1" ]] ||
  { echo "FAIL: expected one vote and one audit row; got $votes/$audits" >&2; exit 1; }
second_actor="$(query "SET ROLE conffratus_lab_gateway; SELECT conffratus_vote_lab.record_fixture_vote(
 '$ballot', 'race_two', gen_random_uuid(), '{\"selected\":\"b\"}'::jsonb
)->>'status';")"
[[ "$second_actor" == "recorded" ]] ||
 { echo "FAIL: separate qualified fixture actor was blocked: $second_actor" >&2; exit 1; }
votes="$(query "SELECT count(*) FROM conffratus_vote_lab.votes WHERE ballot_id='$ballot';")"
audits="$(query "SELECT count(*) FROM conffratus_vote_lab.audit WHERE ballot_id='$ballot';")"
[[ "$votes" == "2" && "$audits" == "2" ]] ||
 { echo "FAIL: two independent actors should have two votes and two audit records" >&2; exit 1; }
echo "PostgreSQL concurrency PASS: 1 recorded; 11 replays; 6 blocked duplicates; second actor accepted; audit atomic"
