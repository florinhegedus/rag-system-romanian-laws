# Romanian Laws Rag
1. Start persistent services:
```bash
docker-compose up -d minio postgres #  mlflow qdrant inference-api react-ui
```
2. Run on-demand components when needed:
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