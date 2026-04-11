# Staging Dockerfile for sjvisualizer pipeline
FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p audio output logs cache assets

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command (run pipeline in dry-run for testing)
CMD ["python", "pipeline.py"]
