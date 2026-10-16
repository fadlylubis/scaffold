.PHONY: sync lab lint hooks
sync:
	uv sync
lab:
	uv run jupyter lab
lint:
	uv run ruff check .
hooks:
	git init -q
	uvx pre-commit install
