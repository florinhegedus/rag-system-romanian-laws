FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL code
COPY etl.py .
COPY models.py .

# Run the ETL pipeline
CMD ["python", "-u", "etl.py"]
