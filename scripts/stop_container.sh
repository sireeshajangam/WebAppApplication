#!/bin/bash
set -e

# Get IDs of all running containers
running_containers=$(sudo docker ps -q)

# Loop through each container ID and stop it
for container_id in $running_containers; do
    sudo docker stop "$container_id"
done
