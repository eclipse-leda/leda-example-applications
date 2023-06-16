# Seat Adjuster example application

## Overview

The Seat Adjuster setup requires:

- Eclipse Mosquitto
- Eclipse Kuksa.VAL Databroker
- Eclipse Kuksa.VAL Seat Service example
- Eclipse Velocitas Seat Adjuster example
- Eclipse Kanto Container Management
- Eclipse Leda Quickstart image

## Integration

The containers are integrated with deployment descriptors in the Leda Quickstart image.
Please see [meta-leda/meta-leda-components/recipes-sdv/eclipse-leda/kanto-containers/example](https://github.com/eclipse-leda/meta-leda/tree/main/meta-leda-components/recipes-sdv/eclipse-leda/kanto-containers/example) for details.

## Building

Mosquitto, Kuksa, Kanto and Leda have pre-built images.

This documentation is about building the Eclipse Velocitas Seat Adjuster example application
using the SDK tooling.

With cloning the repo:

```shell
git clone https://github.com/eclipse-leda/leda-example-applications.git
cd leda-example-applications/seat-adjuster
docker build .
```

Without cloning the repo:

```shell
docker build https://github.com/eclipse-leda/leda-example-applications.git#main:seat-adjuster
```

> Note: If this build fails with *subdir not supported yet*, set `export DOCKER_BUILDKIT=0` and retry.

## Leda Contributors

To build the tagged container (using Eclipse Leda image ref):

```shell
cd seat-adjuster
./build-docker.sh
```

### Cross-Building for ARM64

Set up a Docker BuildX with QEMU support to build for ARM64:

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
