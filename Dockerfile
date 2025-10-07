FROM python:3.12-slim

WORKDIR /app

# Install only what you need
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for better caching)
COPY main-backend/requirements.txt .

# Install Python deps
# RUN pip install --no-cache-dir -r requirements.txt

# Copy only source code (not the whole 2.2 GB)
COPY main-backend/ ./main-backend/

# Run FastAPI
CMD ["uvicorn", "main-backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
