import pytest

from app.errors import AppError


def test_app_error_is_an_exception() -> None:
    assert issubclass(AppError, Exception)


def test_app_error_preserves_message() -> None:
    with pytest.raises(AppError, match="something went wrong"):
        raise AppError("something went wrong")
