"""
inclination_change_delta_v_cost_calculator.py

Calculates the delata_v cost, in meters per (mps), to make the
desired inclination change at the altitude specified while in the
given orbit around the given body.

It is assumed that a normal (or anti-normal) burn is being made at
either the ascending or descending node of the orbit.
"""
import json
from ksp_utils import (
    get_altitude,
    get_apoapsis_and_periapsis,
    get_parent_body_name_and_constants,
)
import math
from orbital_velocity_calculator import obital_velocity_mps
from rich import print


def inclination_change_delta_v_cost_mps(
        parent_body_name,
        apoapsis_m,
        periapsis_m,
        altitude_m,
        angle_change_degrees,
):
    """
    Calculate the delat_v cost (in meters per second, mps), of an inclination
    change of the given angle while at the specified altitude in the given orbit
    around the specified celestial body.

    Reference: https://orbital-mechanics.space/orbital-maneuvers/plane-change-maneuvers.html#equation-eq-plane-change-delta-v-pure-rotation
    """
    # Normalize the angle to 360 degrees and convert to radians for use with the math library
    angle_change_radians = math.radians(angle_change_degrees % 360.0)

    orbital_velocity_mps = obital_velocity_mps(parent_body_name, apoapsis_m, periapsis_m, altitude_m)

    return (2 * orbital_velocity_mps * math.sin(angle_change_radians / 2) )


def main():

    parent_body_name, parent_body_constants = get_parent_body_name_and_constants()

    apoapsis_m, periapsis_m = get_apoapsis_and_periapsis(parent_body_name)

    altitude_m = get_altitude(parent_body_name)

    # Get the deflection in degrees
    change_angle_degrees = float(input("Enter amount of inclination change as an angle expressed in degrees: "))

    delta_v_cost_mps = inclination_change_delta_v_cost_mps(
        parent_body_name,
        apoapsis_m,
        periapsis_m,
        altitude_m,
        change_angle_degrees
    )

    print(f"The cost is {delta_v_cost_mps:,} m/s")


if __name__ == "__main__":
    main()
