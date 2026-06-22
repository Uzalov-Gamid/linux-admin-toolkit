import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[[^\]]+\] "(?P<method>[A-Z]+) (?P<path>\S+) [^"]+" (?P<status>\d{3}) (?P<size>\S+)'
)


def analyze_log(path: Path) -> dict[str, Any]:
    status_codes: Counter[str] = Counter()
    methods: Counter[str] = Counter()
    paths: Counter[str] = Counter()
    total = 0

    for line in path.read_text(encoding="utf-8").splitlines():
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
        "top_paths": dict(paths.most_common(5)),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python -m toolkit.log_analyzer <access.log>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1

    print(json.dumps(analyze_log(path), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

