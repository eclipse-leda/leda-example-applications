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

# Application configuration:
# Note: The mentioned hostnames are not set up by this script!
#   SDV_SEATSERVICE_ADDRESS=grpc://seatservice-example:50051
#   SDV_MQTT_ADDRESS=mqtt://mosquitto:1883
#   SDV_VEHICLEDATABROKER_ADDRESS=grpc://databroker:55555
#   SDV_MIDDLEWARE_TYPE=native

echo "Stopping existing containers..."
docker stop mosquitto
docker stop databroker
docker stop seatservice-example
echo "Removing existing containers..."
docker rm mosquitto
docker rm databroker
docker rm seatservice-example

echo "Removing network..."
docker network rm vehiclenetwork

echo "Creating network..."
docker network create vehiclenetwork


echo "Creating service containers..."
docker create --net=vehiclenetwork --volume $(pwd)/mosquitto-conf:/mosquitto/config --publish "1883:1883" --name mosquitto eclipse-mosquitto
docker start mosquitto

docker create --net=vehiclenetwork --publish "55555:55555" --name databroker ghcr.io/eclipse/kuksa.val/databroker:0.3
docker start databroker

docker create --net=vehiclenetwork --publish "50051:50051" --name seatservice-example ghcr.io/eclipse/kuksa.val.services/seat_service:v0.2.0
docker start seatservice-example

echo "Running application container..."
#    --read-only \
docker run --rm \
    --net=vehiclenetwork \
    --env "SDV_MIDDLEWARE_TYPE=native" \
    --env "SDV_VEHICLEDATABROKER_ADDRESS=grpc://databroker:55555" \
    --env "SDV_MQTT_ADDRESS=mqtt://mosquitto:1883" \
    --env "SDV_SEATSERVICE_ADDRESS=grpc://seatservice-example:50051" \
    --cpus 1.0 \
    --memory "100MB" \
    ghcr.io/eclipse-leda/leda-example-applications/leda-example-seat-adjuster:latest

# Docker Exit Code 137 _may_ indicate OOM.
# For debugging:
# docker run -it --rm \
#     --net=vehiclenetwork \
#     --entrypoint /bin/bash \
#     --env "SDV_MIDDLEWARE_TYPE=native" \
#     --env "SDV_VEHICLEDATABROKER_ADDRESS=grpc://databroker:55555" \
#     --env "SDV_MQTT_ADDRESS=mqtt://mosquitto:1883" \
#     --env "SDV_SEATSERVICE_ADDRESS=grpc://seatservice-example:50051" \
#     --cpus 1.0 \
#     --memory "100MB" \
#     ghcr.io/eclipse-leda/leda-example-seat-adjuster:latest
