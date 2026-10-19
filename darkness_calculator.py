"""
darkness_calculator.py

Calculates the amount of time a craft around a given body would be in
darkness and in the light. This can be used to calulate the size of
battery storage needed.

This uses the calculations found on:

https://wiki.kerbalspaceprogram.com/wiki/Orbit_darkness_time

The caveats mentioned on that page all apply.
"""
from ksp_utils import (
    get_apoapsis_and_periapsis,
    get_parent_body_name_and_constants,
)
import math
from rich import print

def calculate_darkness_s(
    apoapsis_m: float,
    periapsis_m: float,
    parent_equatorial_radius_m: float,
    parent_standard_gravitational_parameter_m3ps2: float) -> float:
    """
    Calculate the amount of time a craft at the given orbit will be in the dark.

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
        float: The amount of time, in seconds that the craft would be in the
            dark when orbiting around the equater and ignoring eclipses.
    """
    # The radius of the parent body
    R = parent_equatorial_radius_m

    # The apoapsis measured from the center of the body
    r_a = apoapsis_m + R

    # The periapsis measured from the center of the body
    r_p = periapsis_m + R

    # The semi-major axis
    a = (r_a + r_p) / 2

    # The semi-minor axis
    b = math.sqrt(r_a * r_p)

    # The eccentricity
    e = (r_a - r_p) / (r_a + r_p)

    # The semi-latus rectum of the orbital ellipse
    l = (2 * r_a * r_p) / (r_a + r_p)

    # The gravitational parameter
    mu = parent_standard_gravitational_parameter_m3ps2

    # The specific angular momentum
    h = math.sqrt(l * mu)

    # The time in the dark
    t_d = ((2 * a * b) / h) * (math.asin(R / b) + ((e * R) / b) )

    return t_d


def main():
    parent_body_name, parent_body_constants = get_parent_body_name_and_constants()

    apoapsis_m, periapsis_m = get_apoapsis_and_periapsis(parent_body_name)

    time_in_dark_s = calculate_darkness_s(
        apoapsis_m,
        periapsis_m,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["standard_gravitational_parameter_m3ps2"]
    )

    print(f"The time in the dark is: {time_in_dark_s} seconds")
    print()

if __name__ == "__main__":
    main()
