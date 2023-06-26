#!/bin/zsh

if [[ ! -z $(docker ps -a | grep directions.api) ]]
then
    docker container stop directions-api
fi

docker build -t directions-api .
docker run --rm -itd -p 8000:8000 --name directions-api directions-api