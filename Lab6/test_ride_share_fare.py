import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status

# Example test cases:
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0

def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True

# Write the rest of the test cases so that the code is 90-100% covered.
