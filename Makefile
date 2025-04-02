test:
	poetry run pytest
lint:
	poetry run flake8 tests/ src/logger_kit
install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
black:
	poetry run black .
autoflake:
	poetry run autoflake --remove-all-unused-imports --remove-unused-variables --recursive .
isort:
	poetry run isort . --profile black
full-check:
	make lint && make autoflake && make isort && make black && make test