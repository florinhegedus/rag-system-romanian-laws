# Romanian Laws Rag
1. Start persistent services:
```bash
docker-compose up -d minio postgres mlflow qdrant inference-api react-ui
```
2. Run on-demand components when needed:
```bash
make collect-data  # Collect data to MinIO bucket
make etl  # Run ETL
```