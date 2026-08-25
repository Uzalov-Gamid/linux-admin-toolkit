#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
process_report="$project_root/scripts/process-report.sh"

assert_invalid_limit() {
  local value=$1
  local output

  if output=$("$process_report" "$value" 2>&1); then
    echo "expected process-report.sh to reject limit: $value" >&2
    exit 1
  fi

  if [[ "$output" != "limit must be a positive integer" ]]; then
    echo "unexpected validation message for limit: $value" >&2
    exit 1
  fi
}

assert_invalid_limit 0
assert_invalid_limit -1
assert_invalid_limit abc

echo "script argument validation passed"
