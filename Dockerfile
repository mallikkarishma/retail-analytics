# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OpenCV system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --retries 5 --timeout 120 -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p backend/retail_analytics/uploads \
    backend/retail_analytics/logs \
    backend/retail_analytics/reports \
    backend/retail_analytics/models

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]