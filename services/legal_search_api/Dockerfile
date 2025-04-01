FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install core package
COPY core ./core

COPY services/legal_search_api/src ./src/
COPY services/legal_search_api/requirements.txt .

RUN pip install -r requirements.txt

# Pre-download the embedding model during build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BlackKakapo/stsb-xlm-r-multilingual-ro')"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
