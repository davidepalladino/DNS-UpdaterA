.PHONY: install v format lint

setup:
	uv venv --allow-existing
setup-clean:
	uv venv -c
sync: pyproject.toml
	uv sync
lint:
	uvx ruff check .
format:
	uvx ruff format .
type-check:
	uvx mypy main.py
build:
	uv build