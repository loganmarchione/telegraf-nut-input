.PHONY: lint security test

lint:
	@echo "################################################################################"
	@echo "# flake8"
	@echo "################################################################################"
	# https://www.flake8rules.com/rules/E501.html
	flake8 --extend-ignore=E501 input.py

	@echo "################################################################################"
	@echo "# isort"
	@echo "################################################################################"
	isort --check-only . --diff

	@echo "################################################################################"
	@echo "# black"
	@echo "################################################################################"
	black --check --diff .

security:
	@echo "################################################################################"
	@echo "# bandit"
	@echo "################################################################################"
	bandit -r --exclude /venv .

test:
	@echo "################################################################################"
	@echo "# tests"
	@echo "################################################################################"
	pytest tests/

check: lint security test