from ksp_utils import get_celestial_body_constants
import pytest
from solar_panel_efficiency_calculator import solar_panel_efficiency

# ==================
# is_moon() tests
# ==================
class TestSolarPanelEfficiencyCalculator:
    # List test data as a tuple of body_name, apoapsis_m, and expected_efficiency
    # as a separate list so that the ids can be dynamically extracted
    # as the first value of each tuple before parameterizing the whole
    # set.
    test_data = [
        ("Eve", 400000, 1.87),
        ("Gilly", 16000, 1.86),
        ("Kerbin", 80000, 1.0),
        ("Mun", 60000, 1.0),
        ("Minmus", 30000, 0.99),
        ("Duna", 140000, 0.39),
        ("Ike", 50000, 0.39)
    ]

    test_ids = [row[0] for row in test_data]

    @pytest.mark.parametrize(
        "body_name, apoapsis_m, expected_efficiency",
        test_data,
        ids=test_ids
    )
    def test_solar_panel_efficiency(self, body_name: str, apoapsis_m: float, expected_efficiency: float):
        body_constants = get_celestial_body_constants(body_name)
        calculated_efficiency = solar_panel_efficiency(
            body_name,
            body_constants["apoapsis_from_parent_center_m"],
            body_constants["equatorial_radius_m"],
            apoapsis_m
        )
        assert calculated_efficiency == pytest.approx(expected_efficiency, rel=0.01)
