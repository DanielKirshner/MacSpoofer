#!/bin/bash

docker build -t spoofer_docker .
docker run -it spoofer_docker /bin/bash