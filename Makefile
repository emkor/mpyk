config: clean setup install
test: lint ut at
all: test build

PY3 = python3
VENV = .venv/$(shell basename $$PWD)
VENV_PY3 = .venv/$(shell basename $$PWD)/bin/python3

clean:
	@echo "---- Doing cleanup ----"
	@rm -rf .venv .mypy_cache .pytest_cache *.egg-info build dist
	@mkdir -p .venv

setup:
	@echo "---- Setting up virtualenv ----"
	@$(PY3) -m venv $(VENV)
	@echo "---- Installing dependencies and app itself in editable mode ----"
	@$(VENV_PY3) -m pip install --upgrade pip wheel setuptools

install:
	@echo "---- Installing package in virtualenv ---- "
	@$(VENV_PY3) -m pip install -e .[dev]

lint:
	@echo "---- Running linter ---- "
	@$(VENV_PY3) -m mypy --ignore-missing-imports mpyk

ut:
	@echo "---- Running unit tests ---- "
	@$(VENV_PY3) -m pytest -ra -v -s test/unit

at:
	@echo "---- Running acceptance tests ---- "
	@$(VENV_PY3) -m pytest -ra -v -s test/acceptance

build:
	@echo "---- Building distributable package ---- "
	@$(VENV_PY3) setup.py sdist --dist-dir ./dist

.PHONY: all config test build clean setup install lint ut at
