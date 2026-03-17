# Code quality and testing - run from repo root.
# Install dev deps: pip install -r library-api/requirements-dev.txt

.PHONY: test lint format quality typecheck check all

test:
	pytest

lint:
	ruff check library-api/

format:
	ruff format library-api/

quality:
	radon cc library-api/ -a -s
	radon mi library-api/ -s

typecheck:
	mypy library-api/

check: lint format typecheck quality test

all: check
