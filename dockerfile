# Use a slim Python base
FROM python:3.12-slim

# Ensure logs print immediately
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install only needed dependencies
RUN pip install --no-cache-dir requests python-dotenv

# Copy your Python code
COPY main.py /app/main.py

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run the script
CMD ["python", "-u", "main.py"]
