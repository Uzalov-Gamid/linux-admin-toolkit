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

