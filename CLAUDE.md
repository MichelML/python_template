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
- Descriptive names first; add a brief comment on any complex or non-obvious section (an algorithm
  choice, a tricky edge case, a business rule). Short docstrings on public classes and non-obvious
  methods only.
- No global state, no magic strings or numbers (use constants or enums), no nested classes.
  Exceptions: the shared `logger` in `src/app/logger.py` and the `api = FastAPI()` object in
  `src/app/api.py`.
- Keep functions short and focused, with early returns over deep nesting.

## Tooling
- Use uv for environment creation and dependency management. Never use `pip` or create venvs manually.
  - Setup: `uv sync` (creates `.venv` with the Python pinned in `.python-version` and installs the
    app plus the `dev` dependency group).
  - Run anything inside the environment with `uv run …` (e.g. `uv run python -m app`).
  - Add dependencies with `uv add <pkg>` (runtime) or `uv add --dev <pkg>` (dev); commit `uv.lock`.
  - An optional `api` group (FastAPI, uvicorn, httpx2) is pre-locked but not installed by default.
    When the problem needs an HTTP API, add `[tool.uv] default-groups = ["dev", "api"]` to
    `pyproject.toml` and run `uv sync`, so mypy, pytest, and `make` all see it.
- Format and lint with ruff, typecheck with mypy (strict). Config lives in `pyproject.toml`.
- The `Makefile` wraps the common commands (`make help` lists them): `make install`, `make run`,
  `make test`, `make format`, `make lint`, `make typecheck`, and `make check` for all checks.
- Before every commit, all of these must pass (`make check` runs them in order):
  ```
  uv run ruff format .
  uv run ruff check --fix .
  uv run mypy
  uv run pytest -q
  ```
- Fix lint and type errors properly; don't silence them with `# noqa` or `# type: ignore` unless there is a stated reason.

## Errors and validation
- Validate input at the boundary, where external data enters the system.
- Raise specific custom exceptions (subclasses of `AppError` in `src/app/errors.py`) with clear messages.
- Never use bare `except`, never swallow errors silently, never return `None` to signal failure when an exception is clearer.

## Project layout
- If a starter repo is provided, its language, layout, and conventions take precedence over this
  section and "Tooling".
- Package code in `src/app/` (src layout), tests in `tests/` mirroring module names
  (`src/app/orders.py` → `tests/test_orders.py`). Tests import the installed package
  (`from app.orders import ...`), never `src.`.
- Shared test fixtures go in `tests/conftest.py`.

## Architecture: pure core, thin adapters
One domain core that never knows how it was called, wrapped by thin adapters for each way in
(CLI, stdin, files, HTTP). Only the adapters change with the shape of the problem.

```
src/app/
  models.py       # value objects (frozen dataclasses) and enums: the domain's nouns
  service.py      # use cases: one public method per operation the problem asks for
  repository.py   # storage Protocol + in-memory implementation (only if state is stored)
  errors.py       # AppError hierarchy
  logger.py       # shared logger: `from app.logger import logger`
  cli.py          # CLI adapter: argparse, `main(argv) -> exit code`
  api.py          # HTTP adapter (only if asked)
  __main__.py     # `python -m app` → `cli.main()`
```

- Create `models.py`, `service.py`, and `repository.py` once the domain is known; no empty
  placeholder modules. Split into one module per core class if they grow.
- Adapters (`cli.py`, `api.py`, `__main__.py`) are the only modules that do I/O. Each one: parses
  input into models, calls the service, formats the output, and maps `AppError` to an exit code or
  HTTP status.
- The service gets its collaborators (repository, clock) through its constructor, typed against a
  `Protocol`. No module-level state, no singletons.

### Recipes by problem shape
- **Pure logic** ("implement a cart with discounts"): models + service + tests. A CLI is optional.
- **CLI**: add subcommands in `cli.py` with `add_subparsers(dest="command", required=True)`, one
  small handler per command. `run(args)` dispatches; `main` handles `AppError` → `EXIT_ERROR`.
- **stdin / line-based input**: the adapter reads `sys.stdin` and passes text to a pure
  `parse_*(text) -> model` function; the core never touches streams.
- **File input (CSV/JSON)**: stdlib `csv` / `json`. `parse_*` functions take text (not paths) and
  return models, so tests use inline strings. Bad rows raise a specific `AppError` naming the line or
  field. Put them in `parsing.py` if more than one adapter uses them.
- **REST API** (`src/app/api.py`, run with `uv run uvicorn app.api:api --reload`):
  - `api = FastAPI()`; route functions stay thin and call the service.
  - Pydantic request/response models live only in `api.py` and are converted to/from domain models.
    The domain stays plain dataclasses.
  - Provide the service with a dependency (`Depends(get_service)`) so tests can override it.
  - One `@api.exception_handler` per error family maps `AppError` subclasses to status codes:
    not found → 404, invalid input → 400 (FastAPI's own validation is 422), conflict/duplicate → 409.
  - Test with `fastapi.testclient.TestClient(api)`: a few tests per route; logic tests stay on the
    service.
- **Persistence** ("now make it survive restarts"): add a class implementing the repository
  `Protocol` (stdlib `sqlite3` or a JSON file). The service doesn't change. Run the repository tests
  against both implementations with a parametrized fixture.
- **Time-dependent rules** (expiry, rate limits, scheduling): inject a clock
  (`Callable[[], datetime]`) instead of calling `datetime.now()` in the core; tests pass a fixed one.
- **Money**: `Decimal` or integer cents, never `float`. Round once, at a stated point.
- **Ids and ordering**: generate ids deterministically (a counter in the repository) and keep output
  ordering explicit (`sorted` with a key), so results are reproducible and testable.
- **Concurrency** (rarely asked): keep the core synchronous; if needed, guard the repository with a
  `threading.Lock` and say so, rather than going async.

## Testing
- pytest with plain `assert`. One behavior per test, with descriptive names (`test_rejects_negative_quantity`).
- Write or update tests alongside every change, not at the end.
- Use `@pytest.mark.parametrize` for input variations and `pytest.raises` for error cases.
- Aim to cover happy path, boundaries, invalid input, and empty or degenerate cases. Start with the
  happy path and one key edge case, then add the rest as time allows.
- Test behavior through public interfaces, not implementation details.
- Most tests target the service (fast, pure, no I/O). Adapters get a few thin tests each: CLI via
  `main([...])` + `capsys`, API via `TestClient`. Only `tests/test_main.py` runs a subprocess.
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
- Never commit or push on your own initiative. The user will always say when to commit and when to
  push; until then, leave changes uncommitted.
- When asked to commit, use a short, imperative message ("Add order validation").
- Ruff, mypy, and tests must all be green before any commit or push.
