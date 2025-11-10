# Simple production-ready Dockerfile
FROM python:3.11-slim

# System packages required by some optional features (WeasyPrint needs extra native libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port (platforms may override via $PORT)
EXPOSE 8080

# Use gunicorn for production. If using platform like Cloud Run the PORT env is expected.
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--workers", "2", "--threads", "2"]
