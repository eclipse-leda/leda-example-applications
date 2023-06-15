# /********************************************************************************
# * Copyright (c) 2023 Contributors to the Eclipse Foundation
# *
# * See the NOTICE file(s) distributed with this work for additional
# * information regarding copyright ownership.
# *
# * This program and the accompanying materials are made available under the
# * terms of the Apache License 2.0 which is available at
# * http://www.apache.org/licenses/LICENSE-2.0
# *
# * SPDX-License-Identifier: Apache-2.0
# ********************************************************************************/

# Direct adaptation of: https://github.com/eclipse/kuksa.val.services/blob/main/hvac_service/Dockerfile


# Build stage, to create a Virtual Environent

FROM --platform=$TARGETPLATFORM python:3.9-slim-bullseye as builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "-- Running on $BUILDPLATFORM, building for $TARGETPLATFORM"

RUN apt-get update -qqy && apt-get upgrade -qqy && apt-get install -qqy binutils g++

COPY . /

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN /opt/venv/bin/python3 -m pip install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install wheel && \
    pip3 install scons && \
    pip3 install pyinstaller && \
    pip3 install patchelf==0.17.0.0 && \
    pip3 install staticx

# install sdv package in edit mode
RUN pip3 install --no-cache-dir -e .

RUN pyinstaller --clean -F -s driver_runner.py

WORKDIR /dist
RUN staticx driver_runner driver_runner-exe

# Runner stage, to copy in the virtual environment and the app
FROM scratch

# LABEL org.opencontainers.image.source="https://github.com/eclipse/kuksa.val.services"

# needed as /dist/binary unpacks and runs from /tmp
WORKDIR /tmp
# optional volume mapping
WORKDIR /conf

WORKDIR /dist

COPY --from=builder /dist/driver_runner-exe .

ENV PATH="/dist:$PATH"

CMD ["./driver_runner-exe"]