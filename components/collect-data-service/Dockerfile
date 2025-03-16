FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy collect data code
COPY collect_data.py .

# Run the data collection service
CMD ["python", "-u", "collect_data.py"] 