.PHONY: setup setup-clean sync lint format type-check build

# Create or reuse the virtual environment
setup:
	uv venv --allow-existing

# Remove the virtual environment
setup-clean:
	uv venv -c

# Sync dependencies from pyproject.toml
sync: pyproject.toml
	uv sync

# Run Ruff for linting
lint:
	uvx ruff check .

# Run Ruff for auto-formatting
format:
	uvx ruff format .

# Run type checking with mypy
type-check:
	uvx mypy main.py

# Build the project (wheel/sdist)
build:
	uv build