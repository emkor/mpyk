config: clean setup install
test: ut lint at
all: test build

PY3 = python3
VENV = .venv/$(shell basename $$PWD)
VENV_PY3 = .venv/$(shell basename $$PWD)/bin/python3

clean:
	@echo "---- Doing cleanup ----"
	@rm -rf .venv .mypy_cache *.egg-info build dist
	@mkdir -p .venv

setup:
	@echo "---- Setting up virtualenv ----"
	@$(PY3) -m venv $(VENV)
	@echo "---- Installing dependencies and app itself in editable mode ----"
	@$(VENV_PY3) -m pip install --upgrade pip wheel setuptools

install:
	@echo "---- Installing napi-py in virtualenv ---- "
	@$(VENV_PY3) -m pip install -e .[dev]

lint:
	@echo "---- Running linter ---- "
	@$(VENV_PY3) -m mypy --ignore-missing-imports napi

ut:
	@echo "---- Running unit tests ---- "
	@$(VENV_PY3) -m pytest -ra -v -s test/unit

at:
	@echo "---- Running acceptance tests (requires napi-py on global PATH) ---- "
	@$(VENV_PY3) -m pytest -ra -v test/acceptance

build:
	@echo "---- Building distributable package ---- "
	@$(VENV_PY3) setup.py sdist bdist_wheel --python-tag py3 --dist-dir ./dist

.PHONY: all config test build clean setup install lint ut at
