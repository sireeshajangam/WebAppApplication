#!/bin/bash
set -e

# Get IDs of all running containers
running_containers=$(sudo docker ps -q)
sudo docker stop $running_containers