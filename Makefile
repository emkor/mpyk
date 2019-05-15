all: test build

PY3 = python3
VENV_DIR = .venv/mpyk
VENV_PY = .venv/mpyk/bin/python

config:
	@echo "---- Cleanup ----"
	@rm -rf $(VENV_DIR)
	@mkdir -p $(VENV_DIR)
	@echo "---- Creating virtualenv ----"
	@$(PY3) -m venv $(VENV_DIR)
	@echo "---- Installing dependencies ----"
	@$(VENV_PY) -m pip install --upgrade pip
	@$(VENV_PY) -m pip install -r requirements.txt
	@$(VENV_PY) -m pip install -r requirements-dev.txt

test:
	@echo "---- Testing ---- "
	@$(VENV_PY) -m mypy --ignore-missing-imports .

.PHONY: all config test
