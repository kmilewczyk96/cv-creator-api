#!/bin/bash

# Function to clean up on exit
cleanup() {
    echo ""
    echo "Stopping containers and removing orphans..."
    docker compose down --remove-orphans
    exit
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

echo "Starting docker compose with watch flag..."
# Run docker compose up with watch. 
# We use exec to let docker compose handle the signals if we weren't trapping, 
# but since we want to run a command AFTER it stops, we just run it normally.
docker compose up --watch
