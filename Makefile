all: install run

run:
	@uv run python3 pac_man.py $(ARGS)

install:
	@which uv > /dev/null 2>&1 || wget -qO- https://astral.sh/uv/install.sh | sh
	@uv add mazegenerator-2.1.0-py3-none-any.whl
	@uv sync


debug:
	uv run python -m pdb -m src

clean:
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -name .DS_Store -delete

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy . --strict
