FROM python:3.11-slim

# Install system dependencies (required for pyttsx3)
RUN apt-get update && apt-get install -y \
    espeak \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run Gunicorn
CMD ["gunicorn", "app:app"]
