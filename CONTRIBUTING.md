# Contributing

Thanks for helping out. This guide covers the workflow; the detailed design and style rules live in
[`CLAUDE.md`](CLAUDE.md) and apply to humans and AI assistants alike.

## Setup

You need [uv](https://docs.astral.sh/uv/). Everything else (Python 3.12, dev tools) is installed
into `.venv` by:

```sh
make install
```

Run anything inside the environment with `uv run …` or a `make` target. Don't use `pip` or create
virtual environments by hand.

## Making a change

1. Create a branch from `main`: `git switch -c short-description`.
2. Work in small increments: one class or function at a time, with its tests in the same change.
3. Run `make check` (format, lint, typecheck, test) after each increment. It must pass before you
   commit.
4. Commit with a short, imperative message, e.g. `Add order validation`.
5. Push and open a pull request against `main`. Describe what changed and any trade-offs.

## Code standards (summary)

- Code lives in `src/app/`; tests live in `tests/`, mirroring module names
  (`src/app/orders.py` → `tests/test_orders.py`).
- Keep the domain pure (no I/O); only the adapters (`cli.py`, `api.py`, `__main__.py`) read input or
  write output.
- Full type hints, strict mypy, no `Any`. Fix lint and type errors instead of silencing them.
- Raise specific `AppError` subclasses (see `src/app/errors.py`), never bare `except`.
- Tests use plain `assert`, one behavior per test, with descriptive names. Cover the happy path,
  boundaries, invalid input, and empty cases.

See [`CLAUDE.md`](CLAUDE.md) for the full rules and the architecture recipes (CLI, files, HTTP API,
persistence).

## Dependencies

Standard library first. If a dependency is clearly justified, add it with `uv add <pkg>` (runtime)
or `uv add --dev <pkg>` (dev tooling) and commit the updated `uv.lock`. To work on an HTTP API,
enable the pre-locked `api` group as described in `CLAUDE.md`.
