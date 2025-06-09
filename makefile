## Welcome to the MakeFile for package_name!

## Runs all of the commands (exlucding setup) (runs by default)
all: check-security check-style format test docs dist

## Runs bandit on the project to check for security issues
check-security:
	uvx "bandit[toml]" -c pyproject.toml --severity-level=medium -r package_name

## Runs ruff to check for style issues
check-style:
	uvx ruff format --check .
	uvx ruff check --select E --select F --select I .

# Builds the package distribution using build
dist:
	uv run --group build python -m build

# Build the documentation using Sphinx
docs:
	uv run --directory docs --group docs make clean html latex epub

# Formats the code using ruff according the the `black` style
format:
	uvx ruff format .
	uvx ruff check --select I --fix .

# Runs the setup script for renaming and setting up the project
setup:
	uv run --with "GitPython==3.1.44" project_setup.py

# Runs the tests using pytest and generates coverage reports
test:
	uv run --group test pytest -v --cov=package_name --cov-report=xml --cov-report=html

# https://stackoverflow.com/a/77245502/2691018
## Print this help
help:
	@awk '/^## / \
        { if (c) {print c}; c=substr($$0, 4); next } \
         c && /(^[[:alpha:]][[:alnum:]_-]+:)/ \
        {print $$1, "\t", c; c=0} \
         END { print c }' $(MAKEFILE_LIST)

.PHONY: all check-security check-style dist docs format help test
