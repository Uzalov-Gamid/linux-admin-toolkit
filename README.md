# Linux Admin Toolkit

Small toolkit for Linux administration practice. It includes Bash and Python utilities for backups, disk reports, process reports, and web access log analysis.

## Tools

| Tool | Purpose |
| --- | --- |
| `scripts/backup.sh` | Create timestamped `.tar.gz` backups |
| `scripts/disk-report.sh` | Show filesystem and directory usage |
| `scripts/process-report.sh` | Show top processes by CPU and memory |
| `scripts/log-summary.sh` | Analyze HTTP access logs with Python |

## Quick start

```bash
chmod +x scripts/*.sh
scripts/disk-report.sh .
scripts/process-report.sh
scripts/process-report.sh 5
scripts/log-summary.sh examples/access.log
```

## Backup example

```bash
scripts/backup.sh examples backups
ls backups
```

## Python log analyzer

```bash
python -m toolkit.log_analyzer examples/access.log
```

Example output:

```json
{
  "total_requests": 6,
  "status_codes": {
    "200": 4,
    "404": 1,
    "500": 1
  }
}
```

## Tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
bash -n scripts/*.sh tests/*.sh
bash tests/test_scripts.sh
```

## What this MVP demonstrates

- Linux command-line automation
- Bash scripting with safe defaults
- Python log parsing
- Basic CI checks for scripts and tests
