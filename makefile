.PHONY: lint test

lint:
	# https://www.flake8rules.com/rules/E501.html
	flake8 --extend-ignore=E501 input.py
	isort --check-only . --diff
	black --check --diff .
	bandit -r .

test:
	pytest test_input.py

check: lint test