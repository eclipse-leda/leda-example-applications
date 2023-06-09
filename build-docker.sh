#!/bin/bash
# Build examples using Docker BuildX

docker buildx create --name mybuilder
docker buildx use mybuilder
docker buildx inspect --bootstrap
docker buildx build --platform linux/amd64,linux/arm64 --tag ghcr.io/eclipse-leda/leda-example-seat-adjuster:latest --progress plain - < Dockerfile.seat-adjuster
