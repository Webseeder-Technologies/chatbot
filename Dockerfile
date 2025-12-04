FROM python:3.12-slim

# Set the working directory to the app folder
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY main-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source
COPY main-backend/ ./main-backend/

# Make sure Python can import from /app/main-backend
ENV PYTHONPATH=/app/main-backend

# Change into main-backend when container runs
WORKDIR /app/main-backend

EXPOSE 5700

# Start FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5700"]
