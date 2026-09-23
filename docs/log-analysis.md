# Access log analysis

Run from the repository root. Plain UTF-8 logs, gzip-compressed logs and piped
input are supported:

```bash
python -m toolkit.log_analyzer examples/access.log --top 10
python -m toolkit.log_analyzer /var/log/nginx/access.log.gz
cat examples/access.log | python -m toolkit.log_analyzer -
```

`--top` is a positive integer and controls both busiest paths and busiest clients.
JSON output contains `total_requests`, `ignored_lines`, `status_codes`, `methods`,
`top_paths` and `top_clients`. Ignored lines include malformed and blank lines.
The default is five entries for each top list. Input is streamed, but counters
retain distinct paths and client addresses in memory.

Exit codes: 0 for a completed summary, 1 for missing/unreadable input or invalid
UTF-8, and 2 for invalid command arguments. A malformed individual line does not
abort the summary. Counted request sizes are not used to estimate bandwidth.

The shell wrapper is intended for the one-file default case. Use the Python
module directly for additional options. Reports contain client addresses from
the input; review the output before sharing it.
