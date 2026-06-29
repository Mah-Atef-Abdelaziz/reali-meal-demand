# ===================================================
# REAL.i Meal Demand AI — Dedicated Backend Dockerfile
# ===================================================
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for PostgreSQL and GCC
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (context is set to backend/ or root)
COPY . ./backend/

# For other folders, if copying from root
# COPY ml/ ./ml/
# COPY database/ ./database/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Hugging Face default port is 7860, Render/others use PORT env var
EXPOSE 7860

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
