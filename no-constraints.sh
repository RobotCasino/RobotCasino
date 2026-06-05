#! /bin/sh

docker container stop robotcasino
docker container rm robotcasino
docker build . -t robotcasino:latest
docker run --name robotcasino -d \
 -v ./output/screenshots/:/home/jhon/Downloads/robotcasino/ \
 -e DISPLAY=host.docker.internal:0 \
 -e HEADLESS=1 \
 robotcasino run \
     no-constraints-chrome one-win aviator simple-strategy \
     --SESSION_TOKEN 99fd136e-1fca-5676-b5ee-5032df308c5d \