FROM python:3.14.6-slim
RUN pip install --no-cache-dir uv \
    && useradd --create-home --uid 1000 app
WORKDIR /app
COPY pyproject.toml uv.lock .env.sample main.py ./
COPY src ./src
RUN cp .env.sample .env && uv sync --frozen && chown -R app:app /app
USER app
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
