# ===================================================
# REAL.i Meal Demand AI — Hugging Face Spaces Dockerfile
# ===================================================
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ ./backend/

# Copy ML models and data if present
COPY ml/ ./ml/ 2>/dev/null || true

# Copy environment file
COPY backend/.env ./backend/.env 2>/dev/null || true

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Hugging Face Spaces uses port 7860
EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
