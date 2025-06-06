check-security:
	uvx bandit -c pyproject.toml --severity-level=medium -r package_name

check-style:
	uvx ruff format --check .
	uvx ruff check --select E --select F --select I .

docs:
	uv run --directory docs --group docs make clean html latex epub

format:
	uvx ruff format .
	uvx ruff check --select I --fix .

.PHONY: check-style docs format
