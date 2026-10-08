FROM python:3.14.8-alpine

ARG VERSION=0.1.0
ARG REVISION=
ARG CREATED=

RUN pip install --no-cache-dir uv \
    && useradd --create-home --uid 1000 app
WORKDIR /app
COPY pyproject.toml uv.lock .env.sample main.py ./
COPY src ./src
RUN cp .env.sample .env && uv sync --frozen && chown -R app:app /app
USER app

LABEL org.opencontainers.image.title="py-fastapi-mecanica-siaes" \
      org.opencontainers.image.description="Basic CRUD system for customer" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${REVISION}" \
      org.opencontainers.image.created="${CREATED}" \
      org.opencontainers.image.source="https://github.com/andrey-murari/py-fastapi-mecanica-siaes" \
      org.opencontainers.image.url="https://github.com/andrey-murari/py-fastapi-mecanica-siaes" \
      org.opencontainers.image.authors="Andrey Murari <contato@andreymurari.com>" \
      org.opencontainers.image.vendor="Andrey Murari"

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
