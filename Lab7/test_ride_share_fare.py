import math

from hypothesis import given, settings, strategies as st
from ride_share_fare import parse_trip, fare_average, payable_fare


# ---------------------------------------------------------------------------
# Part 1: "no crash" properties (required by the lab handout)
# Whatever the input is (text, empty string, None), the function must not raise.
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_trip_no_crash(s):
    try:
        parse_trip(s)
    except Exception as e:
        assert False, f"parse_trip crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_fare_average_no_crash(s):
    try:
        fare_average(s)
    except Exception as e:
        assert False, f"fare_average crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_payable_fare_no_crash(s):
    try:
        payable_fare(s)
    except Exception as e:
        assert False, f"payable_fare crashed with: {e!r} for input {s!r}"


# ---------------------------------------------------------------------------
# Part 2: extra fuzzing with structured / non-string inputs
# ---------------------------------------------------------------------------

any_input = st.one_of(
    st.none(), st.integers(), st.floats(), st.booleans(),
    st.binary(), st.lists(st.integers()), st.text(),
)


@given(any_input)
def test_parse_trip_any_type_no_crash(s):
    parse_trip(s)


@given(any_input)
def test_fare_average_any_type_no_crash(s):
    fare_average(s)


@given(any_input)
def test_payable_fare_any_type_no_crash(s):
    payable_fare(s)


# ---------------------------------------------------------------------------
# Part 3: correctness properties on VALID inputs
# ---------------------------------------------------------------------------

cab_names = st.text(
    alphabet=st.characters(whitelist_categories=("L",)), min_size=1, max_size=15
)
distances = st.floats(min_value=0, max_value=10_000, allow_nan=False)


@given(cab_names, distances)
def test_parse_trip_valid_roundtrip(cab, km):
    result = parse_trip(f"{cab}:{km}")
    assert result is not None
    out_cab, out_km = result
    assert out_cab == cab.strip().title()
    assert out_km == km


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1, max_size=50))
def test_fare_average_within_min_and_max(fares):
    result = fare_average(",".join(map(str, fares)))
    assert result is not None
    assert min(fares) <= result <= max(fares)


@given(
    st.floats(min_value=0, max_value=1e6, allow_nan=False),
    st.floats(min_value=0, max_value=1e6, allow_nan=False),
)
def test_payable_fare_never_negative_and_finite(fare, promo):
    result = payable_fare(f"{fare}|{promo}")
    assert result is not None
    assert math.isfinite(result)
    assert result >= 0


# ---------------------------------------------------------------------------
# Part 4: invalid inputs must be rejected cleanly (return None), never
# silently produce a nonsense value
# ---------------------------------------------------------------------------

@given(st.sampled_from(["nan", "inf", "-inf", "1e999", "-5", "abc", ""]))
def test_parse_trip_rejects_bad_distance(km):
    assert parse_trip(f"sedan:{km}") is None


@given(st.sampled_from(["", ",", "1,,3", "a,b", "-5,10", "1.5,2", "10,"]))
def test_fare_average_rejects_bad_csv(csv):
    assert fare_average(csv) is None


@given(st.sampled_from(["nan|0", "100|nan", "inf|0", "100|-50", "-100|10", "100", "100|1|2", "|"]))
def test_payable_fare_rejects_bad_input(text):
    assert payable_fare(text) is None
