all: test build

PY3 = python3
VENV_DIR = .venv/mpyk
VENV_PY3 = .venv/mpyk/bin/python

config:
	@echo "---- Cleanup ----"
	@rm -rf $(VENV_DIR)
	@mkdir -p $(VENV_DIR)
	@echo "---- Creating virtualenv ----"
	@$(PY3) -m venv $(VENV_DIR)
	@echo "---- Installing dependencies ----"
	@$(VENV_PY3) -m pip install --upgrade pip
	@$(VENV_PY3) -m pip install -r requirements.txt
	@$(VENV_PY3) -m pip install -r requirements-dev.txt

test:
	@echo "---- Testing ---- "
	@$(VENV_PY3) -m mypy --ignore-missing-imports .

.PHONY: all config test
