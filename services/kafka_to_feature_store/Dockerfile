# Use an official Python runtime as a parent image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set the working directory
WORKDIR /app

# Install Poetry and dependencies in a single layer
COPY pyproject.toml poetry.lock /app/
RUN pip install --no-cache-dir poetry==1.8.2 && \
    poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . /app

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]