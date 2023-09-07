[![Build](https://github.com/eclipse-leda/leda-example-applications/actions/workflows/build.yml/badge.svg)](https://github.com/eclipse-leda/leda-example-applications/actions/workflows/build.yml)
[![CodeQL](https://github.com/eclipse-leda/leda-example-applications/workflows/CodeQL/badge.svg)](https://github.com/eclipse-leda/leda-example-applications/actions?query=workflow%3ACodeQL)

<img src="https://eclipse-leda.github.io/leda/assets/eclipse-leda.png" height="150">

# Eclipse Leda Incubator - Example Vehicle Applications

## Usage

These example applications are provided as Docker containers.

The containers are meant to be used in Eclipse Leda quickstart image, which contains default container deployments descriptors for these examples.
Please see [meta-leda/meta-leda-components/recipes-sdv/eclipse-leda/kanto-containers/example](https://github.com/eclipse-leda/meta-leda/tree/main/meta-leda-components/recipes-sdv/eclipse-leda/kanto-containers/example) for details.

However, it is possible to run the containers also in a standalone environment using Docker or other OCI compliant container runtimes.
The environment has to be adapted accordingly, e.g. external dependencies need to be installed or run in Docker and configured.

**General Runtime Requirements:**

Most of the applications are supposed to run in the Leda environment. If you want to run the examples standalone, the following services and configuration must be provided externally:

- Kuksa.VAL [Databroker](https://github.com/eclipse/kuksa.val/tree/master/kuksa_databroker) running on `databroker:55555`
- Eclipse Mosquitto running on `mosquitto:1883` with `allow_anonymous: true`

Please see the respective README in the example folders for specifics.

## Contents

### Seat Adjuster

The **[Seat Adjuster](seat-adjuster/)** example is an [Eclipse Velocitas](https://github.com/eclipse-velocitas) vehicle application,
interacting with an [Eclipse Kuksa.VAL](https://github.com/eclipse/kuksa.val) Vehicle Abstraction Layer (Databroker)
to control the position of the **driver seat**. Actual implementation for the latter is a CAN-Bus-based *vehicle service* implementation
as part of the [Kuksa.VAL Services examples](https://github.com/eclipse/kuksa.val.services/tree/main/seat_service).

### Kuksa CarSim

The **[Kuksa CarSim](kuksa-carsim)** example is based on [Kuksa.VAL Services](https://github.com/eclipse/kuksa.val.services/tree/main).
It provides simulated physical motion telemetry of a moving vehicle to the [Databroker](https://github.com/eclipse/kuksa.val/tree/master/kuksa_databroker).
The databroker is an in-vehicle, in-memory database for signal information. Signal formats are standardized in the [Vehicle Signal Specification](https://github.com/COVESA/vehicle_signal_specification).

### Node-RED

*... TODO ...*

## Contributing

If you want to contribute bug reports or feature requests, please use *GitHub Issues*.
For reporting security vulnerabilities, please follow our [security guideline](https://eclipse-leda.github.io/leda/docs/project-info/security/).

## License and Copyright

This program and the accompanying materials are made available under the
terms of the Apache License 2.0 which is available at
https://www.apache.org/licenses/LICENSE-2.0

For details, please see our license [NOTICE](NOTICE.md)
