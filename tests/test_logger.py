import subprocess
import sys

import pytest

from app.logger import logger


def test_writes_messages_to_stderr() -> None:
    code = "from app.logger import logger; logger.info('hello')"

    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )

    assert result.stderr == "INFO <string>: hello\n"
    assert result.stdout == ""


def test_hides_debug_messages_by_default(caplog: pytest.LogCaptureFixture) -> None:
    logger.debug("details")

    assert caplog.records == []
