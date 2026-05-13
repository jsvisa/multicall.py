

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fmt: ## Run black to format code
	black .

test:  ## Run pytest for files under ./tests
	PYTHONPATH=. python -m pytest --nf --ff tests

test-all:  ## Run pytest for all files
	@export $(sed 's/#.*//g' .env | xargs) >/dev/null 2>&1
	PYTHONPATH=. python -m pytest --nf --ff .

setup:  ## Install dependencies and set up pre-commit hooks
	pip install -e ".[dev]"
	pre-commit install
	pre-commit install-hooks

publish: test test-all ## Package and upload into pypi
	python setup.py sdist
	twine upload dist/*
	rm -rf dist/*
