INCLUDED_KM = {"mini": 5, "sedan": 8, "suv": 12}


def extra_distance_fare(cab_type, distance_km, zone, is_subscriber):
    if cab_type not in INCLUDED_KM:
        raise ValueError("unknown cab type")
    if distance_km < 0:
        raise ValueError("invalid distance")
    included = INCLUDED_KM[cab_type]
    if is_subscriber and cab_type != "suv":
        included += 3
    extra = distance_km - included
    if extra <= 0:
        return 0
    if zone == "city":
        rate = 12
    else:
        rate = 18
    if extra > 20:
        rate = rate + 8
        if zone == "outstation":
            rate += 4
    return extra * rate


def seats_and_bags_ok(passengers, bags, needs_wheelchair):
    if needs_wheelchair:
        return passengers <= 2
    if passengers > 4:
        return False
    return bags <= 2


def pickup_status(minutes_early, is_scheduled, is_airport):
    if is_scheduled:
        cutoff = 10
    else:
        cutoff = 5
    if is_airport:
        cutoff += 10
    if minutes_early >= cutoff:
        return "on_time"
    elif minutes_early >= cutoff - 15:
        return "delayed"
    return "missed"
