# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set PYTHONPATH so the app can find the rag_backend package
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from the backend folder
COPY rag_backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rag_backend folder INTO the container's rag_backend folder
# This preserves the package structure for imports like "from rag_backend.core..."
COPY rag_backend/ ./rag_backend/

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "rag_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
