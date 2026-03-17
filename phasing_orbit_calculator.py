def main():
    print("Hello from ksp-tools!")


if __name__ == "__main__":
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
    main()