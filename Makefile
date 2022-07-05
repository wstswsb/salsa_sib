.PHONY: all test clean


tests: .PHONY
	pytest -s -n 6 --cov-report term-missing --cov=. ./tests/

lint:
	flake8 ./
