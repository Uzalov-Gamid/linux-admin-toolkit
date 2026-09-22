# Backup and restore

Create an archive outside the directory being backed up:

```bash
scripts/backup.sh examples ./backups
```

Each archive has a timestamp and a unique suffix. Repeated runs preserve earlier
archives. Failed archive creation removes the temporary output. `.git` and
`__pycache__` are excluded by default. Final files inherit the restrictive
permissions of the temporary file.

For additional exclusions, put one tar pattern per line in a file:

```text
*/private.env
*/node_modules
```

```bash
BACKUP_EXCLUDES_FILE=./excludes.txt scripts/backup.sh examples ./backups
```

Inspect an archive before extracting it. Extract trusted archives into a separate
empty directory, then compare their contents with the source:

```bash
tar -tzf ./backups/ARCHIVE.tar.gz
mkdir ./restore-check
tar -xzf ./backups/ARCHIVE.tar.gz -C ./restore-check
diff -r examples ./restore-check/examples
```

The script rejects nested destinations, including paths resolved through symlinks.
This is a local snapshot tool: it does not schedule backups or enforce retention.
