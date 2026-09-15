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
