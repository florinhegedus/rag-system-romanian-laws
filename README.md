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
make etl  # Run ETL
```
3. Check articles in postgres DB:
- Connect to the container.
```bash
docker-compose exec postgres psql -U yourusername -d yourdatabase
# Alternative is to connect from host terminal, not from container
psql -h localhost -p 5432 -U yourusername -d yourdatabase
```
- Check all tables and articles table.
```sql
-- List all tables
\dt
-- Describe the articles table
\d articles
-- Select all data from the articles table
SELECT * FROM articles;
```
- Optionally, you can delete all the data in postgres:
```sql
-- Switch to a different database
\c postgres
-- Drop database
DROP DATABASE yourdatabase;
-- Verify the database is dropped
\l
-- Create database
CREATE DATABASE yourdatabase;
```