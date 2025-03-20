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

etl:  # Extract, transform and load data into the database
	docker-compose build etl
	docker-compose run --rm etl

train-model:  # Train the model
	docker-compose build train-model
	docker-compose run --rm train-model

generate-embeddings:  # Generate embeddings for legal documents
	docker-compose build embeddings-generation
	docker-compose run --rm embeddings-generation
	
# --- Infrastructure ---
docker-stop-containers:  # Stop all running containers
	docker compose stop

docker-stop-and-remove-containers:  # Stop and remove all running containers
	docker compose down

start-postgres-db:  # Start the Postgres database
	docker-compose up -d postgres

stop-and-remove-postgres-db:  # Stop and remove the Postgres database
	docker-compose rm -s -v postgres
