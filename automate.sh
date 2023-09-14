#!/bin/bash

apt install docker.io
docker rm -f $(docker ps -aq)
docker system prune -f
cd /home/ubuntu
rm -r recommender_App/
cd /home/ubuntu
mkdir recommender_App
cd recommender_App/
aws s3 cp s3://movie-buck/recommender_App/ . --recursive
docker build -t recommendation .
docker run -p 8501:8501 recommendation
                                       