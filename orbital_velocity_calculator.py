"""
    orbital_velocity_calculator.py

    Calculates the velocity of an orbit around the specified body given the
    apoapsis, periapsis and the altitude of the orbit.
"""
from ksp_utils import (
    add_radius,
    get_altitude,
    get_apoapsis_and_periapsis,
    get_celestial_body_constants,
    get_parent_body_name_and_constants,
    semi_major_axis_radius_m,
)
from lighttime_calculator import calculate_lighttime_s
import math
from rich import print


def obital_velocity_mps(
        parent_body_name: str,
        apoapsis_m: float,
        periapsis_m: float,
        altitude_m: float,
) -> float:
    """
    Given the apoaspis and periapsis of an orbit around a given celestial body, in meters
    above seal level for that body, return the orbital velocity, in meters per second (mps),
    of an object at the altitude spectific (in meters, also above sea level for the parent
    body).

    This is done using the "vis-viva equation" (https://en.wikipedia.org/wiki/Vis-viva_equation)

    Note that the altitude must be on the orbit specified by the apapsis and periapsis
    (i.e., it must be between those two values, inclusive).
    """
    if (altitude_m < periapsis_m or altitude_m > apoapsis_m) and not (math.isclose(altitude_m, periapsis_m) or math.isclose(altitude_m, apoapsis_m)):
        raise ValueError(f"The given altitude is not on the orbit because it is not >= periapsis and <= apoapsis")


    parent_body_constants = get_celestial_body_constants(parent_body_name)

    mu = parent_body_constants["standard_gravitational_parameter_m3ps2"]
    r = add_radius(parent_body_name, altitude_m)
    a = semi_major_axis_radius_m(parent_body_name, apoapsis_m, periapsis_m)

    return math.sqrt(mu * ((2/r) - (1/a)))


def main():
    parent_body_name, _ = get_parent_body_name_and_constants()

    apoapsis_m, periapsis_m = get_apoapsis_and_periapsis(parent_body_name)

    altitude_m = get_altitude(parent_body_name)

    velocity_mps = obital_velocity_mps(parent_body_name, apoapsis_m, periapsis_m, altitude_m)

    print(f"DEBUG: The velocity is {velocity_mps:,} m/s")


if __name__ == "__main__":
    main()
