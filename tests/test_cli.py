import logging
from collections.abc import Iterator

import pytest

from app.cli import EXIT_OK, main
from app.logger import logger

ARGPARSE_USAGE_ERROR = 2


@pytest.fixture(autouse=True)
def restore_log_level() -> Iterator[None]:
    yield
    logger.setLevel(logging.INFO)


def test_runs_and_exits_ok(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == EXIT_OK
    assert capsys.readouterr().out == "app is ready\n"


def test_verbose_flag_enables_debug_logging() -> None:
    main(["--verbose"])

    assert logger.isEnabledFor(logging.DEBUG)


def test_rejects_unknown_arguments() -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--unknown"])

    assert exit_info.value.code == ARGPARSE_USAGE_ERROR
