# Self-Documented Makefile
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help page
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run: ## Runs the app
	python src/main.py

.PHONY: install
install: ## Install only the dependencies needed to build and run the app
	python -m pip install -r requirements.txt
	python -m pip freeze > requirements-lock.txt

.PHONY: install-dev
install-dev: ## Install build and dev dependencies
	python -m pip install -r requirements.txt -r requirements-dev.txt
	python -m pip freeze > requirements-lock.txt

.PHONY: upgrade
upgrade: ## Upgrade all dependencies
	python -m pip install --upgrade -r requirements.txt -r requirements-dev.txt
	python -m pip freeze > requirements-lock.txt
	python tool/scripts/syncdeps.py requirements.txt requirements-lock.txt
	python tool/scripts/syncdeps.py requirements-dev.txt requirements-lock.txt

.PHONY: upgrade-pip
upgrade-pip: ## Upgrade pip
	python -m pip install --upgrade pip

.PHONY: format
format: ## Format code
	python -m isort src tool
	python -m black src tool

.PHONY: format-check
format-check: ## Check code format
	python -m black src tool --check

.PHONY: import-check
import-check: ## Check import order
	python -m isort src tool --check

.PHONY: lint
lint: ## Check for lints
	@RC=0; \
	python -m mypy src tool || RC=1; \
	python -m flake8 src tool || RC=1; \
	python -m pylint src tool || RC=1; \
	exit $$RC

.PHONY: packages
packages: ## Ensure that all packages have an __init__ file
	python tool/scripts/verify_packages.py

.PHONY: packages-check
packages-check: ## Check for packages with a missing __init__ file
	python tool/scripts/verify_packages.py --check

.PHONY: test
test: ## Run tests
	cd src && python -m unittest

.PHONY: test-xml
test-xml: ## Run unit tests and generate xml reports
	cd src && python -m xmlrunner -o ../reports

.PHONY: maps
maps: ## Download and generate maps
	python tool/scripts/make_maps.py

.PHONY: shaders
shaders: ## Compile shaders
	python tool/scripts/compile_shaders.py

.PHONY: models
models: ## Convert all models to .bam
	python tool/scripts/convert_bam.py
