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


FROM nodered/node-red
# FROM nodered/node-red:latest-debian

LABEL org.opencontainers.image.authors="leda-dev@eclipse.org"
LABEL org.opencontainers.image.url="https://github.com/eclipse-leda/leda-example-applications"
LABEL org.opencontainers.image.documentation="https://eclipse-leda.github.io/leda/docs/app-deployment/node-red/"
LABEL org.opencontainers.image.source="https://github.com/eclipse-leda/leda-example-applications/node-red"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.vendor="Eclipse Foundation"
LABEL org.opencontainers.image.title="Eclipse Leda Node-RED Example"
LABEL org.opencontainers.image.description="A Node-RED example with preconfigured nodes, flows and dashboard for the Eclipse Leda distribution."

COPY package.json .
RUN npm install --unsafe-perm --no-update-notifier --no-fund --omit=dev

ENV MQTT_ADDR="mosquitto"
ENV MQTT_PORT="1883"
ENV BROKER_ADDR="databroker"
ENV BROKER_PORT="55555"

# Copy _your_ Node-RED project files into place
# NOTE: This will only work if you DO NOT later mount /data as an external volume.
#       If you need to use an external volume for persistence then
#       copy your settings and flows files to that volume instead.
COPY settings.js /data/settings.js
# COPY flows_cred.json /data/flows_cred.json
COPY flows.json /data/flows.json
