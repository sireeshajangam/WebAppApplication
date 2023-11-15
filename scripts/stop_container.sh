#!/bin/bash
set -e
running_containers=$(sudo docker ps -q)
sudo docker stop "$running_containers"

# Stop the running container (if any).
