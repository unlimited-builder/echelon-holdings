# Production Dockerfile for Deep Echelon Holdings
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create entrypoint script for database initialization
RUN echo '#!/bin/sh\n\
if [ ! -f /app/echelon_holdings.db ]; then\n\
  echo "Initializing database..."\n\
  python init_db.py\n\
fi\n\
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
