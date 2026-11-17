def parse_trip(text):
    cab, km = text.split(':')
    return cab.strip().title(), float(km)

def fare_average(fares_csv):
    values = [int(r) for r in fares_csv.split(',')]
    return sum(values) // len(values)

def payable_fare(text):
    fare, promo = text.split('|')
    total = float(fare) * 1.18 - float(promo)
    return max(total, 0)

def main():
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    result = parse_trip(user_input)
    print("Cab and Distance:", result)

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    result = fare_average(user_input)
    print("Average Fare:", result)

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    result = payable_fare(user_input)
    print("Payable Fare:", result)

if __name__ == "__main__":
    main()
