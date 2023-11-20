#!/bin/bash
set -e

stop_containers() {
    running_containers=$(sudo docker ps -q --filter "expose=8000" || true)

    # Check if there are any running containers to stop
    if [ -n "$running_containers" ]; then
        echo "Containers to stop:"
        echo "$running_containers"

        # Stop each container
        while IFS= read -r container_id; do
            echo "Stopping container $container_id..."
            sudo docker stop "$container_id"
        done <<< "$running_containers"
    else
        echo "No running containers exposing port 8000 found."
    fi
}

# Call function to stop containers
stop_containers
