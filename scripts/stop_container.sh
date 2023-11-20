#!/bin/bash
set -e

# Get IDs of all running containers
running_containers=$(sudo docker ps -q)

# Check if there are any running containers to stop
if [ -n "$running_containers" ]; then
    echo "Containers to stop:"
    echo "$running_containers"

    # Stop each container
    for container_id in $running_containers; do
        echo "Stopping container $container_id..."
        sudo docker stop "$container_id"
    done
else
    echo "No running containers found."
fi
