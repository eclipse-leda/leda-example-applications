# /********************************************************************************
# * Copyright (c) 2023 Contributors to the Eclipse Foundation
# *
# * See the NOTICE file(s) distributed with this work for additional
# * information regarding copyright ownership.
# *
# * This program and the accompanying materials are made available under the
# * terms of the Apache License 2.0 which is available at
# * https://www.apache.org/licenses/LICENSE-2.0
# *
# * SPDX-License-Identifier: Apache-2.0
# ********************************************************************************/
#
# The "Seat Adjuster" use case shows how higher-level vehicle applications
# interact with lower-level vehicle abstraction services and make use
# of the Vehicle Signal Specification to ensure compatibility and standardization
# on vehicle signals.
#
# This Dockerfile describes the "Seat Adjuster" application container to be used
# in the Eclipse Leda example tutorial:
# https://eclipse-leda.github.io/leda/docs/app-deployment/seat-adjuster/
#
# It's derived from the Eclipse Velocitas SDK Examples:
# https://github.com/eclipse-velocitas/vehicle-app-python-sdk/tree/main/examples/seat-adjuster
#
#
#####################
# BUILD CONTAINER   #
#####################
FROM ubuntu AS builder

# Ignore "pip as root" warning, since we're running in a Docker
# https://github.com/pypa/pip/pull/11035
ENV PIP_ROOT_USER_ACTION ignore

# Prevent apt-get and debconf warnings about missing TER
ENV DEBIAN_FRONTEND noninteractive

# "python3 python3-pip git curl wget" is required by velocitas cli
# "binutils python3-dev" is required by pyinstaller
# "python-is-python3" is a workaround for velocitas subshell not finding /usr/bin/python
#   See https://github.com/eclipse-velocitas/devenv-devcontainer-setup/issues/21
RUN apt-get update -y && apt-get install -y --no-install-recommends python3-dev python3-pip git curl wget binutils python-is-python3

# PyInstaller bundles Python apps and their dependencies for distribution
RUN pip3 install --upgrade pip
RUN pip3 install pyinstaller

# Install the Velocitas SDK and cli tooling
# Use the Velocitas Python Template as a base and copy over the seat-adjuster example code.
RUN git clone https://github.com/eclipse-velocitas/vehicle-app-python-template.git /template
RUN git clone https://github.com/eclipse-velocitas/vehicle-app-python-sdk /sdk
RUN cp -rf /sdk/examples/seat-adjuster/* /template/app/
WORKDIR /template
RUN bash -c 'arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/x64/) \
    && curl -L https://github.com/eclipse-velocitas/cli/releases/latest/download/velocitas-linux-${arch} -o /usr/bin/velocitas \
    && chmod +x /usr/bin/velocitas'
RUN git config --global --add safe.directory $(pwd)

# Initializes the Vehicle Application development and
# generates the Vehicle Model for Python
RUN velocitas init --verbose

# Install Velocitas SDK Python dependencies
RUN pip3 install -r ./requirements.txt
RUN pip3 install --no-cache-dir ./gen/vehicle_model

# Install Seat Adjuster application Python dependencies
WORKDIR /template/app
RUN pip3 install -r ./requirements-links.txt
RUN pip3 install -r ./requirements.txt

# Bundle the Python application and its dependencies
# for smaller container size at runtime
# Note: Using "--onedir" to prevent uncompression at runtime,
# which is needed for read-only runtime containers.
RUN pyinstaller \
    --clean \
    --onedir \
    --distpath "./dist" \
    --name "seatadjuster" \
    --strip \
     src/main.py

#####################
# RUNTIME CONTAINER #
#####################
# Create the runtime container for the vehicle application
# We're using the minimal ubuntu container, as it uses glibc.
# PyInstaller cannot cross-compile, so it needs to run on same OS platform
# as the build time (e.g. CPU arch, Standard C library)
FROM ubuntu

# Set default environment variables suitable for Leda deployment
# Can be overridden at runtime.
ENV SDV_SEATSERVICE_ADDRESS="grpc://seatservice-example:50051"
ENV SDV_MQTT_ADDRESS="mqtt://mosquitto:1883"
ENV SDV_VEHICLEDATABROKER_ADDRESS="grpc://databroker:55555"
ENV SDV_MIDDLEWARE_TYPE="native"

# Docker Container Annotations
# See https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.authors="leda-dev@eclipse.org"
LABEL org.opencontainers.image.url="https://github.com/eclipse-leda/leda-example-applications"
LABEL org.opencontainers.image.documentation="https://eclipse-leda.github.io/leda/docs/app-deployment/seat-adjuster/"
LABEL org.opencontainers.image.source="https://github.com/eclipse-leda/leda-example-applications"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.vendor="Eclipse Foundation"
LABEL org.opencontainers.image.title="Eclipse Leda Seat Adjuster Example"
LABEL org.opencontainers.image.description="Seat Adjuster is an Eclipse Velocitas example app, allowing to remote control a vehicles Seat ECU using a standardized Vehicle Signal Specification compatible interface from Eclipse Kuksa."

WORKDIR /dist
COPY --from=builder /template/app/dist/ /dist
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "lsof", "-i:1883", "-sTCP:ESTABLISHED" ]
ENTRYPOINT [ "/dist/seatadjuster/seatadjuster" ]
