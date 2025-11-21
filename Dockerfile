FROM python:3.11-slim

# Set working directory to /app (not /app/backend)
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into /app
# This way backend/app becomes /app/app
COPY backend/ .

# Expose port
EXPOSE 8000

# Run uvicorn - now it can find app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]