# Romanian Laws Rag
1. Start persistent services:
```bash
docker-compose up -d minio postgres mlflow qdrant inference-api react-ui
```
2. Run on-demand components when needed:
```bash
./scripts/run_component1.sh  # Scrape laws
./scripts/run_component2.sh  # Run ETL
./scripts/run_component3.sh  # Train model
./scripts/run_component4.sh  # Generate embeddings
```