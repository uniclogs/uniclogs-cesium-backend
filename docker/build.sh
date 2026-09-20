#!/usr/bin/env bash

TEMPLATE_FILE="docker-compose.yaml"
BUILD_FILE="docker-compose-build.yaml"

VERSION_FILE="../pyproject.toml"
VERSION=$(grep -i 'version' $VERSION_FILE | head -n1 | cut -d'"' -f2 | xargs)

EPHEMERAL_ARTIFACTS="../.ruff_cache ../build ../dist $BUILD_FILE"

function clean() {
    rm -rf $EPHEMERAL_ARTIFACTS
}

function build_wheel() {
    cd ..
    python -m build --wheel
    cd -
}

function build_docker() {
    sed "s/RE_VERSION/$VERSION/g" $TEMPLATE_FILE > $BUILD_FILE
    docker compose -f $BUILD_FILE build
}

clean
build_wheel
build_docker
clean