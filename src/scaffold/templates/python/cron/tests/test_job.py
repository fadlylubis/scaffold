from __PACKAGE__.job import main


def test_dry_run_succeeds():
    assert main(["--dry-run"]) == 0
