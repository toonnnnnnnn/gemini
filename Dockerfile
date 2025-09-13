# Use Debian as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including libxrender1 as specified
RUN apt-get update && apt-get install -y \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create uploads directory
RUN mkdir -p uploads

# Expose port 5001 (as specified in FastHTML docs)
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
