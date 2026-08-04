from check_quarantine import quarantine_violations


def test_genetics_artifacts_respect_domain_quarantine() -> None:
    assert quarantine_violations() == []
