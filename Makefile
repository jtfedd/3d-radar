# Self-Documented Makefile
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

.PHONY: help
help: ## Displays this help page
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies
	python -m pip install -r requirements.txt

.PHONY: upgrade
upgrade: ## Upgrades all dependencies
	sed -i 's/==/>=/g' requirements.txt
	python -m pip install --upgrade -r requirements.txt
	python -m pip freeze > requirements.txt

.PHONY: format
format: ## Format code
	python -m black .

.PHONY: format-check
format-check: ## Check code format
	python -m black . --check

.PHONY: packages
packages: ## Ensure that all packages have an __init__ file
	python tool/scripts/verify_packages.py

.PHONY: packages-check
packages-check: ## Check for packages with a missing __init__ file
	python tool/scripts/verify_packages.py --check

.PHONY: test
test: ## Run tests
	cd src && python -m unittest

.PHONY: test-coverage
test-coverage: ## Run tests and report coverage
	cd src && python -m coverage run --source=lib -m unittest && python -m coverage report && rm .coverage

.PHONY: test-coverage-html
test-coverage-html: ## Run tests and generate html coverage report
	cd src && python -m coverage run --source=lib -m unittest && python -m coverage html

.PHONY: clean
clean: ## Remove all cached data files, config files, etc.
	rm -rfv src/lib/data_connector/cached_data/*
