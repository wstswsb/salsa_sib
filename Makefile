.PHONY: all test clean


tests: .PHONY
	pytest -s --cov-report term-missing --cov=. ./tests/

lint:
	flake8 ./