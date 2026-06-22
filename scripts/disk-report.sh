#!/usr/bin/env bash
set -euo pipefail

target=${1:-.}

if [[ ! -e "$target" ]]; then
  echo "target not found: $target" >&2
  exit 1
fi

echo "Filesystem usage:"
df -h .

echo
echo "Target usage:"
du -sh "$target"

echo
echo "Largest entries:"
du -sh "$target"/* 2>/dev/null | sort -hr | head -10 || true

