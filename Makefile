

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fmt: ## Run black to format code
	pipenv run black .

test:  ## Run pytest for files under ./tests
	PYTHONPATH=. pipenv run python -m pytest --nf --ff tests

test-all:  ## Run pytest for all files
	@export $(sed 's/#.*//g' .env | xargs) >/dev/null 2>&1
	PYTHONPATH=. pipenv run python -m pytest --nf --ff .

setup:  ## Run pipenv install to setup the environment
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --skip-lock
	PIPENV_VENV_IN_PROJECT=1 pipenv run pre-commit install
	PIPENV_VENV_IN_PROJECT=1 pipenv run pre-commit install-hooks
