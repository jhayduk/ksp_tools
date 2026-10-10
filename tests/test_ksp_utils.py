import pytest
from ksp_utils import is_known_celestial_body, is_moon

# ==================
# is_moon() tests
# ==================
class TestIsMoon:
    # Known planets
    @pytest.mark.parametrize(
        "known_planet",
        ["Eve", "Kerbin", "Duna"]
    )
    def test_is_moon_for_planet(self, known_planet: str):
        assert is_moon(known_planet) == False

    # Known moons
    @pytest.mark.parametrize(
        "known_moon",
        ["Gilly", "Mun", "Minmus", "Ike"]
    )
    def test_is_moon_for_moon(self, known_moon: str):
        assert is_moon(known_moon) == True

    # The function should raise a ValueError if name unknown
    def test_is_moon_for_unknown_raises_value_error(self):
        with pytest.raises(ValueError):
            is_moon("NotABody")


# ==========================================
# is_known_celestial_body() tests
# ==========================================
class TestIsKnownCelestialBody:
    # Capitalized is how the names appear in the constants file
    def test_known_body_capitalized(self):
        assert is_known_celestial_body("Kerbin") == True

    # The function should support all lower case
    def test_known_body_lower_case(self):
        assert is_known_celestial_body("kerbin") == True

    # The function should support all Upper case
    def test_known_body_upper_case(self):
        assert is_known_celestial_body("KERBIN") == True

    # The function should flag unknown names
    def test_unknown_body(self):
        assert is_known_celestial_body("NotABody") == False
