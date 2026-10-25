# template <!-- omit in toc -->

A small, clean Python 3.12+ project template. See `CLAUDE.md` for design and style guidelines.

## Table of content <!-- omit in toc -->

- [Setup](#setup)
- [Commands](#commands)
- [Contributing](#contributing)


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
| `make check`     | Format, lint, typecheck, and test         |
| `make clean`     | Remove tool caches                        |
| `make help`      | List all commands                         |

`make check` must pass before every commit.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, the change workflow, and code standards.
