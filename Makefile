PYTHON = python3

run:
	$(PYTHON) main.py

install:
	pip install -r requirements.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*mypy_cache" -exec rm -rf {} +

debug:
	$(PYTHON) -m pdb main.py

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict


.PHONY: install test clean lint-strict lint debug run