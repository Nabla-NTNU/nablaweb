# This Makefile is basically copied from Abakus with no shame.
# https://github.com/webkom/lego

help:
	@echo 'fixme        - Fix code formatting'
	@echo 'check        - Check code formatting'

fixme:
	isort -rc && black nablapps nablaweb manage.py

check:
	isort -rc --check-only && black --check nablapps nablaweb manage.py

.PHONY: fixme check
