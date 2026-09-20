import os
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/disk-report.sh"


def test_disk_report_uses_target_filesystem_and_includes_hidden_entries(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    (target / ".hidden").write_text("data")
    tools = tmp_path / "bin"
    tools.mkdir()
    fake = tools / "df"
    fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$DF_ARGS_OUT"\n')
    fake.chmod(0o755)
    args_file = tmp_path / "df-args"
    env = dict(os.environ, PATH=str(tools)+os.pathsep+os.environ["PATH"], DF_ARGS_OUT=str(args_file))
    result = subprocess.run(["bash", str(SCRIPT), str(target)], env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert str(target) in args_file.read_text()
    assert ".hidden" in result.stdout
