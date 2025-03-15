FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app
COPY training/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy training code
COPY training/ .

# Run the training script
CMD ["python3", "-u", "main.py"]