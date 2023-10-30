# Node-RED example application

## Overview

The Node-RED setup requires:

- Eclipse Mosquitto
- Eclipse Kuksa.VAL Databroker
- Eclipse Kuksa.VAL Seat Service example
- Eclipse Velocitas Seat Adjuster example
- Eclipse Kanto Container Management
- Eclipse Leda Quickstart image

## Integration

The containers are integrated with deployment descriptors in the Leda Quickstart image.
Please see [meta-leda/meta-leda-components/recipes-sdv/eclipse-leda/kanto-containers/example](https://github.com/eclipse-leda/meta-leda/tree/main/meta-leda-components/recipes-sdv/eclipse-leda/kanto-containers/example) for details.

## Usage

You can access the graphical user interface with any web browser on the port 1880, e.g. http://leda-host:1880/.
The generated dashboard is available on http://leda-host:1880/ui/.

Describing how to use the UI is out of the scope of this document. Please consult the excellent [Node-RED documentation](https://nodered.org/docs/).

## Data sources

To make full use of the dashboard example you have to feed some data into the system.
If you don't have real data, some possible sources could be:

- [Kuksa CarSim](../kuksa-carsim/)
- [FeederGPS](https://eclipse-leda.github.io/leda/docs/general-usage/gps-configuration/)
