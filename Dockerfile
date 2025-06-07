FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN python -m pip install .

CMD ["uvicorn", "package_name.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
