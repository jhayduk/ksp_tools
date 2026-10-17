"""
ksp_ utils.py

A collection of miscellaneous utility functions in support of the ksp tools.
"""
from enum import Enum
from functools import cache
import json
from rich import print

class Apsis(Enum):
    APOAPSIS = "apoapsis"
    PERIAPSIS = "periapsis"

def add_radius(parent_body_name: str, altitude_above_sea_level_m: float) -> float:
    """
    Given the name of a celestial body and an altitude above "sea level" of that
    body as it would appear on the maneuver and altitude displays, return the
    same altitude expressed as a distance from the center of the body. In other
    words, with the radius of the body added to it.

    This function assumes that the body name is valid and will throw
    a ValueError exception if it is not (because the function it calls will throw
    an exception).

    This function allows altitude_above_sea_level_m to be negative to allow it to
    be used in valeys and ravines on the surface, but will raise a ValueError
    exception if it is so low that it is actually past the center of the parent
    body as this would be invalid. This is to help catch compound calculation
    errors early.
    """
    body_constants = get_celestial_body_constants(parent_body_name)

    if altitude_above_sea_level_m < - body_constants["equatorial_radius_m"]:
        raise ValueError(f"The passed in altitude_above_sea_level_m of {altitude_above_sea_level_m} m would place it on the other side of the center of {parent_body_name}, and is, therefore, considered invalid.")

    return altitude_above_sea_level_m + body_constants["equatorial_radius_m"]


def get_apsis(
    apsis: Apsis,
    parent_body_name: str,
    parent_equatorial_radius_m: float,
    parent_sphere_of_influence_radius_m: float  
) -> float:
    """
    Gets, from the user, the apsis (apoasis or periapsis) of a craft for
    which the calculations are being made. This is measured from sea level,
    as it would appear on the maneuver and altitude displays, and must be
    within the sphere of influence (SOI) of the parent body.

    Args:
      apsis (Apis): Either "apoapsis" or "periapsis". Specifies which of the
        two values to obtain from the user.
      parent_body_name (str): The name of the celestial body will be orbiting
        around. This is only used for prompts and error messages.
      parent_equatorial_radius_m (float): The radius, in meters, of the celestial
          body around which the craft is orbiting
      parent_sphere_of_influence_radius_m (float): The sphere of influence (SOI), in meters,
          of the celestial body around which the craft is orbiting. Both apsides
          must be within the parent body's SOI to be valid.

    Returns:
        apsis_m: float The apoapsis or periapsis, in meters, as measured
        from sea level of the parent body.
    """
    #
    # The spehere of influence (SOI) of the parenet body is recorded from the center
    # of the body. Subtract the radius of the body, so the result can be used
    # for checking.
    #
    soi_without_radius_m = parent_sphere_of_influence_radius_m - parent_equatorial_radius_m

    got_valid_value = False
    while not got_valid_value:
        try:
            apsis_m = float(input(f"Planned {apsis.value} of craft (from sea level, in meters): "))
            if apsis_m > soi_without_radius_m:
                print(f"[yellow]The {apsis.value} must be be within {parent_body_name}'s SOI ({soi_without_radius_m}m)")
            else:
                got_valid_value = True
        except (ValueError, KeyError) as err:
            print(f"{repr(err)}")

    return apsis_m

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
    calculated_values: dict[Apsis, float] = {}

    for apsis in (Apsis.APOAPSIS, Apsis.PERIAPSIS):
        calculated_values[apsis] = get_apsis(
            apsis,
            parent_body_name,
            parent_equatorial_radius_m,
            parent_sphere_of_influence_radius_m
        )

    return calculated_values[Apsis.APOAPSIS], calculated_values[Apsis.PERIAPSIS]


@cache
def get_celestial_body_constants(parent_body_name: str) -> dict:
    """
    Given the name of a celestial body, return the constants for that body.

    This function is cached, so it is safe to call it multiple times even though
    it gets the constants from a file.

    This utility assumes that the body name is valid and will throw
    a ValueError exception if it is not.
    """
    if not is_known_celestial_body(parent_body_name):
        raise ValueError(f"{parent_body_name} was not found in the body_constants.json file. It is not aknown celestial body.")

    with open('body_constants.json', 'r') as file:
        all_body_constants = json.load(file)

    return all_body_constants[parent_body_name]


def get_parent_body_name_and_constants() -> tuple[str, dict]:
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
                parent_body_constants = get_celestial_body_constants(parent_body)
                got_valid_value = True
            else:
                print()
                print(f"[yellow]Unknown parent body name: {parent_body}")
                print()
        except (ValueError, KeyError) as err:
            print(f"{repr(err)}")

    return parent_body, parent_body_constants

@cache
def is_known_celestial_body(celestial_body_name: str) -> bool:
    """
    Returns True if the given celestial body is in the body_constants.json
    file, and False otherwise.

    This function is cached, so it is safe to call it multiple times even though
    it gets the constants from a file.

    Body names are nromalized to capitalized before checking
    """
    with open('body_constants.json', 'r') as file:
        all_body_constants = json.load(file)
    return celestial_body_name.capitalize() in list(all_body_constants)


def is_moon(celestial_body_name: str) -> bool:
    """
    Returns True if the given celestial body is a moon, and False otherwise.

    This is determined by looking at the given body's parent in the
    body_constants.json file. If the parent is Kerbol (i.e. the Sun), then
    it is considered a planet, otherwise, it is considered a moon.
    """
    with open('body_constants.json', 'r') as file:
        all_body_constants = json.load(file)

    if is_known_celestial_body(celestial_body_name):
        return all_body_constants[celestial_body_name]["parent_body"] != "Kerbol"
    else:
        raise ValueError(f"{celestial_body_name} is not a known celestial body")

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


def subtract_radius(parent_body_name: str, object_radius_from_parent_center_m: float) -> float:
    """
    Given the name of a celestial body and the distance above the center of that
    body return the same altitude expressed as the distance above "sea level" of
    that body as it would appear on the maneuver and altitude displays. In other
    words, with the radius of the body subtracted from it.

    This utility assumes that the body name is valid and will throw
    a ValueError exception if it is not (because the function it calls will throw
    an exception).

    Additionally, this function will throw a ValueError exception if the passed in
    object_radius_from_parent_center_m is negative as this will result in an invalid
    altitude.
    """
    body_constants = get_celestial_body_constants(parent_body_name)

    if object_radius_from_parent_center_m < 0:
        raise ValueError(f"The passed in object_radius_from_parent_center_m value of {object_radius_from_parent_center_m} m cannot be less than 0.")

    altitude_above_sea_level_m = object_radius_from_parent_center_m - body_constants["equatorial_radius_m"]

    return altitude_above_sea_level_m
