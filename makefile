check-style:
	uvx ruff check . --select E --select F --select I

docs:
	uv run --directory docs --group docs make clean html latex epub

.PHONY: check-style docs
