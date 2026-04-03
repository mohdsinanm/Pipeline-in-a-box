FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY . .

RUN uv sync --frozen || uv pip install .

ENV PYTHONUNBUFFERED=1

CMD ["uv","run", "python", "main.py"]