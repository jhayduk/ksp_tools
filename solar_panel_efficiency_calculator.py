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
    from the Sun and the square of the furthest distance the panel
    can be from the Sun.

    This also works for moons, which assume that the moon is at its
    periapsis with its parent body and, at the same time, the parent body
    is at is apoapsis with Kerbol. This generates a worst case value.
    
    Note that the calculation assumes full exposure.
"""
from ksp_utils import (
    Apsis,
    get_apsis,
    get_celestial_body_constants,
    get_parent_body_name_and_constants,
    is_moon
)
from lighttime_calculator import calculate_lighttime_s
from rich import print

def solar_panel_efficiency(
        parent_body_name: str,
        parent_body_apoapsis_from_kerbol_center_m: float,
        parent_body_equatorial_radius_m: float,
        apoapsis_m: float
        ) -> float:
    """
    Given the max distance of a parent body upon, or around, which a solar
    panel is placed, the equatorial radius of that same parent body, and the
    aposapsis of the craft containing the solar panel (or the alititude on
    the surface where the panel is placed), returns an efficiency factor
    that can be multiplied to the expected EC generation value to adjust it
    for its distance from the Sun (Kerbol).

    This is calculated as the ratio of the square of the distance Kerbin is
    from the Sun and the square of the furthest distance the panel can be from the Sun.

    Note that the calculation assumes full exposure.
    """
    kerbin_apoapsis_from_kerbol_center_m = get_celestial_body_constants("Kerbin")["apoapsis_from_parent_center_m"]

    panel_distance_from_kerbol_center_m = parent_body_apoapsis_from_kerbol_center_m + parent_body_equatorial_radius_m + apoapsis_m

    # If the parent body is a moon, then add the apoapsis (from the center)
    # if the moon's parent planet
    if is_moon(parent_body_name):
        moon_body_contants = get_celestial_body_constants(parent_body_name)
        planet_body_contants = get_celestial_body_constants(moon_body_contants["parent_body"])
        panel_distance_from_kerbol_center_m += planet_body_contants["apoapsis_from_parent_center_m"]

    return (kerbin_apoapsis_from_kerbol_center_m ** 2) / (panel_distance_from_kerbol_center_m ** 2)


def main():
    parent_body, parent_body_constants = get_parent_body_name_and_constants()

    apoapsis_m = get_apsis(
        Apsis.APOAPSIS,
        parent_body,
        parent_body_constants["equatorial_radius_m"],
        parent_body_constants["sphere_of_influence_radius_m"]
    )

    panel_efficiency_factor = solar_panel_efficiency(
        parent_body,
        parent_body_constants["apoapsis_from_parent_center_m"],
        parent_body_constants["equatorial_radius_m"],
        apoapsis_m
    )

    print(f"The solar panel efficiency factor is {panel_efficiency_factor}")


if __name__ == "__main__":
    main()
