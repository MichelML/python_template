import pytest

from app.__main__ import EXIT_OK, main


def test_main_exits_successfully(capsys: pytest.CaptureFixture[str]) -> None:
    assert main() == EXIT_OK
    assert capsys.readouterr().out.strip() == "app is ready"
