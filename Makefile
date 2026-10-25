.PHONY: help install run test format lint typecheck check clean

help:  ## Show available commands
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  %-10s %s\n", $$1, $$2}'

install:  ## Create .venv and install the app plus dev tools
	uv sync

run:  ## Run the app
	uv run python -m app

test:  ## Run the tests
	uv run pytest -q

format:  ## Format code with ruff
	uv run ruff format .

lint:  ## Lint with ruff and apply safe fixes
	uv run ruff check --fix .

typecheck:  ## Typecheck with mypy (strict)
	uv run mypy

check: format lint typecheck  ## Format, lint, and typecheck

clean:  ## Remove tool caches
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	find . -name __pycache__ -type d -not -path "./.venv/*" -exec rm -rf {} +
