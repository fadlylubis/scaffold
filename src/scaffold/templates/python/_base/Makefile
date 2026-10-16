.PHONY: sync test lint fmt hooks
sync:
	uv sync
test:
	uv run pytest
lint:
	uv run ruff check .
fmt:
	uv run ruff format .
hooks:
	git init -q
	uvx pre-commit install
