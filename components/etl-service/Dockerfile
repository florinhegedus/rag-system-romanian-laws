FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL code
COPY src/ .

# Run the ETL pipeline
CMD ["python", "-u", "main.py"]