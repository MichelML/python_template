import subprocess
import sys


def test_python_dash_m_app_runs_the_cli() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "app"], capture_output=True, text=True, check=True
    )

    assert result.stdout == "app is ready\n"
