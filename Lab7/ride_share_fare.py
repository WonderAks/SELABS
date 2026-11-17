"""Ride-share fare helpers (hardened after fuzz testing with Hypothesis).

Design decision: every function validates its input and returns ``None`` when the
input is invalid instead of raising an exception. ``main()`` turns ``None`` into a
friendly message for the user.
"""
import math

GST_RATE = 1.18  # fare + 18% tax


def _to_finite_float(value):
    """Convert text to a finite float, or return None (rejects nan / inf / junk)."""
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def parse_trip(text):
    """Parse 'cab:distance_km' -> (Cab Name, distance_km) or None if invalid.

    Rejects: non-strings, missing / extra ':', empty cab name,
    non-numeric, negative, nan or infinite distances.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    cab = parts[0].strip()
    km = _to_finite_float(parts[1])
    if not cab or km is None or km < 0:
        return None
    return cab.title(), km


def fare_average(fares_csv):
    """Average (floor) of comma separated whole-number fares, or None if invalid.

    Rejects: non-strings, empty input, empty elements ("1,,3", "10,"),
    non-integers ("1.5", "abc") and negative fares.
    """
    if not isinstance(fares_csv, str):
        return None
    values = []
    for item in fares_csv.split(','):
        item = item.strip()
        # ASCII digits only: no signs, decimals, underscores or lookalike unicode digits
        if not item or not item.isascii() or not item.isdigit():
            return None
        try:
            values.append(int(item))
        except ValueError:  # e.g. absurdly long digit strings
            return None
    return sum(values) // len(values)


def payable_fare(text):
    """Parse 'fare|promo' -> fare incl. 18% tax minus promo (never < 0), or None.

    Rejects: non-strings, missing / extra '|', non-numeric, negative,
    nan or infinite values, and results that overflow to infinity.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fare = _to_finite_float(parts[0])
    promo = _to_finite_float(parts[1])
    if fare is None or promo is None or fare < 0 or promo < 0:
        return None
    total = fare * GST_RATE - promo
    if not math.isfinite(total):
        return None
    return max(total, 0.0)


def main():
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    result = parse_trip(user_input)
    if result is None:
        print("Invalid input. Expected format cab:distance (e.g. sedan:12)")
    else:
        print("Cab and Distance:", result)

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    result = fare_average(user_input)
    if result is None:
        print("Invalid input. Expected whole-number fares like 120,95,210")
    else:
        print("Average Fare:", result)

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    result = payable_fare(user_input)
    if result is None:
        print("Invalid input. Expected fare|promo with non-negative numbers (e.g. 250|30)")
    else:
        print("Payable Fare:", result)


if __name__ == "__main__":
    main()
