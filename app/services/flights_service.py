import json
from pathlib import Path
from typing import Optional

BASE = Path(__file__).resolve().parents[1] / "data" / "flights"

def _load(name: str):
    with open(BASE / name, encoding="utf-8") as f:
        return json.load(f)

def _apply_filters(results, seat_class: Optional[str], stops: Optional[int],
                   airline: Optional[str], price_min: Optional[float],
                   price_max: Optional[float]):
    out = results

    if seat_class:
        out = [r for r in out if seat_class in r.get("seat_classes", [])]

    if stops is not None:
        if stops in (0, 1):
            out = [r for r in out if r.get("stops") == stops]
        else:
            out = [r for r in out if r.get("stops", 0) >= 2]

    if airline:
        out = [r for r in out if r.get("airline", {}).get("code") == airline.upper()]

    if price_min is not None:
        out = [r for r in out if r.get("price", {}).get("total", 0) >= price_min]

    if price_max is not None:
        out = [r for r in out if r.get("price", {}).get("total", 0) <= price_max]

    return out

def _apply_sort(results, sort_by: Optional[str]):
    if not sort_by:
        return results
    if sort_by == "price_asc":
        return sorted(results, key=lambda r: r["price"]["total"])
    if sort_by == "price_desc":
        return sorted(results, key=lambda r: r["price"]["total"], reverse=True)
    if sort_by == "duration":
        return sorted(results, key=lambda r: r["duration_total_minutes"])
    if sort_by == "departure_time":
        return sorted(results, key=lambda r: r["legs"][0]["segments"][0]["depart_utc"])
    return results

def search_round_trip(origin, destination, depart, returnd, passengers, seat_class,
                      stops, airline, price_min, price_max, sort_by):
    data = _load("round_trip.json")

    filtered = [
        r for r in data
        if r["legs"][0]["segments"][0]["from"]["code"] == origin.upper()
        and r["legs"][-1]["segments"][-1]["to"]["code"] == destination.upper()
    ]

    filtered = _apply_filters(filtered, seat_class, stops, airline, price_min, price_max)
    filtered = _apply_sort(filtered, sort_by)
    return {"trip_type": "round_trip", "count": len(filtered), "items": filtered}

def search_one_way(origin, destination, depart, passengers, seat_class,
                   stops, airline, price_min, price_max, sort_by):
    data = _load("one_way.json")
    filtered = [
        r for r in data
        if r["legs"][0]["segments"][0]["from"]["code"] == origin.upper()
        and r["legs"][0]["segments"][-1]["to"]["code"] == destination.upper()
    ]
    filtered = _apply_filters(filtered, seat_class, stops, airline, price_min, price_max)
    filtered = _apply_sort(filtered, sort_by)
    return {"trip_type": "one_way", "count": len(filtered), "items": filtered}

def search_multi_city(passengers, seat_class, stops, airline, price_min, price_max, sort_by):
    data = _load("multi_city.json")
    filtered = _apply_filters(data, seat_class, stops, airline, price_min, price_max)
    filtered = _apply_sort(filtered, sort_by)
    return {"trip_type": "multi_city", "count": len(filtered), "items": filtered}


def get_flight_details(flight_id: int):
    details = _load("flight_details.json")
    return next((d for d in details if d["id"] == flight_id), {})

def get_flight_status(flight_number: str):
    statuses = _load("flight_status.json")
    return next((s for s in statuses if s["flight_number"].upper() == flight_number), {"flight_number": flight_number, "status": "unknown"})
