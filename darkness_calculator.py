"""
darkness_calculator.py

Calculates the amount of time a satelite around a given body would be in
darkness and in the light. This can be used to calulate the size of
battery storage needed.

This uses the calculations found on:

https://wiki.kerbalspaceprogram.com/wiki/Orbit_darkness_time

The caveats mentioned on that page all apply.
"""
import json
import math
from rich import print

def seconds_in_darkness(
    apoapsis_m: float,
    periapsis_m: float,
    parent_equatorial_radius_m: float,
    parent_standard_gravitational_parameter_m3ps2: float) -> float:
    """
    Calculate the amount of time a satellite at the given orbit will be in the dark.

    Args:
        apoapsis_m (float): The altitude above sea level of the satellite at its
            highest point in its orbit in meters
        periapsis_m (float): The altitude above sea level of the satellite at its
            lowest point in its orbit in meters
        parent_equatorial_radius_m (float): The radius, in meters, of the celestial
            body around which the satellite is orbiting
        parent_standard_gravitational_parameter_m3ps2 (float): The gravitational
            constant (i.e. µ), in meters^3 / s^2, of the celestial
            body around which the satellite is orbiting

    Returns:
        float: The amount of time, in seconds that the satellite would be in the
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


def _get_apoapsis_and_periapsis(parent_body_name: str, parent_body_constants: dict) -> tuple[float, float]:
    """
    Gets, from the user, the planned apopasis and periapsis of the satellite
    for which the calculations are being made. Both are measured from sea level,
    as they would appear on the maneuver and altitude displays, and both must
    be within the sphere of influence (SOI) of the parent body.

    These are returned as a tuple of (apopasis, periapsis)
    """
    calculated_values = {
        "apoapsis": None,
        "periapsis": None
    }

    #
    # The spehere of influence (SOI) of the parenet body is recorded from the center
    # of the body. Subtract the radius of the body, so the result can be used
    # in a couple of checks.
    #
    soi_without_radius_m = parent_body_constants["sphere_of_influence_radius_m"] - parent_body_constants["equatorial_radius_m"]

    for apsis in calculated_values:
        got_valid_value = False
        while not got_valid_value:
            try:
                calculated_values[apsis] = float(input(f"Planned {apsis} of satellite (from sea level, in meters): "))
                if calculated_values[apsis] > soi_without_radius_m:
                    print(f"[yellow]The {apsis} must be be within {parent_body_name}'s SOI ({soi_without_radius_m}m)")
                else:
                    got_valid_value = True
            except (ValueError, KeyError) as err:
                print(f"{repr(err)}")

    return calculated_values["apoapsis"], calculated_values["periapsis"]


def main():
    #
    # First, read in the body constants and then extract the names of the
    # bodies listed in it.
    #
    with open('body_constants.json', 'r') as file:
        all_body_constants = json.load(file)
    known_bodies = list(all_body_constants)

    #
    # Get the name of the parent body.
    # Keep asking until a valid choice is made.
    #
    got_valid_value = False
    body_constants = {}
    print()
    while not got_valid_value:
        print(f"Known celestial bodies are: {known_bodies}")
        print()
        try:
            parent_body = input("Type the name of body the satellite will be orbiting: ").lower()
            if parent_body in known_bodies:
                parent_body_constants = all_body_constants[parent_body]
                got_valid_value = True
            else:
                print()
                print(f"[yellow]Unknown parent body name: {parent_body}")
                print()
        except (ValueError, KeyError) as err:
            print(f"{repr(err)}")

    apoapsis_m, periapsis_m = _get_apoapsis_and_periapsis(parent_body, parent_body_constants)

    time_in_dark_s = seconds_in_darkness(
        apoapsis_m,
        periapsis_m,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["standard_gravitational_parameter_m3ps2"]
    )

    print(f"The time in the dark is: {math.ceil(time_in_dark_s)} seconds")
    print()

if __name__ == "__main__":
    main()
