#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <access.log>" >&2
  exit 2
fi

python3 -m toolkit.log_analyzer "$1"

