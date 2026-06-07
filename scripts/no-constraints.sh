#! /bin/sh

docker container stop robotcasino
docker container rm robotcasino
docker build . -t robotcasino:latest
docker run --name robotcasino -d \
 -v ./output/screenshots/:/app/screenshots/ \
 -m 800mb \
 --memory-swap 800mb \
 --shm-size=2gb \
 -e DISPLAY=host.docker.internal:0 \
 -e HEADLESS=0 \
 -e MEMORY_RELOAD_RATIO=0.95 \
 -e MEMORY_LIMIT_MB=700 \
 robotcasino run \
     no-constraints-chrome one-win aviator simple-strategy \
     --SESSION_TOKEN 99fd136e-1fca-5676-b5ee-5032df308c5d \
     --AUTO_CASHOUT 2.0 \
     --IS_TESTING true