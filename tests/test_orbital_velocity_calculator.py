from ksp_utils import get_celestial_body_constants
import pytest
from orbital_velocity_calculator import obital_velocity_mps

# ===============================
# orbital_velocity_mps() tests
# ===============================
class TestOrbitalVelocityCalculator:
    def test_orbital_velocity_mps_circular_orbit(self):
        calculated_orbital_velocity_mps = obital_velocity_mps(
            "Kerbin",
            apoapsis_m=100000,
            periapsis_m=100000,
            altitude_m=100000
        )
        assert calculated_orbital_velocity_mps == pytest.approx(2246.140)

    def test_orbital_velocity_mps_elliptical_orbit(self):
        calculated_orbital_velocity_mps = obital_velocity_mps(
            "Kerbin",
            apoapsis_m=400000,
            periapsis_m=100000,
            altitude_m=400000
        )
        assert calculated_orbital_velocity_mps == pytest.approx(1705.396)

    # The function should raise a ValueError if name unknown
    def test_orbital_velocity_mps_unknown_body(self):
        with pytest.raises(ValueError):
         calculated_orbital_velocity_mps = obital_velocity_mps(
            "NotABody",
            apoapsis_m=100000,
            periapsis_m=100000,
            altitude_m=100000
        )

    # The function should raise a ValueError if altitude is not on the orbit
    def test_orbital_velocity_mps_altitude_not_on_orbit(self):
        with pytest.raises(ValueError):
            calculated_orbital_velocity_mps = obital_velocity_mps(
                "Kerbin",
                apoapsis_m=100000,
                periapsis_m=100000,
                altitude_m=4000000
            )
