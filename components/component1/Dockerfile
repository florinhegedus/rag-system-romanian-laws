FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scraper code
COPY scraper/ .

# Run the scraper
CMD ["python", "-u", "main.py"] 