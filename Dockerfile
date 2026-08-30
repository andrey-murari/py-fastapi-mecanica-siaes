FROM python:3.14.6-slim
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY . .
RUN cp .env.sample .env && uv sync --frozen
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]