#!/bin/bash
sudo docker build -t intercombot .
ENV_FILE="--env-file $(pwd)/.env"

CONTAINERS=$(sudo docker ps -q)
sudo docker kill $CONTAINERS
sudo docker run -p 0.0.0.0:9000:80 $ENV_FILE -v $(pwd)/intercombot/:/intercombot/intercombot -d -t intercombot
