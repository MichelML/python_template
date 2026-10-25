# Project guidelines

A small, clean Python project. The goal is code that is correct, readable, well-tested, and easy to
extend: something a careful reviewer would approve without changes.

## Design
- Understand the problem first. Surface ambiguities and state assumptions before writing code.
- Model the domain explicitly: small classes with one clear responsibility each.
- Use `@dataclass` for data (`frozen=True` for value objects) and `Enum` for fixed sets of values.
- Keep domain logic pure: no `print`, `input`, or file I/O inside it. Parsing and I/O live at the edges.
- Prefer composition over inheritance, and small methods over long ones.
- Build for the current requirement, but keep the design open to new ones. When requirements change,
  refactor the design first, then add the feature.
- Pick the right data structure up front (e.g. dicts and sets for O(1) lookups, `deque` for queues,
  `heapq` for priority queues) and avoid repeated or wasted work. State the time and space complexity
  of core operations briefly in chat. No micro-optimizations before the feature works: efficient and
  clear, never clever and obscure.
- Keep data in memory. If persistence or an API is requested, put it behind a small interface (e.g. a
  repository class) and keep it minimal.

## Python style
- Python 3.12+, standard library only unless a dependency is clearly justified.
- Full type hints on every function and method signature. Avoid `Any`.
- Descriptive names over comments. Short docstrings on public classes and non-obvious methods only.
- No global state, no magic strings or numbers (use constants or enums), no nested classes.
- Keep functions short and focused, with early returns over deep nesting.

## Tooling
- Use uv for environment creation and dependency management. Never use `pip` or create venvs manually.
  - Setup: `uv sync` (creates `.venv` with the Python pinned in `.python-version` and installs the
    app plus the `dev` dependency group).
  - Run anything inside the environment with `uv run …` (e.g. `uv run python -m app`).
  - Add dependencies with `uv add <pkg>` (runtime) or `uv add --dev <pkg>` (dev); commit `uv.lock`.
- Format and lint with ruff, typecheck with mypy (strict). Config lives in `pyproject.toml`.
- The `Makefile` wraps the common commands (`make help` lists them): `make install`, `make run`,
  `make test`, `make format`, `make lint`, `make typecheck`, and `make check` (format, lint, typecheck).
- Before every commit, all of these must pass (`make check test` runs them in order):
  ```
  uv run ruff format .
  uv run ruff check --fix .
  uv run mypy
  uv run pytest -q
  ```
- Fix lint and type errors properly; don't silence them with `# noqa` or `# type: ignore` unless there is a stated reason.

## Errors and validation
- Validate input at the boundary, where external data enters the system.
- Raise specific custom exceptions (subclasses of `AppError` in `app/errors.py`) with clear messages.
- Never use bare `except`, never swallow errors silently, never return `None` to signal failure when an exception is clearer.

## Project layout
- If a starter repo is provided, its language, layout, and conventions take precedence over this
  section and "Tooling".
- Package code in `app/`, tests in `tests/` mirroring module names (`app/orders.py` → `tests/test_orders.py`).
- `app/__main__.py` is the entry point (`python -m app`) and the only place that does I/O.
- One module per main domain concept, e.g. `models.py` for value objects and enums, plus one module per core class.
- Shared test fixtures go in `tests/conftest.py`.

## Testing
- pytest with plain `assert`. One behavior per test, with descriptive names (`test_rejects_negative_quantity`).
- Write or update tests alongside every change, not at the end.
- Use `@pytest.mark.parametrize` for input variations and `pytest.raises` for error cases.
- Aim to cover happy path, boundaries, invalid input, and empty or degenerate cases. Start with the
  happy path and one key edge case, then add the rest as time allows.
- Test behavior through public interfaces, not implementation details.
- After every change, run the full check (`uv run` ruff, mypy, pytest). Everything must pass before moving on.

## Workflow
- Priority order:
  1. Restate the problem and assumptions.
  2. Build the thinnest end-to-end slice that works and is tested.
  3. Extend one requirement at a time.
  4. Polish only if time allows.
- When a requirement changes: list what changes in the model, refactor with tests green, then add
  the feature.
- Work in small, reviewable increments: one class or function at a time.
- Outline the approach briefly before larger changes.
- Don't rewrite or reformat code unrelated to the current change.
- Ask before adding dependencies or making structural changes.
- After each change, summarize what changed and any trade-offs in one or two sentences.
- Keep explanations short and scannable; the interviewer is reading along. Make small diffs and
  explain the "why", not just the "what".

## Git
- Commit after each working step with a short, imperative message ("Add order validation").
- Keep the working tree clean, with ruff, mypy, and tests all green before pushing.
