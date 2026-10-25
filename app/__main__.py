"""Entry point for `python -m app`. The only module that performs I/O."""

import sys

from app.errors import AppError

EXIT_OK = 0
EXIT_ERROR = 1


def main() -> int:
    try:
        print("app is ready")
    except AppError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
