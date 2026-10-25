# app

A small, clean Python 3.12+ project. See `CLAUDE.md` for design and style guidelines.

## Setup

Environments are managed with [uv](https://docs.astral.sh/uv/):

```sh
make install       # uv sync: creates .venv with Python 3.12 and installs the app + dev tools
```

## Commands

| Command          | What it does                              |
|------------------|-------------------------------------------|
| `make run`       | Run the app (`uv run python -m app`)      |
| `make test`      | Run the tests (`uv run pytest -q`)        |
| `make format`    | Format with ruff                          |
| `make lint`      | Lint with ruff and apply safe fixes       |
| `make typecheck` | Typecheck with mypy (strict)              |
| `make check`     | Format, lint, and typecheck               |
| `make clean`     | Remove tool caches                        |
| `make help`      | List all commands                         |

`make check test` must pass before every commit.
