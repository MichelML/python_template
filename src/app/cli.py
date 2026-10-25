"""Command-line adapter: parses arguments, calls the service, and formats output."""

import argparse
import logging
import sys

from app.errors import AppError
from app.logger import logger

EXIT_OK = 0
EXIT_ERROR = 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="app")
    parser.add_argument("-v", "--verbose", action="store_true", help="show debug logs")
    return parser


def run(args: argparse.Namespace) -> None:
    """Dispatch the parsed command to the service. Replace with the real commands."""
    print("app is ready")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    try:
        run(args)
    except AppError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK
