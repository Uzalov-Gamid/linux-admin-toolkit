#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 <source_dir> <backup_dir>" >&2
  exit 2
fi

source_dir=$1
backup_dir=$2

if [[ ! -d "$source_dir" ]]; then
  echo "source directory not found: $source_dir" >&2
  exit 1
fi

mkdir -p "$backup_dir"

source_name=$(basename "$source_dir")
timestamp=$(date +"%Y%m%d-%H%M%S")
archive="$backup_dir/${source_name}-${timestamp}.tar.gz"

tar --exclude=".git" --exclude="__pycache__" -czf "$archive" -C "$(dirname "$source_dir")" "$source_name"

echo "$archive"

