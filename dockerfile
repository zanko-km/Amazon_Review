FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system packages required by psycopg2 and other compiled libs
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip tools and install dependencies
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# Copy entire project (including scripts/) to the container
COPY . .

# Set environment variables
ENV DB_NAME=Phase_2 \
    DB_USER=postgres \
    DB_PASSWORD=pass \
    DB_HOST=host.docker.internal \
    DB_PORT=5432

# Run main script
CMD ["python", "pipeline.py"]
