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
            "semi_major_axis_of_orbit_m": 47000000,
            "tallest_mountain_m": 5724.6
        }
    }

    #
    # Select the body around which the relay satellite network will be place.
    #
    # TODO: This is hardcoded for now, but would be input inn the console
    # or with a parameter.
    #
    body = "minmus"
    body_constants = constants[body]

    #
    # The minumum altitude for the each satellite in the network is slightly
    # cumbersome to calculate only because you do want to make sure that you
    # clear any mountains so that line of sight is always guaranteed. So,
    # instead of using the radius of the body, you need to also add the
    # height of the tallest mountain.
    #
    # Then the equation is (all in meters):
    #
    #            mountain_height + radius
    #  min_alt = ------------------------  -  radius
    #                 cos 60 degrees
    #
    # or min_alt = (2 * (mountain_height + radius)) - radius
    #
    minimum_altitude_m = (2 * (body_constants["tallest_mountain_m"] + body_constants["equatorial_radius_m"])) - body_constants["equatorial_radius_m"]
 
    #
    # The maximum altitude for each satelite is at the enge of the body's
    # sphere of influence. Ideally, you do not want to be right at that
    # value.
    #
    maximum_altitude_m = body_constants["semi_major_axis_of_orbit_m"] - body_constants["equatorial_radius_m"]

    #
    # Display the results
    #
    print(f"{'Body ':.<30}: {body.capitalize():>17}")
    print(f"{'Minimum RSN Altitude ':.<30}: {minimum_altitude_m:>15.5g} m")
    print(f"{'Maximum RSN Altitude ':.<30}: {maximum_altitude_m:>15.5g} m")

if __name__ == "__main__":
    main()
