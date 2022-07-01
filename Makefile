.PHONY: all test clean


tests: .PHONY
	pytest --tb=short -n 8 --cov-report term-missing --cov=. ./tests/

lint:
	flake8 ./