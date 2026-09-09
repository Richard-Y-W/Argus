from pathlib import Path

from engineering.argus_lab.integrity import verify_experiment_lifecycle


def _completed(root: Path, experiment: str) -> None:
    path = root / "experiments" / experiment
    path.mkdir(parents=True)
    (path / "results.md").write_text("complete", encoding="utf-8")


def _verdict(root: Path, directory: str, experiment: str) -> None:
    path = root / directory
    path.mkdir(parents=True, exist_ok=True)
    (path / f"{experiment}.md").write_text("verdict", encoding="utf-8")


def test_completed_experiment_requires_one_verdict(tmp_path: Path) -> None:
    _completed(tmp_path, "EXP-001-example")
    assert verify_experiment_lifecycle(tmp_path) == [
        "unclassified completed experiment: EXP-001"
    ]


def test_completed_experiment_accepts_one_verdict(tmp_path: Path) -> None:
    _completed(tmp_path, "EXP-001-example")
    _verdict(tmp_path, "successful_experiments", "EXP-001-example")
    assert verify_experiment_lifecycle(tmp_path) == []


def test_completed_experiment_rejects_two_verdicts(tmp_path: Path) -> None:
    _completed(tmp_path, "EXP-001-example")
    _verdict(tmp_path, "successful_experiments", "EXP-001-example")
    _verdict(tmp_path, "failed_experiments", "EXP-001-example")
    assert verify_experiment_lifecycle(tmp_path) == [
        "multiply classified experiment: EXP-001"
    ]
