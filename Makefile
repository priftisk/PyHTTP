.PHONY: run test

PYTHON := python

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m pytest test/test_pyhttp.py -v