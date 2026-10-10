import pytest
from ksp_utils import is_known_celestial_body

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
        assert is_known_celestial_body("NotABody)") == False
