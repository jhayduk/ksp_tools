"""
lighttime_calculator.py

Calculates the amount of time a satelite around a given body would be in
light. This can be used to calulate the size of solar panels or other
electricity generation needed

This uses the following two tools:

orbit_period_calculator.py
darkness_calcuulator.py
"""
from darkness_calculator import calculate_darkness_s
from ksp_utils import (
    get_apoapsis_and_periapsis,
    get_parent_body_name_and_constants,
)
from orbit_period_calculator import calculate_period_s
from rich import print

def calculate_lighttime_s(
    apoapsis_m: float,
    periapsis_m: float,
    parent_equatorial_radius_m: float,
    parent_standard_gravitational_parameter_m3ps2: float) -> float:
    """
    Calculate the amount of time a craft at the given orbit will be in the light.

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
            light when orbiting around the equater and ignoring eclipses.
    """
    orbital_period_s = calculate_period_s(
        apoapsis_m,
        periapsis_m,
        parent_equatorial_radius_m,
        parent_standard_gravitational_parameter_m3ps2
    )

    time_in_dark_s = calculate_darkness_s(
        apoapsis_m,
        periapsis_m,
        parent_equatorial_radius_m,
        parent_standard_gravitational_parameter_m3ps2
    )

    return orbital_period_s - time_in_dark_s

def main():
    parent_body, parent_body_constants = get_parent_body_name_and_constants()

    apoapsis_m, periapsis_m = get_apoapsis_and_periapsis(
        parent_body,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["sphere_of_influence_radius_m"]
    )

    orbital_period_s = calculate_period_s(
        apoapsis_m,
        periapsis_m,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["standard_gravitational_parameter_m3ps2"]
    )

    time_in_light_s = calculate_lighttime_s(
        apoapsis_m,
        periapsis_m,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["standard_gravitational_parameter_m3ps2"]
    )

    print(f"The time in the light is: {time_in_light_s} seconds")
    print()


if __name__ == "__main__":
    main()
