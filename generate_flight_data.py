import json
from datetime import datetime, timedelta
import random
import os

# Airlines, airports, seat classes, and currencies
AIRLINES = [
    {"code": "AA", "name": "American Airlines", "logo": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=80&h=40&fit=crop"},
    {"code": "DL", "name": "Delta Air Lines", "logo": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=80&h=40&fit=crop"},
    {"code": "JL", "name": "Japan Airlines", "logo": "https://images.unsplash.com/photo-1540339832862-44088e611536?w=80&h=40&fit=crop"},
    {"code": "IB", "name": "Iberia", "logo": "https://images.unsplash.com/photo-1597340595281-3fd177219e3c?w=80&h=40&fit=crop"},
    {"code": "SQ", "name": "Singapore Airlines", "logo": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=80&h=40&fit=crop"},
    {"code": "QF", "name": "Qantas", "logo": "https://images.unsplash.com/photo-1521727857535-28d2047314ac?w=80&h=40&fit=crop"},
]
AIRPORTS = [
    {"code": "JFK", "name": "John F. Kennedy International", "city": "New York", "country": "USA"},
    {"code": "LAX", "name": "Los Angeles International", "city": "Los Angeles", "country": "USA"},
    {"code": "NRT", "name": "Narita International Airport", "city": "Tokyo", "country": "Japan"},
    {"code": "HND", "name": "Haneda Airport", "city": "Tokyo", "country": "Japan"},
    {"code": "MAD", "name": "Adolfo Suárez Madrid–Barajas", "city": "Madrid", "country": "Spain"},
    {"code": "BCN", "name": "Barcelona-El Prat", "city": "Barcelona", "country": "Spain"},
    {"code": "SIN", "name": "Changi Airport", "city": "Singapore", "country": "Singapore"},
    {"code": "SYD", "name": "Kingsford Smith Airport", "city": "Sydney", "country": "Australia"},
    {"code": "FLL", "name": "Fort Lauderdale-Hollywood International", "city": "Fort Lauderdale", "country": "USA"},
]
SEAT_CLASSES = ["economy", "premium_economy", "business", "first"]
CURRENCIES = ["USD", "EUR", "JPY", "SGD", "AUD"]

DATA_DIR = os.path.join(os.path.dirname(__file__), "app", "data", "flights")

# Helper to generate a random flight number
def random_flight_number(code):
    return f"{code} {random.randint(100, 9999)}"

def random_price(currency):
    base = random.randint(100, 2000)
    member_discount = random.uniform(0.85, 0.95)  # 5-15% off
    member_price = int(base * member_discount)
    return {"total": base, "currency": currency, "member_price": member_price}

def random_baggage():
    return {"carry_on": f"{random.randint(7,15)}kg", "checked": f"{random.randint(23,32)}kg"}

def random_duration():
    return random.randint(60, 1440)

def random_seat_classes():
    return random.sample(SEAT_CLASSES, random.randint(1, len(SEAT_CLASSES)))

def random_airport(exclude=None):
    airports = [a for a in AIRPORTS if a["code"] != exclude]
    return random.choice(airports)

def generate_one_way():
    flights = []
    today = datetime.utcnow()
    for day in range(30):
        depart_date = today + timedelta(days=day)
        for airline in AIRLINES:
            for origin in AIRPORTS:
                for dest in AIRPORTS:
                    if origin["code"] == dest["code"]:
                        continue
                    for stops in [0, 1, 2]:
                        for seat_class in SEAT_CLASSES:
                            flight = {
                                "id": f"ow-{airline['code']}-{origin['code']}-{dest['code']}-{depart_date.strftime('%Y%m%d')}-{stops}-{seat_class}",
                                "trip_type": "one_way",
                                "airline": airline,
                                "stops": stops,
                                "seat_classes": [seat_class],
                                "price": random_price(random.choice(CURRENCIES)),
                                "duration_total_minutes": random_duration(),
                                "baggage": random_baggage(),
                                "legs": [
                                    {
                                        "direction": "outbound",
                                        "segments": [
                                            {
                                                "flight_number": random_flight_number(airline["code"]),
                                                "airline": airline["code"],
                                                "from": origin,
                                                "to": dest,
                                                "depart_utc": depart_date.strftime("%Y-%m-%dT%H:00:00Z"),
                                                "arrive_utc": (depart_date + timedelta(hours=5)).strftime("%Y-%m-%dT%H:00:00Z"),
                                                "duration_minutes": random_duration()
                                            }
                                        ]
                                    }
                                ]
                            }
                            flights.append(flight)
    with open(os.path.join(DATA_DIR, "one_way.json"), "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2)

def generate_round_trip():
    flights = []
    today = datetime.utcnow()
    for day in range(30):
        depart_date = today + timedelta(days=day)
        return_date = depart_date + timedelta(days=random.randint(1, 14))
        for airline in AIRLINES:
            for origin in AIRPORTS:
                for dest in AIRPORTS:
                    if origin["code"] == dest["code"]:
                        continue
                    for stops in [0, 1, 2]:
                        for seat_class in SEAT_CLASSES:
                            flight = {
                                "id": f"rt-{airline['code']}-{origin['code']}-{dest['code']}-{depart_date.strftime('%Y%m%d')}-{return_date.strftime('%Y%m%d')}-{stops}-{seat_class}",
                                "trip_type": "round_trip",
                                "airline": airline,
                                "stops": stops,
                                "seat_classes": [seat_class],
                                "price": random_price(random.choice(CURRENCIES)),
                                "duration_total_minutes": random_duration(),
                                "baggage": random_baggage(),
                                "legs": [
                                    {
                                        "direction": "outbound",
                                        "segments": [
                                            {
                                                "flight_number": random_flight_number(airline["code"]),
                                                "airline": airline["code"],
                                                "from": origin,
                                                "to": dest,
                                                "depart_utc": depart_date.strftime("%Y-%m-%dT%H:00:00Z"),
                                                "arrive_utc": (depart_date + timedelta(hours=5)).strftime("%Y-%m-%dT%H:00:00Z"),
                                                "duration_minutes": random_duration()
                                            }
                                        ]
                                    },
                                    {
                                        "direction": "return",
                                        "segments": [
                                            {
                                                "flight_number": random_flight_number(airline["code"]),
                                                "airline": airline["code"],
                                                "from": dest,
                                                "to": origin,
                                                "depart_utc": return_date.strftime("%Y-%m-%dT%H:00:00Z"),
                                                "arrive_utc": (return_date + timedelta(hours=5)).strftime("%Y-%m-%dT%H:00:00Z"),
                                                "duration_minutes": random_duration()
                                            }
                                        ]
                                    }
                                ]
                            }
                            flights.append(flight)
    with open(os.path.join(DATA_DIR, "round_trip.json"), "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2)

def generate_multi_city():
    flights = []
    today = datetime.utcnow()
    for day in range(30):
        depart_date = today + timedelta(days=day)
        for airline in AIRLINES:
            for stops in [2]:
                for seat_class in SEAT_CLASSES:
                    # Multi-city: 3 segments, 3 airports
                    airports = random.sample(AIRPORTS, 3)
                    flight = {
                        "id": f"mc-{airline['code']}-{airports[0]['code']}-{airports[1]['code']}-{airports[2]['code']}-{depart_date.strftime('%Y%m%d')}-{stops}-{seat_class}",
                        "trip_type": "multi_city",
                        "airline": airline,
                        "stops": stops,
                        "seat_classes": [seat_class],
                        "price": random_price(random.choice(CURRENCIES)),
                        "duration_total_minutes": random_duration(),
                        "baggage": random_baggage(),
                        "legs": []
                    }
                    for i in range(3):
                        leg = {
                            "direction": f"segment_{i+1}",
                            "segments": [
                                {
                                    "flight_number": random_flight_number(airline["code"]),
                                    "airline": airline["code"],
                                    "from": airports[i],
                                    "to": airports[(i+1)%3],
                                    "depart_utc": (depart_date + timedelta(hours=i*6)).strftime("%Y-%m-%dT%H:00:00Z"),
                                    "arrive_utc": (depart_date + timedelta(hours=(i+1)*6)).strftime("%Y-%m-%dT%H:00:00Z"),
                                    "duration_minutes": random_duration()
                                }
                            ]
                        }
                        flight["legs"].append(leg)
                    flights.append(flight)
    with open(os.path.join(DATA_DIR, "multi_city.json"), "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2)

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Generating one-way flights...")
    generate_one_way()
    print("Generating round-trip flights...")
    generate_round_trip()
    print("Generating multi-city flights...")
    generate_multi_city()

    # --- Generate flight_details.json and flight_status.json ---
    def generate_flight_details_and_status():
        import glob
        details = {"flights": []}
        statuses = []
        # Find all generated flight files
        flight_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
        for fname in flight_files:
            if os.path.basename(fname) in ["flight_details.json", "flight_status.json"]:
                continue
            try:
                with open(fname, encoding="utf-8") as f:
                    flights = json.load(f)
                    # multi_city.json may be a list or dict
                    if isinstance(flights, dict) and "flights" in flights:
                        flights = flights["flights"]
                    for flight in flights:
                        # Details
                        details["flights"].append({
                            "id": flight["id"],
                            "airline_details": {
                                "name": flight["airline"]["name"],
                                "alliance": random.choice(["Oneworld", "SkyTeam", "Star Alliance"]),
                                "rating": round(random.uniform(3.5, 5.0), 1),
                                "reviews_count": random.randint(1000, 50000)
                            },
                            "fare_details": {
                                seat: {
                                    "base_fare": random.randint(100, 2000),
                                    "taxes": random.randint(20, 300),
                                    "total": random.randint(150, 2300),
                                    "member_price": int(random.randint(150, 2300) * random.uniform(0.85, 0.95)),
                                    "baggage": {"carry_on": f"{random.randint(7,15)}kg included", "checked": f"{random.randint(23,32)}kg included"},
                                    "seat_selection": random.choice(["Included", "Available from $10"]),
                                    "changes": random.choice(["Flexible changes", "Changes allowed with fee"]),
                                    "cancellation": random.choice(["Refundable", "Non-refundable", "Refundable with fee"]),
                                    "miles_earned": f"{random.randint(50,200)}% of miles flown"
                                } for seat in flight.get("seat_classes", ["economy"])
                            },
                            "amenities": {
                                "wifi": {"available": True, "price": "$8/hour or $20/flight"},
                                "entertainment": {"available": True, "type": "Personal TV", "features": ["Movies", "TV Shows", "Games"]},
                                "power": {"available": True, "type": "110V + USB"},
                                "seat_pitch": {seat: f"{random.randint(30, 80)} inches" for seat in flight.get("seat_classes", ["economy"])}
                            },
                            "aircraft_details": {
                                "type": random.choice(["Boeing 787-9", "Airbus A350-1000", "Boeing 777-300ER"]),
                                "seat_map": True,
                                "layout": {seat: random.choice(["3-3-3", "2-4-2", "1-2-1"]) for seat in flight.get("seat_classes", ["economy"])}
                            }
                        })
                        # Statuses
                        for leg in flight.get("legs", []):
                            for seg in leg.get("segments", []):
                                statuses.append({
                                    "flight_number": seg["flight_number"],
                                    "status": random.choice(["on_time", "delayed", "scheduled"]),
                                    "gate": random.choice(["A1", "B2", "C3", "D4", "E5"]),
                                    "terminal": random.choice(["T1", "T2", "T3", "T4", "T5"]),
                                    "estimated_depart_utc": seg["depart_utc"],
                                    "delay_minutes": random.choice([0, 10, 20, 30, 45])
                                })
            except Exception as e:
                print(f"Error reading {fname}: {e}")
        # Write details
        with open(os.path.join(DATA_DIR, "flight_details.json"), "w", encoding="utf-8") as f:
            json.dump(details, f, indent=2)
        # Write statuses
        with open(os.path.join(DATA_DIR, "flight_status.json"), "w", encoding="utf-8") as f:
            json.dump(statuses, f, indent=2)

    if __name__ == "__main__":
        os.makedirs(DATA_DIR, exist_ok=True)
        print("Generating one-way flights...")
        generate_one_way()
        print("Generating round-trip flights...")
        generate_round_trip()
        print("Generating multi-city flights...")
        generate_multi_city()
        print("Generating flight details and status...")
        generate_flight_details_and_status()
        print("✅ Flight data generated for all combinations!")
