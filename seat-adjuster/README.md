# Seat Adjuster example application

## Overview

The Seat Adjuster setup requires:

- Eclipse Mosquitto
- Eclipse Kuksa.VAL Databroker
- Eclipse Kuksa.VAL Seat Service example
- Eclipse Velocitas Seat Adjuster example
- Eclipse Kanto Container Management
- Eclipse Leda Quickstart image

## Building

Mosquitto, Kuksa, Kanto and Leda have pre-built images.

This documentation is about building the Eclipse Velocitas Seat Adjuster example application
using the SDK tooling.

```shell
docker build https://github.com/eclipse-leda/leda-example-applications.git#main:seat-adjuster
```


```shell
cd seat-adjuster
./build-docker.sh
```

### Cross-Building for ARM64

Set up a Docker BuildX with QEMU support:

```shell
sudo apt-get install -y qemu-user-static
sudo apt-get install -y binfmt-support
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx rm ledabuilder
docker buildx create --name ledabuilder --use
```

Run the build:

```shell
./build-multiarch.sh
```
