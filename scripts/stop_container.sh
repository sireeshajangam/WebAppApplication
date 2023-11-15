#!/bin/bash

# Get the IDs of running containers publishing port 8000
running_containers=$(sudo docker ps -q --filter "publish=8000")

# Output the IDs
echo "Containers to stop:"
echo "$running_containers"

# Stop each container
while IFS= read -r container_id; do
    echo "Stopping container $container_id..."
    sudo docker stop "$container_id"
done <<< "$running_containers"
