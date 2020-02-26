# This Makefile is basically copied from Abakus with no shame.
# https://github.com/webkom/lego

help:
	@echo 'fixme        - Fix code formatting'
	@echo 'check        - Check code formatting'

fixme:
	isort -rc && black nablapps

check:
	flake8 --max-line-length=88 && isort -rc --check-only

.PHONY: fixme check
