# Romanian Laws RAG

This repository contains a system for collecting, processing, and querying Romanian laws. The system includes various components for data collection, ETL (Extract, Transform, Load) processes, and a backend service for querying the processed data. The architecture is designed to be modular and scalable, leveraging Docker for containerization and PostgreSQL for data storage.

![Architecture](static/rolaw.jpg)


## Local Deployment
1. Start persistent services:
```bash
make start-persistent-services  # minio, postgres
```
2. Run on-demand components:
```bash
make collect-data  # Collect data to MinIO bucket
make etl  # Save legal articles to Postgres
```

Clear all data:
```bash
make docker-nuke
```
