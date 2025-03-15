FROM python:3.12 -slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy inference API code
COPY backend/ .

# Expose the API port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]