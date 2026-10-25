# app

A small, clean Python 3.12+ project. See `CLAUDE.md` for design and style guidelines.

## Setup

Environments are managed with [uv](https://docs.astral.sh/uv/):

```sh
uv sync            # creates .venv with Python 3.12 and installs the app + dev tools
```

## Run

```sh
uv run python -m app
```

## Checks

All of these must pass before every commit:

```sh
uv run ruff format .
uv run ruff check --fix .
uv run mypy
uv run pytest -q
```
