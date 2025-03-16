#!/bin/bash
docker-compose build collect-data
docker-compose run --rm collect-data