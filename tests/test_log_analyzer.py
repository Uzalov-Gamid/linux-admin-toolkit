from pathlib import Path

from toolkit.log_analyzer import analyze_log


def test_analyze_log_counts_requests() -> None:
    result = analyze_log(Path("examples/access.log"))
    assert result["total_requests"] == 6
    assert result["status_codes"]["200"] == 3
    assert result["status_codes"]["201"] == 1
    assert result["status_codes"]["404"] == 1
    assert result["status_codes"]["500"] == 1


def test_analyze_log_tracks_top_paths() -> None:
    result = analyze_log(Path("examples/access.log"))
    assert result["top_paths"]["/api/tasks"] == 3



def test_analyzer_streams_file_without_read_text(tmp_path, monkeypatch):
    log = tmp_path / "access.log"
    entry = '127.0.0.1 - - [01/Jan/2026:00:00:00 +0000] "GET /hello HTTP/1.1" 200 4'
    log.write_text(entry + "\nmalformed line\n" + entry, encoding="utf-8")

    def forbidden_read(*args, **kwargs):
        raise AssertionError("log must be read incrementally")

    monkeypatch.setattr(Path, "read_text", forbidden_read)
    result = analyze_log(log)
    assert result["total_requests"] == 2
    assert result["top_paths"] == {"/hello": 2}


def test_custom_top_path_limit():
    result = analyze_log(Path("examples/access.log"), top=1)
    assert result["top_paths"] == {"/api/tasks": 3}


def test_cli_rejects_invalid_top():
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "-m", "toolkit.log_analyzer", "examples/access.log", "--top", "0"], capture_output=True, text=True)
    assert result.returncode == 2
    assert "positive integer" in result.stderr


def test_cli_reports_invalid_encoding_without_traceback(tmp_path):
    import subprocess
    import sys
    log = tmp_path / "broken.log"
    log.write_bytes(b"\xff\xfe")
    result = subprocess.run([sys.executable, "-m", "toolkit.log_analyzer", str(log)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "cannot read log:" in result.stderr
    assert "Traceback" not in result.stderr


def test_truncated_compressed_log_reports_a_read_error(tmp_path):
    import gzip
    import subprocess
    import sys
    path = tmp_path / "truncated.gz"
    path.write_bytes(gzip.compress(Path("examples/access.log").read_bytes())[:-5])
    result = subprocess.run([sys.executable, "-m", "toolkit.log_analyzer", str(path)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "cannot read log" in result.stderr
    assert "Traceback" not in result.stderr


def test_gzip_and_plain_logs_produce_identical_summaries(tmp_path):
    import gzip
    source = Path("examples/access.log")
    compressed = tmp_path / "access.log.gz"
    with gzip.open(compressed, "wb") as output:
        output.write(source.read_bytes())
    assert analyze_log(compressed) == analyze_log(source)


def test_cli_reads_piped_logs_from_stdin():
    import json
    import subprocess
    import sys
    source = Path("examples/access.log")
    output = subprocess.check_output([sys.executable, "-m", "toolkit.log_analyzer", "-"], input=source.read_text(), text=True)
    assert json.loads(output) == analyze_log(source)


def test_ignored_lines_are_reported_instead_of_silently_lost(tmp_path):
    log = tmp_path / "mixed.log"
    log.write_text(Path("examples/access.log").read_text() + "bad line\n\n")
    result = analyze_log(log)
    assert result["total_requests"] == 6
    assert result["ignored_lines"] == analyze_log(Path("examples/access.log"))["ignored_lines"] + 2
