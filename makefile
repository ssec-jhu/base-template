all: check-security check-style format test docs dist

check-security:
	uvx "bandit[toml]" -c pyproject.toml --severity-level=medium -r package_name

check-style:
	uvx ruff format --check .
	uvx ruff check --select E --select F --select I .

dist:
	uv run --group build python -m build

docs:
	uv run --directory docs --group docs make clean html latex epub

format:
	uvx ruff format .
	uvx ruff check --select I --fix .

setup:
	uv run --with "GitPython==3.1.44" project_setup.py

test:
	uv run --group test pytest -v --cov=package_name --cov-report=xml --cov-report=html

.PHONY: all check-security check-style dist docs format test
