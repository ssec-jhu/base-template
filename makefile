docs:
	uv run --directory docs --group docs make clean html latex epub

.PHONY: docs
