from ksp_utils import get_celestial_body_constants
import pytest
from inclination_change_delta_v_cost_calculator import inclination_change_delta_v_cost_mps




# ==============================================
# inclination_change_delta_v_cost_mps() tests
# ==============================================
class TestIclinationChangeDeltaVCostCalculator:
    def test_inclination_change_delta_v_cost_mps_circular_orbit(self):
        calculated_inclination_change_delta_v_cost_mps = inclination_change_delta_v_cost_mps(
            "Kerbin",
            apoapsis_m=80000,
            periapsis_m=80000,
            altitude_m=80000,
            angle_change_degrees=10
        )
        assert calculated_inclination_change_delta_v_cost_mps == pytest.approx(397.244)

    def test_inclination_change_delta_v_cost_mps_apoapsis_of_elliptical_orbit(self):
        calculated_inclination_change_delta_v_cost_mps = inclination_change_delta_v_cost_mps(
            "Kerbin",
            apoapsis_m=46400000,
            periapsis_m=80000,
            altitude_m=46400000,
            angle_change_degrees=45
        )
        assert calculated_inclination_change_delta_v_cost_mps == pytest.approx(35.433)

    # The function should raise a ValueError if name unknown
    def test_orbital_velocity_mps_unknown_body(self):
        with pytest.raises(ValueError):
         calculated_inclination_change_delta_v_cost_mps = inclination_change_delta_v_cost_mps(
            "NotABody",
            apoapsis_m=80000,
            periapsis_m=80000,
            altitude_m=80000,
            angle_change_degrees=45
        )

    # The function should raise a ValueError if altitude is not on the orbit
    def test_inclination_change_delta_v_cost_mps_altitude_not_on_orbit(self):
        with pytest.raises(ValueError):
            calculated_orbital_velocity_mps = inclination_change_delta_v_cost_mps(
                "Kerbin",
                apoapsis_m=80000,
                periapsis_m=80000,
                altitude_m=4640000,
                angle_change_degrees=45
            )
