FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
COPY src/ ./src/
COPY .git/ ./.git/

RUN pip install --no-cache-dir -e .

ENV GEMINI_COOKIE_PATH=/data/gemini_webapi

EXPOSE 8000

CMD ["python", "-m", "gemini_webapi"]
