import os
import logging
from time import sleep
from typing import Dict
from urllib.parse import urlparse

from retry import retry
from kuksa_client.grpc import VSSClient, VSSClientError
from kuksa_client.grpc import Datapoint

from driver import Driver

DP_BRAKE_POS = "Vehicle.Chassis.Brake.PedalPosition"  # uint8
DP_ACCELR_POS = "Vehicle.Chassis.Accelerator.PedalPosition"  # uint8
DP_STEER_ANGLE = "Vehicle.Chassis.SteeringWheel.Angle"  # int16

SIM_SPEED = float(os.environ.get("SIM_SPEED", 2))  # timeout between updates
DATABROKER_ADDRESS = os.environ.get("DATABROKER_ADDRESS", "127.0.0.1:55555")
DATABROKER_URL = urlparse(f"//{DATABROKER_ADDRESS}/")


logger = logging.getLogger("driversim")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
logging.basicConfig(level=logging.INFO)


def publish_driver_controls(driver_sim, kuksa_client):
    accelerator, brake, steering_angle = driver_sim.get_controls()
    logger.info(
        f"Sending Time={driver_sim.simulation_time} \
        Accelerator(%)={accelerator} \
        Brake(%)={brake} \
        Steering Angle (deg)={steering_angle}"
    )

    kuksa_client.set_current_values(
        {
            DP_BRAKE_POS: Datapoint(brake),
            DP_ACCELR_POS: Datapoint(accelerator),
            DP_STEER_ANGLE: Datapoint(steering_angle),
        }
    )


# global as the state should be preserved even if the databroker connection drops
driver_sim = Driver(simulation_speed=SIM_SPEED)


@retry(VSSClientError, delay=2)
def main_loop():
    # gets a new client on every loop which is not optimal,
    # but otherwise we cannot retry on databroker disconnect (raises a VSSClientError)
    with VSSClient(DATABROKER_URL.hostname, DATABROKER_URL.port) as kuksa_client:
        publish_driver_controls(driver_sim, kuksa_client)
        sleep(SIM_SPEED)


if __name__ == "__main__":
    while True:
        main_loop()
