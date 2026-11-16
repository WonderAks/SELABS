import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ---------- extra_distance_fare ----------
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_unknown_cab_type():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bus", 10, "city", False)


def test_negative_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_subscriber_gets_extra_included_km():
    # mini: 5 + 3 = 8 km included, extra = 2, city rate 12
    assert extra_distance_fare("mini", 10, "city", True) == 24


def test_non_city_zone_uses_higher_rate():
    # suv: 12 km included, extra = 8, non-city rate 18
    assert extra_distance_fare("suv", 20, "outstation", False) == 144


def test_long_extra_distance_city_surcharge():
    # sedan: extra = 32 (>20), rate 12 + 8 = 20
    assert extra_distance_fare("sedan", 40, "city", False) == 640


def test_long_extra_distance_outstation_surcharge():
    # sedan: extra = 32 (>20), rate 18 + 8 + 4 = 30
    assert extra_distance_fare("sedan", 40, "outstation", False) == 960


# ---------- seats_and_bags_ok ----------
def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


def test_wheelchair_within_limit():
    assert seats_and_bags_ok(2, 0, True) is True


def test_too_many_passengers():
    assert seats_and_bags_ok(5, 0, False) is False


def test_too_many_bags():
    assert seats_and_bags_ok(3, 3, False) is False


# ---------- pickup_status ----------
def test_pickup_on_time():
    assert pickup_status(5, False, False) == "on_time"


def test_pickup_delayed():
    assert pickup_status(0, False, False) == "delayed"


def test_pickup_missed():
    assert pickup_status(-20, False, False) == "missed"



# ================= Additional tests for BRANCH coverage =================

# ---------- extra_distance_fare ----------
def test_subscriber_on_suv_gets_no_bonus_km():
    # suv stays at 12 km included even for subscribers, extra = 3, city rate 12
    assert extra_distance_fare("suv", 15, "city", True) == 36


def test_subscriber_extra_km_makes_trip_free():
    # sedan: 8 + 3 = 11 km included, 11 km trip -> extra = 0
    assert extra_distance_fare("sedan", 11, "city", True) == 0


def test_boundary_extra_exactly_20_has_no_surcharge():
    # mini: extra = 20 (not > 20), outstation rate stays 18
    assert extra_distance_fare("mini", 25, "outstation", False) == 360


def test_boundary_extra_21_triggers_surcharge():
    # mini: extra = 21 (> 20), city rate 12 + 8 = 20
    assert extra_distance_fare("mini", 26, "city", False) == 420


def test_zero_distance():
    assert extra_distance_fare("mini", 0, "city", False) == 0


# ---------- seats_and_bags_ok ----------
def test_wheelchair_too_many_passengers():
    assert seats_and_bags_ok(3, 0, True) is False


def test_exactly_four_passengers_two_bags_ok():
    assert seats_and_bags_ok(4, 2, False) is True


# ---------- pickup_status ----------
def test_scheduled_on_time():
    assert pickup_status(10, True, False) == "on_time"


def test_scheduled_delayed():
    assert pickup_status(0, True, False) == "delayed"


def test_scheduled_missed():
    assert pickup_status(-6, True, False) == "missed"


def test_airport_unscheduled_on_time():
    assert pickup_status(15, False, True) == "on_time"


def test_airport_scheduled_on_time():
    assert pickup_status(20, True, True) == "on_time"


def test_airport_delayed():
    assert pickup_status(0, False, True) == "delayed"


def test_airport_missed():
    assert pickup_status(-6, False, True) == "missed"