setup:
	pre-commit install

lint:
	poetry run ruff check .

format:
	poetry run black .

test:
	poetry run pytest tq42/tests/

functional-test:
	poetry run pytest -s tq42/functional_tests/

functional-test-poll:
	poetry run pytest -s --poll tq42/functional_tests/