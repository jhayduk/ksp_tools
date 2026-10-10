"""
solar_panel_efficiency_calculator.py

    Calcluates an efficiency factor for solar panels to account for their
    distance from the Sun.

    Given the max distance of a parent body upon or around which a solar
    panel is placed, the equatorial radius of that same parent body, and the
    aposapsis of the craft containing the solar panel (or the alititude on
    the surface where the panel is placed), returns an efficiency factor
    that can be multiplied to the expected EC generation value to adjust it
    for its distance from the Sun (Kerbol).

    This is calculated as the ratio of the square of the distance Kerbin is
    from the Sun and the square of the furthest distance the panel can be from the Sun.
    
    Note that the calculation assumes full exposure.
"""
from ksp_utils import (
    get_apoapsis_and_periapsis,
    get_parent_body_name_and_constants,
)
from lighttime_calculator import calculate_lighttime_s
from rich import print

def main():
    parent_body, parent_body_constants = get_parent_body_name_and_constants()

    apoapsis_m, periapsis_m = get_apoapsis_and_periapsis(
        parent_body,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["sphere_of_influence_radius_m"]
    )

    print()
    print("Continuous electrical consumption is usually used by probes, lights,")
    print("and the science lab. If there are one or more science labs, that usually")
    print("far outweighs any probles or lights.")
    print()
    continuous_consumption_ecps = float(input("Total continuous electrical consumption, in EC/s: "))

    print()
    print("One time, or discrete, electrical consumption is usually for things")
    print("like transmitting science. This goes towards the minimum amount of")
    print("battery storage needed. The tool assumes that since this is infrequent,")
    print("you probably have a choice of when to do it, and can do it only during the")
    print("time when the craft is in the light and has time to charge back up before")
    print("before going into darkness.")
    print("If none are expected, a value of 0 can be entered.")
    print()
    discrete_consumpution_ec = float(input("Largest discrete electrical consumption in EC: "))

    #
    # Now, the amount of storage required is the greater of the discrete consumption
    # amount, or the continuous amount for the time the craft is in the dark.
    #
    time_in_dark_s = calculate_darkness_s(
        apoapsis_m,
        periapsis_m,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["standard_gravitational_parameter_m3ps2"]
    )

    continuous_consumption_ec = continuous_consumption_ecps * time_in_dark_s

    storage_required_ec = max(discrete_consumpution_ec, continuous_consumption_ec)

    #
    # With the storage required calculated, the amount of generation required
    # is the amount that is enough to support the continuous consumption, as
    # well as fully re-charge the storage while the craft is in the light.
    #
    time_in_light_s = calculate_lighttime_s(
        apoapsis_m,
        periapsis_m,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["standard_gravitational_parameter_m3ps2"]
    )

    recharge_required_ecps = storage_required_ec / time_in_light_s

    panel_efficiency_factor = solar_panel_efficiency(
        parent_body_constants["apoapsis_from_parent_center_m"],
        parent_body_constants["equatorial_radius_m"],
        apoapsis_m
    )

    generation_required_ecps = (continuous_consumption_ecps + recharge_required_ecps) / panel_efficiency_factor

    print(f"The minumum amount of storage (battery) required is {storage_required_ec} EC")
    print(f"The minimum amount of generation required is {generation_required_ecps} EC/s")


if __name__ == "__main__":
    main()
