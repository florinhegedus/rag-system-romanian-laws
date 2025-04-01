# Romanian Laws RAG

This repository contains a system for collecting, processing, and querying Romanian laws. The system includes various components for data collection, ETL (Extract, Transform, Load) processes, and a backend service for querying the processed data. The architecture is designed to be modular and scalable, leveraging Docker for containerization and PostgreSQL for data storage.

![Architecture](static/rolaw.jpg)


## Local Deployment
1. Start persistent services:
```bash
make start-persistent-services  # minio, postgres, qdrant
```
2. Run on-demand components:
```bash
make collect-data  # Collect data to MinIO bucket
make process-data  # Save legal articles to Postgres
make generate-embeddings  # Query Postgres, embed and save laws to Qdrant
```
3. Start FastAPI backend and React frontend:
```bash


Clear all data:
```bash
make docker-nuke
```
