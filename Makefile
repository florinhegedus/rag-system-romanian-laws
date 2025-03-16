ifeq (,$(wildcard .env))
$(error .env file is missing. Please create one based on .env.example)
endif

include .env

# --- Utilities ---
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


# --- Infrastructure --- 
collect-data:  # Collect raw legal data from online sources
	docker-compose build collect-data
	docker-compose run --rm collect-data

local-docker-stop-containers:  # Stop all running containers
	docker compose stop
