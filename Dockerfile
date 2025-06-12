# Adapted from https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY . .

# Install dependencies in the fixed prd group
RUN uv sync --group prd --locked --no-install-project
# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"
# Override the entrypoint to not be uv
ENTRYPOINT []

CMD ["uvicorn", "package_name.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
