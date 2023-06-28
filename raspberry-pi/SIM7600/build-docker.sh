#!/bin/bash
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
# Build examples using Docker BuildX
#
# Setup:
# - sudo apt-get install -y qemu-user-static
# - sudo apt-get install -y binfmt-support
# - docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
# - docker buildx rm ledabuilder
# - docker buildx create --name ledabuilder --use

docker build \
    --tag ghcr.io/eclipse-leda/leda-example-applications/leda-example-sim7600x:latest \
    --progress plain \
    .
