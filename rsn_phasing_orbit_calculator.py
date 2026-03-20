import math

def rsn_formatted_time(seconds: float) -> str:
    """
    Given a time is seconds, format it as string like

      1d, 3h, 23m, 32s

    Note that a Kerbin day is 6 hours (minutes and second are normal)

    Since this is for limited use the milliseconds are dropped off
    of the seconds (which would usually all be zero)
    """
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
    SECONDS_PER_DAY = 6 * SECONDS_PER_HOUR

    # First, and subseconds will always be part of the seconds, so
    # switch things over to integers to start
    remaining_s = math.floor(seconds)
    remaining_ms = float(seconds - float(remaining_s))

    days = remaining_s // SECONDS_PER_DAY
    remaining_s = remaining_s - (days * SECONDS_PER_DAY)

    hours = remaining_s // SECONDS_PER_HOUR
    remaining_s = remaining_s - (hours * SECONDS_PER_HOUR)

    minutes = remaining_s // SECONDS_PER_MINUTE
    remaining_s = remaining_s - (minutes * SECONDS_PER_MINUTE)

    return f"{days}d, {hours}h, {minutes}m, {remaining_s}s"

def semi_major_axis_m(standard_gravitational_parameter_m3ps2: float, period_s: float) -> float:
    """
        a = ((mu*T^2) / (4 * pi^2))^2
    """
    return (((standard_gravitational_parameter_m3ps2 * (period_s ** 2)) / (4 * (math.pi ** 2))) ** (1.0/3.0))

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
            "standard_gravitational_parameter_m3ps2": 1.7658e+10,
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
    print(f"{'Minimum RSN Altitude ':.<30}: {minimum_altitude_m:>15.5g}m")
    print(f"{'Maximum RSN Altitude ':.<30}: {maximum_altitude_m:>15.5g}m")

    #
    # OK, now, loop through all of the possible final periods for the
    # satellite network starting at 3 hours and increasing (in 3 hour
    # increments) until the apoapsis of the phasing orbit is outside
    # the sphere of influence of the body. If the altitude of the
    # satellite network would be below the minimum, do not display
    # the results.
    #
    # Note that the periapsis of the phasing orbit is always the same
    # as the altitude of the circular relay satelite orbit.
    #
    three_hours_as_seconds = 3 * 60 * 60
    rsn_period_s = three_hours_as_seconds
    apoapsis_m = 0
    option_number = 1
    while apoapsis_m < maximum_altitude_m:
        #
        # The period of the phasing orbit should be 1/3 larger than
        # the period of the final orbit ocf the satellites themselves.
        # This allows for a convienent orbital insertion burn for each
        # satellite on sucessive orbits which ends up placing them
        # 1/3 of an orbit apart from each other.
        #
        phasing_period_s = (4 / 3) * rsn_period_s

        #
        # First, calculate the _radius_ of a circular orbit at the
        # desired period. Then subtsract the radius of the body from that
        # to yield the periapsis of the phasing orbit for the desired
        # RSN period
        #
        # a = ((mu*T^2) / (4 * pi^2))^2
        #
        # a is the semi-major axis. For a circular orbit, it is the
        # radius of the orbit from the center of the body being orbited.
        #
        radius = semi_major_axis_m(body_constants["standard_gravitational_parameter_m3ps2"], rsn_period_s)
        periapsis_m = radius  - body_constants["equatorial_radius_m"]

        #
        # Now, calculate an apoapsis for an orbit with the calculated
        # periapsis that has a period equal to the phasing period. Remember
        # to subtract the radius of the body to get the altitude of the
        # apoapsis from the radius of the orbit calculated.
        #
        # TODO
        sma_m =  semi_major_axis_m(body_constants["standard_gravitational_parameter_m3ps2"], phasing_period_s)

        print("")
        print(" Option   Relay Orbit Period   Phasing Orbit Period   Periapsis   Apoapsis")
        print("======== ==================== ====================== =========== ==========")
        print(f" {option_number:>4d}     {rsn_formatted_time(rsn_period_s):>18s}   {rsn_formatted_time(phasing_period_s):>20s}   {periapsis_m:>8.6g}m")
        print(" ")
        print(f"{periapsis_m:>15.6g}m")

        # TODO - Take this out
        break

        option_number = option_number + 1


if __name__ == "__main__":
    main()
