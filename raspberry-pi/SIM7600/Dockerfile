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
# A container to initialize the SIM7600E 4G HAT for the Raspberry Pi
# See https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT#Raspberry_Pi_initialization_settings
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
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends curl wget p7zip binutils ca-certificates
RUN apt-get install -y build-essential

WORKDIR /root

WORKDIR /root/bcm2835
RUN wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.73.tar.gz
RUN tar zxvf bcm2835-1.73.tar.gz
WORKDIR /root/bcm2835/bcm2835-1.73
RUN ls -al
RUN chmod +x ./configure
RUN ./configure
RUN make
RUN make install

WORKDIR /root
RUN wget https://www.waveshare.com/w/upload/2/29/SIM7600X-4G-HAT-Demo.7z
RUN p7zip --force --decompress ./SIM7600X-4G-HAT-Demo.7z
WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry
RUN mv c SIM7600X
WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X
RUN chmod 777 ./sim7600_4G_hat_init
RUN chmod 777 ./sim7600
RUN chmod 777 ./*.sh
#RUN make clean
#RUN make
WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/bcm2835
RUN chmod +x configure
#RUN ./configure --prefix=/root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/rootfs
RUN ./configure
RUN make clean
RUN make
RUN make install
#WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/AT
#RUN make clean
#RUN make
#WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/FTP
#RUN make clean
#RUN make
#WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/GPS
#RUN make clean
#RUN make
#WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/PhoneCall
#RUN make clean
#RUN make
#WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/SMS
#RUN make clean
#RUN make
#WORKDIR /root/SIM7600X-4G-HAT-Demo/Raspberry/SIM7600X/TCP
#RUN make clean
#RUN make

#####################
# RUNTIME CONTAINER #
#####################
# Create the runtime container for the vehicle application
# We're using the minimal ubuntu container, as it uses glibc.
# PyInstaller cannot cross-compile, so it needs to run on same OS platform
# as the build time (e.g. CPU arch, Standard C library)
FROM ubuntu

# Docker Container Annotations
# See https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.authors="leda-dev@eclipse.org"
LABEL org.opencontainers.image.url="https://github.com/eclipse-leda/leda-example-applications"
LABEL org.opencontainers.image.documentation="https://eclipse-leda.github.io/leda/"
LABEL org.opencontainers.image.source="https://github.com/eclipse-leda/leda-example-applications"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.vendor="Eclipse Foundation"
LABEL org.opencontainers.image.title="Eclipse Leda Raspberry Pi SIM7600 HAT"
LABEL org.opencontainers.image.description="Initializer container for the SIM7600 4G LTE GPS HAT"

WORKDIR /root

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends curl wget p7zip ca-certificates libqmi-utils

COPY --from=builder /root/SIM7600X-4G-HAT-Demo/Raspberry /root/SIM7600X-4G-HAT-Demo/Raspberry
ENTRYPOINT [ "/bin/bash" ]
