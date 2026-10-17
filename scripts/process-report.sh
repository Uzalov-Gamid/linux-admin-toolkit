#!/usr/bin/env bash
set -euo pipefail

limit=${1:-10}

if [[ ! "$limit" =~ ^[1-9][0-9]*$ ]]; then
  echo "limit must be a positive integer" >&2
  exit 2
fi

snapshot=$(ps aux)
header=$(printf '%s\n' "$snapshot" | sed -n '1p')

echo "Top processes by CPU:"
printf '%s\n' "$header"
printf '%s\n' "$snapshot" | sed '1d' | sort -k3,3nr | sed -n "1,${limit}p"

echo
echo "Top processes by memory:"
printf '%s\n' "$header"
printf '%s\n' "$snapshot" | sed '1d' | sort -k4,4nr | sed -n "1,${limit}p"
