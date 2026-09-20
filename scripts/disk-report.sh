#!/usr/bin/env bash
set -euo pipefail

target=${1:-.}
if [[ "$target" == -* ]]; then target="./$target"; fi

if [[ ! -e "$target" ]]; then
  echo "target not found: $target" >&2
  exit 1
fi

echo "Filesystem usage:"
df -h "$target"

echo
echo "Target usage:"
du -sh "$target"

echo
echo "Largest entries:"
if [[ -d "$target" ]]; then
  shopt -s nullglob dotglob
  entries=("$target"/*)
  if (( ${#entries[@]} )); then
    du -sh "${entries[@]}" | sort -hr | sed -n '1,10p'
  fi
else
  du -sh "$target"
fi

