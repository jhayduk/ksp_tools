"""
orbit_period_calculator.py

Calulates the period, in seconds, of an orbit around a given body.

This uses the calculations found on:

https://forum.kerbalspaceprogram.com/topic/203611-how-to-determine-the-orbital-period/
"""
import json
from ksp_utils import (
    get_apoapsis_and_periapsis,
    get_parent_body_name_and_constants,
    ksp_formatted_time,
)
import math
from rich import print

def calculate_period_s(
    apoapsis_m: float,
    periapsis_m: float,
    parent_equatorial_radius_m: float,
    parent_standard_gravitational_parameter_m3ps2: float) -> float:
    """
    Calculate the orbital period of a craft given its orbit's asides

    Args:
        apoapsis_m (float): The altitude above sea level of the craft at its
            highest point in its orbit in meters
        periapsis_m (float): The altitude above sea level of the craft at its
            lowest point in its orbit in meters
        parent_equatorial_radius_m (float): The radius, in meters, of the celestial
            body around which the craft is orbiting
        parent_standard_gravitational_parameter_m3ps2 (float): The gravitational
            constant (i.e. µ), in meters^3 / s^2, of the celestial
            body around which the craft is orbiting

    Returns:
        float: The orbital period, in seconds, that the craft will have around
            the parent body
    """
    # The radius of the parent body
    R = parent_equatorial_radius_m

    # The apoapsis measured from the center of the body
    r_a = apoapsis_m + R

    # The periapsis measured from the center of the body
    r_p = periapsis_m + R

    # The semi-major axis
    a = (r_a + r_p) / 2

    # The gravitational parameter
    mu = parent_standard_gravitational_parameter_m3ps2

    # The period
    T = 2 * math.pi * math.sqrt((a ** 3) / mu)

    return T


def main():

    parent_body_name, parent_body_constants = get_parent_body_name_and_constants()

    apoapsis_m, periapsis_m = get_apoapsis_and_periapsis(parent_body_name)

    orbital_period_s = calculate_period_s(
        apoapsis_m,
        periapsis_m,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["standard_gravitational_parameter_m3ps2"]
    )

    print(f"The period is: {orbital_period_s:.2f} seconds ({ksp_formatted_time(orbital_period_s)})")
    print()

if __name__ == "__main__":
    main()
