all: help

.PHONY: help
help: Makefile
	@echo
	@echo " Choose a make command to run"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo

## init: initialize a new python project
.PHONY: init
init:
	uv python install
	uv venv
	uv sync

## install: add a new package (make install <package>), or install all project dependencies (make install)
.PHONY: install
install:
	@if [ -z "$(filter-out install,$(MAKECMDGOALS))" ]; then \
		echo "Installing dependencies"; \
		uv sync; \
	else \
		pkg="$(filter-out install,$(MAKECMDGOALS))"; \
		echo "Adding package $$pkg"; \
		uv add $$pkg; \
	fi

## start: run local project
.PHONY: start
start:
	clear
	@echo ""
	@if [ -f .env ]; then set -a && source .env && set +a && uv run python -u main.py; else uv run python -u main.py; fi

%:
	@:
