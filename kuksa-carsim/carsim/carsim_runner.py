import os
import logging
from time import sleep
from typing import Dict
from urllib.parse import urlparse

import numpy as np
from retry import retry
from kuksa_client.grpc import VSSClient, VSSClientError
from kuksa_client.grpc import Datapoint

from carsim import SimulatedCar


DP_SPEED = "Vehicle.Speed"  # float
DP_ACCEL_LAT = "Vehicle.Acceleration.Lateral"  # float
DP_ACCEL_LONG = "Vehicle.Acceleration.Longitudinal"  # float
DP_ACCEL_VERT = "Vehicle.Acceleration.Vertical"  # float

DP_BRAKE_POS = "Vehicle.Chassis.Brake.PedalPosition"  # uint8
DP_ACCELR_POS = "Vehicle.Chassis.Accelerator.PedalPosition"  # uint8
DP_STEER_ANGLE = "Vehicle.Chassis.SteeringWheel.Angle"  # int16


SIM_SPEED = float(os.environ.get("SIM_SPEED", 2))  # timeout between updates
DATABROKER_ADDRESS = os.environ.get("DATABROKER_ADDRESS", "127.0.0.1:55555")
DATABROKER_URL = urlparse(f"//{DATABROKER_ADDRESS}/")


logger = logging.getLogger("carsim")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
logging.basicConfig(level=logging.INFO)


def update_model_controls(car: SimulatedCar, controls_state: Dict[str, Datapoint]):
    if controls_state[DP_BRAKE_POS]:
        car.brake_position = controls_state[DP_BRAKE_POS].value / 100  # percent

    if controls_state[DP_ACCELR_POS]:
        car.accelerator_position = controls_state[DP_ACCELR_POS].value / 100  # percent

    if controls_state[DP_STEER_ANGLE]:
        car.steer_angle = (
            controls_state[DP_STEER_ANGLE].value * np.pi / 180  # deg to rad
        )


def publish_model_state(car: SimulatedCar, kuksa_client: VSSClient) -> None:
    logger.debug(f"Car State: {car_sim.__dict__}")
    logger.info(
        f"Time={car.simul_time}\
            Speed={car.speed * 3.6} km/h\
            Acceleration (Long)={car.acceleration[0]} m/s^2\
            Acceleration (Lat)={car.acceleration[1]} m/s^2 \
            Steering angle (deg)={car.steer_angle*180/np.pi}"
    )
    kuksa_client.set_current_values(
        {
            DP_SPEED: Datapoint(car.speed * 3.6),  # 1 m/s = 3.6 km/h
            DP_ACCEL_LONG: Datapoint(car.acceleration[0]),  # m/s^2
            DP_ACCEL_LAT: Datapoint(car.acceleration[1]),  # m/s^2
            DP_ACCEL_VERT: Datapoint(0.0),  # m/s^2
        }
    )


# global as the state should be preserved even if the databroker connection drops
car_sim = SimulatedCar(simulation_step=SIM_SPEED)


@retry(VSSClientError, delay=2)
def main_loop():
    # gets a new client on every loop which is not optimal,
    # but otherwise we cannot retry on databroker disconnect (raises a VSSClientError)
    with VSSClient(DATABROKER_URL.hostname, DATABROKER_URL.port) as kuksa_client:
        controls_state = kuksa_client.get_current_values(
            [DP_BRAKE_POS, DP_ACCELR_POS, DP_STEER_ANGLE]
        )
        update_model_controls(car_sim, controls_state)
        car_sim.update_car()
        publish_model_state(car_sim, kuksa_client)
        sleep(SIM_SPEED)


if __name__ == "__main__":
    while True:
        main_loop()
