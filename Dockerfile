# syntax=docker/dockerfile:1

FROM python:3.14.8-slim AS configure

COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /src

COPY pyproject.toml uv.lock ./

# Slim is glibc. Install musl wheels so the packages can run on Alpine.
ARG TARGETARCH
RUN set -eu; \
    case "${TARGETARCH}" in \
      amd64) MUSL_PLATFORM="x86_64-unknown-linux-musl" ;; \
      arm64) MUSL_PLATFORM="aarch64-unknown-linux-musl" ;; \
      *) echo "unsupported architecture: ${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    uv export --frozen --no-dev --no-emit-project --output-file /tmp/requirements.txt; \
    uv pip install \
      --require-hashes \
      --only-binary :all: \
      --python-platform "${MUSL_PLATFORM}" \
      --python-version 3.14 \
      --target /opt/python \
      -r /tmp/requirements.txt; \
    rm -f /tmp/requirements.txt

FROM python:3.14.8-alpine AS runtime

RUN apk upgrade --no-cache \
    && apk add --no-cache libstdc++ libgcc \
    && addgroup -g 1000 -S app \
    && adduser -u 1000 -S -D -H -G app -s /sbin/nologin app \
    && rm -rf \
        /usr/local/lib/python3.14/site-packages/pip \
        /usr/local/lib/python3.14/site-packages/pip-*.dist-info \
        /usr/local/lib/python3.14/site-packages/setuptools \
        /usr/local/lib/python3.14/site-packages/setuptools-*.dist-info \
        /usr/local/lib/python3.14/site-packages/wheel \
        /usr/local/lib/python3.14/site-packages/wheel-*.dist-info \
        /usr/local/lib/python3.14/ensurepip \
        /usr/local/bin/pip \
        /usr/local/bin/pip3 \
        /usr/local/bin/pip3.* \
        /root/.cache

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONSAFEPATH=1 \
    PYTHONPATH=/app:/opt/python

COPY --from=configure /opt/python /opt/python
COPY main.py ./
COPY src ./src
COPY .env.sample ./

RUN cp .env.sample .env \
    && rm .env.sample \
    && chown -R root:app /app /opt/python \
    && find /app /opt/python -type d -exec chmod 0755 {} + \
    && find /app /opt/python -type f -exec chmod 0644 {} + \
    && chmod 0440 /app/.env \
    && if [ -d /opt/python/bin ]; then find /opt/python/bin -type f -exec chmod 0755 {} +; fi

ARG VERSION=0.1.0
ARG REVISION=
ARG CREATED=

LABEL org.opencontainers.image.title="py-fastapi-mecanica-siaes" \
      org.opencontainers.image.description="Basic CRUD system for customer" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${REVISION}" \
      org.opencontainers.image.created="${CREATED}" \
      org.opencontainers.image.source="https://github.com/andrey-murari/py-fastapi-mecanica-siaes" \
      org.opencontainers.image.url="https://github.com/andrey-murari/py-fastapi-mecanica-siaes" \
      org.opencontainers.image.authors="Andrey Murari <contato@andreymurari.com>" \
      org.opencontainers.image.vendor="Andrey Murari"

USER app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
