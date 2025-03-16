FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY embeddings/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy embedding generation code
COPY embeddings/ .

# Run the embedding generator
CMD ["python", "-u", "main.py"]