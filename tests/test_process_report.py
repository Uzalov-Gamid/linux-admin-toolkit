import os
import subprocess
from pathlib import Path


def test_large_process_listing_does_not_fail_from_sigpipe(tmp_path):
    fake_ps = tmp_path / "ps"
    fake_ps.write_text("#!/bin/sh\necho 'USER PID CPU MEM COMMAND'\nawk 'BEGIN {for(i=1;i<=8000;i++) print \"user\", i, i, 8001-i, \"worker\"}'\n")
    fake_ps.chmod(0o755)
    env = dict(os.environ, PATH=str(tmp_path) + os.pathsep + os.environ["PATH"])
    script = Path(__file__).resolve().parents[1] / "scripts/process-report.sh"
    result = subprocess.run(["bash", str(script), "2"], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "user 8000 8000 1 worker" in result.stdout
    assert "user 1 1 8000 worker" in result.stdout
    assert result.stdout.count("USER PID CPU MEM COMMAND") == 2
