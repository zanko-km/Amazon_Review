FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_NAME=Phase_2 \
    DB_USER=postgres \
    DB_PASSWORD=pass \
    DB_HOST=host.docker.internal \
    DB_PORT=5432

CMD ["python", "pipeline.py"]