FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv==0.11.29
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN uv sync --frozen --no-dev


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY src ./src

RUN useradd --create-home --uid 10001 nakshatra
USER nakshatra

EXPOSE 8000
CMD [".venv/bin/uvicorn", "nakshatra.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
