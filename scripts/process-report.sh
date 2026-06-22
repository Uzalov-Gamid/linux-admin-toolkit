#!/usr/bin/env bash
set -euo pipefail

limit=${1:-10}

echo "Top processes by CPU:"
ps aux | sort -rk 3,3 | head -n "$((limit + 1))"

echo
echo "Top processes by memory:"
ps aux | sort -rk 4,4 | head -n "$((limit + 1))"

