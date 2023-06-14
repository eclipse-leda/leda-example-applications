#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Build examples using Docker BuildX
# sudo apt-get install -y qemu-user-static
# sudo apt-get install -y binfmt-support
# docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
# docker buildx rm ledabuilder
# docker buildx create --name ledabuilder --use

docker buildx build \
    --builder ledabuilder \
    --platform "linux/amd64,linux/arm64" \
    --tag ghcr.io/eclipse-leda/leda-example-seat-adjuster:latest \
    --push \
    --progress plain \
    --file Dockerfile.seat-adjuster \
    .
