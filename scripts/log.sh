#! /bin/bash

for arg in "$@"; do
  if [[ "$arg" == "-f" || "$arg" == "--follow" ]]; then
    docker logs robotcasino -f
  else
    docker logs robotcasino
  fi
done


docker logs robotcasino

