FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y git
RUN python -m pip install --upgrade pip
RUN python -m pip install .

CMD ["uvicorn", "package_name.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
