#!/bin/bash

CURRENT_DIR=`pwd`
PROJECT_NAME=`basename ${CURRENT_DIR}`
ARTIFACT_DIR="${CURRENT_DIR}/artifacts"

mkdir -p $ARTIFACT_DIR

docker build -t "${PROJECT_NAME}/deb:latest" -f Dockerbuild ./
docker run -v $ARTIFACT_DIR:/artifacts -it "${PROJECT_NAME}/deb:latest"
