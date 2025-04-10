# Romanian Laws RAG

This repository contains a system for collecting, processing, and querying Romanian laws. The system includes various components for data collection and processing, an API for getting legal information and LLM responses and a frontend application. The architecture is designed to be modular and scalable, leveraging Docker for containerization.

![Architecture](static/rolaw.jpg)

## Prerequisites
`Docker` and `CMake` installed.

## Local Deployment
1. Start persistent services:
```bash
make start-persistent-services  # minio, postgres, qdrant
```
2. Run on-demand services:
- collect data and save to S3 compatible bucket
- extract laws and save to postgres db
- generate embeddings for the laws and save them to qdrant db:
```bash
make run-on-demand-services
```
3. Start FastAPI backend and NextJS frontend:
```bash
make start-backend
make start-frontend
```
4. Test backend:
```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"question": "ce se poate intampla daca fac evaziune fiscala", "top_k": 3}'  # get relevant laws
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"question": "ce se poate intampla daca fac evaziune fiscala", "top_k": 3}'  # get llm response interpreting the laws
```

Clear all data:
```bash
make docker-nuke
```

## Web App
After starting the backend API and the frontend, you can access the frontend at `localhost:3000`. The LLM responds based on retrieved laws and displays links that point directly to the specific law.
![webapp](static/webapp.png)
