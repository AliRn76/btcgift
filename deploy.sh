#!/bin/bash

git pull origin master
docker build -t btcgift:v1 .
docker rm -f btcgift
./docker_run.sh
echo "🚀 Deployed Successfully."