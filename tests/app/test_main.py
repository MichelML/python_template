import subprocess
import sys

import pytest

from app.__main__ import EXIT_OK, main


def test_main_prints_ready_and_exits_ok(capsys: pytest.CaptureFixture[str]) -> None:
    assert main() == EXIT_OK
    assert capsys.readouterr().out == "app is ready\n"


def test_python_dash_m_app_runs_main() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "app"], capture_output=True, text=True, check=True
    )

    assert result.stdout == "app is ready\n"
