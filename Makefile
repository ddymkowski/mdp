.PHONY: install lint format test typecheck clean

install_dev:
	uv venv
	uv sync

lint:
	. .venv/bin/activate && ruff check .

format:
	. .venv/bin/activate && ruff format .

test:
	. .venv/bin/activate && pytest --cov=plmdp --cov-report=html

typecheck:
	. .venv/bin/activate && mypy .

build:
	uv build