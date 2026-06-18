PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

help:
	@echo "Commands: install, run, debug, clean, lint, lint-strict"
run:
	$(PYTHON) $(MAIN) $(CONFIG)

install:
	pip install mazegen-1.0.0-py3-none-any.whl

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*mypy_cache" -exec rm -rf {} +

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict


.PHONY: install build test clean lint-strict lint debug run
