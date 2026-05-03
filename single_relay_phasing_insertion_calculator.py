"""
single_relay_phasing_insertion_calculator.py

Given the characteristics of an existing relay satellite network,
and the relative pahse angle of a new satellite, calculate the period
of phasing orbit such that after a single orbit, the new satellite
will be exactly 1/3 of an orbit ahead or behind (as selected) of the
target existing satellite.

The code assumes that both the new and existing satellites are in
the same circular orbit, both with the same target period.
"""
from ksp_utils import ksp_formatted_time
import re

def parse_period_to_secs(period_ksp_str: str) -> int:
    """
    Given an orbital perdiod in KSP string format (e.g. 1d, 3h, 0m, 0s),
    return the value of that period in seconds. There is limited checking.

    Note that a Kerbin day is only 6 hours long.
    """
    if not period_ksp_str:
        raise ValueError("The value cannot be missing or blank")

    parsed_values = re.findall(r"\d+", period_ksp_str)
    if not parsed_values:
        raise ValueError("There were no numbers in the input.")

    if len(parsed_values) < 4:
        raise ValueError("There were not enough numbers in the input")

    if len(parsed_values) > 4:
        raise ValueError("There were too many numbers in the input")


    #
    # If, for some odd reason, the int conversion fails, the conversion
    # itself will raise a ValueError which the caller is already expected
    # to handle as bad input. Therefore, nothing special needs to be done
    # here for that.
    #
    period_seconds = int(parsed_values[0]) * 6                       # Days in hours
    period_seconds = (period_seconds + int(parsed_values[1])) * 60   # Days + Hours in minutes
    period_seconds = (period_seconds + int(parsed_values[2])) * 60   # Days + Hours + Minutes in sexonds
    period_seconds = (period_seconds + int(parsed_values[3]))        # Days + Hours + Minutes + Seconds in seconds

    return period_seconds

def main():
    print()
    print("This tool assumes that both the new and existing satellites are in the")
    print("same circular parking orbit around the same body and have the same")
    print("orbital period, which is the planned final period for the satellite")
    print("network.")
    print()

    #
    # Get the final period, the one both satellites should be at now.
    # Keep trying until the format is valid.
    #
    got_valid_value = False
    while not got_valid_value:
        final_period_ksp_str = input(f"{'Final period in ksp display format (e.g. 1d, 0h, 0m, 0s) ':.<60} : ")
        try:
            final_period_seconds = parse_period_to_secs(final_period_ksp_str)
            got_valid_value = True
        except ValueError as err:
            print(f"{err}")

    #
    # Get the rest of the parameters, again loop until valid for each
    #
    got_valid_value = False
    while not got_valid_value:
        try:
            current_phase_angle_degrees = float(input(f"{'Current phase angle in degress (include sign and decimal) ':.<60} : "))
            got_valid_value = True
        except ValueError as err:
            print(f"{err}")

    got_valid_value = False
    while not got_valid_value:
        try:
            desired_phase_angle_degrees = float(input(f"{'Desired phase angle in degress (include sign and decimal) ':.<60} : "))
            got_valid_value = True
        except ValueError as err:
            print(f"{err}")

    required_phase_angle_offset_degrees = desired_phase_angle_degrees - current_phase_angle_degrees
    required_period_seconds = (1 + (required_phase_angle_offset_degrees / 360)) * final_period_seconds
    if (required_period_seconds > final_period_seconds):
        required_phasing_burn_direction = "Prograde"
    else:
        required_phasing_burn_direction = "Retrograde"

    print()
    print(f"{'Required phasing period ':.<60} : {ksp_formatted_time(required_period_seconds)}")
    print(f"{'Phasing burn direction ':.<60} : {required_phasing_burn_direction}")
    print()

if __name__ == "__main__":
    main()

