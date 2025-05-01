#!/bin/bash

# Run "docker build -t unit3dup ." inside the Docker folder first
# run the script

# Fixed path to Unit3Dbot.json on the host (edit as needed)
HOST_PATH="/home/parzival/Unit3Dup_config/Unit3Dbot.json"

# Fixed path in the container (guest)
GUEST_PATH="/root/Unit3Dup_config/Unit3Dbot.json"

# Controlla se il file JSON esiste sull'host
if [ ! -f "$HOST_PATH" ]; then
  echo "Error: The JSON config file does not exist $HOST_PATH"
  exit 1
fi

# Run Test
docker run --rm \
  -v "$HOST_PATH:$GUEST_PATH" \
  unit3dup --help
