import argparse
import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[[^\]]+\] "(?P<method>[A-Z]+) (?P<path>\S+) [^"]+" (?P<status>\d{3}) (?P<size>\S+)'
)


def analyze_log(path: Path, top: int = 5) -> dict[str, Any]:
    if top < 1:
        raise ValueError("top must be a positive integer")
    status_codes: Counter[str] = Counter()
    methods: Counter[str] = Counter()
    paths: Counter[str] = Counter()
    total = 0

    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as log_file:
        for line in log_file:
            match = LOG_PATTERN.match(line)
            if not match:
                continue
            total += 1
            status_codes[match.group("status")] += 1
            methods[match.group("method")] += 1
            paths[match.group("path")] += 1

    return {
        "total_requests": total,
        "status_codes": dict(status_codes.most_common()),
        "methods": dict(methods.most_common()),
        "top_paths": dict(paths.most_common(top)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize HTTP access logs")
    parser.add_argument("path", type=Path)
    parser.add_argument("--top", type=int, default=5, help="Number of paths to show")
    args = parser.parse_args()
    if args.top < 1:
        parser.error("--top must be a positive integer")

    path = args.path
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1

    try:
        result = analyze_log(path, top=args.top)
    except (OSError, UnicodeError, EOFError) as error:
        print(f"cannot read log: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

