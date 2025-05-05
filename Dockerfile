FROM python:3.12.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction --no-ansi
COPY . .
EXPOSE 8000

CMD ["poetry", "run", "litestar", "--app", "app.main:app", "run", "--reload", "--host", "0.0.0.0", "--port", "8000"]