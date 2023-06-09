#!/bin/bash
# Build examples using Docker BuildX

# docker buildx create --use
# docker buildx inspect --bootstrap
#docker buildx build --platform linux/amd64,linux/arm64 --tag ghcr.io/eclipse-leda/leda-example-seat-adjuster:latest --progress plain - < Dockerfile.seat-adjuster
docker build --tag leda/seat-adjuster --progress plain - < Dockerfile.seat-adjuster
