# Helper to lint/check formatting and format code
# Also used in our github actions

# Files/directories to check
targets := nablapps nablaweb manage.py

help:
	@echo 'Commands:'
	@echo 'fixme             - Fix code formatting'
	@echo 'check             - Check code formatting'
	@echo 'lint              - Report linting/security warnings'
	@echo
	@echo 'check-fatal       - Check for fatal errors'
	@echo 'check-formatting  - Check for formatting errors'
	@echo 'report-flake8     - Report linting errors from flake8'
	@echo 'report-pylint     - Report linting errors from pylint'
	@echo 'report-bandit     - Report security audit from bandit'

# Check for Python syntax errors and undefined names
check-fatal:
	flake8 --count --select=E9,F63,F7,F82 --show-source --statistics $(targets)

check-formatting:
	isort --check-only $(targets)
	black --check $(targets)

# The 'report' targets use || true to always exit with code 0 (success). This is
# because they are only intended to report on potential errors for the time being.
report-flake8:
	flake8 --count --statistics $(targets) || true

report-pylint:
	pylint $(targets) || true

report-bandit:
	bandit -r $(targets) || true

check: check-fatal check-formatting

lint: report-flake8 report-pylint report-bandit

fixme:
	isort $(targets)
	black $(targets)

.PHONY: help check-fatal check-formatting report-flake8 report-pylint report-bandit check fixme
