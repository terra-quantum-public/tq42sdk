rm -rf dist/
rm poetry.lock
poetry build
poetry install
poetry shell

