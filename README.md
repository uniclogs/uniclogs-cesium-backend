# Cesium Backend API

A supplimentary API for the CesiumJS App

&nbsp;

***

## Usage

### Run as a local python service

`$` `cesium-api --help`

## Run as a Docker container

`$` `docker compose up -d`

&nbsp;

***

## Development and Contribution

### Generate Tiles

`$` `make tiles`

### Install package locally

`$` `pip install -e .`

### Build wheel

`$` `python -m pip wheel . -w build --no-deps`

### Build Docker Image

`$` `make docker`