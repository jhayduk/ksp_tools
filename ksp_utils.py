"""
ksp_ utils.py

A collection of miscellaneous utility functions in support of the ksp tools.
"""
import json
from rich import print

def get_apoapsis_and_periapsis(
        parent_body_name: str,
        parent_equatorial_radius_m: float,
        parent_sphere_of_influence_radius_m: float) -> tuple[float, float]:
    """
    Gets, from the user, the apopasis and periapsis of a craft for which the
    calculations are being made. Both apsides are measured from sea level,
    as they would appear on the maneuver and altitude displays, and both must
    be within the sphere of influence (SOI) of the parent body.

    Args:
      parent_body_name (str): The name of the celestial body will be orbiting
        around. This is only used for prompts and error messages.
      parent_equatorial_radius_m (float): The radius, in meters, of the celestial
          body around which the craft is orbiting
      parent_sphere_of_influence_radius_m (float): The sphere of influence (SOI), in meters,
          of the celestial body around which the craft is orbiting. Both apsides
          must be within the parent body's SOI to be valid.

    Returns:
        (apoapsis_m: float, periapsis_m: float) The apoapsis and periapsis, in meters,
          as measured from the sea level of the parent body.
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
    soi_without_radius_m = parent_sphere_of_influence_radius_m - parent_equatorial_radius_m

    for apsis in calculated_values:
        got_valid_value = False
        while not got_valid_value:
            try:
                calculated_values[apsis] = float(input(f"Planned {apsis} of craft (from sea level, in meters): "))
                if calculated_values[apsis] > soi_without_radius_m:
                    print(f"[yellow]The {apsis} must be be within {parent_body_name}'s SOI ({soi_without_radius_m}m)")
                else:
                    got_valid_value = True
            except (ValueError, KeyError) as err:
                print(f"{repr(err)}")

    return calculated_values["apoapsis"], calculated_values["periapsis"]


def get_parent_body_name_and_contstants() -> tuple[str, dict]:
    """
    Gets, from the user, the name of the celestial body that the craft is,
    or will be, orbiting around and returns the name and its constants.
    The name will have its first letter capitalized, and it msut be known
    to the system.
    """
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
    print()
    while not got_valid_value:
        print(f"Known celestial bodies are: {known_bodies}")
        print()
        try:
            parent_body = input("Type the name of body the craft is/will be orbiting: ").capitalize()
            if parent_body in known_bodies:
                parent_body_constants = all_body_constants[parent_body]
                got_valid_value = True
            else:
                print()
                print(f"[yellow]Unknown parent body name: {parent_body}")
                print()
        except (ValueError, KeyError) as err:
            print(f"{repr(err)}")

    return parent_body, parent_body_constants


def ksp_formatted_time(seconds: int | float) -> str:
    """
    Given a time is seconds, format it as string like

      1d, 3h, 23m, 32s

    Note that a Kerbin day is 6 hours (minutes and second are normal)

    Milliseconds are rounded to the nearest second.
    """
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
    SECONDS_PER_DAY = 6 * SECONDS_PER_HOUR

    # First, any subseconds will always be part of the seconds, so
    # switch things over to integers to start
    remaining_s = round(seconds)

    days = remaining_s // SECONDS_PER_DAY
    remaining_s = remaining_s - (days * SECONDS_PER_DAY)

    hours = remaining_s // SECONDS_PER_HOUR
    remaining_s = remaining_s - (hours * SECONDS_PER_HOUR)

    minutes = remaining_s // SECONDS_PER_MINUTE
    remaining_s = remaining_s - (minutes * SECONDS_PER_MINUTE)

    return f"{days}d, {hours}h, {minutes}m, {remaining_s}s"