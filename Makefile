# This Makefile is basically copied from Abakus with no shame.
# https://github.com/webkom/lego

help:
	@echo 'fixme        - Fix code formatting'
	@echo 'check        - Check code formatting'

fixme:
	black nablaweb nablapps

check:
	flake8 --max-line-length=88

.PHONY: fixme check
