def semi_major_axis_m(periapsis_m: float, apoapsis_m: float, equatorial_radius_of_body_m : float) -> float:
    """
    Given the periapis and apoapsis of and orbit (Pe and Ap respectively), and
    the radius of the body around which that orbit exists (r), return the 
    semi-major axis if that orbit. All values are in meters.
    Note that the peripsis and apoapsis is as displayed in the game and is
    the altitude above "sea level" (which is the same as the equitorial radius
    of the body). That is what the radius is needed in this function.
    """
    return  (
                (periapsis_m + equatorial_radius_of_body_m) +
                (apoapsis_m + equatorial_radius_of_body_m)
            ) / 2

def sphere_of_influence_kg(semi_major_axis_of_orbit_m : float, mass_of_body_kg: float, mass_of_parent_body_kg: float) -> float:
    """
    The radius of the sphere around a given body where its gravitational
    influence is more than that of the parent body. In KSP, only the
    one extra body of the parent is considered.

    Reference:
        https://wiki.kerbalspaceprogram.com/wiki/Sphere_of_influence
    """
    return semi_major_axis_of_orbit_m * (mass_of_body_kg / mass_of_parent_body_kg)^2/5 # TBD - In progress...

def main():
    """
    Given the properties of a celestial body in KSP, calculate all of the
    viable options for the periapsis (pe) and apoapsis (ap) of a phasing
    orbit suitable for placing three relay satellites in orbit around the
    body so that they are equidistant from each other.

    This means that the period of an orbit using that periapsis and apoapsis
    is 1/3 longer than a circular orbit at the altitude of the periapsis.
    To keep the period as an easy to target value, only circular orbits with
    a period that is a multiple of 10,800 seconds (3 hours) are considered.

    To be valid, the orbit must be such that each satellite has line of sight
    with the other two satellites at all times. This means that a line between
    each satellite must always be higher that the highest mountaintop on the
    given body.

    Additionally, the altitude of the orbit must be within the sphere of
    influence (SOI) of the given body to be a valid option.

    At the moment, the utility asks for the values of constants as well as
    the name of the body. As the tool is used, it will record the values
    entered and use those as defaults the next time the same body is
    used.
    """

    constants = {
        "kerbin": {
            "mass_kg": 5.2915158e22
        },
        "minmus": {
            "apoapsis_m": 47000000,
            "equatorial_radius_m": 60000,
            "mass_kg": 2.6457580e+19,
            "orbits": "kerbin",
            "periapsis_m": 47000000,
            "semi_major_axis_of_orbit_m": 47000000
        }
    }
    body = "minmus"
    sma =  semi_major_axis_m(
        periapsis_m=constants["minmus"]["periapsis_m"] - constants["minmus"]["equatorial_radius_m"],
        apoapsis_m=constants["minmus"]["periapsis_m"] - constants["minmus"]["equatorial_radius_m"],
        equatorial_radius_of_body_m=constants["minmus"]["equatorial_radius_m"]
    )
    print(f"{'Body ':.<30}: {body.capitalize()}")
    print(f"{'Maximum altitude ':.<30}:")
    msg=f"Semi-Major Axis ({body.capitalize()}) "
    print(f"{msg:.<30}: {sma} meters")


if __name__ == "__main__":
    main()
