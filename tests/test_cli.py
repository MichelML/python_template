import pytest

from app.cli import EXIT_OK, main

ARGPARSE_USAGE_ERROR = 2


def test_runs_and_exits_ok(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == EXIT_OK
    assert capsys.readouterr().out == "app is ready\n"


def test_rejects_unknown_arguments() -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--unknown"])

    assert exit_info.value.code == ARGPARSE_USAGE_ERROR
