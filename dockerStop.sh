#!/bin/zsh

if [[ ! -z $(docker ps -a | grep directions.api) ]]
then
    docker container stop directions-api
fi