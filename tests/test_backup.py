import subprocess
import tarfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/backup.sh"


def test_repeated_backup_preserves_both_archives(tmp_path):
    source = tmp_path / "source with spaces"
    source.mkdir()
    (source / "note.txt").write_text("first")
    dest = tmp_path / "backups"
    first = subprocess.check_output(["bash", str(SCRIPT), str(source), str(dest)], text=True).strip()
    (source / "note.txt").write_text("second")
    second = subprocess.check_output(["bash", str(SCRIPT), str(source), str(dest)], text=True).strip()
    assert first != second
    for archive, expected in [(first, b"first"), (second, b"second")]:
        with tarfile.open(archive) as saved:
            assert saved.extractfile(source.name + "/note.txt").read() == expected
    assert len(list(dest.iterdir())) == 2
