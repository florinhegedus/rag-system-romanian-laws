FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install core package
COPY core ./core

# Install data collection package
COPY services/embeddings_generation/src ./src/
COPY services/embeddings_generation/requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-m", "src.main"]
