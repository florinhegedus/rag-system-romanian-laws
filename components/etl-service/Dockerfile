FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY etl-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL code
COPY etl-service/etl.py .
COPY ./common ./common

# Run the ETL pipeline
CMD ["python", "-u", "etl.py"]
