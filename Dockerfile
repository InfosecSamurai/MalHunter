FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    tshark \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Setup directories
RUN mkdir -p /app/samples /app/reports /app/logs

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV VT_API_KEY=""
ENV NETWORK_INTERFACE=eth0

CMD ["python", "main.py"]
