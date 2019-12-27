#!/bin/bash
set -e

TAG=${1:-`date '+%Y%m%d%H%M%S'`}
REGISTRY=${2:-vpereskokov/vpagroup}

echo "${TAG}" "${REGISTRY}"

DOCKER_CONTAINER_NAME="trkir_pyadmin_test"
DOCKER_CONTAINER_INDEX="1"

function pushToRegistry() {
    # $1 - TAG
    REGISTRY_WITH_TAG="${REGISTRY}:$1"
    echo "Registry with tag: ${REGISTRY}:${TAG}"
    docker tag "${DOCKER_CONTAINER_NAME}" "${REGISTRY}:${TAG}"
    docker push "${REGISTRY}:${TAG}"
}

if docker stop "${DOCKER_CONTAINER_NAME}_${DOCKER_CONTAINER_INDEX}"; then
    echo Stopped
fi

# Build and push to registry
docker-compose up --build -d
docker commit "${DOCKER_CONTAINER_NAME}_${DOCKER_CONTAINER_INDEX}" "${DOCKER_CONTAINER_NAME}"
pushToRegistry "${TAG}" "${DOCKER_CONTAINER_NAME}"

# Clear artifacts
if docker stop "${DOCKER_CONTAINER_NAME}_${DOCKER_CONTAINER_INDEX}"; then
    echo Stopped
else
    echo Not started
fi
docker rmi -f "${DOCKER_CONTAINER_NAME}"

# Show the correct tag
echo "Tag: ${TAG}"
