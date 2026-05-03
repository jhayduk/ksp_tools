"""
ksp_ utils.py

A collection of miscellaneous utility functions in support of the ksp tools.
"""
import math

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