.PHONY: lint security test

lint:
	# https://www.flake8rules.com/rules/E501.html
	flake8 --extend-ignore=E501 input.py
	isort --check-only . --diff
	black --check --diff .

security:
	bandit -r .

test:
	pytest tests/

check: lint security test