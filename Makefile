.PHONY: install lint format test typecheck build

install_dev:
	uv venv
	uv sync

lint:
	. .venv/bin/activate && ruff check .  &&

format:
	. .venv/bin/activate && ruff format .

test:
	. .venv/bin/activate && pytest --cov=plmdp --cov-report=html

typecheck:
	. .venv/bin/activate && mypy .

build:
	uv build

publish:
	uv publish --token "$(PYPI_TOKEN)"