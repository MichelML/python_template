"""Entry point for `python -m app`. Delegate to the client's `main` once one exists."""

import sys

EXIT_OK = 0


def main() -> int:
    print("app is ready")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
