.DEFAULT_GOAL := help

.PHONY: install
install: ## Install dependencies
	@python -m pip install -r requirements.txt

.PHONY: format
format: ## Format code
	@python -m black .

.PHONY: test
test: ## Run tests
	@cd src && python -m unittest

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
