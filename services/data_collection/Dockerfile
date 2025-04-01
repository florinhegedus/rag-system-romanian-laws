FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install core package
COPY core ./core

# Install data collection package
COPY services/data_collection/src ./src/
COPY services/data_collection/requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-m", "src.main"]
