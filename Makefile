ifeq (,$(wildcard .env))
$(error .env file is missing. Please create one based on .env.example)
endif

include .env

# --- Utilities ---
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


# --- On-demand Services --- 
collect-data:  # Collect raw legal data from online sources
	docker-compose build collect-data
	docker-compose run --rm collect-data

process-data:  # Extract, transform and load data into the database
	docker-compose build process-data
	docker-compose run --rm process-data

train-model:  # Train the model
	docker-compose build train-model
	docker-compose run --rm train-model

generate-embeddings:  # Generate embeddings for legal documents
	docker-compose build generate-embeddings
	docker-compose run --rm generate-embeddings
	
# --- Infrastructure ---
docker-stop-containers:  # Stop all running containers
	docker compose stop

docker-stop-and-remove-containers:  # Stop and remove all running containers
	docker compose down

start-persistent-services:  # Start the Minio and Postgres services
	docker-compose up -d minio postgres qdrant

stop-and-remove-postgres-db:  # Stop and remove the Postgres container and its data
	docker-compose rm -s -v postgres
	docker volume rm rag-system-romanian-laws_pg_data

.PHONY: docker-nuke

docker-nuke: confirm ## COMPLETELY remove all Docker artifacts
	@echo "Stopping and removing all containers..."
	docker-compose down --volumes --remove-orphans
	@echo "Removing any remaining containers..."
	docker rm -f $(shell docker ps -aq) 2>/dev/null || true
	@echo "Removing project volumes..."
	docker volume rm $(shell docker volume ls -q | grep -E 'minio_data|pg_data|qdrant_data') 2>/dev/null || true
	@echo "Pruning networks..."
	docker network prune -f
	@echo "Cleanup complete!"

confirm:
	@echo -n "Are you sure you want to delete ALL Docker data? [y/N] " && read ans && [ $${ans:-N} = y ]
